"""
Kempower Self-Operating Charging Network - Core Engine
Package: src.core

Exports:
- Dynamic Power Routing (DPR) Matrix & Contactor Zero-Arc Switching
- Virtual Replug & Dual-Gun Satellite Multiplexing
- Macro 15-minute Rolling Horizon MPC / MILP Optimizer
- Edge Micro Finite State Machine & 5 Hidden Failure Defenses
"""

from src.core.dpr_matrix import (
    DPRMatrix,
    PowerModule,
    BreakBeforeMakeStep,
    BreakBeforeMakeSequence,
    DPRAllocationResult,
    ContactorState,
    MODULE_POWER_KW,
    INVERTER_EFFICIENCY,
    CONTACTOR_MAX_SWITCH_DELAY_MS,
    STATION_CABINET_TOPOLOGY,
)

from src.core.virtual_replug import (
    VirtualReplugManager,
    PlugAndQueueHub,
    BusState,
    PlugType,
    PlugState,
    DualGunDispatchResult,
)

from src.core.mpc_optimizer import (
    MPCOptimizer,
    VehicleSchedule,
    BESSConfig,
    SiteMPCConfig,
    DispatchPlan,
)

from src.core.self_healing import (
    EdgeFSM,
    EdgeState,
    CabinetTelemetry,
    ChargerTelemetry,
    TelemetrySnapshot,
    ContactorCommand,
    FSMStateAction,
    InverterEfficiencyGuard,
    PredictiveThermalEngine,
    OfflineIslandingController,
    CommissioningAutoCalibrator,
)

__all__ = [
    # DPR Matrix
    "DPRMatrix",
    "PowerModule",
    "BreakBeforeMakeStep",
    "BreakBeforeMakeSequence",
    "DPRAllocationResult",
    "ContactorState",
    "MODULE_POWER_KW",
    "INVERTER_EFFICIENCY",
    "CONTACTOR_MAX_SWITCH_DELAY_MS",
    # Virtual Replug
    "VirtualReplugManager",
    "PlugAndQueueHub",
    "BusState",
    "PlugType",
    "PlugState",
    "DualGunDispatchResult",
    # MPC Optimizer
    "MPCOptimizer",
    "VehicleSchedule",
    "BESSConfig",
    "SiteMPCConfig",
    "DispatchPlan",
    # Self-Healing Edge FSM
    "EdgeFSM",
    "EdgeState",
    "CabinetTelemetry",
    "ChargerTelemetry",
    "TelemetrySnapshot",
    "ContactorCommand",
    "FSMStateAction",
    "InverterEfficiencyGuard",
    "PredictiveThermalEngine",
    "OfflineIslandingController",
    "CommissioningAutoCalibrator",
]
