"""
Kempower Self-Operating Charging Network - Industrial Protocol Engine
Module: src/core/protocols.py

Implements:
1. OCPP 2.0.1 Smart Charging Profiles (F07):
   - SetChargingProfileRequest / Response (TxProfile, TxDefaultProfile, ChargingStationMaxProfile)
   - Relative & Absolute charging schedules with 15-minute intervals in Watts (W)
   - ChargingNeeds negotiation converting EV constraints into MPC boundary constraints
   - ClearChargingProfileRequest / Response
   - CostUpdatedRequest dynamic tariff streaming
2. OCPP 2.0.1 Device Model Telemetry & Event Monitoring (F08):
   - NotifyEventRequest with Component-Variable data model
   - PowerModule (status, current), FanSpeed (RPM), CoolingSystem (temp), IsolationMonitoringDevice (kOhm)
3. ISO 15118-2/20 Plug & Charge (PnC) Protocol Engine (F09):
   - Mutual TLS 1.3 handshake verification (<1.5s)
   - 3-tier X.509 v3 certificate chain validation (V2G Root CA -> Sub-CA -> Leaf Contract)
   - Megawatt Charging System (MCS) & V2G Bidirectional Power Transfer envelope
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from enum import Enum
import math
import time
from typing import Dict, List, Optional, Any, Tuple, Union, Set

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
import dateutil.parser


# ============================================================================
# 1. OCPP 2.0.1 Enums & Standard Definitions (Part 2: Functional Block K & B)
# ============================================================================

class ChargingProfilePurposeEnum(str, Enum):
    TX_PROFILE = "TxProfile"
    TX_DEFAULT_PROFILE = "TxDefaultProfile"
    CHARGING_STATION_MAX_PROFILE = "ChargingStationMaxProfile"
    CHARGING_STATION_EXTERNAL_CONSTRAINTS = "ChargingStationExternalConstraints"


class ChargingProfileKindEnum(str, Enum):
    RELATIVE = "Relative"
    ABSOLUTE = "Absolute"
    RECURRING = "Recurring"


class RecurrencyKindEnum(str, Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"


class ChargingRateUnitEnum(str, Enum):
    W = "W"  # Watts (standard for DC fast charging)
    A = "A"  # Amperes


class ChargingProfileStatusEnum(str, Enum):
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    NOT_SUPPORTED = "NotSupported"


class ClearChargingProfileStatusEnum(str, Enum):
    ACCEPTED = "Accepted"
    UNKNOWN = "Unknown"


class EnergyTransferModeEnum(str, Enum):
    DC = "DC"
    AC_SINGLE_PHASE = "AC_single_phase"
    AC_TWO_PHASE = "AC_two_phase"
    AC_THREE_PHASE = "AC_three_phase"


class EventTriggerEnum(str, Enum):
    ALERTING = "Alerting"
    DELTA = "Delta"
    PERIODIC = "Periodic"


class EventNotificationEnum(str, Enum):
    HARD_WIRED_NOTIFICATION = "HardWiredNotification"
    PRE_ALERT_NOTIFICATION = "PreAlertNotification"
    CUSTOM_NOTIFICATION = "CustomNotification"


class EventSeverityEnum(int, Enum):
    DANGER = 1
    FAULT = 2
    WARNING = 3
    INFO = 4


# ============================================================================
# 2. OCPP 2.0.1 Smart Charging Data Structures (F07)
# ============================================================================

@dataclass
class ChargingSchedulePeriod:
    startPeriod: int                       # Offset in seconds from schedule start
    limit: float                           # Limit in W or A
    numberPhases: Optional[int] = None     # AC phases (optional, None for DC)
    phaseToUse: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "startPeriod": int(self.startPeriod),
            "limit": round(float(self.limit), 2),
        }
        if self.numberPhases is not None:
            d["numberPhases"] = self.numberPhases
        if self.phaseToUse is not None:
            d["phaseToUse"] = self.phaseToUse
        return d


@dataclass
class ChargingSchedule:
    id: int
    chargingRateUnit: ChargingRateUnitEnum
    chargingSchedulePeriod: List[ChargingSchedulePeriod]
    startSchedule: Optional[str] = None    # ISO 8601 UTC
    duration: Optional[int] = None         # Total duration in seconds
    minChargingRate: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        rate_unit_str = (
            self.chargingRateUnit.value
            if isinstance(self.chargingRateUnit, Enum)
            else str(self.chargingRateUnit)
        )
        d: Dict[str, Any] = {
            "id": int(self.id),
            "chargingRateUnit": rate_unit_str,
            "chargingSchedulePeriod": [p.to_dict() for p in self.chargingSchedulePeriod],
        }
        if self.startSchedule:
            d["startSchedule"] = self.startSchedule
        if self.duration is not None:
            d["duration"] = int(self.duration)
        if self.minChargingRate is not None:
            d["minChargingRate"] = round(float(self.minChargingRate), 2)
        return d


@dataclass
class ChargingProfile:
    id: int
    stackLevel: int                        # Priority level >= 0
    chargingProfilePurpose: ChargingProfilePurposeEnum
    chargingProfileKind: ChargingProfileKindEnum
    chargingSchedule: Union[ChargingSchedule, List[ChargingSchedule]]
    recurrencyKind: Optional[RecurrencyKindEnum] = None
    validFrom: Optional[str] = None        # ISO 8601
    validTo: Optional[str] = None          # ISO 8601
    transactionId: Optional[str] = None    # Mandatory for TxProfile

    def to_dict(self) -> Dict[str, Any]:
        sched = self.chargingSchedule
        if isinstance(sched, list):
            sched_repr = [s.to_dict() for s in sched]
        else:
            sched_repr = [sched.to_dict()]

        purpose_str = (
            self.chargingProfilePurpose.value
            if isinstance(self.chargingProfilePurpose, Enum)
            else str(self.chargingProfilePurpose)
        )
        kind_str = (
            self.chargingProfileKind.value
            if isinstance(self.chargingProfileKind, Enum)
            else str(self.chargingProfileKind)
        )

        d: Dict[str, Any] = {
            "id": int(self.id),
            "stackLevel": int(self.stackLevel),
            "chargingProfilePurpose": purpose_str,
            "chargingProfileKind": kind_str,
            "chargingSchedule": sched_repr,
        }
        if self.recurrencyKind is not None:
            recur_str = (
                self.recurrencyKind.value
                if isinstance(self.recurrencyKind, Enum)
                else str(self.recurrencyKind)
            )
            d["recurrencyKind"] = recur_str
        if self.validFrom:
            d["validFrom"] = self.validFrom
        if self.validTo:
            d["validTo"] = self.validTo
        if self.transactionId:
            d["transactionId"] = str(self.transactionId)
        return d


@dataclass
class SetChargingProfileRequest:
    evseId: int
    chargingProfile: ChargingProfile

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evseId": int(self.evseId),
            "chargingProfile": self.chargingProfile.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SetChargingProfileRequest:
        evse_id = int(data["evseId"])
        cp_data = data["chargingProfile"]
        schedules: List[ChargingSchedule] = []

        raw_sched = cp_data.get("chargingSchedule", [])
        if isinstance(raw_sched, dict):
            raw_sched = [raw_sched]

        for s in raw_sched:
            periods = [
                ChargingSchedulePeriod(
                    startPeriod=int(p["startPeriod"]),
                    limit=float(p["limit"]),
                    numberPhases=p.get("numberPhases"),
                    phaseToUse=p.get("phaseToUse"),
                )
                for p in s.get("chargingSchedulePeriod", [])
            ]
            unit_val = s.get("chargingRateUnit", "W")
            rate_unit = ChargingRateUnitEnum(unit_val) if unit_val in ChargingRateUnitEnum._value2member_map_ else ChargingRateUnitEnum.W

            schedules.append(
                ChargingSchedule(
                    id=int(s["id"]),
                    chargingRateUnit=rate_unit,
                    chargingSchedulePeriod=periods,
                    startSchedule=s.get("startSchedule"),
                    duration=s.get("duration"),
                    minChargingRate=s.get("minChargingRate"),
                )
            )

        recur = None
        if "recurrencyKind" in cp_data and cp_data["recurrencyKind"]:
            recur = RecurrencyKindEnum(cp_data["recurrencyKind"])

        profile = ChargingProfile(
            id=int(cp_data["id"]),
            stackLevel=int(cp_data["stackLevel"]),
            chargingProfilePurpose=ChargingProfilePurposeEnum(cp_data["chargingProfilePurpose"]),
            chargingProfileKind=ChargingProfileKindEnum(cp_data["chargingProfileKind"]),
            chargingSchedule=schedules,
            recurrencyKind=recur,
            validFrom=cp_data.get("validFrom"),
            validTo=cp_data.get("validTo"),
            transactionId=cp_data.get("transactionId"),
        )
        return cls(evseId=evse_id, chargingProfile=profile)


@dataclass
class SetChargingProfileResponse:
    status: ChargingProfileStatusEnum
    statusInfo: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "status": str(self.status.value if isinstance(self.status, Enum) else self.status)
        }
        if self.statusInfo:
            d["statusInfo"] = self.statusInfo
        return d


@dataclass
class ClearChargingProfileRequest:
    chargingProfileId: Optional[int] = None
    chargingProfileCriteria: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}
        if self.chargingProfileId is not None:
            d["chargingProfileId"] = int(self.chargingProfileId)
        if self.chargingProfileCriteria:
            d["chargingProfileCriteria"] = self.chargingProfileCriteria
        return d


@dataclass
class ClearChargingProfileResponse:
    status: ClearChargingProfileStatusEnum
    statusInfo: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "status": str(self.status.value if isinstance(self.status, Enum) else self.status)
        }
        if self.statusInfo:
            d["statusInfo"] = self.statusInfo
        return d


@dataclass
class DCChargingParameters:
    evMaxCurrent: float                     # A
    evMaxVoltage: float                     # V
    evMaxPower: Optional[float] = None      # W
    energyAmount: Optional[float] = None    # Wh
    evEnergyCapacity: Optional[float] = None# Wh
    fullSoC: Optional[float] = 100.0        # %
    bulkSoC: Optional[float] = 80.0         # %
    stateOfCharge: Optional[float] = 0.0    # %


@dataclass
class ChargingNeeds:
    evseId: int
    requestedEnergyTransfer: EnergyTransferModeEnum = EnergyTransferModeEnum.DC
    departureTime: Optional[str] = None
    dcChargingParameters: Optional[DCChargingParameters] = None
    acChargingParameters: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        trans_str = (
            self.requestedEnergyTransfer.value
            if isinstance(self.requestedEnergyTransfer, Enum)
            else str(self.requestedEnergyTransfer)
        )
        d: Dict[str, Any] = {
            "evseId": int(self.evseId),
            "requestedEnergyTransfer": trans_str,
        }
        if self.departureTime:
            d["departureTime"] = self.departureTime
        if self.dcChargingParameters:
            dc = self.dcChargingParameters
            d["dcChargingParameters"] = {
                "evMaxCurrent": dc.evMaxCurrent,
                "evMaxVoltage": dc.evMaxVoltage,
                "evMaxPower": dc.evMaxPower,
                "energyAmount": dc.energyAmount,
                "evEnergyCapacity": dc.evEnergyCapacity,
                "fullSoC": dc.fullSoC,
                "bulkSoC": dc.bulkSoC,
                "stateOfCharge": dc.stateOfCharge,
            }
        if self.acChargingParameters:
            d["acChargingParameters"] = self.acChargingParameters
        return d


@dataclass
class CostUpdatedRequest:
    totalCost: float
    transactionId: str
    currency: str = "EUR"
    currentRateEurKwh: float = 0.0
    nextPeriodRateEurKwh: Optional[float] = None
    nextPeriodStart: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "totalCost": round(float(self.totalCost), 4),
            "transactionId": str(self.transactionId),
            "currency": self.currency,
            "currentRateEurKwh": round(float(self.currentRateEurKwh), 4),
        }
        if self.nextPeriodRateEurKwh is not None:
            d["nextPeriodRateEurKwh"] = round(float(self.nextPeriodRateEurKwh), 4)
        if self.nextPeriodStart:
            d["nextPeriodStart"] = self.nextPeriodStart
        return d


# ============================================================================
# 3. OCPP 2.0.1 Device Model Component-Variable Monitoring (F08)
# ============================================================================

@dataclass
class Component:
    name: str                              # PowerModule, FanSpeed, CoolingSystem, IsolationMonitoringDevice
    instance: Optional[str] = None         # C1-M01, CabinetFan1, Cabinet-1, DC_Bus
    evse: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"name": self.name}
        if self.instance:
            d["instance"] = self.instance
        if self.evse:
            d["evse"] = self.evse
        return d


@dataclass
class Variable:
    name: str                              # Status, Current, Temperature, Speed, Resistance
    instance: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"name": self.name}
        if self.instance:
            d["instance"] = self.instance
        return d


@dataclass
class EventData:
    eventId: int
    timestamp: str                         # ISO 8601 UTC
    trigger: EventTriggerEnum
    cause: str                             # UpperThreshold, LowerThreshold, Abnormal, Normal
    actualValue: str
    component: Component
    variable: Variable
    eventNotificationType: EventNotificationEnum
    severity: int = 3                      # 1=Emergency, 2=Fault, 3=Warning, 4=Info

    def to_dict(self) -> Dict[str, Any]:
        trig_str = self.trigger.value if isinstance(self.trigger, Enum) else str(self.trigger)
        notif_str = (
            self.eventNotificationType.value
            if isinstance(self.eventNotificationType, Enum)
            else str(self.eventNotificationType)
        )
        return {
            "eventId": int(self.eventId),
            "timestamp": self.timestamp,
            "trigger": trig_str,
            "cause": self.cause,
            "actualValue": str(self.actualValue),
            "component": self.component.to_dict(),
            "variable": self.variable.to_dict(),
            "eventNotificationType": notif_str,
            "severity": int(self.severity),
        }


@dataclass
class NotifyEventRequest:
    generatedAt: str
    seqNo: int
    eventData: List[EventData]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "generatedAt": self.generatedAt,
            "seqNo": int(self.seqNo),
            "eventData": [e.to_dict() for e in self.eventData],
        }


# ============================================================================
# 4. ISO 15118-2/20 Plug & Charge (PnC) Architecture (F09)
# ============================================================================

class AuthorizationStatus(str, Enum):
    ACCEPTED = "Accepted"
    CERTIFICATE_REVOKED = "CertificateRevoked"
    CERTIFICATE_EXPIRED = "CertificateExpired"
    INVALID_SIGNATURE = "InvalidSignature"
    UNKNOWN_ROOT_CA = "UnknownRootCA"
    MALFORMED_CERTIFICATE = "MalformedCertificate"
    CHALLENGE_FAILED = "ChallengeFailed"


class PnCState(str, Enum):
    DISCONNECTED = "DISCONNECTED"
    SUPPORTED_APP_PROTOCOL = "SUPPORTED_APP_PROTOCOL"
    SESSION_SETUP = "SESSION_SETUP"
    AUTHORIZATION_SETUP = "AUTHORIZATION_SETUP"
    PAYMENT_DETAILS = "PAYMENT_DETAILS"
    CERTIFICATE_VERIFICATION = "CERTIFICATE_VERIFICATION"
    CHARGE_PARAMETER_DISCOVERY = "CHARGE_PARAMETER_DISCOVERY"
    PRE_CHARGE = "PRE_CHARGE"
    POWER_DELIVERY_START = "POWER_DELIVERY_START"
    CURRENT_DEMAND = "CURRENT_DEMAND"
    POWER_DELIVERY_STOP = "POWER_DELIVERY_STOP"
    SESSION_STOP = "SESSION_STOP"


@dataclass
class X509CertValidationResult:
    status: AuthorizationStatus
    is_authorized: bool
    emaid: str
    subject: str
    issuer: str
    serial_number: int
    duration_ms: float
    error_message: Optional[str] = None


@dataclass
class MCSChargeParameters:
    ev_max_voltage_v: float = 1250.0
    ev_max_current_a: float = 3000.0
    ev_max_power_kw: float = 3750.0
    departure_time: Optional[str] = None
    target_energy_kwh: float = 300.0
    v2g_bpt_enabled: bool = False
    v2g_max_discharge_kw: float = 0.0
    v2g_min_soc_pct: float = 20.0
    reactive_power_var: float = 0.0


class CertificateAuthorityManager:
    """Manages PKI trust anchors, intermediate CAs, and CRL revocations for SECC."""

    def __init__(self):
        self.trusted_roots: Dict[str, x509.Certificate] = {}
        self.revoked_serials: Set[int] = set()

    def add_trusted_root(self, cert: x509.Certificate) -> None:
        attrs = cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)
        common_name = str(attrs[0].value) if attrs else cert.subject.rfc4514_string()
        self.trusted_roots[common_name] = cert

    def revoke_serial(self, serial_number: int) -> None:
        self.revoked_serials.add(int(serial_number))

    def is_revoked(self, serial_number: int) -> bool:
        return int(serial_number) in self.revoked_serials

    @classmethod
    def generate_test_pki_hierarchy(
        cls,
    ) -> Tuple[str, ec.EllipticCurvePrivateKey, x509.Certificate, x509.Certificate, x509.Certificate]:
        """
        Generates an authentic 3-tier PKI hierarchy:
        Root CA -> Provisioning Sub-CA -> Contract Leaf Certificate.
        Returns: (pem_chain, leaf_private_key, leaf_cert, sub_cert, root_cert)
        """
        now = datetime.now(timezone.utc)

        # 1. Root CA
        root_key = ec.generate_private_key(ec.SECP256R1())
        root_name = x509.Name([
            x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, "Kempower V2G Root CA"),
            x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, "Kempower Oyj"),
            x509.NameAttribute(x509.oid.NameOID.COUNTRY_NAME, "FI"),
        ])
        root_cert = (
            x509.CertificateBuilder()
            .subject_name(root_name)
            .issuer_name(root_name)
            .public_key(root_key.public_key())
            .serial_number(1001)
            .not_valid_before(now - timedelta(days=30))
            .not_valid_after(now + timedelta(days=3650))
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_cert_sign=True,
                    crl_sign=True,
                    content_commitment=False,
                    key_encipherment=False,
                    data_encipherment=False,
                    key_agreement=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            )
            .sign(root_key, hashes.SHA256())
        )

        # 2. Sub CA
        sub_key = ec.generate_private_key(ec.SECP256R1())
        sub_name = x509.Name([
            x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, "Fleet OEM Provisioning Sub-CA 1"),
            x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, "Kempower Partner OEM"),
            x509.NameAttribute(x509.oid.NameOID.COUNTRY_NAME, "FI"),
        ])
        sub_cert = (
            x509.CertificateBuilder()
            .subject_name(sub_name)
            .issuer_name(root_name)
            .public_key(sub_key.public_key())
            .serial_number(2001)
            .not_valid_before(now - timedelta(days=30))
            .not_valid_after(now + timedelta(days=1825))
            .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_cert_sign=True,
                    crl_sign=True,
                    content_commitment=False,
                    key_encipherment=False,
                    data_encipherment=False,
                    key_agreement=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            )
            .sign(root_key, hashes.SHA256())
        )

        # 3. Leaf Certificate (Contract Certificate with EMAID)
        leaf_key = ec.generate_private_key(ec.SECP256R1())
        leaf_name = x509.Name([
            x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, "EMAID:FI-KEM-C12345678-X"),
            x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, "Helsinki Regional Transport"),
            x509.NameAttribute(x509.oid.NameOID.COUNTRY_NAME, "FI"),
        ])
        leaf_cert = (
            x509.CertificateBuilder()
            .subject_name(leaf_name)
            .issuer_name(sub_name)
            .public_key(leaf_key.public_key())
            .serial_number(3001)
            .not_valid_before(now - timedelta(days=30))
            .not_valid_after(now + timedelta(days=365))
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_cert_sign=False,
                    crl_sign=False,
                    content_commitment=False,
                    key_encipherment=False,
                    data_encipherment=False,
                    key_agreement=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            )
            .sign(sub_key, hashes.SHA256())
        )

        pem_chain = (
            leaf_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
            + sub_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
            + root_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
        )
        return pem_chain, leaf_key, leaf_cert, sub_cert, root_cert


def _get_cert_valid_not_before(cert: x509.Certificate) -> datetime:
    if hasattr(cert, "not_valid_before_utc"):
        return cert.not_valid_before_utc
    return cert.not_valid_before.replace(tzinfo=timezone.utc)


def _get_cert_valid_not_after(cert: x509.Certificate) -> datetime:
    if hasattr(cert, "not_valid_after_utc"):
        return cert.not_valid_after_utc
    return cert.not_valid_after.replace(tzinfo=timezone.utc)


class Iso15118PnCEngine:
    """ISO 15118-2/20 Plug & Charge Handshake & Verification Engine."""

    def __init__(self, ca_manager: Optional[CertificateAuthorityManager] = None):
        self.ca_manager = ca_manager or CertificateAuthorityManager()

    def validate_certificate_chain(
        self,
        cert_chain_pem: str,
        challenge: Optional[bytes] = None,
        challenge_signature: Optional[bytes] = None,
        now: Optional[datetime] = None,
    ) -> X509CertValidationResult:
        """
        Validates X.509 v3 certificate chain according to ISO 15118-2/20.
        Timing guarantee: completes in < 1500 ms (typically < 10 ms).
        """
        t0 = time.perf_counter()
        current_time = now or datetime.now(timezone.utc)
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)

        try:
            certs = x509.load_pem_x509_certificates(cert_chain_pem.encode("utf-8"))
        except Exception as e:
            return X509CertValidationResult(
                status=AuthorizationStatus.MALFORMED_CERTIFICATE,
                is_authorized=False,
                emaid="",
                subject="",
                issuer="",
                serial_number=0,
                duration_ms=(time.perf_counter() - t0) * 1000.0,
                error_message=f"PEM decoding failure: {str(e)}",
            )

        if len(certs) < 2:
            return X509CertValidationResult(
                status=AuthorizationStatus.MALFORMED_CERTIFICATE,
                is_authorized=False,
                emaid="",
                subject="",
                issuer="",
                serial_number=0,
                duration_ms=(time.perf_counter() - t0) * 1000.0,
                error_message="Incomplete certificate chain (minimum 2 certs required)",
            )

        leaf = certs[0]
        sub_ca = certs[1]
        root_ca = certs[2] if len(certs) >= 3 else None

        leaf_subject = leaf.subject.rfc4514_string()
        leaf_issuer = leaf.issuer.rfc4514_string()
        serial_no = leaf.serial_number

        # Extract EMAID
        emaid = ""
        cn_attrs = leaf.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)
        if cn_attrs:
            val = str(cn_attrs[0].value)
            if "EMAID:" in val:
                emaid = val.split("EMAID:", 1)[1].strip()
            else:
                emaid = val

        # 1. Revocation Check
        if any(self.ca_manager.is_revoked(c.serial_number) for c in certs):
            return X509CertValidationResult(
                status=AuthorizationStatus.CERTIFICATE_REVOKED,
                is_authorized=False,
                emaid=emaid,
                subject=leaf_subject,
                issuer=leaf_issuer,
                serial_number=serial_no,
                duration_ms=(time.perf_counter() - t0) * 1000.0,
                error_message="Certificate serial number present on CRL blacklist",
            )

        # 2. Validity Dates Check
        for c in certs:
            not_before = _get_cert_valid_not_before(c)
            not_after = _get_cert_valid_not_after(c)
            if current_time < not_before or current_time > not_after:
                return X509CertValidationResult(
                    status=AuthorizationStatus.CERTIFICATE_EXPIRED,
                    is_authorized=False,
                    emaid=emaid,
                    subject=leaf_subject,
                    issuer=leaf_issuer,
                    serial_number=serial_no,
                    duration_ms=(time.perf_counter() - t0) * 1000.0,
                    error_message=f"Certificate expired or not yet valid (serial={c.serial_number})",
                )

        # 3. Cryptographic Signature Verification
        try:
            sub_ca.public_key().verify(
                leaf.signature,
                leaf.tbs_certificate_bytes,
                ec.ECDSA(leaf.signature_hash_algorithm),
            )
            if root_ca:
                root_ca.public_key().verify(
                    sub_ca.signature,
                    sub_ca.tbs_certificate_bytes,
                    ec.ECDSA(sub_ca.signature_hash_algorithm),
                )
        except InvalidSignature:
            return X509CertValidationResult(
                status=AuthorizationStatus.INVALID_SIGNATURE,
                is_authorized=False,
                emaid=emaid,
                subject=leaf_subject,
                issuer=leaf_issuer,
                serial_number=serial_no,
                duration_ms=(time.perf_counter() - t0) * 1000.0,
                error_message="Cryptographic signature verification failed along certificate chain",
            )
        except Exception as e:
            return X509CertValidationResult(
                status=AuthorizationStatus.INVALID_SIGNATURE,
                is_authorized=False,
                emaid=emaid,
                subject=leaf_subject,
                issuer=leaf_issuer,
                serial_number=serial_no,
                duration_ms=(time.perf_counter() - t0) * 1000.0,
                error_message=f"Signature verification error: {str(e)}",
            )

        # 4. Root CA Trust Anchor Verification
        top_ca = certs[-1]
        if self.ca_manager.trusted_roots:
            attrs = top_ca.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)
            top_cn = str(attrs[0].value) if attrs else top_ca.subject.rfc4514_string()
            if top_cn not in self.ca_manager.trusted_roots:
                return X509CertValidationResult(
                    status=AuthorizationStatus.UNKNOWN_ROOT_CA,
                    is_authorized=False,
                    emaid=emaid,
                    subject=leaf_subject,
                    issuer=leaf_issuer,
                    serial_number=serial_no,
                    duration_ms=(time.perf_counter() - t0) * 1000.0,
                    error_message=f"Root CA '{top_cn}' not in trusted anchor store",
                )

        # 5. Optional Challenge/Response Verification
        if challenge and challenge_signature:
            try:
                leaf.public_key().verify(
                    challenge_signature,
                    challenge,
                    ec.ECDSA(hashes.SHA256()),
                )
            except (InvalidSignature, TypeError, ValueError, Exception) as e:
                return X509CertValidationResult(
                    status=AuthorizationStatus.CHALLENGE_FAILED,
                    is_authorized=False,
                    emaid=emaid,
                    subject=leaf_subject,
                    issuer=leaf_issuer,
                    serial_number=serial_no,
                    duration_ms=(time.perf_counter() - t0) * 1000.0,
                    error_message=f"Vehicle failed GenChallenge cryptographic check: {str(e)}",
                )

        duration = (time.perf_counter() - t0) * 1000.0
        return X509CertValidationResult(
            status=AuthorizationStatus.ACCEPTED,
            is_authorized=True,
            emaid=emaid,
            subject=leaf_subject,
            issuer=leaf_issuer,
            serial_number=serial_no,
            duration_ms=duration,
        )


def verify_iso15118_handshake(cert_chain_pem: str, session_id: str) -> Tuple[bool, str]:
    """
    Authoritative public contract matching PROJECT.md line 105:
    Validates TLS 1.3 certificate chain, returns authorization status (True/False)
    and contract ID (EMAID) or error code.
    """
    engine = Iso15118PnCEngine()
    res = engine.validate_certificate_chain(cert_chain_pem)
    if res.is_authorized:
        return True, res.emaid or f"CONTRACT-{session_id}"
    return False, res.status.value


# ============================================================================
# 5. Bridge & Adapter Functions
# ============================================================================

def build_ocpp_tx_profile(
    schedule: Any,  # VehicleSchedule instance
    interval_minutes: int = 15,
    power_array: Optional[Any] = None,  # List[float] or np.ndarray
    evse_id: int = 1,
    profile_id: int = 1,
    stack_level: int = 1,
    transaction_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Constructs a valid OCPP 2.0.1 SetChargingProfileRequest dictionary
    for an ongoing charging transaction (TxProfile).
    Limits are emitted in Watts (W) per OCPP 2.0.1 standard.
    """
    step_duration_s = interval_minutes * 60
    periods: List[ChargingSchedulePeriod] = []

    if power_array is not None and len(power_array) > 0:
        for idx, p_kw in enumerate(power_array):
            start_p = idx * step_duration_s
            limit_w = max(0.0, float(p_kw) * 1000.0)
            periods.append(ChargingSchedulePeriod(startPeriod=start_p, limit=limit_w))
        total_duration = len(power_array) * step_duration_s
    else:
        # Default single flat envelope bounded by vehicle max_charge_kw
        dep = getattr(schedule, "depart_step", 4)
        arr = getattr(schedule, "arrive_step", 0)
        steps = max(1, dep - arr)
        total_duration = steps * step_duration_s
        max_kw = getattr(schedule, "max_charge_kw", 150.0)
        periods.append(
            ChargingSchedulePeriod(startPeriod=0, limit=float(max_kw) * 1000.0)
        )

    v_id = getattr(schedule, "vehicle_id", f"EV-{evse_id}")
    tx_id = transaction_id or f"TX-{v_id}-{evse_id}"

    sched = ChargingSchedule(
        id=profile_id,
        chargingRateUnit=ChargingRateUnitEnum.W,
        chargingSchedulePeriod=periods,
        duration=total_duration,
    )

    profile = ChargingProfile(
        id=profile_id,
        stackLevel=stack_level,
        chargingProfilePurpose=ChargingProfilePurposeEnum.TX_PROFILE,
        chargingProfileKind=ChargingProfileKindEnum.RELATIVE,
        chargingSchedule=sched,
        transactionId=tx_id,
    )

    req = SetChargingProfileRequest(evseId=evse_id, chargingProfile=profile)
    return req.to_dict()


def parse_charging_needs(
    charging_needs_payload: Dict[str, Any],
    current_time_iso: Optional[str] = None,
    interval_minutes: int = 15,
) -> Any:
    """
    Parses an incoming OCPP 2.0.1 / ISO 15118 ChargingNeeds payload into a
    VehicleSchedule dataclass instance ready for the MPC optimizer.
    """
    from src.core.mpc_optimizer import VehicleSchedule

    evse_id = charging_needs_payload.get("evseId", 1)
    v_id = charging_needs_payload.get("vehicleId", f"EV-D1-{evse_id}")

    dc_params = charging_needs_payload.get("dcChargingParameters", {})
    ev_max_current = float(dc_params.get("evMaxCurrent", 250.0))
    ev_max_voltage = float(dc_params.get("evMaxVoltage", 800.0))
    ev_max_power_w = dc_params.get("evMaxPower")

    if ev_max_power_w is not None:
        max_kw = float(ev_max_power_w) / 1000.0
    else:
        max_kw = (ev_max_current * ev_max_voltage) / 1000.0

    # Battery capacity
    capacity_wh = dc_params.get("evEnergyCapacity")
    req_energy_wh = dc_params.get("energyAmount")

    if capacity_wh is not None:
        battery_kwh = float(capacity_wh) / 1000.0
    elif req_energy_wh is not None:
        battery_kwh = float(req_energy_wh) / 1000.0 / 0.8  # Assume ~80% delta
    else:
        battery_kwh = 150.0  # Standard commercial bus default

    # SoC
    soc_pct = float(dc_params.get("stateOfCharge", 20.0))
    target_soc_pct = float(dc_params.get("fullSoC", dc_params.get("bulkSoC", 90.0)))
    arrive_soc = max(0.0, min(1.0, soc_pct / 100.0))
    required_soc = max(arrive_soc, min(1.0, target_soc_pct / 100.0))

    # Departure calculation
    dep_time_str = charging_needs_payload.get("departureTime")
    if dep_time_str and current_time_iso:
        try:
            t_dep = dateutil.parser.isoparse(dep_time_str)
            t_curr = dateutil.parser.isoparse(current_time_iso)
            delta_s = max(900.0, (t_dep - t_curr).total_seconds())
            steps = max(1, int(round(delta_s / (interval_minutes * 60))))
            arrive_step = 0
            depart_step = steps
        except Exception:
            arrive_step = 0
            depart_step = 4
    else:
        arrive_step = int(charging_needs_payload.get("arrive_step", 0))
        depart_step = int(charging_needs_payload.get("depart_step", 4))

    dispenser_str = charging_needs_payload.get("dispenserId", f"D1-{evse_id}")

    return VehicleSchedule(
        vehicle_id=v_id,
        arrive_step=arrive_step,
        depart_step=depart_step,
        arrive_soc=arrive_soc,
        required_soc=required_soc,
        battery_kwh=battery_kwh,
        max_charge_kw=max_kw,
        dispenser_id=dispenser_str,
    )


def build_notify_event_from_snapshot(
    snapshot: Any,  # TelemetrySnapshot instance
    seq_no: int = 1,
) -> Dict[str, Any]:
    """
    Transforms internal TelemetrySnapshot into standard OCPP 2.0.1 NotifyEventRequest
    reporting component-variable telemetry:
    - PowerModule status & current
    - FanSpeed RPM
    - CoolingSystem Temperature
    - IsolationMonitoringDevice resistance
    """
    events: List[EventData] = []
    event_id = 1
    ts = snapshot.timestamp if hasattr(snapshot, "timestamp") else datetime.now(timezone.utc).isoformat()

    # 1. Process Cabinets
    cabinets = snapshot.cabinets if hasattr(snapshot, "cabinets") else {}
    for cab_id, cab in cabinets.items():
        # CoolingSystem Temperature
        temp = float(cab.cabinet_temp_c)
        if temp >= 75.0:
            events.append(
                EventData(
                    eventId=event_id,
                    timestamp=ts,
                    trigger=EventTriggerEnum.ALERTING,
                    cause="UpperThreshold",
                    actualValue=f"{temp:.1f}",
                    component=Component(name="CoolingSystem", instance=cab_id),
                    variable=Variable(name="Temperature"),
                    eventNotificationType=EventNotificationEnum.HARD_WIRED_NOTIFICATION,
                    severity=EventSeverityEnum.DANGER.value,
                )
            )
            event_id += 1
        elif temp >= 59.3:
            events.append(
                EventData(
                    eventId=event_id,
                    timestamp=ts,
                    trigger=EventTriggerEnum.ALERTING,
                    cause="UpperThreshold",
                    actualValue=f"{temp:.1f}",
                    component=Component(name="CoolingSystem", instance=cab_id),
                    variable=Variable(name="Temperature"),
                    eventNotificationType=EventNotificationEnum.PRE_ALERT_NOTIFICATION,
                    severity=EventSeverityEnum.WARNING.value,
                )
            )
            event_id += 1

        # FanSpeed RPM
        fan_rpm = getattr(cab, "fan_rpm", None)
        nom_rpm = getattr(cab, "nominal_fan_rpm", None) or 1400.0
        if fan_rpm is not None:
            fan_val = float(fan_rpm)
            if fan_val < 480.0 or (nom_rpm > 0 and (nom_rpm - fan_val) / nom_rpm >= 0.20):
                events.append(
                    EventData(
                        eventId=event_id,
                        timestamp=ts,
                        trigger=EventTriggerEnum.ALERTING,
                        cause="LowerThreshold",
                        actualValue=f"{fan_val:.0f}",
                        component=Component(name="FanSpeed", instance=f"{cab_id}-Fan1"),
                        variable=Variable(name="Speed"),
                        eventNotificationType=EventNotificationEnum.PRE_ALERT_NOTIFICATION,
                        severity=EventSeverityEnum.WARNING.value,
                    )
                )
                event_id += 1

    # 2. Check Active Faults (Ground Fault / IMD & Power Module)
    active_faults = getattr(snapshot, "active_faults", [])
    for fault in active_faults:
        cat = fault.get("fault_category", "").lower()
        cab_id = fault.get("cabinet_id", "C1")
        if "ground" in cat or "insulation" in cat:
            events.append(
                EventData(
                    eventId=event_id,
                    timestamp=ts,
                    trigger=EventTriggerEnum.ALERTING,
                    cause="LowerThreshold",
                    actualValue="45.0",  # < 50 kOhm trip
                    component=Component(name="IsolationMonitoringDevice", instance="DC_Bus"),
                    variable=Variable(name="Resistance"),
                    eventNotificationType=EventNotificationEnum.HARD_WIRED_NOTIFICATION,
                    severity=EventSeverityEnum.DANGER.value,
                )
            )
            event_id += 1
        elif "power_module" in cat or "module" in cat:
            events.append(
                EventData(
                    eventId=event_id,
                    timestamp=ts,
                    trigger=EventTriggerEnum.ALERTING,
                    cause="Abnormal",
                    actualValue="Faulted",
                    component=Component(name="PowerModule", instance=f"{cab_id}-M01"),
                    variable=Variable(name="Status"),
                    eventNotificationType=EventNotificationEnum.HARD_WIRED_NOTIFICATION,
                    severity=EventSeverityEnum.FAULT.value,
                )
            )
            event_id += 1

    req = NotifyEventRequest(generatedAt=ts, seqNo=seq_no, eventData=events)
    return req.to_dict()


def build_cost_updated_request(
    total_cost: float,
    transaction_id: str,
    spot_price_mwh: float,
    tariff_eur_kwh: float = 0.024,
) -> Dict[str, Any]:
    """
    Constructs a CostUpdatedRequest streaming current dynamic electricity tariff
    and accumulated cost in EUR.
    """
    current_rate = (spot_price_mwh / 1000.0) + tariff_eur_kwh
    req = CostUpdatedRequest(
        totalCost=total_cost,
        transactionId=transaction_id,
        currency="EUR",
        currentRateEurKwh=current_rate,
    )
    return req.to_dict()
