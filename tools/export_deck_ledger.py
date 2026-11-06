"""Deck ledger exporter (read-only).

Single source of truth for presentation.html: every number the deck shows comes from either
(a) the shipped simulation engine ScenarioEngine.run_all_scenarios(), or (b) the unmodified
official CSVs. This script never edits the engine or the dataset; its only output is
demo/deck_ledger.json.

Usage:  python tools/export_deck_ledger.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kempower-challenge" / "kempower-challenge-data"
OUT = ROOT / "demo" / "deck_ledger.json"
sys.path.insert(0, str(ROOT))

import pandas as pd  # noqa: E402

from src.sim.data_loader import KempowerDataLoader  # noqa: E402
from src.sim.scenario_engine import ScenarioEngine  # noqa: E402
from src.sim.discrete_sim import Job, run_discrete_event_simulation  # noqa: E402

TZS = "+02:00"
DAY, PREV = "2026-11-13", "2026-11-12"
DROP = {"vehicle_records", "undercharged_vehicles", "never_charged", "last_finish_ts"}

ENGINE = ScenarioEngine(KempowerDataLoader()).run_all_scenarios()
S1, S2, S3, S4, S5 = ENGINE["S1"], ENGINE["S2"], ENGINE["S3"], ENGINE["S4"], ENGINE["S5"]
CSV = {p.name: p for p in sorted(DATA.glob("*.csv"))}


def rd(name):
    return pd.read_csv(CSV[name])


def r(x, n=2):
    try:
        if x is None or pd.isna(x):
            return None
        return round(float(x), n)
    except (TypeError, ValueError):
        return None


def slim(d):
    if not isinstance(d, dict):
        return {}
    return {k: (v if k != "undercharged" else [list(u) for u in v]) for k, v in d.items() if k not in DROP}


_FS = rd("fleet_schedule.csv")
JOB_COUNT = {s: (int(g["vehicle_id"].count()), int(g["vehicle_id"].nunique())) for s, g in
             _FS[_FS.depart_ts.astype(str).str.startswith(DAY)].groupby("site_id")}


def variant(site, cab, ppc, tie, gun, fault_ts, strategy, dep=DAY):
    veh = {v["vehicle_id"]: v for v in rd("vehicles.csv").to_dict("records")}
    jobs = []
    for row in rd("fleet_schedule.csv").to_dict("records"):
        if row["site_id"] != site or pd.isna(row["depart_ts"]) or not str(row["depart_ts"]).startswith(dep):
            continue
        v = veh.get(row["vehicle_id"], {})
        jobs.append(Job(vehicle_id=row["vehicle_id"], arrive=datetime.fromisoformat(str(row["arrive_ts"])),
                        depart=datetime.fromisoformat(str(row["depart_ts"])),
                        battery_kwh=float(v.get("battery_kwh", 400.0)), soc_in=float(row["arrive_soc_pct"]) / 100.0,
                        soc_req=float(row["required_soc_pct"]) / 100.0, max_kw=float(v.get("max_charge_kw", 150.0))))
    jobs.sort(key=lambda j: j.arrive)
    fault = (datetime.fromisoformat(fault_ts + TZS), [2]) if fault_ts else None
    res = slim(run_discrete_event_simulation(jobs, site, dep, cab, ppc, strategy=strategy, fault=fault,
                                             cross_tie=tie, gun_kw=gun).to_dict())
    res["jobs"], res["unique_vehicles"] = len(jobs), len({j.vehicle_id for j in jobs})
    return res


L = {"meta": {}, "engine": {}, "labor": {}, "events": [], "sites": {}, "grid": {}, "utilization": {},
     "cost": {}, "commercial": {}, "growth": {}, "anim": {}, "flags": []}

# ------------------------------------------------------------------ meta
rows = 0
for p in CSV.values():
    with open(p, encoding="utf-8", errors="ignore") as f:
        rows += len(f.readlines()) - 1
L["meta"] = {"csv_files": len(CSV), "data_rows": rows, "sites_total": 100, "sites_network": 95,
             "sites_close_up": 5, "scenario_day": DAY, "blueprint": "PITCH_DECK_OUTLINE.md",
             "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "generator": "tools/export_deck_ledger.py",
             "authority": "ScenarioEngine.run_all_scenarios() + official CSVs (dataset unmodified)",
             "brief": "LahtiES Energy Tech Hackathon 2026 / Kempower challenge - Self-Operating Charging Network",
             "rubric": {"degree_of_autonomy": 25, "energy_and_grid_impact": 20, "technical_credibility": 20,
                        "commercial_viability": 20, "clarity": 15}}

# ------------------------------------------------------------------ engine headline
L["engine"] = {
    "scenario_day_missed_before": ENGINE.get("scenario_day_missed_before"),
    "scenario_day_missed_after": ENGINE.get("scenario_day_missed_after"),
    "zero_over_limit_verified": ENGINE["network_zero_over_limit"].get("zero_over_limit_verified"),
    "zero_over_limit_rows": ENGINE["network_zero_over_limit"].get("total_rows"),
    "s1_thermal": slim(S1["thermal_anomaly_audit"]), "s1_n1": slim(S1["n1_post_fault_audit"]),
    "s1_connector": slim(S1["connector_feasibility"]), "s1_strategy_a": slim(S1["strategy_a_0capex"]),
    "s1_strategy_b": slim(S1["strategy_b_hardware"]),
    "s2_reallocation": {"headroom_1420_1600_kwh": S2.get("true_grid_headroom_1420_1600_kwh"),
                        "overnight_pool_kwh": S2.get("overnight_trucks_t05_t08_afternoon_kwh"),
                        "reallocated_kwh": S2.get("reallocated_from_t05_t08_kwh"),
                        "truck_deficits_kwh": S2.get("truck_deficits_kwh"),
                        "all_8_on_time_after": S2.get("all_8_trucks_on_time_after")},
    "s3_offline": {"state": S3.get("offline_islanding_state"), "max_safe_dc_kw": S3.get("offline_max_safe_dc_kw"),
                   "steady_ac_kw": S3.get("offline_steady_ac_kw"),
                   "queue_left_eliminated_14d": S3.get("left_queue_eliminated_by_plug_and_queue_14d"),
                   "queue_left_eliminated_day": S3.get("left_queue_eliminated_by_plug_and_queue_1113")},
    "s4_mpc": {k: v for k, v in S4.items() if k != "site_id"},
    "s5_reconcile": slim(S5.get("three_way_reconciliation", {})),
}

# ------------------------------------------------------------------ sites
def block(bl, opt, extra=None):
    b, o = slim(bl), slim(opt)
    d = {"baseline": b, "optimized": o, "moves_eliminated": [b.get("moves"), o.get("moves")]}
    d["deficit_closed_pct"] = r(100 * (b["deficit_kwh"] - o["deficit_kwh"]) / b["deficit_kwh"], 1) if b.get("deficit_kwh") else None
    for w in (b, o):
        if "jobs" not in w:
            w["jobs"], w["unique_vehicles"] = JOB_COUNT.get(w.get("site_id"), (None, None))
    if extra:
        d.update(extra)
    return d


F16 = "2026-11-13T02:25:00"
L["sites"]["S1"] = block(S1.get("baseline_discrete_sim", S1["discrete_sim"]), S1["discrete_sim"], {
    "official_recorded": {"departures": 32, "below_required": S1.get("baseline_missed_departures"),
                          "vehicles": S1.get("baseline_undercharged_vehicles"),
                          "still_under_after": S1.get("optimized_undercharged_vehicles"),
                          "zero_session_gap_kwh": S1.get("baseline_official_deficit_kwh")},
    "engine_fields": {"baseline_deficit_kwh": S1.get("baseline_deficit_kwh"),
                      "optimized_missed_departures": S1.get("optimized_missed_departures"),
                      "optimized_deficit_kwh": S1.get("optimized_deficit_kwh"),
                      "capacity_expansion_missed": S1.get("capacity_expansion_missed_departures")},
    "variants": {"busbar_tie_12guns": variant("S1", [360.0] * 3, 4, True, 150.0, F16, "urgency"),
                 "plugs_only_24_no_tie": variant("S1", [360.0] * 3, 8, False, 150.0, F16, "urgency"),
                 "plugs_and_tie_24": variant("S1", [360.0] * 3, 8, True, 150.0, F16, "urgency"),
                 "no_fault_fcfs": variant("S1", [360.0] * 3, 4, False, 150.0, None, "fcfs"),
                 "no_fault_urgency": variant("S1", [360.0] * 3, 4, False, 150.0, None, "urgency"),
                 "cabinet_3x450_no_cap": variant("S1", [450.0] * 3, 4, False, 150.0, F16, "urgency")},
    "capacity_sweep": [dict(cabinet_kw=kw, **{k: v for k, v in variant("S1", [kw] * 3, 4, False, 150.0, F16, "urgency").items()
                                               if k in ("missed_departures", "deficit_kwh", "peak_kw", "total_kwh")})
                       for kw in (325.0, 350.0, 360.0, 375.0, 380.0, 400.0, 450.0, 500.0)],
    "gun_sweep": [dict(gun_kw=g, **{k: v for k, v in variant("S1", [360.0] * 3, 4, False, g, F16, "urgency").items()
                                     if k in ("missed_departures", "deficit_kwh")}) for g in (140.0, 150.0, 120.0)]})

L["sites"]["S2"] = block(S2.get("baseline_discrete_sim", {}), S2["discrete_sim"], {
    "official_recorded": {"departures": 18, "below_required": S2.get("baseline_missed_departures"),
                          "vehicles": S2.get("baseline_undercharged_vehicles"),
                          "recorded_deficit_kwh": S2.get("baseline_deficit_kwh"),
                          "sim_deficit_kwh": S2.get("baseline_sim_deficit_kwh")},
    "note": "reference point is the official recorded deficit; same-engine sim deficit labelled separately"})

L["sites"]["S5"] = block(S5.get("baseline_discrete_sim", {}), S5["discrete_sim"], {
    "official_recorded": {"departures": 12, "below_required": S5.get("baseline_missed_departures"),
                          "sim_missed": S5.get("baseline_sim_missed_departures"),
                          "sim_deficit_kwh": S5.get("baseline_sim_deficit_kwh"),
                          "recorded_deficit_kwh": S5.get("baseline_deficit_kwh"),
                          "vehicles": S5.get("baseline_undercharged_vehicles"),
                          "still_under_after": S5.get("optimized_undercharged_vehicles")},
    "note": "config fix, not a same-engine A/B: 4 of the 5 official failures are plug-queueing we do not model"})

pub = S3.get("public_arrivals_empirical", {})
ns = rd("network_sites.csv").set_index("site_id")
fb = rd("site_config.csv")
fb = fb[fb.parameter == "offline_fallback_kw_per_dispenser"]
fb3 = float(fb[fb.site_id == "S3"].configured_value.iloc[0])
L["sites"]["S3"] = {"official_recorded": pub, "offline": L["engine"]["s3_offline"],
                    "fallback": {"kw_per_dispenser": fb3, "dispensers": int(ns.loc["S3", "dispensers"]),
                                 "station_kw": r(fb3 * int(ns.loc["S3", "dispensers"]), 1)},
                    "hardware": {"dispensers": int(ns.loc["S3", "dispensers"]), "dispenser_kw": float(ns.loc["S3", "dispenser_kw"]),
                                 "grid_limit_kw": float(ns.loc["S3", "grid_limit_kw"]), "eta": 0.955},
                    "no_post_hoc_abandonment_claim": True}
# --- S3 abandonment: ONE basis per file, both reported, never blended in one sentence
_pa = rd("public_arrivals.csv"); _pa["ts"] = pd.to_datetime(_pa["ts"])
_s3 = _pa[(_pa.site_id == "S3") & (_pa.ts.dt.strftime("%Y-%m-%d") == DAY)].copy()
_s3["ab"] = _s3.outcome != "charged"
_lo = pd.Timestamp(DAY + "T11:00:00" + TZS); _hi = pd.Timestamp(DAY + "T13:00:00" + TZS)
_w = _s3[(_s3.ts >= _lo) & (_s3.ts < _hi)]
_o = _s3[~((_s3.ts >= _lo) & (_s3.ts < _hi))]
_sp = rd("network_site_power.csv"); _sp["ts"] = pd.to_datetime(_sp["ts"])
_spw = _sp[(_sp.site_id == "S3") & (_sp.ts >= _lo) & (_sp.ts <= _hi)]
L["sites"]["S3"]["window_basis"] = {
    "public_arrivals_row_level": {
        "day": {"arrivals": int(len(_s3)), "abandoned": int(_s3.ab.sum()), "pct": r(100 * _s3.ab.mean(), 2)},
        "outage_window_11_13": {"arrivals": int(len(_w)), "abandoned": int(_w.ab.sum()),
                                "pct": r(100 * _w.ab.mean(), 2)},
        "outside_window": {"arrivals": int(len(_o)), "abandoned": int(_o.ab.sum()),
                           "pct": r(100 * _o.ab.mean(), 2)},
        "left_full_in_window": int((_w.outcome == "left_full").sum()),
        "left_queue_in_window": int((_w.outcome == "left_queue").sum())},
    "network_site_power_15min": {
        "arrivals": int(_spw.arrivals.sum()), "abandoned": int(_spw.abandoned.sum()),
        "pct": r(100 * _spw.abandoned.sum() / max(_spw.arrivals.sum(), 1), 2)},
    "rule": ("29.69% (day) and 44.83% (13/29, in-window) both come from public_arrivals.csv and may be "
             "quoted together; 46.88% (15/32) is the 15-minute aggregate in network_site_power.csv and "
             "must never be paired with the 76/256 day figure."),
}
L["sites"]["S4"] = {"mpc": L["engine"]["s4_mpc"],
                    "fault_F017": {"asset": "D4-2", "start": "2026-11-13T21:30", "cleared_by": "open"},
                    "hardware": {c: float(ns.loc["S4", c]) for c in ("dispensers", "dispenser_kw", "grid_limit_kw", "pv_kwp")}}

# ------------------------------------------------------------------ labor
op = rd("operations_log.csv")
by = op.groupby("action")[["count", "staff_minutes"]].sum()
WK = 37.5 * 60 * 2
RATE = float(rd("equipment_costs.csv").set_index("item").loc["operations_staff", "eur"])
ADDR = ["move_and_replug_vehicle", "manual_load_adjustment", "remote_reset", "manual_price_change"]
tn, tm = int(op["count"].sum()), int(op["staff_minutes"].sum())
L["labor"] = {
    "events": tn, "minutes_biweekly": tm, "hours_biweekly": r(tm / 60, 2), "fte_recorded": r(tm / WK, 2),
    "eur_per_hour": RATE, "eur_per_fte_year": r(RATE * 37.5 * 52, 0), "eur_year_recorded": r(tm / 60 * RATE * 26, 0),
    "addressable_events": int(by.loc[ADDR, "count"].sum()), "addressable_minutes": int(by.loc[ADDR, "staff_minutes"].sum()),
    "addressable_fte": r(by.loc[ADDR, "staff_minutes"].sum() / WK, 2),
    "addressable_eur_year": r(by.loc[ADDR, "staff_minutes"].sum() / 60 * RATE * 26, 0),
    "addressable_share_events_pct": r(100 * by.loc[ADDR, "count"].sum() / tn, 2),
    "addressable_share_minutes_pct": r(100 * by.loc[ADDR, "staff_minutes"].sum() / tm, 2),
    "retained": {"technician_events": int(by.loc["technician_visit", "count"]),
                 "technician_minutes": int(by.loc["technician_visit", "staff_minutes"]),
                 "technician_fte": r(by.loc["technician_visit", "staff_minutes"] / WK, 2),
                 "technician_eur_year": r(by.loc["technician_visit", "staff_minutes"] / 60 * RATE * 26, 0),
                 "contact_events": int(by.loc["customer_contact", "count"]),
                 "contact_fte": r(by.loc["customer_contact", "staff_minutes"] / WK, 2),
                 "reason": "official faults.csv clears 8 of 19 faults with cleared_by=technician -> attendance required"},
    "replug": {"events": int(by.loc["move_and_replug_vehicle", "count"]),
               "minutes": int(by.loc["move_and_replug_vehicle", "staff_minutes"]),
               "share_events_pct": r(100 * by.loc["move_and_replug_vehicle", "count"] / tn, 2),
               "share_minutes_pct": r(100 * by.loc["move_and_replug_vehicle", "staff_minutes"] / tm, 2),
               "fte": r(by.loc["move_and_replug_vehicle", "staff_minutes"] / WK, 2),
               "eur_year": r(by.loc["move_and_replug_vehicle", "staff_minutes"] / 60 * RATE * 26, 0)},
    "by_action": {a: {"events": int(by.loc[a, "count"]), "minutes": int(by.loc[a, "staff_minutes"]),
                      "share_minutes_pct": r(100 * by.loc[a, "staff_minutes"] / tm, 2),
                      "fte": r(by.loc[a, "staff_minutes"] / WK, 2),
                      "eur_year": r(by.loc[a, "staff_minutes"] / 60 * RATE * 26, 0)} for a in by.index},
    "who_pays_replug": "the fleet operator (customer) - it is the value we sell, not a cost we carry"}

# ------------------------------------------------------------------ events
fl, co, ge, pr = rd("faults.csv"), rd("connectivity_outages.csv"), rd("grid_events.csv"), rd("prices.csv")
pr["ts"] = pd.to_datetime(pr["ts"])
sp600 = pr[(pr.ts.dt.strftime("%Y-%m-%d") == DAY) & (pr.spot_eur_mwh > 600)]
g1 = ge[ge.event_id == "G1"].iloc[0]
L["events"] = [
    {"id": "F015", "site": "S1", "asset": "C1-3", "kind": "thermal", "start": "2026-11-13T01:50", "end": "2026-11-13T02:25",
     "minutes": 35, "text": "Cabinet derated to 50% (overtemperature)", "cleared_by": "superseded",
     "modelled_in_engine": False, "optimistic_bias_kwh": 105.0},
    {"id": "F016", "site": "S1", "asset": "C1-3", "kind": "thermal", "start": "2026-11-13T02:25", "end": "2026-11-13T06:31",
     "minutes": 246, "text": "Cabinet stopped (overtemperature)", "cleared_by": "technician", "modelled_in_engine": True},
    {"id": str(g1.event_id), "site": str(g1.site_id), "kind": "grid_limit", "start": str(g1.start_ts), "end": str(g1.end_ts),
     "limit_kw": float(g1.limit_kw), "notified_at": str(g1.notified_ts), "text": str(g1.note)},
    {"id": "PRICE", "site": "network", "kind": "price", "text": "official spot > 600 EUR/MWh occurs only in these intervals",
     "intervals": [t.strftime("%H:%M") for t in sp600.ts], "values": [r(v) for v in sp600.spot_eur_mwh],
     "peak_eur_mwh": r(pr.spot_eur_mwh.max(), 2), "peak_at": pr.loc[pr.spot_eur_mwh.idxmax(), "ts"].strftime("%Y-%m-%d %H:%M")},
    {"id": "WAN", "site": "S3", "kind": "connectivity", "text": "cellular outage on scenario day",
     "windows": [{"start": str(x.start_ts), "end": str(x.end_ts)} for x in
                 co[(co.site_id == "S3") & co.start_ts.astype(str).str.startswith(DAY)].itertuples()]},
    {"id": "F017", "site": "S4", "asset": "D4-2", "kind": "connector", "start": "2026-11-13T21:30", "end": None,
     "text": "Cable damage detected, dispenser locked out for safety", "cleared_by": "open",
     "note": "F017 is an S4 cable fault, not the S3 outage"},
]
L["events_audit"] = {"faults_total": int(len(fl)),
                     "cleared_by_counts": {str(k): int(v) for k, v in fl.cleared_by.value_counts(dropna=False).items()},
                     "grid_events": [{k: str(v) for k, v in x.items()} for x in ge.to_dict("records")]}

# ------------------------------------------------------------------ grid
sp = rd("network_site_power.csv"); sp["ts"] = pd.to_datetime(sp["ts"])
kp = rd("network_kpis.csv")
over = (sp.demand_kw - sp.grid_limit_kw).clip(lower=0) * 0.25
gagg = sp.assign(ov=over).groupby("site_id").agg(over_kwh=("ov", "sum"),
                                                 over_h=("ov", lambda s: (s > 0).sum() * 0.25),
                                                 peak_del=("delivered_kw", "max"), lim=("grid_limit_kw", "max"))
net = gagg.drop(index=[i for i in ("S1", "S2", "S3", "S4", "S5") if i in gagg.index])
mla = op[op.action == "manual_load_adjustment"].groupby("site_id").agg(n=("count", "sum"), m=("staff_minutes", "sum"))
j = gagg[["over_h"]].join(mla, how="outer").fillna(0)
capped = sp.demand_kw > sp.grid_limit_kw
gc = rd("grid_capacity.csv").set_index("site_id")
eqm1 = (abs(sp.delivered_kw - sp[["demand_kw", "grid_limit_kw"]].min(axis=1)) < 0.51)
L["grid"] = {
    "basis_audit": {"rows": int(len(sp)), "grid_kw_over_limit": int((sp.grid_kw > sp.grid_limit_kw + 1e-9).sum()),
                    "delivered_over_limit": int((sp.delivered_kw > sp.grid_limit_kw + 0.5).sum()),
                    "delivered_div_eta_over_limit": int((sp.delivered_kw / 0.955 > sp.grid_limit_kw + 1e-9).sum()),
                    "demand_over_limit_intervals": int(capped.sum()),
                    "delivered_eq_min_demand_or_limit": int(eqm1.sum()), "delivered_eq_min_pct": r(100 * eqm1.mean(), 2),
                    "sites_with_time_variable_limit": int((sp.groupby("site_id")["grid_limit_kw"].nunique() > 1).sum())},
    "shed": {"mwh_14d": r(over.sum() / 1000, 1), "mwh_annualised": r(over.sum() / 1000 / 14 * 365, 0),
             "hours_100sites": r((over > 0).sum() * 0.25, 1), "sites_100": int((gagg.over_kwh > 0).sum()),
             "share_of_delivered_pct": r(100 * over.sum() / (sp.delivered_kw.sum() * 0.25), 2),
             "delivered_mwh_14d": r(sp.delivered_kw.sum() * 0.25 / 1000, 1),
             "demand_mwh_14d": r(sp.demand_kw.sum() * 0.25 / 1000, 1)},
    "network_kpis_95": {"sites": int(len(kp)), "hours_demand_above_grid_limit": r(kp.hours_demand_above_grid_limit.sum(), 1),
                        "sites_breaching": int((kp.hours_demand_above_grid_limit > 0).sum()),
                        "peak_equals_limit_sites": int((kp.peak_grid_kw == kp.grid_limit_kw).sum()),
                        "energy_mwh": r(kp.energy_mwh.sum(), 1), "departures_below_required": int(kp.departures_below_required.sum()),
                        "arrivals": int(kp.arrivals.sum()), "abandoned": int(kp.abandoned.sum()),
                        "abandon_pct": r(100 * kp.abandoned.sum() / kp.arrivals.sum(), 2),
                        "availability_mean_pct": r(kp.dispenser_availability_pct.mean(), 2),
                        "recomputed_hours_95": r(net.over_h.sum(), 1), "recomputed_sites_95": int((net.over_kwh > 0).sum())},
    "manual_cap_linkage": {"events": int(mla.n.sum()), "minutes_biweekly": int(mla.m.sum()), "fte": r(mla.m.sum() / WK, 2),
                           "eur_year": r(mla.m.sum() / 60 * RATE * 26, 0),
                           "share_of_minutes_on_breach_sites_pct": r(100 * j.loc[j.over_h > 0, "m"].sum() / j["m"].sum(), 1),
                           "breach_sites_with_zero_manual_ops": int(((j.over_h > 0) & (j.m == 0)).sum()),
                           "spearman": r(j.over_h.corr(j.m, method="spearman"), 3), "pearson": r(j.over_h.corr(j.m), 3),
                           "top_breach_sites": j[j.over_h > 0].nlargest(8, "over_h").round(2).to_dict("index")},
    "capped_vs_uncapped": {"abandon_pct_capped": r(100 * sp[capped].abandoned.sum() / max(sp[capped].arrivals.sum(), 1), 2),
                           "abandon_pct_uncapped": r(100 * sp[~capped].abandoned.sum() / max(sp[~capped].arrivals.sum(), 1), 2),
                           "queue_len_capped": r(sp[capped].queue_len.mean(), 2),
                           "queue_len_uncapped": r(sp[~capped].queue_len.mean(), 2)},
    "flex": {"breach_sites_95": int((net.over_kwh > 0).sum()),
             "sites_with_contractual_flex_kw": int((gc.flexible_extra_kw > 0).sum()),
             "breach_sites_with_flex_gt0": int((gc.reindex(j[j.over_h > 0].index).flexible_extra_kw.fillna(0) > 0).sum()),
             "total_flexible_extra_kw": int(gc.flexible_extra_kw.sum()),
             "upgrade_lead_months": [int(gc.upgrade_lead_time_months.min()), int(gc.upgrade_lead_time_months.max())],
             "naive_upgrade_cost_eur": r(((gc.current_limit_kw * 0.1) * gc.upgrade_cost_eur_per_kw).sum(), 0),
             "note": "flex headroom is contractual and free; a physical upgrade is priced and takes months"}
}

# ------------------------------------------------------------------ utilization
H = 14 * 24.0
nall = rd("network_sites.csv")
avail_h = float((nall.dispensers * nall.dispenser_kw).sum()) * H / 1000
avail_g = float(sp.groupby("site_id").grid_limit_kw.max().sum()) * H / 1000
deliv = float(sp.delivered_kw.sum() * 0.25 / 1000)
b1, o1 = L["sites"]["S1"]["baseline"], L["sites"]["S1"]["optimized"]
GUN_W, CAB_W = 16470.0, 10986.0
target = b1["total_kwh"] + b1["deficit_kwh"]
L["utilization"] = {
    "network": {"hardware_window_mwh_14d": r(avail_h, 1), "grid_window_mwh_14d": r(avail_g, 1),
                "delivered_mwh_14d": r(deliv, 1), "hardware_util_pct": r(100 * deliv / avail_h, 2),
                "idle_hardware_pct": r(100 - 100 * deliv / avail_h, 2), "grid_window_util_pct": r(100 * deliv / avail_g, 2),
                "sites": int(len(nall))},
    "per_site_util_pct": {s: r(100 * float(sp[sp.site_id == s].delivered_kw.sum() * 0.25) /
                               (int(ns.loc[s, "dispensers"]) * float(ns.loc[s, "dispenser_kw"]) * H), 2)
                          for s in ("S1", "S2", "S3", "S4", "S5")},
    "s1_night_windows": {"gun_window_kwh": GUN_W, "cabinet_window_kwh": CAB_W, "fleet_target_kwh": r(target, 1),
                         "fcfs": {"delivered_kwh": b1["total_kwh"], "gun_util_pct": r(100 * b1["total_kwh"] / GUN_W, 2),
                                  "cab_util_pct": r(100 * b1["total_kwh"] / CAB_W, 2),
                                  "fulfilment_pct": r(100 * b1["total_kwh"] / target, 2)},
                         "urgency": {"delivered_kwh": o1["total_kwh"], "gun_util_pct": r(100 * o1["total_kwh"] / GUN_W, 2),
                                     "cab_util_pct": r(100 * o1["total_kwh"] / CAB_W, 2),
                                     "fulfilment_pct": r(100 * o1["total_kwh"] / target, 2)},
                         "extra_kwh": r(o1["total_kwh"] - b1["total_kwh"], 1),
                         "delta_gun_pp": r(100 * (o1["total_kwh"] - b1["total_kwh"]) / GUN_W, 2),
                         "delta_cab_pp": r(100 * (o1["total_kwh"] - b1["total_kwh"]) / CAB_W, 2)},
    "windows_source": "S1 night envelope per docs/energy_impact.md (incl. the F016 window)"}

# ------------------------------------------------------------------ cost
bk = rd("baseline_kpis.csv")
a14 = bk[bk.period == "all_14_days"].set_index("site_id")
sd = bk[bk.period == "scenario_day"].set_index("site_id")
s5t = rd("sites.csv").set_index("site_id")
tar = rd("tariffs.csv").set_index("tariff_id")


def price_map(tid):
    out = {}
    for t, s in pr[["ts", "spot_eur_mwh"]].itertuples(index=False):
        row = tar.loc[tid]
        h = t.hour + t.minute / 60
        base = float(row.day_eur_mwh) if float(str(row.day_from)[:2]) <= h < float(str(row.day_to)[:2]) else float(row.night_eur_mwh)
        out[t] = float(s) + base
    return out


repro, unit = {}, {}
for s in ("S1", "S2", "S3", "S4", "S5"):
    c = price_map(s5t.loc[s, "tariff_id"])
    sub = sp[sp.site_id == s]
    cost = sum(c.get(t, 0.0) * float(k) * 0.25 / 1000 for t, k in zip(sub.ts, sub.delivered_kw))
    repro[s] = {"recomputed_eur_14d": r(cost, 1), "official_eur_14d": float(a14.loc[s, "energy_cost_eur"]),
                "diff_eur": r(cost - a14.loc[s, "energy_cost_eur"], 2)}
    d = sub[sub.ts.dt.strftime("%Y-%m-%d") == DAY]
    cost_d = sum(c.get(t, 0.0) * float(k) * 0.25 / 1000 for t, k in zip(d.ts, d.delivered_kw))
    kwh_d = float(d.delivered_kw.sum() * 0.25)
    unit[s] = {"official_scenario_day_eur": float(sd.loc[s, "energy_cost_eur"]),
               "official_scenario_day_mwh": float(sd.loc[s, "energy_mwh"]),
               "official_cost_per_mwh": r(float(sd.loc[s, "energy_cost_eur"]) / float(sd.loc[s, "energy_mwh"]), 1),
               "curve_recomputed_day_eur": r(cost_d, 1), "curve_recomputed_day_kwh": r(kwh_d, 1),
               "recomputed_cost_per_mwh": r(1000 * cost_d / kwh_d, 2) if kwh_d else None,
               "official_peak_kw": float(sd.loc[s, "peak_kw"]), "official_availability_pct": float(sd.loc[s, "charger_availability_pct"]),
               "official_departures": int(sd.loc[s, "departures"]),
               "official_departures_below_required": int(sd.loc[s, "departures_below_required_soc"])}
fee = {}
for s in ("S1", "S2", "S3", "S4", "S5"):
    tid = s5t.loc[s, "tariff_id"]
    pk, f = float(sd.loc[s, "peak_kw"]), float(tar.loc[tid, "peak_power_fee_eur_kw_month"])
    fee[s] = {"peak_kw_official_recorded": pk, "eur_per_kw_month": f, "monthly_eur": r(pk * f, 0),
              "save_5pct_year_eur": r(0.05 * pk * f * 12, 0)}
L["cost"] = {"official_14d_reproduction": repro, "scenario_day_per_site": unit,
             "peak_fee": {"per_site": fee, "total_monthly_eur": r(sum(v["monthly_eur"] for v in fee.values()), 0),
                          "total_save_5pct_year_eur": r(sum(v["save_5pct_year_eur"] for v in fee.values()), 0),
                          "basis": "official recorded peaks x official tariffs.csv monthly peak rate (billing basis)"},
             "spot_stats": {"min": r(pr.spot_eur_mwh.min(), 2), "p10": r(pr.spot_eur_mwh.quantile(.10), 2),
                            "median": r(pr.spot_eur_mwh.median(), 2), "p95": r(pr.spot_eur_mwh.quantile(.95), 2),
                            "max": r(pr.spot_eur_mwh.max(), 2), "intervals_above_300": int((pr.spot_eur_mwh > 300).sum()),
                            "tariff_depot_day_night": [float(tar.loc["T_DEPOT", "day_eur_mwh"]), float(tar.loc["T_DEPOT", "night_eur_mwh"])],
                            "synthetic_per_brief": True}}

# ------------------------------------------------------------------ commercial
ct = rd("contracts.csv"); eq = rd("equipment_costs.csv").set_index("item")
c1 = ct[ct.customer_id == "C1"].iloc[0]
brk = []
for s in ("S1", "S2", "S3", "S4", "S5"):
    m = ct[ct.sites.astype(str).str.contains(s)]
    if not len(m):
        continue
    c = m.iloc[0]
    av = float(sd.loc[s, "charger_availability_pct"])
    brk.append({"site": s, "customer": str(c.customer), "contract_type": str(c.contract_type),
                "recorded_availability_pct": av, "contracted_sla_pct": float(c.uptime_sla_pct),
                "breach": bool(av < float(c.uptime_sla_pct)),
                "below_required_departures": int(sd.loc[s, "departures_below_required_soc"]),
                "departure_penalty_eur": float(c.penalty_eur_per_late_departure),
                "penalty_due_scenario_day_eur": r(int(sd.loc[s, "departures_below_required_soc"]) * float(c.penalty_eur_per_late_departure), 0),
                "annual_fee_eur": float(c.annual_fee_eur), "daily_fee_eur": r(float(c.annual_fee_eur) / 365, 0)})
L["commercial"] = {"contracts": int(len(ct)), "annual_fee_total_eur": int(ct.annual_fee_eur.sum()),
                   "sla_mean_pct": r(ct.uptime_sla_pct.mean(), 2),
                   "contracts_with_service_scope": int(ct.contract_type.str.contains("service").sum()),
                   "contracts_with_departure_penalty": int((ct.penalty_eur_per_late_departure > 0).sum()),
                   "penalty_on_pure_hardware_contracts": int(((ct.penalty_eur_per_late_departure > 0) & (ct.contract_type == "hardware")).sum()),
                   "C1": {"customer": str(c1.customer), "sites": str(c1.sites), "uptime_sla_pct": float(c1.uptime_sla_pct),
                          "response_time_h": float(c1.response_time_h),
                          "penalty_eur_per_late_departure": float(c1.penalty_eur_per_late_departure),
                          "annual_fee_eur": float(c1.annual_fee_eur), "daily_fee_eur": r(float(c1.annual_fee_eur) / 365, 0)},
                   "breach_today": brk, "penalty_due_total_eur": r(sum(b["penalty_due_scenario_day_eur"] for b in brk), 0),
                   "equipment_costs": {str(k): float(v) for k, v in eq.eur.items()},
                   "capex_tiers": S1["strategy_b_hardware"], "strategy_a": S1["strategy_a_0capex"],
                   "sla_terms": {"mrdt_worked_example_min": 57.11, "liability_cap_monthly_pct": 150,
                                 "eta_system": 0.95, "handover_buffer_min": 15.0}}

# ------------------------------------------------------------------ growth
gf = rd("growth_forecast.csv")
fi = gf[gf.country == "FI"].pivot_table(index="segment", columns="year", values="index_2026_100")
L["growth"] = {"fi_index": {str(k): {int(y): float(v) for y, v in fi.loc[k].items()} for k in fi.index},
               "truck_2029_max_country_index": float(gf[(gf.year == 2029) & (gf.segment == "truck")].index_2026_100.max()),
               "util_2029_city_bus_pct": r(100 * deliv * float(fi.loc["city_bus", 2029]) / 100 / avail_h, 1),
               "util_2029_truck_pct": r(100 * deliv * float(fi.loc["truck", 2029]) / 100 / avail_h, 1)}

# ------------------------------------------------------------------ animation payload
W0, W1 = f"{PREV}T18:00", f"{DAY}T08:00"
tel = rd("sessions_baseline.csv")
tel["st"] = pd.to_datetime(tel.start_ts, errors="coerce"); tel["en"] = pd.to_datetime(tel.end_ts, errors="coerce")
sch = rd("fleet_schedule.csv")
veh = {v["vehicle_id"]: v for v in rd("vehicles.csv").to_dict("records")}


def series(site, a=W0, b=W1):
    d = sp[(sp.site_id == site) & (sp.ts >= pd.Timestamp(a + TZS)) & (sp.ts <= pd.Timestamp(b + TZS))]
    return {"t": [x.strftime("%d %H:%M") for x in d.ts], "demand_kw": [r(v, 1) for v in d.demand_kw],
            "delivered_kw": [r(v, 1) for v in d.delivered_kw], "limit_kw": [float(v) for v in d.grid_limit_kw],
            "queue_len": [int(v) for v in d.queue_len], "arrivals": [int(v) for v in d.arrivals],
            "abandoned": [int(v) for v in d.abandoned], "pv_kw": [r(v, 1) for v in d.pv_kw]}


def sessions(site, a=W0, b=W1):
    d = tel[(tel.site_id == site) & (tel.st >= pd.Timestamp(a + TZS)) & (tel.st <= pd.Timestamp(b + TZS))]
    return [{"id": str(x.session_id), "gun": str(x.charger_id), "veh": None if pd.isna(x.vehicle_id) else str(x.vehicle_id),
             "start": x.st.strftime("%d %H:%M"), "end": x.en.strftime("%d %H:%M") if pd.notna(x.en) else None,
             "kwh": r(x.energy_kwh, 1), "max_kw": r(x.max_kw, 1), "reason": str(x.end_reason)} for x in d.itertuples()]


s1d = sch[(sch.site_id == "S1") & sch.depart_ts.astype(str).str.startswith(DAY)]
b1v = L["sites"]["S1"]["baseline"]["delivered_per_vehicle"]
o1v = L["sites"]["S1"]["optimized"]["delivered_per_vehicle"]
s1_compare = {k: [b1v.get(k), o1v.get(k)] for k in sorted(set(b1v) | set(o1v))}
s1_delta = [{"id": k, "fcfs": w[0], "urgency": w[1], "delta": r((w[1] or 0) - (w[0] or 0), 1)}
            for k, w in s1_compare.items()]
L["anim"] = {
    "window": [W0, W1], "resolution_min": 15,
    "price_day": {"t": [x.strftime("%H:%M") for x in pr[pr.ts.dt.strftime("%Y-%m-%d") == DAY].ts],
                  "spot_eur_mwh": [r(v, 2) for v in pr[pr.ts.dt.strftime("%Y-%m-%d") == DAY].spot_eur_mwh]},
    "S1": {"series": series("S1"), "sessions": sessions("S1"),
           "vehicles": [{"id": x.vehicle_id, "arr": str(x.arrive_ts)[11:16], "dep": str(x.depart_ts)[11:16],
                         "soc_in": r(x.arrive_soc_pct, 1), "soc_req": r(x.required_soc_pct, 1),
                         "bat_kwh": float(veh.get(x.vehicle_id, {}).get("battery_kwh", 400.0)),
                         "max_kw": float(veh.get(x.vehicle_id, {}).get("max_charge_kw", 150.0)),
                         "need_kwh": r(max(0.0, float(veh.get(x.vehicle_id, {}).get("battery_kwh", 400.0)) *
                                           (float(x.required_soc_pct) - float(x.arrive_soc_pct)) / 100.0), 1)}
                        for x in s1d.itertuples()],
           "delivered_compare": s1_compare,
           "cabinets": {"C1-1": ["D1-1", "D1-2", "D1-3", "D1-4"], "C1-2": ["D1-5", "D1-6", "D1-7", "D1-8"],
                        "C1-3": ["D1-9", "D1-10", "D1-11", "D1-12"]},
           "grid_limit_kw": float(ns.loc["S1", "grid_limit_kw"]),
           "per_vehicle_delta": s1_delta},
    "S2": {"series": series("S2", f"{DAY}T12:00", f"{DAY}T23:45"),
           "sessions": sessions("S2", f"{DAY}T12:00", f"{DAY}T23:45"), "grid_limit_kw": float(ns.loc["S2", "grid_limit_kw"])},
    "S3": {"series": series("S3", f"{DAY}T08:00", f"{DAY}T16:00"), "grid_limit_kw": float(ns.loc["S3", "grid_limit_kw"])},
    "S4": {"series": series("S4", f"{DAY}T14:00", f"{DAY}T22:00"), "grid_limit_kw": float(ns.loc["S4", "grid_limit_kw"])},
    "topology": [{"site": x.site_id, "cabinet": x.cabinet_id, "gun": x.charger_id, "kw": float(x.max_kw),
                  "connector": x.connector_type} for x in rd("chargers.csv").itertuples()
                 if x.site_id in ("S1", "S2", "S3", "S4", "S5")],
}

# ------------------------------------------------------------------ flags
v = L["sites"]["S1"]["variants"]
L["flags"] = [
    "NOT USED (no script produces them): '-47.7% spot saving', '8.4-month payback', 'abandonment <0.5% / 76 drivers "
    "saved', '35% module lifetime extension', 'Nord Pool day-ahead' (prices.csv is synthetic per the brief).",
    "CORRECTED against official files: S3 outage 11:00-13:00 (outline said 10:00-12:00); G1 curtailment "
    f"{g1.start_ts[11:16]}-{g1.end_ts[11:16]} at {g1.limit_kw} kW (outline said until 20:00); spike intervals "
    f"{L['events'][3]['intervals']} (outline said 17:15-18:45); S3 naive fallback = 50 kW x 10 dispensers = "
    f"{L['sites']['S3']['fallback']['station_kw']} kW station (outline said 400 kW).",
    "REATTRIBUTED: F017 is an S4 cable fault (cleared_by=open), not the S3 cellular outage.",
    f"S5 rewritten to engine truth: misconfigured 600 kW -> {L['sites']['S5']['baseline'].get('missed_departures')} missed / "
    f"{L['sites']['S5']['baseline'].get('deficit_kwh')} kWh, 900 kW all-open -> "
    f"{L['sites']['S5']['optimized'].get('missed_departures')} missed / {L['sites']['S5']['optimized'].get('deficit_kwh')} kWh; "
    f"official recorded 5 missed / {L['sites']['S5']['official_recorded']['recorded_deficit_kwh']} kWh (config fix, not A/B).",
    f"S2 reference point: official recorded {L['sites']['S2']['official_recorded']['recorded_deficit_kwh']} kWh "
    f"(T01-T04); same-engine sim {L['sites']['S2']['official_recorded']['sim_deficit_kwh']} kWh.",
    f"Zero-miss honesty: plugs alone (24 pts, no tie) = {v['plugs_only_24_no_tie']['missed_departures']} missed (worse); "
    f"busbar tie on the existing 12 guns = {v['busbar_tie_12guns']['missed_departures']} missed at "
    f"{v['busbar_tie_12guns']['peak_kw']} kW; 24 pts + tie = {v['plugs_and_tie_24']['missed_departures']} missed "
    f"for 324,000 EUR; 3x450 kW uncapped = {v['cabinet_3x450_no_cap']['missed_departures']} missed at "
    f"{v['cabinet_3x450_no_cap']['peak_kw']} kW but the sweep is non-monotonic, so it is shown as a boundary case only.",
    "STATED ASSUMPTION on-slide: a vehicle with two departures on 2026-11-13 is modelled as one overnight energy "
    f"requirement (S1 {L['sites']['S1']['baseline']['unique_vehicles']} vehicles / "
    f"{L['sites']['S1']['baseline']['jobs']} departures; S2 {L['sites']['S2']['baseline']['unique_vehicles']}/"
    f"{L['sites']['S2']['baseline']['jobs']}).",
    "F015 (35 min at 50% derate) is not modelled -> ~105 kWh optimistic bias, disclosed.",
    "No post-hoc public-abandonment outcome is claimed for S3: the deck shows the 1,425 kW DC vs 500 kW fallback "
    f"contrast and that left_queue is {L['sites']['S3']['official_recorded'].get('scenario_day_2026_11_13_left_queue')} "
    f"of {int((L['sites']['S3']['official_recorded'].get('scenario_day_2026_11_13_left_full') or 0) + (L['sites']['S3']['official_recorded'].get('scenario_day_2026_11_13_left_queue') or 0))} abandoned that queue logic can address.",
]

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(L, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.1f} KiB)")

print("\n--- headline sanity (engine-sourced) ---")
for s in ("S1", "S2", "S5"):
    e = L["sites"][s]
    print(f"{s}: base missed {e['baseline'].get('missed_departures')} ({e['baseline'].get('deficit_kwh')} kWh, "
          f"{e['baseline'].get('moves')} moves, {e['baseline'].get('jobs')}/{e['baseline'].get('unique_vehicles')}v) -> "
          f"opt {e['optimized'].get('missed_departures')} ({e['optimized'].get('deficit_kwh')} kWh, "
          f"{e['optimized'].get('moves')} moves) closed {e.get('deficit_closed_pct')}%")
print("S1 variants:", {k: (w["missed_departures"], w["deficit_kwh"], w["peak_kw"]) for k, w in v.items()})
print("S1 sweep:", [(x["cabinet_kw"], x["missed_departures"], x["deficit_kwh"]) for x in L["sites"]["S1"]["capacity_sweep"]])
print("S1 gun sweep:", [(x["gun_kw"], x["missed_departures"]) for x in L["sites"]["S1"]["gun_sweep"]])
print("grid:", L["grid"]["shed"], L["grid"]["network_kpis_95"])
print("linkage:", {k: L["grid"]["manual_cap_linkage"][k] for k in ("events", "minutes_biweekly", "share_of_minutes_on_breach_sites_pct", "spearman", "breach_sites_with_zero_manual_ops")})
print("capped/uncapped:", L["grid"]["capped_vs_uncapped"], "basis:", L["grid"]["basis_audit"])
print("util:", L["utilization"]["network"], "\n   s1:", L["utilization"]["s1_night_windows"])
print("repro:", L["cost"]["official_14d_reproduction"], "peakfee:", L["cost"]["peak_fee"]["total_monthly_eur"])
print("S3:", L["sites"]["S3"]["fallback"], L["sites"]["S3"]["offline"], {k: L["sites"]["S3"]["official_recorded"][k] for k in list(L["sites"]["S3"]["official_recorded"])[:9]})
print("breach:", [(b["site"], b["recorded_availability_pct"], b["contracted_sla_pct"], b["penalty_due_scenario_day_eur"]) for b in L["commercial"]["breach_today"]], L["commercial"]["penalty_due_total_eur"])
print("labor:", {k: L["labor"][k] for k in ("fte_recorded", "addressable_fte", "addressable_share_minutes_pct", "events")}, L["labor"]["retained"])
print("growth:", L["growth"]["fi_index"], L["growth"]["util_2029_truck_pct"], L["growth"]["util_2029_city_bus_pct"])
print("anim:", {k: (len(L["anim"][k]["series"]["t"]) if isinstance(L["anim"].get(k), dict) and "series" in L["anim"][k] else "-") for k in ("S1", "S2", "S3", "S4")},
      "S1 sessions", len(L["anim"]["S1"]["sessions"]), "vehicles", len(L["anim"]["S1"]["vehicles"]), "topology", len(L["anim"]["topology"]))
