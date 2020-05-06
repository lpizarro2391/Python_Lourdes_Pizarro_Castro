import requests


def esmoneda(cripto):
    return cripto in monedas


monedas = ()
monedas_dict = {}

COINMARKET_API_KEY = "7dc3eb05-b9ca-401e-835e-1eaceaef62cf"
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '7dc3eb05-b9ca-401e-835e-1eaceaef62cf'
}
data = requests.get(
    "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest", headers=headers).json()
for id in data["data"]:
   monedas_dict[id["symbol"]] = id["quote"]["USD"]["price"]

monedas = monedas_dict.keys()

moneda = input("Indique el nombre de la moneda a obtener el precio")
while not esmoneda(moneda):
    print("Moneda Inválida")
    moneda = input("Ingrese el nombre de la moneda")

else:
    print("La moneda con symbol:", moneda,
          "tiene un precio de : ", monedas_dict.get(moneda), "USD")
