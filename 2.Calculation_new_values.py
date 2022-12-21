import pandas
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy

MONTH_STR = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
dates_dict = {'Apple': [], 'Twitter': [], 'Amazon': [], 'Hp': [], 'Google': [], 'Microsoft': [],
              'Blackberry': [], 'Ebay': [], 'Ibm': [], 'Adobe': [], 'Facebook': [], 'Disney': []}
new_df = {'Avg stocks prev. year': [], 'Avg stocks next year': [],
          'Avg S&P prev. year': [], 'Avg S&P next year': []}

SP_df = pandas.read_csv('./DATA/S&P500.csv', index_col=0, na_values='-')[['Close']]
SP_df.index = pandas.DatetimeIndex(SP_df.index)
print(SP_df)

companies_df = pandas.read_csv('./DATA/companies.csv', index_col=0, na_values='-')
companies_df.index = pandas.DatetimeIndex(companies_df.index)
print(companies_df)

excel_df = pandas.read_excel('./DATA/acquisitions_Svetlov.xls', sheet_name='Worksheet', na_values='-')
print(excel_df)
dates_list = excel_df.loc[:, ['Parent Company', 'Acquisition Year', 'Acquisition Month']].values.tolist()
print(dates_list)

for company, i_year, i_month in dates_list:
    year = str(i_year).split('.')[0]
    if i_month in MONTH_STR and year == year:
        month = str(MONTH_STR.index(i_month) + 1).zfill(2)
        dates_dict[company].append(year + '-' + month)
    else:
        dates_dict[company].append(numpy.NaN)
print(dates_dict)

for company in dates_dict:
    for date in dates_dict[company]:
        l_stocks_avg, r_stocks_avg, l_SP_avg, r_SP_avg = numpy.NaN, numpy.NaN, numpy.NaN, numpy.NaN
        if date == date:
            c_date = datetime.strptime(date, '%Y-%m').date()

            l_period_start = c_date - relativedelta(years=1) - pandas.offsets.MonthBegin(0)
            l_period_end = c_date - relativedelta(months=1) + pandas.offsets.MonthEnd(0)
            r_period_start = c_date + relativedelta(months=1) - pandas.offsets.MonthBegin(0)
            r_period_end = c_date + relativedelta(years=1) + pandas.offsets.MonthEnd(0)

            l_stocks_list = companies_df.loc[l_period_start:l_period_end, company]
            r_stocks_list = companies_df.loc[r_period_start:r_period_end, company]

            l_SP_list = SP_df.loc[l_period_start:l_period_end, 'Close']
            r_SP_list = SP_df.loc[r_period_start:r_period_end, 'Close']

            if len(l_stocks_list) > 180 and len(r_stocks_list) > 180:  # 180 - min values count in year
                l_stocks_avg = sum(l_stocks_list) / len(l_stocks_list)
                r_stocks_avg = sum(r_stocks_list) / len(r_stocks_list)
            if len(l_SP_list) > 200 and len(r_SP_list) > 200:  # 200 - min values count in year
                l_SP_avg = sum(l_SP_list) / len(l_SP_list)
                r_SP_avg = sum(r_SP_list) / len(r_SP_list)

        new_df['Avg stocks prev. year'].append(l_stocks_avg), new_df['Avg stocks next year'].append(r_stocks_avg)
        new_df['Avg S&P prev. year'].append(l_SP_avg), new_df['Avg S&P next year'].append(r_SP_avg)


new_df = pandas.DataFrame(new_df)
new_df['Avg stocks change %'] = [(y/x-1) if (x == x and y == y) else numpy.NaN
                                 for x, y in zip(new_df['Avg stocks prev. year'], new_df['Avg stocks next year'])]
new_df['Avg S&P change %'] = [(y/x-1) if (x == x and y == y) else numpy.NaN
                              for x, y in zip(new_df['Avg S&P prev. year'], new_df['Avg S&P next year'])]
new_df['Benchmark index'] = [(x-y) if (x == x and y == y) else numpy.NaN
                             for x, y in zip(new_df['Avg stocks change %'], new_df['Avg S&P change %'])]
print(new_df)

result_df = pandas.concat([excel_df, new_df], axis=1)
writer = pandas.ExcelWriter('./DATA/acquisitions_Svetlov_new.xlsx', engine='xlsxwriter')
result_df.to_excel(writer, sheet_name='Worksheet', index=False)
writer.close()
