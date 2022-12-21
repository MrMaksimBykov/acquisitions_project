import pandas
import seaborn
import numpy
import matplotlib.pyplot as plot

MONTH_STR = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
excel_df = pandas.read_excel('./DATA/acquisitions_Svetlov_new.xlsx', sheet_name='Worksheet', na_values='')
excel_df.rename(columns={'Parent Company': 'Par_comp'}, inplace=True)
companies = list(excel_df.Par_comp.unique())
print(excel_df)
print(companies)
df_cps, df_acs, df_countries = excel_df.copy(), excel_df.copy(), excel_df.copy()

df_cps.dropna(subset=['Acquisition Year', 'Acquisition Month'], inplace=True)
df_cps['Acquisition Year'] = df_cps['Acquisition Year'].astype(float)
df_cps['Acquisition Month'] = [MONTH_STR.index(x)+1 for x in df_cps['Acquisition Month']]
df_cps['Acquisition Year'] = df_cps['Acquisition Year'] + df_cps['Acquisition Month']/12

df_acs.dropna(subset=['Acquisition Year'], inplace=True)
df_acs = df_acs.groupby(['Par_comp', 'Acquisition Year']).count().ID.reset_index()
df_acs['Acquisition Year'] = df_acs['Acquisition Year'].astype(float)

df_countries = df_countries[numpy.isin(df_countries, ['Ibm', 'Facebook']).any(axis=1)]
df_countries.dropna(subset=['Country'], inplace=True)
df_countries = df_countries.groupby(['Par_comp', 'Country']).count().ID.reset_index()
df_countries = df_countries[df_countries.ID != 1]
companies_p = ['Ibm', 'Facebook']
print(df_cps)
print(df_acs)
print(df_countries)

xlim_l, xlim_r = 1987, 2021
xa = range(xlim_l, xlim_r+1)
xa_short = [str(date)[2:] for date in xa]
xa2 = range(xlim_l, xlim_r+1, 2)
xa2_short = [str(date)[2:] for date in xa2]

seaborn.set(font_scale=0.8)

fig1 = plot.figure(figsize=(20, 10), layout="constrained")
for i, company in enumerate(companies):
    df_cps_i = df_cps[(df_cps == str(company)).any(axis=1)]
    df_acs_i = df_acs[(df_acs == str(company)).any(axis=1)]

    ax = plot.subplot(4, 3, i+1)
    ax.set_xticks(xa2, xa2_short)
    ax2 = ax.twinx()
    line1, = ax.plot(df_cps_i['Acquisition Year'], df_cps_i['Avg stocks change %'], color='red', label='Stocks')
    line2, = ax.plot(df_cps_i['Acquisition Year'], df_cps_i['Avg S&P change %'], color='blue', label='S&P')
    pl_b = ax2.bar(df_acs_i['Acquisition Year'], df_acs_i['ID'], alpha=0.5, color='#fff0', edgecolor='#10941d')

    ax.set_title(company)
    ax.legend(handles=[line1, line2], prop={'size': 8}, loc=2)
    ax.set_ylabel('Price change', fontsize=8)
    ax.set_xlabel('Date', fontsize=8)
    ax2.set_ylabel('Acquisition count', fontsize=8)
    ax.grid(False)
    ax2.grid(False)
    if ax.get_xlim()[0] < 1987:
        ax.set_xlim(1987, ax.get_xlim()[1])
fig1.savefig("./IMG/result_v1")

fig2 = plot.figure(figsize=(20, 10), layout="constrained")
for i, company in enumerate(companies):
    df_cps_i = df_cps[(df_cps == str(company)).any(axis=1)]
    df_acs_i = df_acs[(df_acs == str(company)).any(axis=1)]

    ax = plot.subplot(4, 3, i+1)
    ax.set_xticks(xa2, xa2_short)
    ax2 = ax.twinx()
    line1, = ax.plot(df_cps_i['Acquisition Year'], df_cps_i['Benchmark index'], color='blue')
    pl_b = ax2.bar(df_acs_i['Acquisition Year'], df_acs_i['ID'], alpha=0.5, color='#fff0', edgecolor='#10941d')

    ax.set_title(company)
    ax.set_ylabel('Benchmark index', fontsize=8)
    ax.set_xlabel('Date', fontsize=8)
    ax2.set_ylabel('Acquisition count', fontsize=8)
    ax.grid(False)
    ax2.grid(False)
    if ax.get_xlim()[0] < 1987:
        ax.set_xlim(1987, ax.get_xlim()[1])
fig2.savefig("./IMG/result_v2", dpi=400)


fig3 = plot.figure(figsize=(20, 10), layout="constrained")
fig3.suptitle('Countries from where Ibm and Facebook acquired (except for countries with one acquired)',
              fontsize=14)
for i, company in enumerate(companies_p):
    df_countries_i = df_countries[(df_countries == str(company)).any(axis=1)]

    ax = plot.subplot(1, 2, i+1)
    pie = ax.pie(df_countries_i['ID'], labels=df_countries_i['Country'], textprops={"fontsize": 9},
                 labeldistance=1.02, autopct='%.1f%%', pctdistance=0.9,
                 startangle=-20, rotatelabels=180, colors=seaborn.color_palette("crest"))
    ax.set_title(company, fontsize=12)
fig3.savefig("./IMG/Countries from where Ibm and Facebook acquired", dpi=300)

plot.show()
