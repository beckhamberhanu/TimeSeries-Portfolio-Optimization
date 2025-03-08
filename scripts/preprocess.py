import yfinance as yf
import pandas as pd

# Fetch stock data
def fetch_stock_data(tickers, start_date="2015-01-01", end_date="2025-01-31"):
    data = {}
    for ticker in tickers:
        stock = yf.download(ticker, start=start_date, end=end_date)
        data[ticker] = stock
        print(f"✅ {ticker} Data Fetched: {stock.shape[0]} rows")
    return data

# Clean data
def clean_data(df):
    print("\n🔍 Checking Missing Values:")
    print(df.isnull().sum())
    df = df.ffill().bfill()
    df["Date"] = pd.to_datetime(df["Date"])
    return df

# Normalize data
def normalize_data(df, tickers):
    for ticker in tickers:
        close_col = f"{ticker}_Close"
        if close_col in df.columns:
            df[f"{ticker}_Norm_Close"] = (df[close_col] - df[close_col].min()) / \
                                        (df[close_col].max() - df[close_col].min())
        else:
            print(f"Warning: Column '{close_col}' not found in DataFrame.")
    return df

# Main execution
tickers = ["TSLA", "BND", "SPY"]
stock_data = fetch_stock_data(tickers)

# Concatenate and flatten columns
df = pd.concat(stock_data, axis=1)
df.columns = [f"{ticker}_{metric}" for ticker, metric in df.columns]

# Reset index to make 'Date' a column
df.reset_index(inplace=True)

# Clean and normalize
df = clean_data(df)
df = normalize_data(df, tickers)

print("\nProcessed DataFrame head:")
print(df.head())