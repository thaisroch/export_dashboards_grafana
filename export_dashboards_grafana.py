# Autenticar na API do grafana
# Listar os Dashboard
# Exportar cada dashboard listado


from email import header
from importlib.resources import contents
import os
from pickletools import read_uint1
from urllib import response
import requests
import json

api_key = os.getenv('API_KEY_GRAFANA')
if not api_key:
    print('Variavel de ambiente API_KEY_GRAFANA não encontrada, verifique')

base_url = 'http://172.0.0.1:3000/api'
headers = {
    'Authorization':'Bearer'+ api_key
}



def get_all_dashboards():
    """""
    return: Lista de dashboard com as informações filtredas
    """""

    response =requests.get(url=base_url + '/search', headers=headers)

    #print(response.status_code)
    #print(response.text)
    #print(json.dumps(content,indent=4))

    if response.status_code == 200:
        content = response.json()
        list_dashboards = []
        for dash in content:
            temp_dict = {}
            temp_dict['dash_title']= dash['title']
            temp_dict['dash_uri']= dash['uri']
            list_dashboards.append(temp_dict)
        return list_dashboards
#print(get_all_dashboards())

def prepare_urls():
    """""
    return: Uma lista com as URLS  de cada dashboard 
    """""
    list_url = []
    for dash in get_all_dashboards():
        dash_title = dash ['dash_title']
        dash_uri = dash ['dash_uri']
        url = base_url +'/dashboards' + dash_uri
        list_url.append(url)
    return list_url



for url in prepare_urls():
    reponse = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        dashboard_data = content ['dashboard']
        dashboard_title = dashboard_data['title']
        file_name = dashboard_title + '.json'
        with open(file_name, 'w') as json_file:
            json.dump(dashboard_data, json_file)
            print('Dashboard {} foi exportado com sucesso'.format(dashboard_title))


