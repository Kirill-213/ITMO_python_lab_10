# Выполнил: Васильев К.И R3135
# Поток:
# Вариант:

# подключение библиотек
import requests
from bs4 import BeautifulSoup as BS
import speech_recognition as sr

# ссылка на сайт с курсом валют
url = 'https://upd2xml.ru/valuta/?ysclid=lhzzi3wq6q301325803'
# название создаваемого txt файла
txt_file_name = 'price_data.txt'


# функция обработки речи
def audio_processing():

    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        print('Назови интересующую валюту:\n')
        audio = r.listen(source)

    text = r.recognize_google(audio, language='ru-RU')
    return text.lower()


# функция получения данных о котировках с сайта в виде txt файла
def parse_currency(website_url):

    r = requests.get(website_url)
    soup = BS(r.text, 'lxml')
    price = (soup.find("table", {"class": "table table-hover table-sm"})).get_text()

    # открываем файл и записываем значение котировок
    f = open(txt_file_name, 'r+')
    f.write(price)
    f.close()


# функция обработки txt файла
def txt_proccesing(filename, currency_name):

    # открываем файл с котировками
    f = open(filename, 'r+')
    # чтение файла и закрытие файла
    line = f.readlines()
    f.close()
    mass = []

    # преобразование строки
    for i in range(len(line)):
        mass.append(line[i].replace('\n', '').lower())

    if currency_name in mass:
        # получение индекса в списке нужной валютной пары
        index = mass.index(currency_name)
        # вывод стоимости 1 ед валюты к стоимости к рублю
        print('Цена:', mass[index], '=', float(mass[index + 2]) / float(mass[index + 1]), 'rub')


# главная функция
def main():
    parse_currency(url)
    txt_proccesing(txt_file_name, audio_processing())



if __name__ == '__main__':
    main()