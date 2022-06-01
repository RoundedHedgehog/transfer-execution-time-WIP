from django.shortcuts import render, redirect
from .models import Bank
import datetime

# Create your views here.


def home(response):
    banki = Bank.objects.all()
    data = {
        'banki': banki
    }

    return render(response, 'oblicz/home.html', data)


def godzina(response):
    
    # saves names of banks
    bank1_nazwa = response.POST['bank1']
    bank2_nazwa = response.POST['bank2']

    # takes objects from db
    bank1 = Bank.objects.get(nazwa_banku=bank1_nazwa)
    bank2 = Bank.objects.get(nazwa_banku=bank2_nazwa)

    # saves data of provided banks
    dane = {
        'wyjscia':  {        
            'bank1_wyjscie1': bank1.sesja_wych1,
            'bank1_wyjscie2': bank1.sesja_wych2,
            'bank1_wyjscie3': bank1.sesja_wych3,
                    },

        'wejscia': {
            'bank2_wejscie1': bank2.sesja_przych1,
            'bank2_wejscie2': bank2.sesja_przych2,
            'bank2_wejscie3': bank2.sesja_przych3,
                    },

        'data': response.POST['data']
    }
    
    # little tweaks of string cause I want to use it as datetime module

    data_obiekt = change_to_datetime(dane)

    kiedy_dotrze = oblicz_kiedy_dotrze(data_obiekt, dane)
    

    return render(response, 'oblicz/home.html')



def change_to_datetime(dane):
    data = dane['data'].split('T')[0]
    godzina = dane['data'].split('T')[1]

    hours = int(godzina.split(':')[0])
    minutes = int(godzina.split(':')[1])

    rok = int(data.split('-')[0])
    miesiac = int(data.split('-')[1])
    dzien = int(data.split('-')[2])

    data_obiekt = datetime.datetime(rok, miesiac, dzien, hours, minutes)
    
    return data_obiekt

def oblicz_kiedy_dotrze(data_obiekt, dane):

    godzina = data_obiekt.time()
    dzien = data_obiekt.weekday()
    godzina_wyjscia = None

    # check hour of transfer FROM bank
    for mozliwa_godzina_wyjscia in dane['wyjscia'].values():
        if godzina < mozliwa_godzina_wyjscia:
            godzina_wyjscia = mozliwa_godzina_wyjscia
            break
    
    # if transfer was made too late, he will be send next day ASAP
    if godzina_wyjscia == None:
        dzien += 1
        godzina_wyjscia = dane['wyjscia']['bank1_wyjscie1']

    # if transfer would be send during weekend, day is changed to manday
    if dzien > 4:
        dzien = 0

    for mozliwa_godzina_dotarcia in dane['wejscia'].values():
        if godzina_wyjscia < mozliwa_godzina_dotarcia:
            godzina_dotarcia = mozliwa_godzina_dotarcia
            break
    

    print(godzina_dotarcia)


    
    pass

