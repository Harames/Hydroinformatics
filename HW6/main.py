import pandas as pd
import matplotlib.pyplot as plt

# Load in data
df = pd.read_csv('datalog_richards_hall.csv', header=1, sep=',', index_col=0, parse_dates=True, low_memory=False)

# Question 1

# Days to delineate between spring break and after
beginSpringBreak = '2017-03-04 00:00:00'
endSpringBreak = '2017-03-12 23:59:59'
beginNotSpringBreak = '2017-03-13 00:00:00'

# Create subsets
df_springBreak = df[beginSpringBreak:endSpringBreak]
df_notSpringBreak = df[beginNotSpringBreak:]

# Resample into daily values
springBreakDaily = df_springBreak.resample(rule='D', origin='start_day').sum()
notSpringBreakDaily = df_notSpringBreak.resample(rule='D', origin='start_day').sum()

# Find average daily water usage between the two date ranges
print("Average daily water used during spring break:", springBreakDaily['IncrementalVolume'].mean())
print("Average daily water used after spring break:", notSpringBreakDaily['IncrementalVolume'].mean())

# Create plot for visual
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

springBreakDaily.plot(ax=axes[0], y='IncrementalVolume', kind='line', use_index=True,
                      style='-', ylim=[0, 6500], marker='o',
                      label='Daily total volume (gal)')
axes[0].set_ylabel('Total Volume (gallons)')
axes[0].set_xlabel('Date/Time')
axes[0].grid(True)
axes[0].legend(loc='upper right', shadow=True)
axes[0].set_title("Spring Break")

notSpringBreakDaily.plot(ax=axes[1], y='IncrementalVolume', kind='line', use_index=True,
                         style='-', ylim=[0, 6500], marker='o',
                         label='Daily total volume (gal)')
axes[1].set_ylabel('Total Volume (gallons)')
axes[1].set_xlabel('Date/Time')
axes[1].grid(True)
axes[1].legend(loc='upper right', shadow=True)
axes[1].set_title("After Spring Break")

plt.tight_layout()
plt.savefig("Question1.png")
plt.show()

# Question 2

# Split into weekdays and weekends
df['TypeOfDay'] = df.index.dayofweek
df_weekday = df[df['TypeOfDay'] < 5]
df_weekend = df[df['TypeOfDay'] >= 5]

# Calculate stats for weekdays
hourlyTotVolWeekday = df_weekday['IncrementalVolume'].resample(rule='h', origin='start_day').sum()
hourlyAvgVolWeekday = hourlyTotVolWeekday.groupby(hourlyTotVolWeekday.index.hour).mean()
hourlyStDevVolWeekday = hourlyTotVolWeekday.groupby(hourlyTotVolWeekday.index.hour).std()

# Calculate stats for weekends
hourlyTotVolWeekend = df_weekend['IncrementalVolume'].resample(rule='h', origin='start_day').sum()
hourlyAvgVolWeekend = hourlyTotVolWeekend.groupby(hourlyTotVolWeekend.index.hour).mean()
hourlyStDevVolWeekend = hourlyTotVolWeekend.groupby(hourlyTotVolWeekend.index.hour).std()

# Plot two error bars on top of each other
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

plt.errorbar(x=hourlyAvgVolWeekday.index, y=hourlyAvgVolWeekday,
             yerr=hourlyStDevVolWeekday, capsize=3,
             capthick=0.5, fmt='--',
             label='Average Hourly Volumes Weekday', marker='o')

plt.errorbar(x=hourlyAvgVolWeekend.index, y=hourlyAvgVolWeekend,
             yerr=hourlyStDevVolWeekend, capsize=3,
             capthick=0.5, fmt='--',
             label='Average Hourly Volumes Weekend', marker='o')

ax.legend(loc='upper right', shadow=True)
ax.set_ylabel("Average Hourly Volume (gal)")
ax.set_xlabel("Hour of the Day")
ax.grid(False)
ax.set_xlim(-0.5, 23.5)
xmarks = range(0, 23 + 1, 1)
plt.xticks(xmarks)
plt.title("Average Hourly Volume Estimates")
plt.tight_layout()
plt.savefig("Question2.png")
plt.show()

# Question 3

# Set the dates and create the needed dataframes
beginDate = '2017-03-03 15:13:00'
endDate = '2017-03-27 16:20:00'
df_1s = df[beginDate:endDate].copy()
df_5s = df_1s[0::5].copy()
df_10s = df_1s[0::10].copy()
df_30s = df_1s[0::30].copy()

# Generate the needed data in the dataframes
df_1s['CumVol'] = df_1s.FlowRate.cumsum() * 1.0 / 60.0
df_5s['CumVol'] = df_5s.FlowRate.cumsum() * 5.0 / 60.0
df_10s['CumVol'] = df_10s.FlowRate.cumsum() * 10.0 / 60.0
df_30s['CumVol'] = df_30s.FlowRate.cumsum() * 30.0 / 60.0

# Create plots
fig, axes = plt.subplots(nrows=2, ncols=2)
df_1s['CumVol'].plot(ax=axes[0, 0])
df_5s['CumVol'].plot(ax=axes[0, 1])
df_10s['CumVol'].plot(ax=axes[1, 0])
df_30s['CumVol'].plot(ax=axes[1, 1])

axes[0, 0].set_title('1 Second Data')
axes[0, 0].set_xlabel('Date/Time')
axes[0, 0].set_ylabel('Cumulative Volume (gal)')

axes[0, 1].set_title('5 Second Data')
axes[0, 1].set_xlabel('Date/Time')
axes[0, 1].set_ylabel('Cumulative Volume (gal)')

axes[1, 0].set_title('10 Second Data')
axes[1, 0].set_xlabel('Date/Time')
axes[1, 0].set_ylabel('Cumulative Volume (gal)')

axes[1, 1].set_title('30 Second Data')
axes[1, 1].set_xlabel('Date/Time')
axes[1, 1].set_ylabel('Cumulative Volume (gal)')

plt.tight_layout()
plt.savefig("Question3a.png")
plt.show()

# Create second plot with the data overlapping
fig, axes = plt.subplots()
df_1s['CumVol'].plot(label="1 Second Data")
df_5s['CumVol'].plot(label="5 Second Data")
df_10s['CumVol'].plot(label="10 Second Data")
df_30s['CumVol'].plot(label="30 Second Data")

axes.set_xlabel('Date/Time')
axes.set_ylabel('Cumulative Volume (gal)')
axes.legend(loc="upper left", shadow=True)

plt.tight_layout()
plt.savefig("Question3b.png")
plt.show()

# Print out values to compare to manual read data
print("1 Second Final Value: ", df_1s['CumVol'].iloc[-1])
print("5 Second Final Value: ", df_5s['CumVol'].iloc[-1])
print("10 Second Final Value: ", df_10s['CumVol'].iloc[-1])
print("30 Second Final Value: ", df_30s['CumVol'].iloc[-1])
