from django.shortcuts import render, redirect
import requests


def exchange_get(request):

    response = requests.get("https://v6.exchangerate-api.com/v6/0f4f6bd40a93f62532b34f0c/latest/USD").json()
    currencies = response.get('conversion_rates')

    context = {
        'currencies': currencies
    }

    return render(request=request, template_name='exchange_app/index.html', context=context)

def exchange_post(request):
    if request.method == 'POST':
        response = requests.get("https://v6.exchangerate-api.com/v6/0f4f6bd40a93f62532b34f0c/latest/USD").json()
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
