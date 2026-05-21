---
name: researching-utility-energy-costs
description: >
  Use when asked to research pump station energy costs, electricity tariffs, or
  water utility operational benchmarks for financial modelling (performance fees,
  savings calculations, ROI projections). Covers Taiwan, Malaysia, Indonesia and
  the methodology to compute per-station energy spend from first principles when
  published data is unavailable.
tags: [energy, water, utilities, financial-model, [Product], performance-fee]
---

# Researching Utility Energy Costs

Use this skill when building or validating financial model assumptions for water
utility pump station energy costs and NRW savings — especially for [Product]
performance fee calculations.

---

## Confirmed Data Points (as of May 2026)

### Electricity Tariffs

| Country | Rate | Category | Source |
|---|---|---|---|
| Taiwan | **USD 0.13/kWh** | Industrial/HV (Taipower, post Oct 2024 +12.5%) | GlobalPetrolPrices, Taipower announcement |
| Malaysia | **USD 0.095/kWh** | TNB Medium Voltage E2, water utility category (RP4 Jul 2025) | TNB ENGLISH_TARIFF_2024.pdf |
| Indonesia | **USD 0.065/kWh** | PLN subsidised PDAM/government tariff | PDAM Surabaya 2022 energy audit cross-check |

**Notes:**
- Malaysia water utilities get reduced ICPT surcharge: 2.7 sen/kWh (vs 16 sen general industry)
- Indonesia PDAM effective rate is subsidised (~IDR 731/kWh implied from Surabaya audit) — use USD 0.065 not the commercial IDR 1,444/kWh rate
- Taiwan industrial rate increased 12.5% in Oct 2024 — check for further increases annually

### NRW (Non-Revenue Water) Ratios

| Country/State | NRW Rate | Source |
|---|---|---|
| Taiwan (TWC) | 14–17% | TWC annual sustainability reports |
| Malaysia national average | **34.6%** (2023) | SPAN Annual Report 2024 |
| Malaysia — Negeri Sembilan (SAINS) | ~35–38% | SPAN 2024 |
| Malaysia — Johor (Ranhill SAJ) | ~30–34% | SPAN 2024 |
| Malaysia — Selangor (Air Selangor) | ~28–32% | SPAN 2024 |
| Indonesia — national PDAM average | **30–35%** | BPPSPAM / World Bank |
| Indonesia — Central Java | 28–40% | BPPSPAM 2022 |

**Use 33% for MY, 32% for ID in models unless client data is available.**

### Water Tariffs (for NRW saving monetisation)

| Country | Tariff | Model Value |
|---|---|---|
| Malaysia | MYR 0.75–1.32/m³ = USD 0.165–0.29/m³ | **USD 0.22/m³** |
| Indonesia | IDR 7,500–10,000/m³ = USD 0.046–0.062/m³ | **USD 0.055/m³** |

**Indonesia's low water tariff severely limits NRW saving in dollar terms. Electricity saving is the dominant driver in Indonesia.**

---

## First-Principles Pump Energy Calculation

When per-station energy data is not published, calculate from physics:

```python
# Constants
HP_TO_KW = 0.746           # shaft power conversion
OVERALL_EFFICIENCY = 0.68  # pump (72%) × motor (94%) — real-world wire-to-water

def monthly_kwh(hp, hours_per_day=18):
    kw_input = hp * HP_TO_KW / OVERALL_EFFICIENCY
    return kw_input * hours_per_day * 30

def monthly_water_m3(hp, hours_per_day=18, flow_m3_per_hp_per_hour=3.0):
    """Flow rate: HP × 3.0 m³/h (conservative, 30-50m head)"""
    return hp * flow_m3_per_hp_per_hour * hours_per_day * 30

def monthly_energy_cost(hp, tariff_usd_kwh, hours_per_day=18):
    return monthly_kwh(hp, hours_per_day) * tariff_usd_kwh
```

**Typical operating hours by tier:**
- Tier 4 (<500 HP): 18 hours/day
- Tier 3 (500–1,500 HP): 18 hours/day
- Tier 2 (1,500–3,000 HP): 20 hours/day
- Tier 1 (>3,000 HP): 20 hours/day

---

## Specific Energy Consumption (SEC) Benchmark

SEC = kWh of electricity per m³ of water delivered:

| Context | SEC (kWh/m³) | Notes |
|---|---|---|
| Taiwan flat terrain | 0.21 | Literature (Semantic Scholar) |
| Indonesia PDAM Gowongan | 0.221 | Efficient, low-head station |
| Seoul Metropolitan City (2020) | 0.36 | Modern infrastructure |
| Indonesia PDAM Surabaya (2022 audit) | 0.56 | Real operational audit |
| Indonesia PDAM average | 0.30–0.80 | Aging infrastructure range |
| Malaysia estimated | 0.35–0.55 | No published figure; estimated from regional benchmarks |
| Global developing country benchmark | 0.30–1.00 | World Bank / IEA |

**Model default: SEC = 0.35 kWh/m³** — conservative mid-range for unoptimised Asian utility stations.

Energy via SEC is often more accurate than first-principles for financial models because it reflects real-world inefficiencies.

---

## Performance Fee Calculation ([Product] Model)

```python
def electricity_saving_share(monthly_kwh, tariff, saving_pct, share=0.50):
    """50/50 sharing of measured electricity savings"""
    return monthly_kwh * tariff * saving_pct * share

def nrw_saving_share(monthly_m3, nrw_ratio, reduction_pct, water_value_usd, share=0.50):
    """50/50 sharing of NRW reduction value"""
    return monthly_m3 * nrw_ratio * reduction_pct * water_value_usd * share

def total_perf_fee(hp, country, saving_pct_elec, nrw_reduction_pct):
    tariffs = {"TW": 0.130, "MY": 0.095, "ID": 0.065}
    nrw     = {"TW": 0.15,  "MY": 0.33,  "ID": 0.32}
    water_v = {"TW": 0.35,  "MY": 0.22,  "ID": 0.055}
    SEC = 0.35
    hours = 20 if hp > 1500 else 18
    m3_mo  = hp * 3.0 * hours * 30
    kwh_mo = SEC * m3_mo
    elec   = electricity_saving_share(kwh_mo, tariffs[country], saving_pct_elec)
    nrw_s  = nrw_saving_share(m3_mo, nrw[country], nrw_reduction_pct, water_v[country])
    return elec + nrw_s
```

**Validated outputs (70 non-TW stations, mixed tier):**
- Conservative (10% elec + 5% NRW): **USD 3,487/mo per station average**
- Aggressive (15% elec + 8% NRW): **USD 5,386/mo per station average**

---

## Research Search Strategy

When you need to find or update these numbers:

### Electricity tariffs
- Taiwan: `site:globalpetrolprices.com Taiwan electricity prices` or `Taipower industrial tariff [YEAR]`
- Malaysia: `TNB ENGLISH_TARIFF_[YEAR].pdf` — direct PDF from tnb.com.my
- Indonesia: `PLN electricity tariff industrial [YEAR] IDR per kWh site:globalpetrolprices.com`

### NRW data
- Malaysia: `SPAN NRW [YEAR] national average state` — SPAN publishes annual water & sewerage fact books
- Indonesia: `BPPSPAM PDAM NRW [YEAR] national` — BPPSPAM is the Indonesian water regulator
- General: World Bank / ADB WASH sector reports

### Per-station energy audits
- Search: `PDAM [city] energy audit SEC kWh m3 IOP Conference` — Indonesia energy audits often published in IOP Conference Series
- Search: `water pumping station specific energy consumption kWh m3 Asia developing`
- Cross-check: if you find IDR/m³ cost, divide by SEC to back-calculate effective tariff

### Pump energy (no published data)
- Use first-principles HP → kW → kWh/month calculation above
- Cross-validate with SEC method — they should be within 20% of each other
- If they diverge, real station SEC is likely higher (aging infrastructure, poor pump selection)

---

## Pitfalls

1. **Indonesia PDAM tariff is subsidised** — do NOT use the commercial IDR 1,444/kWh rate. PDAM effective rate is ~IDR 700–900/kWh. Validated via PDAM Surabaya energy audit.
2. **Malaysia TNB water utility category** — water operators get a lower ICPT surcharge (2.7 sen vs 16 sen). Factor this in or you'll overstate energy cost.
3. **NRW monetisation is not guaranteed** — a PDAM must be able to SELL recovered water (demand-constrained) for NRW saving to have dollar value. Supply-constrained PDAMs can't monetise NRW reduction. Confirm during sales process.
4. **Taiwan energy saving ≠ performance fee** — Taiwan uses subscription-only. But the Taiwan energy saving data (20% demonstrated) is the proof point that validates the MY/ID performance fee projections.
5. **Indonesia water tariff is very low** — USD 0.055/m³ means NRW saving in Indonesia is worth ~4× less than in Malaysia per m³. Electricity dominates the performance fee in Indonesia.
6. **First-principles underestimates real energy use** — assuming 68% overall efficiency gives ~0.10 kWh/m³ which is below the PDAM actual range (0.30–0.60). Real stations are less efficient. Use SEC = 0.35 as floor.
7. **NRW saving should NOT be in the base-case performance fee** — it's an indirect mechanism (pressure control reduces burst frequency, doesn't fix pipes). Attribution is disputed by regulators and auditors. The existing Taiwan proof covers energy saving only, not NRW. **Exclude NRW from contractual PF base case; treat as upside once a measurement protocol is established.** Electricity saving alone is the contractually defensible component.
8. **Flow rate assumption is head-dependent** — HP × 3.0 m³/h assumes 30–50m head. Booster pump stations (60–100m head) flow significantly less per HP. At 80m head, 900 HP ≈ 641 m³/h (not 2,700 m³/h). This matters for NRW calculation but NOT for electricity calculation (same kWh regardless of flow). Confirm actual head of deployed stations before using flow-based NRW numbers.
