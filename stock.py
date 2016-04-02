#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

stockNo = '3662'
stockAmountResult = []
stockPercentResult = []

# the date when the data is released
def fetchScaDate():
    url = 'http://www.tdcc.com.tw/smWeb/QryStock.jsp'
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    result = soup.find('select', {'name' : 'SCA_DATE'})
    return result.contents


def fetchStock(scaDate):
    url = 'http://www.tdcc.com.tw/smWeb/QryStock.jsp?SCA_DATE=' + scaDate + '&SqlMethod=StockNo&StockNo=' + stockNo + '&StockName=&sub=%ACd%B8%DF'
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    tables = soup.find_all('table')
    if len(tables) < 8:
        print('Data not found at scaDate = ' + scaDate)
        return
    # The table that contains 序, 持股/單位數分級, 人數, 股數/單位數, 佔集保庫存數比例(%)
    targetTable = tables[7]
    rows = targetTable.find_all('tr')

    # The row where 持股/單位數分級 = 1,000,001以上
    targetRow = rows[15]

    cols = targetRow.find_all('td')
    # The column representing 股數/單位數
    stockAmountCol = cols[3]

    stockPercentCol = cols[4]

    stockAmountResult.append(stockAmountCol.text)
    stockPercentResult.append(stockPercentCol.text)

if __name__ == '__main__':
    scaDate = fetchScaDate()
    scaDate = [d.string.strip() for d in scaDate]
    for d in scaDate:
        if d == '':
            continue
        print('date: ' + d)
        fetchStock(d)

    stockAmountResult = list(reversed(stockAmountResult))
    stockPercentResult = list(reversed(stockPercentResult))

    print(stockPercentResult)
    print(scaDate)