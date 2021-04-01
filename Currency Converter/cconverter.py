import requests


usd_rates_info = requests.get('http://www.floatrates.com/daily/usd.json').json()
eur_rates_info = requests.get('http://www.floatrates.com/daily/eur.json').json()
ils_rates_info = requests.get('http://www.floatrates.com/daily/ils.json').json()

usd_to_eur_rate = usd_rates_info.get('eur').get('rate')
eur_to_usd_rate = eur_rates_info.get('usd').get('rate')
ils_to_eur_rate = ils_rates_info.get('eur').get('rate')

cached_rates = dict()
cached_rates.update({'usd': {'eur': usd_to_eur_rate}})
cached_rates.update({'eur': {'usd': eur_to_usd_rate}})
cached_rates.update({'ils': {'eur': ils_to_eur_rate}})

cached_rates['ils']['usd'] = ils_rates_info.get('usd').get('rate')

# cached_rates['usd']['eur'] = usd_rates_info.get('eur')
# cached_rates['eur']['usd'] = eur_rates_info.get('usd')


def enter_currency():
    to_currency_currency_code = input()
    if not to_currency_currency_code:
        exit()
    amount_to_exchange = input()
    return to_currency_currency_code, float(amount_to_exchange)


# def empty_check(from_currency, to_currency, amount):
#     if from_currency is None or to_currency is None or amount is None:
#         print("Your input is empty")
#         sys.exit()
#     else:
#         return True


def get_rate(from_currency, to_currency):
    print('Checking the cache...')
    from_currency_lower = from_currency.lower()
    to_currency_lower = to_currency.lower()
    if from_currency_lower in cached_rates and to_currency_lower in cached_rates.get(from_currency_lower, {}):
        print('Oh! It is in the cache!')
        return cached_rates[from_currency_lower][to_currency_lower]
    else:
        print('Sorry, but it is not in the cache!')
        rate_info = retrieve_new_rates(from_currency_lower, to_currency_lower)
        return rate_info


        # if cached_rates.get(to_currency) is not None:
        #     print('Oh! It is in the cache!')
        #     return cached_rates.get(to_currency_code_lower).get(from_currency_lower).get('inverseRate')
        # else:

def retrieve_new_rates(from_currency_code_retrieve, to_currency_code_retrieve):
    main_url = 'http://www.floatrates.com/daily/'
    url = main_url + from_currency_code_retrieve + '.json'
    new_currency_info = requests.get(url).json()
    new_rate = new_currency_info.get(to_currency_code_retrieve).get('rate')
    if from_currency_code_retrieve in cached_rates:
        cached_rates[from_currency_code_retrieve].update({to_currency_code_retrieve: new_rate})
    else:
        cached_rates.update({from_currency_code_retrieve: {to_currency_code_retrieve: new_rate}})
    return new_rate


def exchange_calc(currency_rate, amount_to_exchange, currency_code):
    exchange_amount = round(amount_to_exchange * currency_rate, 2)
    print('You received ' + str(exchange_amount) + ' ' + str(currency_code.upper()) + '.')


from_currency_code = input()
if not from_currency_code:
    exit()

while True:
    result = enter_currency()
    to_currency_code = result[0]
    amount = result[1]
    if not to_currency_code:
        exit()
    else:
        rate = get_rate(from_currency_code, to_currency_code)
        exchange_calc(rate, amount, to_currency_code)

#
# if empty_check(from_currency_code, to_currency_code, amount_to_exchange) is True:
#     rate = get_rate(from_currency_code_lower, to_currency_code_lower)
#     exchange_calc(rate, amount_to_exchange, to_currency_code)
# else:
#     print("Input error")
