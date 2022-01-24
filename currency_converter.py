from cgi import print_form
from bs4 import BeautifulSoup as bs
from flask_login import ID_ATTRIBUTE
import requests

class CurrencyConverter():
    def __init__(self,url):
        self.data= requests.get(url).json()
        self.currencies = self.data['rates']

    
    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        #first convert it into RSD if it is not in RSD.
        # because our base currency is RSD
        if from_currency != 'RSD' : 
            amount = amount / self.currencies[from_currency] 
    
        # limiting the precision to 4 decimal places 
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

