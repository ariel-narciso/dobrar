from bs4 import BeautifulSoup
import requests

TICKER_URI = 'https://statusinvest.com.br/acoes'
ETF_URI = 'https://statusinvest.com.br/etfs'
HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
}

def findCnpj(quote: str, ticker = True):
	soup = BeautifulSoup(
		requests.get('{}/{}'.format(
			TICKER_URI if ticker else ETF_URI, quote), headers=HEADERS
		).text,
		features='html.parser',
	)
	try:
		if ticker:
			ret = (
				soup.find('div', attrs={"class": "company-description"})
					.h4.small
			)
		else:
			ret = (
				soup.find('h3', string='CNPJ')
					.next_sibling.next_sibling
			)
		return ret.contents[0]
	except (AttributeError, IndexError) as err:
		return err
