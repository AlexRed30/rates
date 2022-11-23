from operator import itemgetter
import requests
import json
import io

from datetime import datetime

payload ={
        "proMerchantAds":False,
        "page":1,
        "rows":20,
        "payTypes":["Banesco"],
        "countries":[],
        "publisherType":None,
        "tradeType":"SELL",
        "asset":"USDT",
        "fiat":"VES",
        "authority": "p2p.binance.com",
        'path': "/bapi/c2c/v2/friendly/c2c/adv/search"
}
headers ={"X-Reserve-Client": "reserve-marketplace","Content-Type": "application/json"}
url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

response = requests.post(url,headers=headers,json=payload)

datos = response.json()
#print(datos)
verified = []

for data in datos["data"]:
        if data["advertiser"]["userGrade"] == 3:
                verified.append(data)

suma=0
binanceUsers = []
only_verified = False


for x in range(0,3):
    if len(verified) >= 3:
        suma = suma+float(verified[x]["adv"]["price"])
        binanceUsers.append(""+verified[x]["advertiser"]["nickName"]+"["+verified[x]["adv"]["price"]+"]")
        only_verified = True
    else:
        suma = suma+float(data[x]["adv"]["price"])
        binanceUsers.append(""+data[x]["advertiser"]["nickName"]+"["+data[x]["adv"]["price"]+"]")

if only_verified == True:
        binanceUsers.append("Verificados")
else:
        binanceUsers.append("No Verificados")


now = datetime.now()  
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

print('-'.join(binanceUsers))
print("date and time:",date_time)	

rate = suma/3
rateFormated = "{:.2f}".format(suma/3)
spreadBUY = "{:.2f}".format(rate+rate*0.003)
spreadSELL = "{:.2f}".format(rate-rate*0.002)


print(f"Rate:{rateFormated} spreadBUY:{spreadBUY} spreadSELL:{spreadSELL}")

 
with io.open("VESrates.txt", mode='a', encoding='utf-8') as f:
    f.write(f"{'-'.join(binanceUsers)} => Rate:{rateFormated} spreadBUY:{spreadBUY} spreadSELL:{spreadSELL} => {date_time}\n")
