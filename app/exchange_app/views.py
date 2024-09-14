from django.shortcuts import render
import requests


def exchange(request):

    response = requests.get("https://v6.exchangerate-api.com/v6/0f4f6bd40a93f62532b34f0c/latest/USD").json()
    currencies = response.get('conversion_rates')

    if request.method == 'GET':
        context = {
            'currencies': currencies
        }


    if request.method == 'POST':
        from_amount = request.POST.get('from-amount')
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')

        if from_amount and from_curr and to_curr:
            try:
                from_amount = float(from_amount)

                converted_amount = round((currencies[to_curr] / currencies[from_curr]) * from_amount, 2)

                context = {
                    'from_curr': from_curr,
                    'to_curr': to_curr,
                    'from_amount': from_amount,
                    'converted_amount': converted_amount,
                    'currencies': currencies
                }

            except ValueError:
                context = {'error': "Некорректное значение суммы."}
        else:
            context = {'error' : "Пожалуйста, заполните все поля."}

    return render(request=request, template_name='exchange_app/index.html', context=context)
