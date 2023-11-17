import requests
from bs4 import BeautifulSoup
import pandas as pd

# Shift-JIS の csv ファイルを読み込む
df = pd.read_csv('stock.csv', encoding='shift_jis')

df_out = pd.DataFrame(columns=['コード', '銘柄', '市場', '前日終値', '始値', '高値', '安値', '配当利回り', '単元株数', 'PER', 'PSR', 'PBR', '出来高', '時価総額', '発行済株数', '株主優待'])

for i, row in df.iterrows():
    code = row['コード']
    name = row['銘柄名']
    market = row['市場・商品区分']
    
    if not(market == 'プライム（内国株式）' or  market == 'スタンダード（内国株式）' or market == 'グロース（内国株式）'):
        continue

    if code == 25935: # 伊藤園 優先株式
        continue

    # みんかぶ
    url = 'https://minkabu.jp/stock/{0}'.format(code)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    basic_info = []
    tr_list = soup.find_all('tr')
    for tr in tr_list:
        th = tr.find('th')
        if th is None:
            continue
        td = tr.find('td')
        basic_info.append(td.text)
    
    df_out.loc[i] = [code, name, market, basic_info[0][:-1], basic_info[1][:-1], basic_info[2][:-1], basic_info[3][:-1], basic_info[4][:-1], basic_info[5][:-1], basic_info[6][:-1], basic_info[7][:-1], basic_info[8][:-1], basic_info[9][:-1], basic_info[10], basic_info[11], basic_info[12]]

df_out.to_csv('stock_info.csv', index=False)
