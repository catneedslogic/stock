import pandas as pd
import mplfinance as mpf
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# ======================
# STEP 1: Load ALL data first
# ======================
def load_full_data(filename):
    df = pd.read_csv(filename, parse_dates=['datetime'], index_col='datetime')
    return df.sort_index(ascending=True)

# ======================
# STEP 2: Calculate MAs on FULL data
# ======================
def calculate_mas(df):
    # Calculate moving averages using ALL historical data
    df['MA50'] = df['close'].rolling(50).mean()  # 50-day MA
    df['MA200'] = df['close'].rolling(200).mean()  # 200-day MA
    return df

# ======================
# STEP 3: Filter timeframe AFTER MA calculation
# ======================
def filter_timeframe(df, months=None, years=None):
    if months:
        cutoff_date = datetime.now() - relativedelta(months=months)
    elif years:
        cutoff_date = datetime.now() - relativedelta(years=years)
    else:
        return df
    return df[df.index >= cutoff_date]

# ======================
# MAIN EXECUTION
# ======================
if __name__ == "__main__":

    # months = 6
    months = None
    ticker = 'CAVA'

    # 1. Load ALL historical data
    full_data = load_full_data(f'data/{ticker}_5y_data.csv')
    
    # 2. Calculate MAs using full history
    full_data_with_mas = calculate_mas(full_data)
    
    # # 3. Filter to desired timeframe (e.g., last 6 months)
    filtered_data = filter_timeframe(full_data_with_mas, months=months)
    
    # 4. Generate Fibonacci levels from FILTERED data
    swing_high = filtered_data['high'].max()
    swing_low = filtered_data['low'].min()
    price_range = swing_high - swing_low
    
    fib_levels = {
        '0% (High)': swing_high,
        '23.6%': swing_high - 0.236 * price_range,
        '28%' : swing_high - 0.28 * price_range,
        '38.2%': swing_high - 0.382 * price_range,
        '50%': swing_high - 0.5 * price_range,
        '61.8%': swing_high - 0.618 * price_range,
        '72%' : swing_high - 0.72 * price_range,
        '78.6%': swing_high - 0.786 * price_range,
        '100% (Low)': swing_low
    }
    
    # 5. Prepare plots
    fib_plots = []
    colors = ['#FF9900', '#FF3300', '#9900FF', '#00AA00', '#0099FF']
    
    for i, (level, price) in enumerate(fib_levels.items()):
        fib_plots.append(mpf.make_addplot(
            pd.Series(price, index=filtered_data.index, name=f"{level} ({price:.2f})"),
            type='line',
            color=colors[i % len(colors)],
            linestyle='dashed' if 'High' not in level and 'Low' not in level else 'solid',
            alpha=0.8
        ))
    
    # Add MAs (already calculated on full data)
    fib_plots.append(mpf.make_addplot(filtered_data['MA50'], color='green', width=1.2))
    if 'MA200' in filtered_data.columns and filtered_data['MA200'].notna().any():
        fib_plots.append(mpf.make_addplot(filtered_data['MA200'], color='blue', width=1.2))
    
    print("Fibonacci Levels:")
    for label, price in fib_levels.items():
        print(f"{label}: {price:.2f}")

    # 6. Plot
    titleM = f"\n{ticker} - Last {months} Months"
    if months == None:
        titleM = f"\n{ticker} - 5 Years"
    mpf.plot(filtered_data,
             type='candle',
             style='yahoo',
             title=titleM,
             ylabel='Price ($)',
             addplot=fib_plots,
             figratio=(16, 8),
             volume=True)