import requests
import os
from dotenv import load_dotenv


def get_gold_rate():
    load_dotenv('.env')

    '''
    api_key = os.getenv('API_KEY')

    url = f"https://www.goldapi.io/api/XAU/INR"

    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    result = response.json()['price_gram_24k']
    '''

    api_key = os.getenv('CC_API_KEY')

    url = f"https://free.currconv.com/api/v7/convert?q=XAU_INR&compact=ultra&apiKey={api_key}"

    response = requests.get(url)
    result = response.json()['XAU_INR']

    price001 = result / 1000
    return price001


def get_gold_from_inr(amount_inr: int):
    gold_bits = amount_inr / get_gold_rate()
    return gold_bits


def get_inr_from_gold(amount_gold: int):
    amount = amount_gold * get_gold_rate()
    return amount


if __name__ == '__main__':
    print(get_gold_rate())
