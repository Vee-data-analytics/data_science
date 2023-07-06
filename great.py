from datetime import datetime as dt
import pandas as pd
import calendar
import plotly
import plotly.express as px 

files = ['Janury.xlsx','February.xlsx', 'March.xlsx']


combined = pd.DataFrame()

for file in files:
    df = pd.read_excel(file)
    df['Date'] = df['Date'].date
    df['Day'] = dt.DataTimeIndex(df['Date']).day
    df['Month'] = dt.DatetimeIndex(df['Date']).month
    df['Year'] = dt.DatetimeIndex(df['Date']).year
    df['Month_Name'] = dt.DatetimeIndex['Month'].apply(lambda x: calendar.month_abbr[x])
    combined = combined.append(df,ignore_index=True)

# plot chart
fig = px.bar(combined, x='Month_Name', y='Sales', title='Sales 1Q 2021')

# Save Bar Chart and Export to HTML
plotly.offline.plot(fig, filename='Sales_1Q_2020.html' )

combined.to_excel('Sales')

# Export combined files Excel
combined.to_excel('blow_1Q2020.xlsx', index= False, sheet_name='1Q 2020 Sales')