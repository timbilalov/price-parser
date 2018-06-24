# coding: utf8

from bs4 import BeautifulSoup
import requests
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

page = requests.get('https://www.bethowen.ru/catalogue/dogs/korma/syxoi/korm-dlya-sobak-duke-s-farm-dlya-srednikh-i-krupnykh-porod-indeyka-sukh-12kg/')

source_code = page.text
soup = BeautifulSoup(source_code, "lxml")

productCodeElements = soup.findAll("h3", {"class": "product-code"})
for elem in productCodeElements:
	if not elem.findAll("a"):
		parentBlock = elem.find_parents("div", {"class": "productFilter"})[0]

# Error handling
if not parentBlock:
	Notify.init("Error while parsing prices")

	summary = "Error while parsing prices"
	body = "See and explore parser.py to find what went wrong"

	notification = Notify.Notification.new(
	    summary,
	    body,
	)

	notification.show()

	# Clean
	Notify.uninit()
	exit()

# Successfully found parentBlock
titleElement = soup.findAll("h1", {"class": "product-title"})
priceElemStandart = parentBlock.findAll("span", {"class": "price-standard"})
priceElemSales = parentBlock.findAll("span", {"class": "price-sales"})

title = titleElement[0].contents[0].strip() if len(titleElement) > 0 else False
priceStandart = (int)(priceElemStandart[0].contents[0].strip()) if len(priceElemStandart) > 0 else False
priceSales = (int)(priceElemSales[0].contents[0].strip()) if len(priceElemSales) > 0 else False
if not priceStandart and priceSales > 0:
    priceStandart = priceSales
    priceSales = False

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