# Imports
import pandas as pd
import datetime as dt
import calendar
import plotly
import plotly.express as px


# Specify Files Names [ff the files are NOT in the same directory as the script, please use the absolute path to the files]
files = ['January.xlsx', 'February.xlsx', 'March.xlsx']

# // Get File Names dynamically
# import os
# import glob
# extension = 'xlsx'
# files = glob.glob('*.{}'.format(extension))

combined = pd.DataFrame()

for file in files:
    df = pd.read_excel(file)
    df['Date'] = df['Date'].dt.date
    df['Day'] = pd.DatetimeIndex(df['Date']).day
    df['Month'] = pd.DatetimeIndex(df['Date']).month
    df['Year'] = pd.DatetimeIndex(df['Date']).year
    df['Month_Name'] = df['Month'].apply(lambda x: calendar.month_abbr[x])
    combined = combined.append(df,ignore_index = True)
# Create Bar Chart
fig = px.bar(combined, x='Month_Name', y='Sales', title='Sales 1Q 2020')
#Save Bar Chart and Export to HTML
plotly.offline.plot(fig, filename='Sales_1Q_2020.html')
# Send Report as attached mail
# Create more charts
# ...
# Export combined files to Excel
combined.to_excel('Sales_1Q2020.xlsx', index = False, sheet_name='1Q 2020 Sales')
