#Para ejecutar se utiliza> python BilletaraDigital.py  (desde la consola)
#Las cotizaciones se procesan y actualizan al principio de la aplicación para todas las monedas de la lista
import random
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime


def resMoned(nombremone, CantMone, preciomon):  
    print(nombremone.upper())
    print("En este momento usted posee:", CantMone[nombremone], nombremone.upper())
    print("Equivalente a:", str(CantMone[nombremone]*preciomon[nombremone]), "USD")


def is_int(dat):  # Para validar si es dato ingresado es un número
    try:
        int(dat)
        return True
    except:
        print("Error: Tipo de dato inválido")
        return False


def printMat(lis):
    for i in lis:
        for j in i:
            print(j, end='\t\t')
        print('')


def monedasDict():
    opcionMonedas = ["BTC", "ETH", "XRP", "BCH", "LTC", "EOS", "BNB", "XTZ"]
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '7dc3eb05-b9ca-401e-835e-1eaceaef62cf',
    }

    session = Session()
    session.headers.update(headers)
    moneda_dict = {}

    for criptomoneda in opcionMonedas:
        print("Actualizando cotizaciones", criptomoneda)
        parametros = {'symbol': criptomoneda}
        response = session.get(url, params=parametros)
        data = json.loads(response.text)
        precio = (data["data"][criptomoneda]["quote"]["USD"]["price"])
        moneda_dict[criptomoneda] = precio
    print("precio:", moneda_dict)
    return moneda_dict


def main():
    cond = "1"
    #Variables
    # Este es el codigo del usuario en la plataforma
    miCode = random.randint(1000, 5000)
    historial = [['Fecha(D/M/A)', 'Moneda', 'Tipo Op',
                  'Origen', 'Destino', 'Monto(USD)']]
    precio = monedasDict()  # {'BTC': 6854.88282521, 'ETH': 145.254122723}
    defmoneda = {}

    while cond in ['1', '2', '3', '4', '5', '6']:
        print("     *********************  MENÚ PRINCIPAL  ********************")
        print("     #     Ha ingresado con el código: ",
              miCode, "                  #")
        print("     #     Bienvenido a coinmarketcap. Digite una opción       #")
        print("     #     1: Recibir cantidad.                                #")
        print("     #     2: Transaferir monto.                               #")
        print("     #     3: Mostrar balance de una moneda.                   #")
        print("     #     4: Mostrar balance general.                         #")
        print("     #     5: Mostrar histórico de transacciones.              #")
        print("     #     6: Salir del programa.                              #")
        print("     ***********************************************************")
        print("Notas:")
        print("- Las transferencias se realizan en USD")
        print("- Escriba la abreviatura de la moneda")
        print("------------------------------------------------------------------------------------")
        cond = input("").strip()  # Siguiente Menu
        #Variables
        fecha = str(datetime.now().day)+' / ' + \
            str(datetime.now().month)+' / '+str(datetime.now().year)
        h = [0, 0, 0, 0, 0, 0]
        #Menú de Opciones
        if cond == '1':
            print("Recibir Cantidad")
            # Este es el código del usuario que envía el monto
            codeusertransfiere = random.randint(1000, 5000)
            cripto = input(
                "Qué Criptomoneda va a recibir? (BTC, ETH, XRP, BCH, LTC, EOS, BNB, XTZ) ").upper().strip()
            if cripto in precio:
                if codeusertransfiere != miCode:
                    cant = int(input("Qué cantidad va a recibir? "))
                    if cripto in defmoneda:
                        defmoneda[cripto] += cant
                    else:
                        defmoneda[cripto] = cant
                    h = [fecha, cripto.upper(), 'Recibir', str(
                        codeusertransfiere), str(miCode), str(cant*precio[cripto])]
                    historial.append(h)
                    print("Transferencia exitosa de ", cant, cripto)
                    seguir = input("Volver al menú principal? (S/N):").upper()
                    if (seguir == "S"):
                        print()
                    elif (seguir == "N"):
                        exit()
                else:
                    print("ERROR: El código de Origen y Destino no puede ser el mismo.")
            else:
                print("ERROR: La Criptomoneda ", cripto,
                      " no es aceptada en esta plataforma.")
                seguir = input("Volver al menú principal? (S/N):").upper()
                if (seguir == "S"):
                    print()
                elif (seguir == "N"):
                    exit()
        elif cond == '2':
            print("Transferir Monto")
            validadestinat = False
            while not validadestinat:
                codigodestinatario = input("Ingrese el código del destinatario: ")
                validadestinat = is_int(codigodestinatario)  # Verifica que lo ingresado sea un entero
                if (validadestinat and not(1000 <= int(codigodestinatario) <= 5000)):
                    validadestinat = False
                    print("ERROR: El código debe estar entre 1000 y 5000")
                if (validadestinat and (int(codigodestinatario) == miCode)):
                    validadestinat = False
                    print(
                        "ERROR: El código del remitente y del destinatario no puede ser el mismo.")
            cripto = input(
                "Qué Criptomoneda va a enviar? (BTC, ETH, XRP, BCH, LTC, EOS, BNB, XTZ) ").upper().strip()
            if cripto in defmoneda:
                cant = int(input("Qué cantidad va a enviar? "))
                if defmoneda[cripto] >= cant:
                    defmoneda[cripto] -= cant
                    h = [fecha, cripto.upper(), 'Enviar', str(
                        miCode), str(codigodestinatario), str(cant*precio[cripto])]
                    historial.append(h)
                    print("Transferencia exitosa de ", cant, cripto)
                    seguir = input("Volver al menú principal? (S/N):").upper()
                    if (seguir == "S"):
                        print()
                    elif (seguir == "N"):
                        exit()
                else:
                    print("ERROR: Usted no posee suficientes",
                          cripto, "para realizar esta transacción.")
                    seguir = input("Volver al menú principal? (S/N):").upper()
                    if (seguir == "S"):
                        print()
                    elif (seguir == "N"):
                        exit()
            else:
                print("ERROR: Usted no posee", cripto, "suficiantes.")
                seguir = input("Volver al menú principal? (S/N):").upper()
                if (seguir == "S"):
                    print()
                elif (seguir == "N"):
                    exit()
        elif cond == '3':
            print("Mostrar balance de una moneda")
            mon = input(
                "Qué moneda va a consultar? (BTC, ETH, XRP, BCH, LTC, EOS, BNB, XTZ) ").upper().strip()
            if mon in defmoneda:
                resMoned(mon, defmoneda, precio)
                seguir = input("Volver al menú principal? (S/N):").upper()
                if (seguir == "S"):
                    print()
                elif (seguir == "N"):
                    exit()
            else:
                print("ERROR: Usted no posee", mon, "suficientes.")
                seguir = input("Volver al menú principal? (S/N):").upper()
                if (seguir == "S"):
                    print()
                elif (seguir == "N"):
                    exit()
        elif cond == '4':
            print("Mostrar balance general")
            lisC = list(defmoneda.keys())
            for i in lisC:
                resMoned(i, defmoneda, precio)
            seguir = input("Volver al menú principal? (S/N):").upper()
            if (seguir == "S"):
                print()
            elif (seguir == "N"):
                exit()
        elif cond == '5':
            print("Mostrar histórico de transacciones")
            printMat(historial)  # Funcion creada para imprimir matriz
            seguir = input("Volver al menú principal? (S/N):").upper()
            if (seguir == "S"):
                print()
            elif (seguir == "N"):
                exit()
        elif cond == '6':
            cond = '7'  # Para que salga
            print("Hasta la proxima!!!.")
        else:
            cond = '1'  # Para que se repita
            print("Opción inválida, por favor intente nuevamente:")


main()
