#!/usr/bin/env python3
"""Build data-center-electricity.csv / .json: published data center electricity use, each traced to its publisher.

Two kinds of row, distinguished by `scope`:
  - region: national, regional and world estimates and projections (LBNL, IEA, European Commission, CSO Ireland),
    in TWh as published, with the share of total electricity where the publisher gives it.
  - operator: electricity consumption as an operator reports it, in MWh as published (Google, Microsoft, Meta).
Values are copied exactly as published; the only derived column is electricity_twh on operator rows (MWh / 1,000,000).

    python3 build.py
"""
import csv, json, pathlib

HERE = pathlib.Path(__file__).parent
VERSION = "2026.10.12"
RETRIEVED = "2026-10-12"
FIELDS = ["id", "publisher", "scope", "geography", "period", "estimate_type", "scenario", "electricity_twh", "electricity_mwh",
          "share_of_electricity_pct", "source_title", "source_url", "source_date", "retrieved", "notes"]

LBNL_T = "Smith, Hubbard, Newkirk et al., United States Data Center Energy Usage Report: 2025 Update, Lawrence Berkeley National Laboratory (doi:10.71468/P1RP4F), CC BY 4.0"
LBNL_U = "https://escholarship.org/uc/item/33m6w3x0"
GOOG_T = "Google 2026 Environmental Report, table 'Electricity consumption' (row 'Data centers')"
GOOG_U = "https://sustainability.google/files/google-2026-environmental-report.pdf"
MSFT_T = "Microsoft 2026 Environmental Data Fact Sheet, energy table ('Electricity consumed within the organization (MWh)')"
MSFT_U = "https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/2026-Microsoft-Environmental-Data-Fact-Sheet-PDF.pdf"
META_T = "Meta 2025 Environmental Data Index, section 2.1 'Electricity Consumption by Facility (in MWh)', row 'Data centers total'"
META_U = "https://sustainability.atmeta.com/asset/2025-environmental-data-index"


def rows():
    out = []

    def add(**kw):
        out.append(kw)

    # LBNL 2025 Update (published 2026-06-18): 2024 historical, 2028 and 2030 projections (Table 2).
    add(publisher="Lawrence Berkeley National Laboratory", scope="region", geography="United States", period="2024", estimate_type="historical",
        electricity_twh="192", share_of_electricity_pct="4.7", source_title=LBNL_T + ", section 2", source_url=LBNL_U, source_date="2026-06-18",
        notes="'The updated estimate of data center electricity use in 2024 is 192 terawatt-hours (TWh), accounting for 4.7% of total U.S. electricity consumption.' Excludes cryptocurrency mining.")
    add(publisher="Lawrence Berkeley National Laboratory", scope="region", geography="United States", period="2028", estimate_type="projection", scenario="Reference Case",
        electricity_twh="464", source_title=LBNL_T + ", section 2", source_url=LBNL_U, source_date="2026-06-18", notes="Reference Case forecast for 2028.")
    for sc, twh, pct in [("Reference Case", "649", "11.8"), ("Consolidated Deployment", "578", "10.5"), ("High ASIC", "664", "12.1"),
                         ("Low Accelerator Lifetime", "590", "10.7"), ("High Inference Energy", "782", "14.2"),
                         ("Compounded Uncertainty - Low", "521", "9.5"), ("Compounded Uncertainty - High", "843", "15.3")]:
        add(publisher="Lawrence Berkeley National Laboratory", scope="region", geography="United States", period="2030", estimate_type="projection", scenario=sc,
            electricity_twh=twh, share_of_electricity_pct=pct, source_title=LBNL_T + ", Table 2", source_url=LBNL_U, source_date="2026-06-18",
            notes="Share of forecast 2030 US electricity per NERC's 2025 Long-Term Reliability Assessment.")
    # IEA
    add(publisher="International Energy Agency", scope="region", geography="World", period="2024", estimate_type="historical",
        electricity_twh="415", share_of_electricity_pct="1.5", source_title="IEA (2025), Energy and AI, 'Energy demand from AI'",
        source_url="https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai", source_date="2025",
        notes="'around 415 terawatt hours (TWh), or about 1.5% of global electricity consumption in 2024'. Excludes crypto mining.")
    add(publisher="International Energy Agency", scope="region", geography="World", period="2030", estimate_type="projection", scenario="Base Case",
        electricity_twh="945", source_title="IEA (2025), Energy and AI, 'Energy demand from AI'",
        source_url="https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai", source_date="2025",
        notes="'around 945 TWh by 2030', 'just under 3%' of global electricity consumption.")
    add(publisher="International Energy Agency", scope="region", geography="World", period="2025", estimate_type="historical",
        electricity_twh="485", share_of_electricity_pct="1.5", source_title="IEA (2026), Key Questions on Energy and AI, as reported by Our World in Data (20 Jul 2026)",
        source_url="https://ourworldindata.org/how-much-energy-do-data-centers-and-artificial-intelligence-use", source_date="2026-04-16",
        notes="Secondary: the IEA report's own figures could not be retrieved; Our World in Data cites IEA (2026) for 'around 485 terawatt-hours' and 155 TWh for AI-focused data centers. IEA's press release (16 Apr 2026) confirms 'Electricity demand from data centres soared by 17% in 2025'.")
    add(publisher="International Energy Agency", scope="region", geography="World (AI-focused data centers)", period="2025", estimate_type="historical",
        electricity_twh="155", source_title="IEA (2026), Key Questions on Energy and AI, as reported by Our World in Data (20 Jul 2026)",
        source_url="https://ourworldindata.org/how-much-energy-do-data-centers-and-artificial-intelligence-use", source_date="2026-04-16",
        notes="Secondary, as the row above. About a third of the 485 TWh total.")
    # EU
    ec = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52026DC0500"
    add(publisher="European Commission", scope="region", geography="European Union", period="2024", estimate_type="historical", electricity_twh="68",
        source_title="European Commission, COM(2026) 500 final, section 1 (21 Sep 2026)", source_url=ec, source_date="2026-09-21",
        notes="'In 2024, data centres in the EU consumed 68 TWh of electricity.'")
    add(publisher="European Commission", scope="region", geography="European Union", period="2030", estimate_type="projection", electricity_twh="114",
        share_of_electricity_pct="3.2", source_title="European Commission, COM(2026) 500 final, section 1 (21 Sep 2026)", source_url=ec, source_date="2026-09-21",
        notes="'expected to rise to 114 TWh by 2030, reaching 3.2% of the electricity demand of the EU'.")
    # Ireland
    cso = "https://www.cso.ie/en/releasesandpublications/ep/p-dcmec/datacentresmeteredelectricityconsumption2025/keyfindings/"
    add(publisher="Central Statistics Office Ireland", scope="region", geography="Ireland", period="2025", estimate_type="historical", electricity_twh="7.663",
        share_of_electricity_pct="23", source_title="CSO, Data Centres Metered Electricity Consumption 2025, key findings", source_url=cso, source_date="2026-07-07",
        notes="Published as 7,663 GWh, 'rising from 6,973 Gigawatt hours (GWh) in 2024'; 23% of total metered electricity (urban households 18%).")
    add(publisher="Central Statistics Office Ireland", scope="region", geography="Ireland", period="2024", estimate_type="historical", electricity_twh="6.973",
        source_title="CSO, Data Centres Metered Electricity Consumption 2025, key findings", source_url=cso, source_date="2026-07-07",
        notes="Published as 6,973 GWh (revised; the 2024 release gave 6,969 GWh and 22%).")
    # Operators
    for yr, mwh in [("2025", 42415800), ("2024", 30637100), ("2023", 23980800), ("2022", 20616500), ("2021", 17429800)]:
        add(publisher="Google", scope="operator", geography="Google data centers", period=yr, estimate_type="reported", electricity_mwh=str(mwh),
            source_title=GOOG_T, source_url=GOOG_U, source_date="2026", notes="Data centers only; offices reported separately.")
    for fy, mwh in [("FY25", 37026353), ("FY24", 29829540), ("FY23", 23567502), ("FY22", 18153454), ("FY21", 13621517), ("FY20", 10770714)]:
        add(publisher="Microsoft", scope="operator", geography="Microsoft (company-wide)", period=fy, estimate_type="reported", electricity_mwh=str(mwh),
            source_title=MSFT_T, source_url=MSFT_U, source_date="2026",
            notes="Company-wide electricity, mostly data centers; fiscal years run July to June. Per-datacenter figures are in the fact sheet's Table 15.")
    for yr, mwh in [("2024", 18061781), ("2023", 14975435), ("2022", 11167416), ("2021", 9117122), ("2020", 6966000)]:
        add(publisher="Meta", scope="operator", geography="Meta data centers", period=yr, estimate_type="reported", electricity_mwh=str(mwh),
            source_title=META_T, source_url=META_U, source_date="2025", notes="Data centers total, including leased and other data center-related facilities.")
    for n, r in enumerate(out, 1):
        r["id"] = f"dce-{n:04d}"
        r["retrieved"] = RETRIEVED
        r.setdefault("scenario", "")
        if r.get("electricity_mwh") and not r.get("electricity_twh"):
            r["electricity_twh"] = f"{int(r['electricity_mwh']) / 1e6:.6f}".rstrip("0").rstrip(".")
    return out


def main():
    data = rows()
    with open(HERE / "data-center-electricity.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader()
        for r in data:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    (HERE / "data-center-electricity.json").write_text(json.dumps({"version": VERSION, "retrieved": RETRIEVED, "rows": data}, indent=1, ensure_ascii=False))
    print(f"{len(data)} rows")


if __name__ == "__main__":
    main()
