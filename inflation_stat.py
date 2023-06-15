import pandas as pd
import matplotlib.pyplot as plt
import os


def rename_columns(df, year):
    months = {
        'январь': 1,
        'января': 1,
        'февраль': 2,
        'февраля': 2,
        'март': 3,
        'марта': 3,
        'апрель': 4,
        'апреля': 4,
        'май': 5,
        'мая': 5,
        'июнь': 6,
        'июня': 6,
        'июль': 7,
        'июля': 7,
        'август': 8,
        'августа': 8,
        'сентябрь': 9,
        'сентября': 9,
        'октябрь': 10,
        'октября': 10,
        'ноябрь': 11,
        'ноября': 11,
        'декабрь': 12,
        'декабря': 12,
    }
    columns = list(df.columns)
    renames = {}
    for c in columns:
        day, month = c.strip('на ').split()
        renames[c] = pd.Timestamp(year=year, month=months[month], day=int(day))
    return df.rename(columns=renames)


fname = 'Nedel_sred_cen.xlsx'
if not os.path.exists(fname):
    os.system(
        'wget https://rosstat.gov.ru/storage/mediabank/Nedel_sred_cen.xlsx')
df1 = pd.read_excel(fname, sheet_name=1, header=3, index_col=0)
df2 = pd.read_excel(fname, sheet_name=2, header=3, index_col=0)

df1 = rename_columns(df1, year=2022)
df2 = rename_columns(df2, year=2023)
# print(df1)
# print(df2)

names = [
    # 'Легковой автомобиль отечественный новый, шт.',
    # 'Легковой автомобиль иностранной марки новый, шт.',
    # 'Свинина (кроме бескостного мяса), кг',
    # 'Молоко питьевое цельное пастеризованное 2,5-3,2% жирности, л',
    # 'Молоко питьевое цельное стерилизованное 2,5-3,2% жирности, л',
    # 'Яйца куриные, 10 шт.',
    # 'Смартфон, шт.',
    # 'Подгузники детские бумажные, 10 шт.',
    'Огурцы свежие, кг',
]

prices = {}
for name in names:
    s1 = df1.loc[name].astype(float)
    s2 = df2.loc[name].astype(float)
    prices[name] = pd.concat([s1, s2])
prices = pd.DataFrame(prices)

dates = prices.index
start_date = pd.Timestamp(year=2023, month=1, day=1)
inflation = {}
for date in dates[dates >= start_date]:
    prev_date = pd.Timestamp(year=date.year - 1,
                             month=date.month,
                             day=date.day)
    prev_date = dates[dates.searchsorted(prev_date)]
    inflation[date] = 100 * (prices.loc[date] / prices.loc[prev_date] - 1)
inflation = pd.DataFrame(inflation).T

prices.plot()
plt.title('Цена')
plt.grid(True)
plt.legend()

inflation.plot()
plt.title('Инфляция')
plt.grid(True)
plt.legend()
plt.show()