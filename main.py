import requests
all_countries = []
countries = {
    'ОАЭ': 'https://postimg.cc/N9WbnQZL',
    'Андорра': 'https://postimg.cc/VdFBq9sJ',
    'Афганистан': 'https://postimg.cc/MfmRYxSC',
    'Албания': 'https://postimg.cc/zV9bRVKy',
    'Армения': 'https://postimg.cc/mt4KZS6k',
    'Аргентина': 'https://postimg.cc/sQy0fjw8',
    'Австрия': 'https://postimg.cc/nsVDnNq2',
    'Австралия': 'https://postimg.cc/4mz7VX5w',
    'Азербайджан': 'https://postimg.cc/wyy3vzMX',
    'Барбадос': 'https://postimg.cc/9DLfY0qP',
    'Бельгия': 'https://postimg.cc/t1LpBxR6',
    'Бахрейн': 'https://postimg.cc/Sjbgcfbh',
    'Бразилия': 'https://postimg.cc/bszLBYvV',
    'Беларусь': 'https://postimg.cc/njbGYp5k',
    'Канада': 'https://postimg.cc/ppTzjmrv',
    'Республика Конго': 'https://postimg.cc/2q5sRF8J',
    'Швейцария': 'https://postimg.cc/9rpgmRSj',
    'Чили': 'https://postimg.cc/bdjjdn6G',
    'Камерун': 'https://postimg.cc/94MQ893X',
    'Китай': 'https://postimg.cc/PNtT2Z1g',
    'Колумбия': 'https://postimg.cc/bs75FcKZ',
    'Коста-Рика': 'https://postimg.cc/JstWrXbH',
    'Куба': 'https://postimg.cc/WF5n1dmt',
    'Кипр': 'https://postimg.cc/dh9TYzjV',
    'Чехия': 'https://postimg.cc/vxMsbSzG',
    'Германия': 'https://postimg.cc/nXscdgSW',
    'Дания': 'https://postimg.cc/JGFB4b99',
    'Алжир': 'https://postimg.cc/FYtsBDts',
    'Эквадор': 'https://postimg.cc/HJhN6vK6',
    'Эстония': 'https://postimg.cc/5XZ7vQFr',
    'Египет': 'https://postimg.cc/G8ZmnQBQ',
    'Испания': 'https://postimg.cc/Z0HJc4HH',
    'Эфиопия': 'https://postimg.cc/WqqLTcRF',
    'Финляндия': 'https://postimg.cc/mP8dXpq0',
    'Фиджи': 'https://postimg.cc/GB66KSTb',
    'Франция': 'https://postimg.cc/qgNx4MFD',
    'Англия': 'https://postimg.cc/4H4y510N',
    'Шотландия': 'https://postimg.cc/JGcKt7NN',
    'Уэльс': 'https://postimg.cc/sMCXHyqN',
    'Грузия': 'https://postimg.cc/GTPNcF3Y',
    'Гибралтар': 'https://postimg.cc/2L3wtnbr',
    'Греция': 'https://postimg.cc/3dqKzh6T',
    'Гватемала': 'https://postimg.cc/kR8c9qcp',
    'Гонконг': 'https://postimg.cc/RJRWwYV0',
    'Гондурас': 'https://postimg.cc/bGxSzdcb',
    'Хорватия': 'https://postimg.cc/z3FmnN5j',
    'Гаити': 'https://postimg.cc/m1DSz7BK',
    'Индонезия': 'https://postimg.cc/ZB1MSfrV',
    'Ирландия': 'https://postimg.cc/LnmV1K6j',
    'Израиль': 'https://postimg.cc/dD3CPs1H',
    'Индия': 'https://postimg.cc/CZJ47cPz',
    'Ирак': 'https://postimg.cc/kBxpr3fH',
    'Иран': 'https://postimg.cc/VSjqvmby',
    'Исландия': 'https://postimg.cc/5Yy2GmJP',
    'Италия': 'https://postimg.cc/NyfXsmYX',
    'Ямайка': 'https://postimg.cc/vDL3ZLwq',
    'Иордан': 'https://postimg.cc/CZxVcLHY',
    'Япония': 'https://postimg.cc/JDdJsnKh',
    'Кения': 'https://postimg.cc/rDQpVHfV',
    'Кыргызстан': 'https://postimg.cc/hf4jkg0y',
    'КНДР': 'https://postimg.cc/CRVvhPzQ',
    'Республика Корея': 'https://postimg.cc/BLxb0nyy',
    'Либерия': 'https://postimg.cc/fkyWC5Wp',
    'Латвия': 'https://postimg.cc/7fT2sqPF',
    'Марокко': 'https://postimg.cc/Zv6JNsZM',
    'Монако': 'https://postimg.cc/DmhfkFgV',
    'Молдавия': 'https://postimg.cc/xcWFhjvM',
    'Македония': 'https://postimg.cc/xcyzDtH5',
    'Монголия': 'https://postimg.cc/q6BNxCMr',
    'Мьянма': 'https://postimg.cc/0MBTcT9N',
    'Мальта': 'https://postimg.cc/sQQ6DvRV',
    'Мексика': 'https://postimg.cc/QVNgbFzV',
    'Малазия': 'https://postimg.cc/hXV7gnYH',
    'Мозамбик': 'https://postimg.cc/GB5R58Qr',
    'Нигер': 'https://postimg.cc/Hj4YpxW0',
    'Нигерия': 'https://postimg.cc/hXm3BJcc',
    'Никарагуа': 'https://postimg.cc/kBbyVkZy',
    'Нидерланды': 'https://postimg.cc/9DcqWKj0',
    'Норвегия': 'https://postimg.cc/2VD1wMyG',
    'Панама': 'https://postimg.cc/gxMrG0Dt',
    'Перу': 'https://postimg.cc/s1pXvmmh',
    'Оман': 'https://postimg.cc/N5drjbGx',
    'Филиппины': 'https://postimg.cc/478T9KYj',
    'Пакистан': 'https://postimg.cc/mPxWCWrZ',
    'Польша': 'https://postimg.cc/fS31S8n0',
    'Пуэрто-Рико': 'https://postimg.cc/gL6B2r8V',
    'Португалия': 'https://postimg.cc/HVdQxVwT',
    'Парагвай': 'https://postimg.cc/vxM6cN60',
    'Катар': 'https://postimg.cc/phQJG8f1',
    'Румыния': 'https://postimg.cc/XGg9cWWR',
    'Сербия': 'https://postimg.cc/0rsszsb8',
    'Россия': 'https://postimg.cc/CBC9GRzw',
    'Саудовская Аравия': 'https://postimg.cc/MXWLkKnj',
    'Соломонские острова': 'https://postimg.cc/bDL3YkZS',
    'Судан': 'https://postimg.cc/N9GknFds',
    'Сингапур': 'https://postimg.cc/c6HcMKKT',
    'Словения': 'https://postimg.cc/hfQb6H1d',
    'Словакия': 'https://postimg.cc/v4L9dMgc',
    'Сан-Марино': 'https://postimg.cc/LhY18jgd',
    'Сомали': 'https://postimg.cc/sv5GpyJw',
    'Сирия': 'https://postimg.cc/0M6brqQG',
    'Таиланд': 'https://postimg.cc/kBND2snH',
    'Таджикистан': 'https://postimg.cc/zHCDRD1h',
    'Туркменистан': 'https://postimg.cc/sGrsyFZg',
    'Тунис': 'https://postimg.cc/N2BqS1Wy',
    'Турция': 'https://postimg.cc/9RJH34VJ',
    'Тайвань': 'https://postimg.cc/xq1SvPy7',
    'Украина': 'https://postimg.cc/G4G5vBB9',
    'Уганда': 'https://postimg.cc/Bjbv60th',
    'США': 'https://postimg.cc/1fqPXrQq',
    'Уругвай': 'https://postimg.cc/w7v2Qwv1',
    'Узбекистан': 'https://postimg.cc/tYNbFCsq',
    'Венесуэла': 'https://postimg.cc/8F0fDbG0',
    'Вьетнам': 'https://postimg.cc/MXjPCPwg',
    'Йемен': 'https://postimg.cc/w10Y1f70',
    'ЮАР': 'https://postimg.cc/0zpdnFp0',
    'Зимбабве': 'https://postimg.cc/DW6Nj8q6',
}
if __name__ == '__main__':
    for title, image in countries.items():
        r = requests.post('https://flags-server.onrender.com/add-country/', json={'title': title, 'image': image})
        print(title, r)
    print(all_countries)