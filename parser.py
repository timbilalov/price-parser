# coding: utf8

from bs4 import BeautifulSoup
import requests
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

page = requests.get('https://www.bethowen.ru/catalogue/dogs/korma/syxoi/korm-dlya-shchenkov-dukes-dlya-krupnykh-porod-kuritsa-sukh-12kg/')

source_code = page.text
soup = BeautifulSoup(source_code, "lxml")

titleElement = soup.findAll("h1", {"class": "product-title"})
priceElemStandart = soup.findAll("span", {"class": "price-standard"})
priceElemSales = soup.findAll("span", {"class": "price-sales"})

title = titleElement[0].contents[0].strip() if len(titleElement) > 0 else False
priceStandart = (int)(priceElemStandart[0].contents[0].strip()) if len(priceElemStandart) > 0 else False
priceSales = (int)(priceElemSales[0].contents[0].strip()) if len(priceElemSales) > 0 else False
if not priceStandart and priceSales > 0:
    priceStandart = priceSales
    priceSales = False
# print title
# print priceStandart
# print priceSales

Notify.init("Prices")

summary = title if title else ""
body = ("Стандартная цена: " + (str)(priceStandart) + " руб.") if priceStandart else ""
body += ("\nЦена со скидкой: " + (str)(priceSales) + " руб.") if priceSales else ""
body += ("\nСкидка: " + (str)((int)(round((float)(priceStandart - priceSales) / (float)(priceStandart) * 100))) + "%") if priceSales else ""
body += ("\nНадо брать! :)") if priceSales and priceSales <= 3400 else ""

notification = Notify.Notification.new(
    summary,
    body,
)

notification.show()

# Clean
Notify.uninit()