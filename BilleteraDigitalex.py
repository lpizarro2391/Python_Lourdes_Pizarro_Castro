#Para ejecutar se utiliza> python BilletaraDigital.py  (desde la consola)
#Las cotizaciones se procesan y actualizan al principio de la aplicación para todas las monedas de la lista
import random
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime
def mosMon(mon,dMio,dPrecio):#para imprimir lo que se debe mostrar de las monedas
    print(mon.upper())
    print("En este momento usted posee:",dMio[mon],mon.upper())
    print("Equivalente a:",str(dMio[mon]*dPrecio[mon]),"USD")

def is_int(dat): #Para validar si es dato ingresado es un número
    try:
        int(dat)
        return True
    except:
        print("Error: Tipo de dato inválido")
        return False

def printMat(lis):
    for i in lis:
        for j in i:
            print(j,end='\t\t')
        print('')

def creaDictP():
    opcionMonedas=["BTC", "ETH", "XRP", "BCH", "LTC", "EOS", "BNB", "XTZ"]
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'd10af3bd-3f7f-49ae-a62a-e682eae09ad0',
    }

    session = Session()
    session.headers.update(headers)
    moneda_dict = {}

    for crip in opcionMonedas:
        print("Actualizando cotizaciones",crip)
        parametros = {'symbol': crip}
        response = session.get(url, params=parametros)
        data = json.loads(response.text)
        precio = (data["data"][crip]["quote"]["USD"]["price"])
        moneda_dict[crip] = precio
    print("precio:",moneda_dict)
    return moneda_dict

def main():
    cond = "1"
    #Variables
    miCode = random.randint(1000,5000) #Este es el codigo del usuario en la plataforma
    historial = [['Fecha(D/M/A)','Moneda','Tipo Op','Origen','Destino','Monto(USD)']]
    dPrecio = creaDictP() #{'BTC': 6854.88282521, 'ETH': 145.254122723}
    dMio = {}

    while cond in ['1','2','3','4','5','6']:
        print("     *********************  MENÚ PRINCIPAL  ********************")
        print("     #     Ha ingresado con el código: ",miCode,"                  #")
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
        cond = input("").strip()#Siguiente Menu
        #Variables 
        fecha = str(datetime.now().day)+' / '+str(datetime.now().month)+' / '+str(datetime.now().year)
        h = [0,0,0,0,0,0]
        #Menú de Opciones      
        if cond == '1':
            print("Recibir Cantidad")
            cRem = random.randint(1000,5000) #Este es el código del usuario que envía el monto
            crip = input("Qué Criptomoneda va a recibir? (BTC, ETH, XRP, BCH, LTC, EOS, BNB, XTZ) ").upper().strip()
            if crip in dPrecio:
                if cRem != miCode:
                    cant = int(input("Qué cantidad va a recibir? "))
                    if crip in dMio:
                        dMio[crip]+=cant
                    else:
                        dMio[crip]=cant
                    h=[fecha,crip.upper(),'Recibir',str(cRem),str(miCode),str(cant*dPrecio[crip])]
                    historial.append(h)
                    print("Transferencia exitosa de ",cant, crip)
                    seguir = input("Volver al menú principal? (S/N):").upper()
                    if (seguir=="S"):
                        print()
                    elif (seguir=="N"):
                        exit()
                else:
                    print("ERROR: El código de Origen y Destino no puede ser el mismo.")
            else:
                print("ERROR: La Criptomoneda ", crip, " no es aceptada en esta plataforma.")
                seguir = input("Volver al menú principal? (S/N):").upper()
                if (seguir=="S"):
                    print()
                elif (seguir=="N"):
                    exit()
        elif cond == '2':
            print("Transferir Monto")
            varC = False
            while not varC:
                cDes = input("Ingrese el código del destinatario: ")
                varC = is_int(cDes) #Verifica que lo ingresado sea un entero
                if (varC and not(1000<=int(cDes)<=5000)):
                    varC = False
                    print("ERROR: El código debe estar entre 1000 y 5000")
                if (varC and (int(cDes)==miCode)):
                    varC = False
                    print("ERROR: El código del remitente y del destinatario no puede ser el mismo.")
            crip = input("Qué Criptomoneda va a enviar? (BTC, ETH, XRP, BCH, LTC, EOS, BNB, XTZ) ").upper().strip()
            if crip in dMio:
                cant = int(input("Qué cantidad va a enviar? "))
                if dMio[crip] >= cant:
                    dMio[crip] -= cant
                    h=[fecha,crip.upper(),'Enviar',str(miCode),str(cDes),str(cant*dPrecio[crip])]
                    historial.append(h)
                    print("Transferencia exitosa de ",cant, crip)
                    seguir = input("Volver al menú principal? (S/N):").upper()
                    if (seguir=="S"):
                        print()
                    elif (seguir=="N"):
                        exit()
                else:
                    print("ERROR: Usted no posee suficientes",crip,"para realizar esta transacción.")
                    seguir = input("Volver al menú principal? (S/N):").upper()
                    if (seguir=="S"):
                        print()
                    elif (seguir=="N"):
                        exit()
            else:
                print("ERROR: Usted no posee",crip,"suficiantes.")
                seguir = input("Volver al menú principal? (S/N):").upper()
                if (seguir=="S"):
                    print()
                elif (seguir=="N"):
                    exit()
        elif cond == '3':
            print("Mostrar balance de una moneda")
            mon = input("Qué moneda va a consultar? (BTC, ETH, XRP, BCH, LTC, EOS, BNB, XTZ) ").upper().strip()
            if mon in dMio:
                mosMon(mon,dMio,dPrecio)
                seguir = input("Volver al menú principal? (S/N):").upper()
                if (seguir=="S"):
                    print()
                elif (seguir=="N"):
                    exit()
            else:
                print("ERROR: Usted no posee",mon,"suficientes.")
                seguir = input("Volver al menú principal? (S/N):").upper()
                if (seguir=="S"):
                    print()
                elif (seguir=="N"):
                    exit()
        elif cond == '4':
            print("Mostrar balance general")
            lisC = list(dMio.keys())
            for i in lisC:
                mosMon(i,dMio,dPrecio)
            seguir = input("Volver al menú principal? (S/N):").upper()
            if (seguir=="S"):
                print()
            elif (seguir=="N"):
                exit() 
        elif cond == '5':
            print("Mostrar histórico de transacciones")
            printMat(historial)#Funcion creada para imprimir matriz
            seguir = input("Volver al menú principal? (S/N):").upper()
            if (seguir=="S"):
                print()
            elif (seguir=="N"):
                exit()
        elif cond == '6':
            cond = '7' #Para que salga
            print("Hasta la proxima!!!.")
        else:
            cond = '1' #Para que se repita
            print("Opción inválida, por favor intente nuevamente:")
main()
