#!/usr/bin/env python
# coding: utf-8

# In[11]:

from tkinter import *
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from datetime import datetime


root = Tk()
root.geometry("500x600")
root.configure(bg='#0070E8')
root.title("USD Rate In Vladivostok")
root.resizable(False, False)


Label(root, text="USD RATE IN VLADIVOSTOK", bg='#0070E8', fg='#F1F1F1', font="arial 24 bold").place(relx=0.5, rely=0.2,
                                                                                                  anchor=CENTER)


def get_rate_info():
    data = []

    url = "https://www.vl.ru/dengi/"
    try:
        r = requests.get(url)
        sleep(2)
    except:
        pass

    soup = BeautifulSoup(r.text, 'lxml')

    raw_rate_info = soup.find('tbody', class_='rates-desktop__content')

    dollar_rate_infos = raw_rate_info.findAll('tr', class_='rates-desktop__table-row')

    for dollar_rate_info in dollar_rate_infos:
        try:
            bank_name = dollar_rate_info.find('a', class_='link rates-desktop__bank-name').text
        except:
            bank_name = '-'
        try:
            rate_buy_which = dollar_rate_info.find('td', class_='rates-desktop__table-cell').get('data-currency')
            if rate_buy_which == 'USD':
                rate_buy = dollar_rate_info.find('td', class_='rates-desktop__table-cell').get('data-buy')
                rate_sell = dollar_rate_info.find('td', class_='rates-desktop__table-cell').get('data-sell')
        except:
            rate_buy = '-'
            rate_sell = '-'
        try:
            bank_address = dollar_rate_info.find('a', class_='link rates-desktop__bank-name').get('href')
        except:
            bank_address = '-' 
        try:
            phone_number = dollar_rate_info.find('span', class_='icon icon_phone-desktop rates-desktop__bank-icon js-tooltip').get('data-title')
        except:
            phone_number = '-'
        
        data.append([bank_name, rate_buy, rate_sell, phone_number, bank_address])

    data = sorted(data,key=lambda l:l[1], reverse=True)    
    header = ['은행이름', 'USD구입가격', 'USD판매가격', '전화번호', '은행주소']
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d---%H-%M-%S")
    excel_file_name = f"오늘의 USD시세{dt_string}.xlsx"
    df = pd.DataFrame(data, columns=header)
    df.to_excel(excel_file_name)

    #csv_file_name = f"오늘의 USD시세{dt_string}.csv"
    #df.to_csv(csv_file_name, sep=';',encoding='utf8')
        

Button(root, text="USD RATE", font="arial 15 bold", bg="#0B96F7", fg='#F1F1F1', padx=2,
       command=get_rate_info).place(relx=0.5, rely=0.8, anchor=CENTER)

root.mainloop()





