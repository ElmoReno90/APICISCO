import json

import controller as controller
import requests
import admpw

sandbox = "https://sandboxapicdc.cisco.com"


def obtener_token(user, passwd):
    url = sandbox + "/api/aaaLogin.json"
    body = {
        "aaaUser": {
            "attributes": {
                "name": user,
                "pwd": passwd
            }
        }
    }
    cabecera = {
        "Content-Type": "application/json"
    }
    requests.packages.urllib3.disable_warnings()
    respuesta = requests.post(url, headers=cabecera, data=json.dumps(body), verify=False)
    token = respuesta.json()['imdata'][0]['aaaLogin']['attributes']['token']
    return token


token = obtener_token(admpw.user, admpw.passwd)


# GET https://apic-ip-address/api/mo/topology/pod-1/node-1/sys/ch/bslot/board/sensor-3.json

def top_system():
    cabecera = {
        "Content-Type": "application/json"
    }
    galleta = {
        "APIC-Cookie": obtener_token(admpw.user, admpw.passwd)
    }

    requests.packages.urllib3.disable_warnings()
    respuesta = requests.get(sandbox + "/api/class/topSystem.json", headers=cabecera, cookies=galleta, verify=False)

    total_nodos = int(respuesta.json()["totalCount"])

    for i in range(0, total_nodos):
        dn_local = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["dn"]
        print(dn_local)

top_system()


# GET http://apic-ip-address/api/mo/topology/pod-1/node-1/sys/ch/bslot/board/sensor-3.json

def sensor3():
    cabecera = {
        "Content-Type": "application/json"
    }
    elmocookie = {
        "APIC-Cookie": obtener_token(admpw.user, admpw.passwd)
    }

    requests.packages.urllib3.disable_warnings()
    respuesta = requests.get(sandbox + "/api/mo/topology/pod-101/node-1/sys/ch/bslot/board/sensor-3.json", headers=cabecera, cookies=elmocookie, verify=False)
    print(respuesta.json())

sensor3()
