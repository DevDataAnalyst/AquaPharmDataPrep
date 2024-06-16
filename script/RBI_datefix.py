import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
# Read the original Excel file
df = pd.read_excel("01062024RBI_Rates.xlsx")

# Convert 'Date' column to datetime format and rename it
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Create a date range from the minimum date to the maximum date in the dataset
date_range = pd.date_range(start=df['Date'].min(), end=df['Date'].max())

# Reindex the DataFrame with the complete date range
df = df.set_index('Date').reindex(date_range)

# Forward fill missing values
df[['USD', 'GBP', 'EURO', 'YEN']] = df[['USD', 'GBP', 'EURO', 'YEN']].ffill()

# Reset index and rename the index column to 'Date'
df.reset_index(inplace=True)
df.rename(columns={'index': 'Date'}, inplace=True)

# Format 'Date' column to show only date without timestamp
df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')

# Add a new column 'INR' with constant value 1.0
df['INR'] = 1.0

# Save the DataFrame to a new Excel file
#df.to_excel("RBI_rates_with_INR.xlsx", index=False)

# Unpivot the DataFrame to transform the columns 'USD', 'GBP', 'EURO', 'YEN','INR' into rows under a column named FCURR
df = df.melt(id_vars=['Date'], value_vars=['USD', 'GBP', 'EURO', 'YEN', 'INR'], var_name='FCURR', value_name='RATE')

# Rename 'EURO' column to 'EUR'
df['FCURR'].replace({'EURO': 'EUR'}, inplace=True)

# Add 'TCURR' column with constant value 'INR'
df['TCURR'] = 'INR'

# Rename 'Date' column to 'FDATE'
df.rename(columns={'Date': 'FDATE'}, inplace=True)

# Save the resulting DataFrame to a new Excel file
df.to_excel("unpivoted_RBI_rates.xlsx", index=False)
