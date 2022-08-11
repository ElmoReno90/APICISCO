import json

import controller as controller
import requests
import admpw

sandbox = "https://sandboxapicdc.cisco.com"


def obtener_token(user, passwd): ##Se realiza una definicion aparte para "Obtener el Token"
    url = sandbox + "/api/aaaLogin.json" ##Se realiza el llamado al metodo expuesto como Sandbox y se le agrega el link necesario para consumir API y acceder a las crendicales.
    body = {
        "aaaUser": {
            "attributes": {
                "name": user, ##hace un match entre los recursos necesarios del API con el user de autenticacion.
                "pwd": passwd ##hace un match entre los recursos necesarios del API con el passwd de autenticacion.
            }
        }
    }
    cabecera = {
        "Content-Type": "application/json"
    }
    requests.packages.urllib3.disable_warnings()
    respuesta = requests.post(url, headers=cabecera, data=json.dumps(body), verify=False) ##estructura general del consumo de la API segun el requerimiento del Token
    token = respuesta.json()['imdata'][0]['aaaLogin']['attributes']['token'] ##ruta especifica para obtener el token necesario para consumir API.
    return token


token = obtener_token(admpw.user, admpw.passwd) ##Se realiza metodo por medio de la palabra Token, por lo que es necesario llamar a user y paswd insertos en archivo admpw.py


# GET https://apic-ip-address/api/mo/topology/pod-1/node-1/sys/ch/bslot/board/sensor-3.json

def top_system():
    cabecera = {
        "Content-Type": "application/json"
    }
    galletita = {
        "APIC-Cookie": obtener_token(admpw.user, admpw.passwd)
    }

    requests.packages.urllib3.disable_warnings()
    respuesta = requests.get(sandbox + "/api/class/topSystem.json", headers=cabecera, cookies=galletita, verify=False)

    total_nodos = int(respuesta.json()["totalCount"])

    for i in range(0, total_nodos):
        dn_local = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["dn"]
        print(dn_local)

#top_system()


# GET http://apic-ip-address/api/mo/topology/pod-1/node-1/sys/ch/bslot/board/sensor-3.json

def sensor3():
    cabecera = {
        "Content-Type": "application/json"
    }
    elmocookie = {
        "APIC-Cookie": obtener_token(admpw.user, admpw.passwd)
    }

    requests.packages.urllib3.disable_warnings()
    respuesta_sensor = requests.get(sandbox + "/api/mo/topology/pod-1/node-101/sys/ch/bslot/board/sensor-3.json", headers=cabecera, cookies=elmocookie, verify=False)
    print(respuesta_sensor.json())

#sensor3()

#GET http://apic-ip-address/api/class/firmware:CtrlrFwStatusCont.json?query-target=subtree&target-subtree-class=firmwareCtrlrRunning

def firmware():
    cabecera = {
        "Content-Type": "application/json"
    }
    elmocookie = {
        "APIC-Cookie": obtener_token(admpw.user, admpw.passwd)
    }

    requests.packages.urllib3.disable_warnings()
    respuesta_firmware = requests.get(sandbox + "/api/class/firmwareCtrlrFwStatusCont.json?query-target=subtree&target-subtree-class=firmwareCtrlrRunning", headers=cabecera, cookies=elmocookie, verify=False)
    print(respuesta_firmware.json())

firmware()