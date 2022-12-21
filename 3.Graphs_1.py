import pandas
import seaborn
import numpy
import matplotlib.pyplot as plot


excel_df = pandas.read_excel('./DATA/acquisitions_Svetlov_new.xlsx', sheet_name='Worksheet', na_values='')
print(excel_df)
df_year_f, df_month_f, df_change_type1 = excel_df.copy(), excel_df.copy(), excel_df.copy()
df_bsn, df_comp = excel_df.copy(), excel_df.copy()

df_year_f.dropna(subset=['Acquisition Year'], inplace=True)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
df_month_f.dropna(subset=['Acquisition Month'], inplace=True)
df_month_f = df_month_f.groupby(['Acquisition Month']).count().ID.reset_index()
df_month_f['Acquisition Month'] = pandas.Categorical(df_month_f['Acquisition Month'], categories=months, ordered=True)

df_change_type1.dropna(subset=['Avg stocks prev. year', 'Avg stocks next year'], inplace=True)
df_change_type2 = df_change_type1.copy()
df_change_type1['type'], df_change_type2['type'] = 'prev. year', 'next year'
df_change_type1.rename(columns={'Avg stocks prev. year': 'avg stocks'}, inplace=True)
df_change_type2.rename(columns={'Avg stocks next year': 'avg stocks'}, inplace=True)
df_change_f = pandas.concat([df_change_type1, df_change_type2])

df_bsn.dropna(subset=['Business'], inplace=True)
df_bsn = df_bsn.groupby(['Business']).count().ID.reset_index()
df_bsn = df_bsn.sort_values(by=['ID'], ascending=False).head(30)

df_comp.dropna(subset=['Acquisition Year'], inplace=True)
df_comp = df_comp.groupby(['Parent Company']).count().ID.reset_index()
df_comp = df_comp.sort_values(by=['ID'], ascending=False)

print(df_year_f)
print(df_month_f)
print(df_change_f)
print(df_bsn)
print(df_comp)

xlim_l, xlim_r = 1987, 2021
xa = range(xlim_l, xlim_r+1)
xa_short = [str(date)[2:] for date in xa]
xa2 = range(xlim_l, xlim_r+1, 2)
xa2_short = [str(date)[2:] for date in xa2]

seaborn.set(font_scale=0.8)

# Acquisitions per year
fig1, ax1 = plot.subplots(figsize=(20, 10))
seaborn.histplot(data=df_year_f, ax=ax1, x="Acquisition Year", binwidth=1, bins=len(xa), kde=True).\
    set(title='Acquisitions per year', xlabel="Acquisition year", ylabel='Acquisitions count')
ax1.set_xlim(xlim_l, xlim_r)
ax1.set_xticks(xa, xa_short)
fig1.savefig("./IMG/Acquisitions per year.png")

# Acquisitions per month
fig2, ax2 = plot.subplots()
seaborn.barplot(data=df_month_f, x="Acquisition Month", y="ID", color='#5D76CB').\
    set(title='Acquisitions per month', xlabel="Acquisition month", ylabel='Acquisitions count')
fig2.savefig("./IMG/Acquisitions per month.png")

# Acquisitions per year for each company
gr1 = seaborn.FacetGrid(df_year_f, col="Parent Company", col_wrap=4, xlim=(xlim_l, xlim_r))
gr1.map(seaborn.histplot, "Acquisition Year", bins=len(xa), kde=True)
gr1.set_axis_labels("Acquisition year", "Acquisitions count")
for ax in gr1.axes_dict.values():
    ax.set_xticks(xa2, xa2_short)
gr1.fig.subplots_adjust(top=0.9)
gr1.fig.suptitle('Acquisitions per year for each company')
gr1.savefig("./IMG/Acquisitions per year for each company.png", dpi=400)

# Acquisitions count for each company
fig3, ax3 = plot.subplots()
seaborn.barplot(data=df_comp, x="Parent Company", y='ID').\
    set(title='Acquisitions count for each company', xlabel="Company", ylabel='Acquisitions count')
fig3.savefig("./IMG/Acquisitions count for each company.png")

# 30 most popular business to acquire
fig4, ax4 = plot.subplots(figsize=(20, 10))
seaborn.barplot(data=df_bsn, x="ID", y="Business", color='#5D76CB').\
    set(title='30 most popular business to acquire', xlabel="Acquisitions count", ylabel='Business')
fig4.savefig("./IMG/30 most popular business to acquire.png")
fig4.subplots_adjust(left=0.2)

# Comparison of prev. and next year avg stock prices
gr2 = seaborn.FacetGrid(df_change_f, col="Parent Company", hue='type', col_wrap=4, xlim=(xlim_l, xlim_r))
gr2.map(seaborn.lineplot, "Acquisition Year", "avg stocks")
gr2.set_axis_labels("Acquisition year", "Stock price")
for ax in gr2.axes_dict.values():
    ax.set_xticks(xa2, xa2_short)
    ax.legend()
gr2.fig.subplots_adjust(top=0.9)
gr2.fig.suptitle('Comparison of prev. and next year avg stock prices')
gr2.savefig("./IMG/Comparison of prev. and next year avg stock prices.png", dpi=400)

plot.show()
