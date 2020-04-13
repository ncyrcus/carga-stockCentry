
import requests
import time
import json
import traceback, sys

class Centry:


    def __init__ (self, app_id, secret_key, redirect_uri="urn:ietf:wg:oauth:2.0:oob" ,auth_code="", refresh_token="", access_token="" , scopes= "public+read_orders+write_orders+read_products+write_products+read_integration_config+write_integration_config+read_user+write_user+read_webhook+write_webhook+read_warehouses+write_warehouses" ):
        self.app_id         = app_id
        self.secret_key     = secret_key
        self.auth_code      = auth_code
        self.refresh_token  = refresh_token
        self.access_token   = access_token
        self.scopes         = scopes
        self.redirect_uri   = redirect_uri


    def client_credentials(self ):
        url = "https://www.centry.cl/oauth/token?grant_type=client_credentials&client_id={}&client_secret={}&redirect_uri={}&scope={}".format(self.app_id,self.secret_key,self.redirect_uri,self.scopes)
        headers = {'content-type': 'application/json'}
        r = requests.post(url,  headers=headers)
        
        if(r.status_code==200):
            data = json.loads(r.text)
            self.access_token = str(data['access_token'])
            return True
        return False


    def request(self, endpoint, method, params=None, payload=None):
        if payload is None:
            payload = {}
        if params is None:
            params = {}
        req = None
        uri = "https://www.centry.cl/conexion/v1/{}".format(endpoint)
        header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization' : "Bearer {}".format(self.access_token)
        }
        try:
            if method == 'get':
                req = requests.get(uri, params=params, headers=header)
            elif method == 'post':
                req = requests.post(uri, params=params, headers=header, json=payload)
            elif method == 'put':
                req = requests.put(uri, params=params, headers=header, json=payload)
            elif method == 'delete':
                req = requests.delete(uri, params=params, headers=header)

        except Exception as e:
            print(e)
            print(traceback.format_exc())
        
        return req

    def get(self, endpoint, params=None):
        if params is None:
            params = {}
        return self.request(endpoint, 'get', params)
  
    def post(self, endpoint, params=None, payload=None):
        if payload is None:
            payload = {}
        if params is None:
            params = {}
        return self.request(endpoint, 'post', params, payload)

    def put(self, endpoint, params=None, payload=None):
        if payload is None:
            payload = {}
        if params is None:
            params = {}
        return self.request(endpoint, 'put', params, payload)

    def delete(self, endpoint, params=None):
        if params is None:
            params = {}
        return self.request(endpoint, 'delete', params)

    def get_products(self,params=None):
        return self.get('products.json',params)
    
    def CompanyInfo(self):
        return self.get("company_info.json")
    
    def getVariant(self, id_variant):
        return self.get("variants/{}.json".format(id_variant))

    def updateVariant(self,id_variant,payload):
        return self.put("variants/{}.json".format(id_variant),None,payload)

    def getVariantWarehouseByIdVariant(self,id_variant):
        return self.get("variant_warehouses.json?variant_id={}".format(id_variant))

    def updateVariantWarehouse(self,id_variant_warehouse,payload):
        return self.put("variant_warehouses/{}.json".format(id_variant_warehouse),None,payload)