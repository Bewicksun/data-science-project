# Data and analysis codebook

| Source file | Coverage |
|---|---|
| owid-co2-data.csv | Full OWID CSV retrieved at the commit recorded in the manifest. The analysis selects the CHN, JPN, and KOR rows for 2000–2022 and reads country code, name, year, and CO₂ per person. |
| worldbank_gdp_per_capita.json | Complete WDI API response for indicator NY.GDP.PCAP.KD, CHN/JPN/KOR, 2000–2022. The first array element gives response metadata. The second contains all 69 requested records. |
| owid-co2-codebook.csv, owid_README.md, owid_commit.json | Provider field definitions and source documentation. The links and snapshot commit are recorded in the manifest. |
| worldbank_indicator_metadata.json | Definition and source organizations for the GDP indicator. The metadata URL is recorded in the manifest. |
| manifest.json | Retrieval dates, URLs, file sizes, and SHA-256 hashes for the listed downloads. |

The notebook joins the sources one-to-one by country code and year. There are 23 complete records per country. Annual observations are used directly, with no imputation or smoothing.

## Master and annual tables

| Field | Definition |
|---|---|
| iso_code, country, year | ISO3 code (CHN, JPN, KOR), standardized name, and calendar year |
| gdp_per_capita_constant_2015_usd | Real GDP per person in constant 2015 US dollars |
| co2_per_capita_tonnes | Territorial CO₂ in tonnes per person from fossil fuels and industrial processes, excluding land-use change |
| owid_country, wb_country | Original country names from the two providers |
| gdp_source_indicator, co2_source_variable | Original indicator identifier and source column name |
| gdp_index_2000_100, co2_index_2000_100 | 100 × current value ÷ the same country's value in 2000 for the same indicator |
| gdp_yoy_pct, co2_yoy_pct | 100 × (current value ÷ previous-year value − 1). Blank in 2000 because it is the first study year. |
| intensity_proxy_kg_per_usd | 1,000 × CO₂ per person ÷ real GDP per person. Unit is kg CO₂ per constant 2015 US dollar. A proxy because the sources may use different population estimates. |

## Period growth and endpoint tables

| Field | Definition |
|---|---|
| period | Year range or three-year averaging windows |
| gdp_growth_pct, co2_growth_pct | Cumulative change of each measure, calculated as 100 × (end ÷ start − 1) |
| intensity_change_pct | 100 × (end CO₂/GDP ratio ÷ start CO₂/GDP ratio − 1) |
| classification | Category determined from unrounded GDP and CO₂ changes using the rules below |
| category_changed_vs_baseline | True when the scenario changes a country's category relative to 2000–2022 |

The averaged scenario applies the same growth formulas to the arithmetic means of each indicator in 2000–2002 and 2020–2022. Let G be GDP growth and C be CO₂ growth.

| Condition | Category |
|---|---|
| G > 0 and C < 0 | Absolute per-capita decoupling |
| G > 0 and 0 ≤ C < G | Relative per-capita decoupling |
| G > 0 and C ≥ G | No decoupling during growth |
| G ≤ 0 | No positive income growth |
