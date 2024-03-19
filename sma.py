# Import libraries
import pandas as pd
import numpy as np
import talib as ta

# Input data
input_data = [
    44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08, 
    45.89, 46.03, 45.61, 46.28, 46.28, 46.00, 46.03, 46.41, 46.22, 45.64, 
    46.21, 46.25, 45.71, 46.45, 45.78, 45.35, 44.03, 44.18, 44.22, 44.57, 
    43.42, 42.66, 43.13
]

# Convert input data to DataFrame
df = pd.DataFrame({'Input': input_data})

# Calculate Change
# It is difference of the current one and between the previous one
df['Change'] = df['Input'].diff()

# Gain is shown when Change is greater than zero or else 0 and vise-versa
# Calculate Gain and Loss
df['Gain'] = df['Change'].apply(lambda x: x if x > 0 else 0)
df['Loss'] = df['Change'].apply(lambda x: abs(x) if x < 0 else 0) # abs()- absolute value converts negative to possitive

# Calculate Average Gain and Average Loss
# rolling() function provides the feature of rolling window calculations it used when working with time-series
# Calculate the average gain and average loss over a 14-day period
df['Avg Gain'] = df['Gain'].rolling(window=14, min_periods=1).mean()
df['Avg Loss'] = df['Loss'].rolling(window=14, min_periods=1).mean()

# Calculate HM Average Gain divided by Average loss
df['HM'] = (df['Avg Gain']) / df['Avg Loss']

# Calculate 14-day HMA
# 14-day Hull Moving Average using the SMA (Simple Moving Average) function from the talib library.
df['14-day HMA'] = ta.SMA(df['Input'].values, timeperiod=14)

# Print the resulting DataFrame
print(df)
