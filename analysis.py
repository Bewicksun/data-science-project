# CISC7204 Assignment 02 Pair 01
# Simple monthly extension of the Assignment 01 recovery comparison.
# Run this notebook from the proposal folder. Requires pandas and matplotlib.
# Sources, definitions and rounding checks: see the source record at the end of this notebook.

from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
Path("figures").mkdir(exist_ok=True)
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt

# 1 Read the two official monthly datasets.
visitors = pd.read_csv('data/visitor_monthly.csv')
gaming = pd.read_csv('data/gaming_monthly.csv')
monthly = pd.merge(visitors, gaming, on=['Year', 'Month'])
print('Monthly rows:', len(monthly))
print('Missing values:')
print(monthly.isna().sum())
print('Duplicate months:', monthly.duplicated(['Year', 'Month']).sum())



# 2 Match each month to the same month of 2019.
baseline = monthly[monthly['Year'] == 2019][['Month', 'Visitors', 'Gaming_Revenue']]
baseline = baseline.rename(columns={'Visitors': 'Visitors_2019',
                                    'Gaming_Revenue': 'Gaming_2019'})
df = monthly[monthly['Year'] >= 2023].copy()
df = pd.merge(df, baseline, on='Month')
df = df.sort_values(['Year', 'Month']).reset_index(drop=True)
df['Visitor_Index'] = df['Visitors'] / df['Visitors_2019'] * 100
df['Gaming_Index'] = df['Gaming_Revenue'] / df['Gaming_2019'] * 100
df['Gap'] = df['Visitor_Index'] - df['Gaming_Index']
df['Period'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)
print(df[['Period', 'Visitor_Index', 'Gaming_Index', 'Gap']].round(1))



# 3 Summarize the monthly gaps and compare sums with published annual totals.
summary = df.groupby('Year')['Gap'].agg(['mean', 'median', 'min', 'max'])
print('\nMonthly gap summary (percentage points):')
print(summary.round(1))
print('\nLargest monthly gap:')
print(df.loc[df['Gap'].idxmax(), ['Period', 'Visitor_Index', 'Gaming_Index', 'Gap']])
print('\nSmallest monthly gap:')
print(df.loc[df['Gap'].idxmin(), ['Period', 'Visitor_Index', 'Gaming_Index', 'Gap']])
print('\nMonths at or above the 2019 monthly level:')
print(df[df['Visitor_Index'] >= 100].groupby('Year').size().reindex([2023, 2024, 2025], fill_value=0))
print('Gaming months at or above 100:', (df['Gaming_Index'] >= 100).sum())
annual = pd.read_csv('data/annual_2019_2025.csv').set_index('Year')
sums = monthly.groupby('Year')[['Visitors', 'Gaming_Revenue']].sum()
check = sums - annual.loc[sums.index, ['Visitors', 'Gaming_Revenue']]
print('\nMonthly sums minus official annual totals:')
print(check)
# DICJ reports monthly values in whole MOP million. For 2019 their sum is
# 292456, versus the official annual 292455. Keep both published measures.



# 4 Annual line chart: extend the original Assignment 01 chart.
annual['Visitor_Index'] = annual['Visitors'] / annual.loc[2019, 'Visitors'] * 100
annual['Gaming_Index'] = annual['Gaming_Revenue'] / annual.loc[2019, 'Gaming_Revenue'] * 100
annual[['Visitor_Index', 'Gaming_Index']].plot(
    kind='line', figsize=(9, 4.1), marker='o', color=['#0072B2', '#D55E00'])
plt.axhline(100, color='gray', linestyle='--', linewidth=1)
plt.title('Annual Recovery of Macao Visitors and Gaming Revenue')
plt.xlabel('Year')
plt.ylabel('Recovery index (2019 = 100)')
plt.xticks(annual.index)
plt.ylim(0, 115)
plt.legend(['Visitor arrivals', 'Gaming revenue', '2019 level'])
plt.grid(axis='y', alpha=0.25)
plt.tight_layout()
plt.savefig('figures/01_annual_recovery.png', dpi=180)

plt.close()



# 5 Monthly line chart: same plotting method as Module 01 Lab 02.
df.set_index('Period')[['Visitor_Index', 'Gaming_Index']].plot(
    kind='line', figsize=(9, 4.1), marker='o', markersize=3,
    color=['#0072B2', '#D55E00'])
plt.axhline(100, color='gray', linestyle='--', linewidth=1)
plt.title('Monthly Recovery Relative to the Same Month in 2019')
plt.xlabel('Month')
plt.ylabel('Recovery index (same month in 2019 = 100)')
plt.xticks(range(0, 36, 3), df['Period'].iloc[::3], rotation=45)
plt.ylim(0, 130)
plt.legend(['Visitor arrivals', 'Gaming revenue', '2019 level'])
plt.grid(axis='y', alpha=0.25)
plt.tight_layout()
plt.savefig('figures/02_monthly_recovery.png', dpi=180)

plt.close()



# 6 Monthly bar chart: same method as Module 02 Lab 01.
df.set_index('Period')['Gap'].plot(kind='bar', figsize=(9, 4.1), color='#0072B2')
plt.axhline(0, color='gray', linewidth=1)
plt.title('Monthly Recovery Gap Between Visitors and Gaming Revenue')
plt.xlabel('Month')
plt.ylabel('Visitor index minus gaming index (pp)')
plt.xticks(range(0, 36, 3), df['Period'].iloc[::3], rotation=45)
plt.ylim(-10, 40)
plt.grid(axis='y', alpha=0.25)
plt.tight_layout()
plt.savefig('figures/03_monthly_gap.png', dpi=180)

plt.close()



# 7 Box plot: compare the 12 monthly gaps in each year (Module 02 Lab 02).
gaps_by_year = df.pivot(index='Month', columns='Year', values='Gap')
gaps_by_year.plot(kind='box', figsize=(8.5, 4.1))
plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.title('Distribution of Monthly Recovery Gaps by Year')
plt.xlabel('Year (12 months per year)')
plt.ylabel('Recovery gap (percentage points)')
plt.grid(axis='y', alpha=0.25)
plt.tight_layout()
plt.savefig('figures/04_gap_boxplot.png', dpi=180)

plt.close()



# 8 Save calculated values without rounding the underlying data.
monthly.to_csv('data/monthly_merged.csv', index=False)
df.to_csv('data/monthly_recovery_results.csv', index=False)
summary.to_csv('data/monthly_gap_summary.csv')
check.to_csv('data/annual_total_check.csv')
annual.to_csv('data/annual_recovery_results.csv')
print('\nSaved four figures and the calculated tables.')
