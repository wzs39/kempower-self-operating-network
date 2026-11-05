"""
Kempower Self-Operating Charging Network - Anti-Phantom Replug & Fraud Defense
Module: src/core/anti_fraud.py

Implements:
1. Three-pillar detection criteria (F10):
   - Temporal proximity: Delta t < 180s
   - SoC continuity: |Delta SoC| <= 1.0%
   - Electrical fingerprinting / current ramp: dI/dt > 100 A/s
2. Automated Session Stitching:
   - Root session ID retention
   - Delivered energy accumulation
   - Base connection fee duplicate waiver (€2.50)
   - Continuous dwell time preservation for SLA MRDT gate
3. Pre-charge bypass protection and contactor soft-lockout
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math
from typing import Dict, List, Optional, Tuple, Any
import dateutil.parser

class ReplugFraudType(str, Enum):
    GENUINE_NEW_SESSION = "GENUINE_NEW_SESSION"
    PHANTOM_REPLUG_STITCHED = "PHANTOM_REPLUG_STITCHED"
    ABNORMAL_CURRENT_RAMP = "ABNORMAL_CURRENT_RAMP"
    SLA_MANIPULATION_ATTEMPT = "SLA_MANIPULATION_ATTEMPT"

@dataclass
class AntiFraudConfig:
    reconnect_time_threshold_sec: float = 180.0       # 3 minutes maximum reconnect gap
    soc_continuity_threshold_pct: float = 1.0         # <= 1.0% SoC difference
    abnormal_ramp_threshold_a_per_sec: float = 100.0  # > 100 A/s current ramp rate
    base_connection_fee_eur: float = 2.50             # Waived on stitched phantom sessions

@dataclass
class ReplugEvaluation:
    is_phantom: bool
    fraud_type: ReplugFraudType
    delta_time_sec: float
    delta_soc_pct: float
    current_ramp_rate: float
    root_session_id: str
    action_taken: str
    details: Dict[str, Any] = field(default_factory=dict)

def _safe_float(val: Any, fallback: float = 0.0) -> float:
    """Safely extracts a float value with fallback on None or invalid types."""
    if val is None:
        return float(fallback)
    try:
        return float(val)
    except (ValueError, TypeError):
        return float(fallback)

class PhantomReplugDetector:
    """Detects rapid reconnects, SoC continuity, and electrical ramp anomalies."""

    def __init__(self, config: Optional[AntiFraudConfig] = None):
        self.config = config or AntiFraudConfig()

    def evaluate_reconnect(
        self,
        prev_session: Dict[str, Any],
        new_session: Dict[str, Any],
        current_samples: Optional[List[Dict[str, float]]] = None,
    ) -> ReplugEvaluation:
        """
        Evaluates whether a new session is an accidental/fraudulent phantom replug.
        """
        # 1. Reconnect Time Delta
        prev_end_str = prev_session.get("end_ts") or prev_session.get("depart_ts")
        new_start_str = new_session.get("start_ts") or new_session.get("arrive_ts")

        if not prev_end_str or not new_start_str:
            delta_t = float("inf")
        else:
            try:
                t_prev_end = dateutil.parser.isoparse(str(prev_end_str))
                t_new_start = dateutil.parser.isoparse(str(new_start_str))
                delta_t = max(0.0, (t_new_start - t_prev_end).total_seconds())
            except Exception:
                delta_t = float("inf")

        # 2. SoC Continuity Delta
        prev_end_val = prev_session.get("end_soc")
        if prev_end_val is None:
            prev_end_val = prev_session.get("current_soc_pct")
        if prev_end_val is None:
            prev_end_val = prev_session.get("soc_pct", 0.0)
        prev_end_soc = _safe_float(prev_end_val, 0.0)

        new_start_val = new_session.get("start_soc")
        if new_start_val is None:
            new_start_val = new_session.get("current_soc_pct")
        if new_start_val is None:
            new_start_val = new_session.get("soc_pct", 0.0)
        new_start_soc = _safe_float(new_start_val, 0.0)

        delta_soc = abs(new_start_soc - prev_end_soc)

        # 3. Current Ramp Rate Calculation (dI/dt)
        ramp_val = new_session.get("current_ramp_rate")
        if ramp_val is None:
            ramp_val = new_session.get("dI_dt", 0.0)
        ramp_rate = _safe_float(ramp_val, 0.0)
        if current_samples and len(current_samples) >= 2:
            i_prev = _safe_float(current_samples[0].get("current_a"), 0.0)
            i_curr = _safe_float(current_samples[-1].get("current_a"), 0.0)
            dt_sample = _safe_float(current_samples[-1].get("time_s"), 1.0) - _safe_float(current_samples[0].get("time_s"), 0.0)
            if dt_sample > 0.0:
                ramp_rate = max(0.0, (i_curr - i_prev) / dt_sample)

        # Check vehicle and charger spatial correlation
        same_vehicle = bool(
            prev_session.get("vehicle_id")
            and new_session.get("vehicle_id")
            and prev_session.get("vehicle_id") == new_session.get("vehicle_id")
        )
        same_charger = bool(
            prev_session.get("charger_id")
            and new_session.get("charger_id")
            and prev_session.get("charger_id") == new_session.get("charger_id")
        )

        root_id = str(prev_session.get("session_id", "SE_ROOT"))

        # Decision Logic:
        # A. Current Ramp Fraud Check (pre-charge bypass)
        if ramp_rate > self.config.abnormal_ramp_threshold_a_per_sec:
            return ReplugEvaluation(
                is_phantom=True,
                fraud_type=ReplugFraudType.ABNORMAL_CURRENT_RAMP,
                delta_time_sec=delta_t,
                delta_soc_pct=delta_soc,
                current_ramp_rate=ramp_rate,
                root_session_id=root_id,
                action_taken="CLAMP_CURRENT_LOCKOUT_CONTACTOR",
                details={"reason": f"dI/dt of {ramp_rate:.1f} A/s exceeds safe 100 A/s limit"},
            )

        # B. Phantom Replug Criteria (Delta t < 180s AND Delta SoC <= 1.0%)
        is_temporal_match = delta_t < self.config.reconnect_time_threshold_sec
        is_soc_match = delta_soc <= (self.config.soc_continuity_threshold_pct + 1e-5)

        if is_temporal_match and is_soc_match and (same_vehicle or same_charger):
            return ReplugEvaluation(
                is_phantom=True,
                fraud_type=ReplugFraudType.PHANTOM_REPLUG_STITCHED,
                delta_time_sec=delta_t,
                delta_soc_pct=delta_soc,
                current_ramp_rate=ramp_rate,
                root_session_id=root_id,
                action_taken="STITCH_SESSION_AND_PRESERVE_MPC",
                details={
                    "waived_fee_eur": self.config.base_connection_fee_eur,
                    "reconnect_delay_s": delta_t,
                },
            )

        # C. Genuine New Session
        return ReplugEvaluation(
            is_phantom=False,
            fraud_type=ReplugFraudType.GENUINE_NEW_SESSION,
            delta_time_sec=delta_t,
            delta_soc_pct=delta_soc,
            current_ramp_rate=ramp_rate,
            root_session_id=str(new_session.get("session_id", "SE_NEW")),
            action_taken="INITIATE_INDEPENDENT_TRANSACTION",
            details={},
        )

    def stitch_sessions(
        self,
        prev_session: Dict[str, Any],
        new_session: Dict[str, Any],
        eval_result: ReplugEvaluation,
    ) -> Dict[str, Any]:
        """
        Merges two fragmented sessions into a seamless, unified transaction.
        """
        root_session_id = prev_session.get("session_id", "SE_ROOT")
        prev_energy = _safe_float(prev_session.get("energy_kwh"), 0.0)
        new_energy = _safe_float(new_session.get("energy_kwh"), 0.0)

        merged = dict(prev_session)
        merged["session_id"] = root_session_id
        merged["start_ts"] = prev_session.get("start_ts") or prev_session.get("arrive_ts")
        merged["end_ts"] = new_session.get("end_ts") or new_session.get("depart_ts")
        merged["start_soc"] = prev_session.get("start_soc", prev_session.get("current_soc_pct", 0.0))
        merged["end_soc"] = new_session.get("end_soc", new_session.get("current_soc_pct", 0.0))
        merged["energy_kwh"] = round(prev_energy + new_energy, 4)
        merged["max_kw"] = max(
            _safe_float(prev_session.get("max_kw"), 0.0),
            _safe_float(new_session.get("max_kw"), 0.0),
        )
        merged["is_phantom"] = True
        merged["stitched"] = True
        merged["stitch_count"] = prev_session.get("stitch_count", 0) + 1
        merged["child_session_ids"] = prev_session.get("child_session_ids", []) + [new_session.get("session_id")]
        merged["reconnect_delta_sec"] = eval_result.delta_time_sec
        prev_waived = _safe_float(prev_session.get("duplicate_base_fee_waived_eur"), 0.0)
        merged["duplicate_base_fee_waived_eur"] = round(prev_waived + self.config.base_connection_fee_eur, 2)
        merged["fraud_type"] = eval_result.fraud_type.value
        return merged

def anti_phantom_replug_check(
    prev_session: Dict[str, Any],
    new_session: Dict[str, Any],
) -> Tuple[bool, Dict[str, Any]]:
    """
    Authoritative public contract matching PROJECT.md line 107:
    Computes reconnect delta time, SoC difference, and current ramp slope;
    returns (is_phantom, merged_session).
    """
    detector = PhantomReplugDetector()
    eval_result = detector.evaluate_reconnect(prev_session, new_session)
    if eval_result.is_phantom and eval_result.fraud_type == ReplugFraudType.PHANTOM_REPLUG_STITCHED:
        merged = detector.stitch_sessions(prev_session, new_session, eval_result)
        return True, merged
    elif eval_result.is_phantom:
        # Ramp fraud or other violation
        merged = dict(new_session)
        merged["is_phantom"] = True
        merged["fraud_type"] = eval_result.fraud_type.value
        merged["action_taken"] = eval_result.action_taken
        return True, merged
    else:
        return False, new_session
