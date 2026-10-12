# Data Center Electricity Use

Published estimates of how much electricity data centers use, each traced to its publisher: national, regional and world totals and projections, and the consumption the largest operators report.

- **33 rows** from 7 publishers:
  - Lawrence Berkeley National Laboratory: US 2024 (192 TWh, 4.7% of US electricity), the 2028 Reference Case and all seven 2030 scenarios (521 to 843 TWh)
  - International Energy Agency: world 2024 (415 TWh) and the 2030 Base Case (945 TWh); 2025 (485 TWh, AI-focused 155 TWh) as reported by Our World in Data
  - European Commission: EU 2024 (68 TWh) and 2030 (114 TWh)
  - Central Statistics Office Ireland: 2024 and 2025 (7,663 GWh, 23% of metered electricity)
  - Google (data centers 2021–2025), Microsoft (company-wide FY20–FY25) and Meta (data centers 2020–2024), in MWh as reported
- **Each value is copied exactly** as the publisher printed it. The only derived column is `electricity_twh` on operator rows (MWh ÷ 1,000,000).
- **Retrieved 12 October 2026.** Every row records its source URL and the table or passage it came from.

Interactive version with a data center electricity calculator: https://greencalculus.com/data/data-center-energy-consumption/

## Columns

| Column | Meaning |
|---|---|
| `id` | Row id, stable within a version |
| `publisher` | Who published the figure |
| `scope` | `region` (country, region or world estimate) or `operator` (company-reported consumption) |
| `geography` | The area or operator the figure covers |
| `period` | Calendar year, or fiscal year for Microsoft (FYnn = July to June) |
| `estimate_type` | `historical`, `projection` or `reported` |
| `scenario` | Scenario name for projections |
| `electricity_twh` | TWh as published (region rows); derived from MWh on operator rows |
| `electricity_mwh` | MWh as reported (operator rows) |
| `share_of_electricity_pct` | Share of total electricity, where the publisher gives it |
| `source_title`, `source_url`, `source_date`, `retrieved` | Where and when the figure was read |
| `notes` | Quotes, definitions and caveats |

## Read before comparing

- **Boundaries differ.** LBNL and the IEA exclude cryptocurrency mining. Microsoft reports company-wide electricity, mostly but not only data centers. Meta's total includes leased facilities.
- **The 2025 IEA figures are secondary.** The IEA's 2026 report could not be retrieved, so its 2025 numbers are taken from Our World in Data, which cites it. The IEA's own press release confirms 17% growth in 2025.
- **Projections are scenarios, not forecasts of one number.** LBNL's 2030 range runs from 521 to 843 TWh. Its Reference Case (649 TWh) is above the IEA's 2025 projection for the US.
- **Electricity is not emissions.** Operators buy renewable electricity contracts; the physical grid mix sets location-based emissions. The calculator above computes both energy and location-based CO₂e.

## Licence and citation

The compilation is released under **CC BY 4.0**. The figures are facts published by the organisations named in each row; cite them as well as this dataset. The LBNL report is itself CC BY 4.0.

Corrections: open an issue on this repository with the row id and the source.
