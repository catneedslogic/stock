import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta

ticker = 'AMD'

# ======================
# STEP 1: Load data
# ======================

#6 months
df = pd.read_csv(f'data/{ticker}_5y_data.csv', parse_dates=['datetime'])
df = df[df['datetime'] >= (datetime.now() - relativedelta(months=6))].copy()
df.sort_values('datetime', inplace=True)

# 5 years
# df = pd.read_csv(f'data/{ticker}_5y_data.csv', parse_dates=['datetime'])
# df.sort_values('datetime', inplace=True)

# ======================
# STEP 2: Set up price bins
# ======================
bin_size = 1  # price bin width in dollars
min_price = df['low'].min()
max_price = df['high'].max()
price_bins = np.arange(np.floor(min_price), np.ceil(max_price) + bin_size, bin_size)

# Create mapping: each bin will accumulate volume for each day
heatmap = {price: [] for price in price_bins}

# ======================
# STEP 3: Assign volume to bins for each day
# ======================
for _, row in df.iterrows():
    low = row['low']
    high = row['high']
    volume = row['volume']

    # Identify which bins are within the day's range
    in_range_bins = price_bins[(price_bins >= low) & (price_bins <= high)]
    if len(in_range_bins) == 0:
        for price in price_bins:
            heatmap[price].append(0)
        continue

    vol_per_bin = volume / len(in_range_bins)

    for price in price_bins:
        if price in in_range_bins:
            heatmap[price].append(vol_per_bin)
        else:
            heatmap[price].append(0)

# ======================
# STEP 4: Create heatmap array
# ======================
heatmap_df = pd.DataFrame(heatmap).T  # Transpose so rows = price bins
heatmap_df.columns = df['datetime'].dt.date  # One column per date
heatmap_array = heatmap_df.values

# ======================
# STEP 5: Plot heatmap
# ======================
plt.figure(figsize=(18, 10))
plt.imshow(
    heatmap_array,
    aspect='auto',
    cmap='inferno',
    origin='lower',
    extent=[0, heatmap_array.shape[1], price_bins[0], price_bins[-1]]
)

plt.colorbar(label='Estimated Volume')
plt.title(f'{ticker} Liquidity Heat Map (Volume by Price Over Time)')
plt.xlabel('Date')
plt.ylabel('Price ($)')

# Set xticks to match some date labels
num_dates = heatmap_df.shape[1]
tick_step = max(1, num_dates // 10)
xtick_positions = np.arange(0, num_dates, tick_step)
xtick_labels = heatmap_df.columns[::tick_step]
plt.xticks(ticks=xtick_positions, labels=xtick_labels, rotation=45)

plt.tight_layout()
plt.show()
