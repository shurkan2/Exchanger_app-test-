from django.shortcuts import render
import requests

def exchange(request):
    print(request.method)
    currencies = {}
    #''' Не работал на GET запросы!!'''

    context = {}
    response = requests.get(url="https://v6.exchangerate-api.com/v6/0f4f6bd40a93f62532b34f0c/latest/USD").json()
    currencies = response.get('conversion_rates', {})

    if request.method == 'GET':
        if currencies:
            context = {
                'currencies': currencies
            }

        return render(request=request, template_name='exchange_app/index.html', context=context)

    if request.method == 'POST':
        #Своя логика
        return render(request=request, template_name='exchange_app/index.html', context=context)
        from_amount = request.POST.get('from_amount')
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')
        try:
            converted_amount = round(currencies[to_curr]/currencies[from_curr] * float(from_amount), 2)
            context['converted_amount'] = converted_amount
        except KeyError:
            print(fr'Не,нихуч')
        finally:
            context = {
                'from_amount': from_amount,
                'from_curr': from_curr,
                'to_curr': to_curr,
                'currencies': currencies
            }
        return render(request=request, template_name='exchange_app/index.html', context=context)
        pass

