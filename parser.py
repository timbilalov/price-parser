# coding: utf8

from bs4 import BeautifulSoup
import requests
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
import re

pageAddresses = [
	'https://4lapy.ru/catalog/sobaki/Grandin_Fresh_Meat_suhoy_korm_dlya_sobak_krupnyh_i_gigantskih_porod_kuritsa.html?offer=44192',
	'https://4lapy.ru/catalog/sobaki/Grandin_Fresh_Meat_suhoy_korm_dlya_shchenkov_krupnyh_i_gigantskih_porod_kuritsa.html?offer=44190',
	'https://4lapy.ru/catalog/sobaki/Grandin_Fresh_Meat_suhoy_korm_dlya_sobak_vseh_porod_yagnenok.html?offer=44188',
	'https://4lapy.ru/catalog/sobaki/Avva_Premium_suhoy_korm_dlya_sobak_krupnyh_porod_kuritsa.html?offer=45767',
	'https://4lapy.ru/catalog/sobaki/Avva_Premium_Fresh_Meat_suhoy_korm_dlya_sobak_vseh_porodososris.html?offer=44103',
	'https://4lapy.ru/catalog/sobaki/Avva_Premium_suhoy_korm_dlya_sobak_vseh_porod_yagnenokris.html?offer=45768',
	'https://4lapy.ru/catalog/sobaki/korm-sobaki/sukhoy-korm-sobaki/Grandin_Fresh_Meat_suhoy_korm_dlya_sobak_melkih_porod_yagnenok.html?offer=81072',
]

# Error handling
def fail():
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

def checkPage(pageAddress):
	page = requests.get(pageAddress)

	source_code = page.text
	soup = BeautifulSoup(source_code, "lxml")

	parentBlock = soup.findAll("div", {"class": "b-product-card__top"})[0]

	if not parentBlock:
		fail()
		exit()

	# Successfully found parentBlock
	brandElement = parentBlock.findAll("span", {"itemprop": "brand"})
	titleElement = parentBlock.findAll("h1", {"class": "b-title b-title--h1 b-title--card"})
	priceElemOld = soup.find("span", {"class": "b-advice__old-price"})
	priceElemStandart = soup.find("span", {"class": "b-advice__cost"})
	priceStandart = False
	priceSales = False

	if priceElemStandart:
		priceStandart = (int)(re.sub('[^0-9]','', priceElemStandart.text.strip()))
		if priceElemOld:
			priceSales = priceStandart
			priceStandart = (int)(re.sub('[^0-9]','', priceElemOld.text.strip()))
	else:
		priceElemStandart = soup.findAll("meta", itemprop = "price")
		if priceElemStandart and len(priceElemStandart) > 0:
			prices = []
			for elem in priceElemStandart:
				prices.append((int)(elem["content"]))
			prices.sort(reverse = True)
			priceStandart = prices[0]
		else:
			priceStandart = False

	if not priceStandart:
		fail()
		exit()

	title = titleElement[0].contents[0].strip() if len(titleElement) > 0 else False
	if len(brandElement) > 0:
		title = brandElement[0].contents[0].strip() + " " + title

	Notify.init("Prices")

	summary = title if title else ""
	discountPercents = (int)(round((float)(priceStandart - priceSales) / (float)(priceStandart) * 100))
	body = ("Стандартная цена: " + (str)(priceStandart) + " руб.") if priceStandart else ""
	body += ("\nЦена со скидкой: " + (str)(priceSales) + " руб.") if priceSales else ""
	body += ("\nСкидка: " + (str)(discountPercents) + "%") if priceSales else ""
	body += ("\nНадо брать! :)") if priceSales and discountPercents >= 15 else ""

	notification = Notify.Notification.new(
	    summary,
	    body,
	)

	notification.show()

	# Clean
	Notify.uninit()

for pageAddress in pageAddresses:
	checkPage(pageAddress)