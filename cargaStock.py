#!/usr/bin/env python
# -*- coding: utf-8 -*- 


# from __future__ import unicode_literals
# import xlsxwriter
import requests
from CentrySDK import Centry
import json
from time import sleep
import concurrent.futures
import threading
import traceback, sys



def updateStockBySku(data, attemps = 0):
    getVWid= conexion.getVariantWarehouseByIdVariant(data["id_variante_centry"])
    getVWid = json.loads(getVWid.text)
    if( len(getVWid) == 1 ):
        getVWid = getVWid[0]
        id_variant_warehouse = getVWid['_id']
    else:
        Resultados[data["id_variante_centry"]] = "No actualizado, Especifique Bodega"
        return False
    if attemps < 3 : 
        payload = {
            "quantity" : data["stock"]
        }
        if(int (getVWid['quantity'])  ==  int(data["stock"] )):
            Resultados[data["id_variante_centry"]] = "Sin Cambios"
            return True
        update= conexion.updateVariantWarehouse(id_variant_warehouse,payload)

        if (update.status_code == 200 ): 
            Resultados[data["id_variante_centry"]] = "Exitoso" if json.loads(update.text)["quantity"] == data["stock"] else "Fallo"
            return json.loads(update.text)["quantity"] == data["stock"]
        else :
            sleep(2)
            attemps+=1
            updateStockBySku(data, attemps)
    else : 
        return False


with open('configs.json') as data:
    companies = json.load(data)
    counter=0
    for company in companies:
        print("Compañia {} sincronizando stock".format(counter))
        counter+=1
        app_id          = company["app_id"]
        secret_id       = company["secret_id"]
        redirect_uri    = company["redirect_uri"]
        url_data        = company["url_data"]
        Resultados      = {}

        conexion =  Centry(app_id , secret_id ,redirect_uri)

        if (conexion.client_credentials()) :
            Company_name = json.loads(  conexion.CompanyInfo().text)['name']
            print( "Conectado a : "+ Company_name  )

            response = requests.request("GET", url_data)
            if( response.status_code == 200):
                productList = json.loads(response.text)

            MAX_THREADS = 20

            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                executor.map(updateStockBySku, productList.values())

            print("Resumen de Ejecución:")
            print("Variantes Afectadas      : {}".format(     str(list(Resultados.values()).count("Exitoso"))       ))
            print("Variantes sin cambios    : {}".format(     str(list(Resultados.values()).count("Sin Cambios"))   ))
            print("Variantes Que Fallaron   : {}".format(     str(list(Resultados.values()).count("Fallo"))         ))
            with open('log/resultados_{}.json'.format(Company_name),'w') as outfile:
                json.dump(Resultados,outfile)
        else:
            print("No se pudo establecer conexión con Centry.cl")





    
    
   



