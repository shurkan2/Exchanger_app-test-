from django.shortcuts import render, redirect
import requests
from django.core.paginator import Paginator

API_URL = "https://v6.exchangerate-api.com/v6/0f4f6bd40a93f62532b34f0c/latest/USD"
API_URL2 = "https://restcountries.com/v3.1/all?fields=name,flags,currencies"

def exchange_get(request):

    response = requests.get(API_URL).json()
    currencies = response.get('conversion_rates')

    context = {
        'currencies': currencies
    }

    return render(request=request, template_name='exchange_app/index.html', context=context)

def exchange_post(request):
    if request.method == 'POST':
        response = requests.get(API_URL).json()
        currencies = response.get('conversion_rates')

        from_amount = float(request.POST.get('from-amount'))
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')

        converted_amount = round((currencies[to_curr] / currencies[from_curr]) * from_amount, 2)

        context = {
            'from_curr': from_curr,
            'to_curr': to_curr,
            'from_amount': from_amount,
            'converted_amount': converted_amount,
            'currencies': currencies
        }

        return render(request=request, template_name='exchange_app/index.html', context=context)


    return redirect('exchange_get')

def parce_countries(countries, currencies) -> list:
    parsed_countries = []

    for country in countries:
        official_name = country['name']['official']

        flag_url = country['flags']['png']

        currency_code = ''
        for e in list(country['currencies'].keys()):
            currency_code = e
            break
        if currencies.get(currency_code, 0) == 0:
            print(f'{official_name} is Not OK')
            continue

        currency_symbol = country['currencies'][currency_code]['symbol']

        parsed_country = {
            'name': official_name,
            'flags': flag_url,
            'currencies': currency_code,
            'symbol': currency_symbol,
            'rate': currencies[currency_code]
        }
        parsed_countries.append(parsed_country)

    return parsed_countries

def courses_table(request):
    response = requests.get(API_URL).json()
    currencies = response.get('conversion_rates')

    countries = parce_countries(countries = requests.get(API_URL2).json(), currencies=currencies)

    print(f"{countries=}")

    items_per_page = int(request.GET.get('items_per_page', 10))
    sorted_currencies = sorted(countries, key=lambda x: x['name'])

    paginator = Paginator(sorted_currencies, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'countries': page_obj,
        'items_per_page': items_per_page
    }

    return render(request, 'exchange_app/courses_table.html', context)