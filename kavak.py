# Imports
import http.client
from bs4 import BeautifulSoup
import requests
import pandas as pd


def obtener_ids():
    '''
    Función que busca los links de las publicaciones de todos los autos usados y nuevos
    '''
    


    
def obtener_datos_auto(ids):
    """
    Función que obtiene todos los datos de un auto
    """
    conn = http.client.HTTPSConnection("api.kavak.com")

    payload = ""

    headers = {
        'Accept': "application/json, text/plain, */*",
        'Accept-Language': "en-US,en;q=0.9,es-ES;q=0.8,es;q=0.7",
        'Connection': "keep-alive",
        'Origin': "https://www.kavak.com",
        'Referer': "https://www.kavak.com/",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-site",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        'kavak-country-acronym': "ar",
        'sec-ch-ua': "^\^Not.A/Brand^^;v=^\^8^^, ^\^Chromium^^;v=^\^114^^, ^\^Google",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "^\^Windows^^"
        }
    
    df = pd.DataFrame(columns=["car_id","car_make","car_year","km","region_id","car_model","price","monthly_payment","car_trim","promotion_price","promotion_name","body_type","transmission","filter_status","ext_color","location_filter","fuel_type","financing_only","status","filter_status_code"])

    for id in ids:
        conn.request("GET", f"/drago-vip/dynamic?stockId={id}", payload, headers)

        res = conn.getresponse()
        data = res.read()

        df_aux = df.from_dict(data.decode("utf-8")["data"]["mainResult"])
        df = pd.concat([df, df_aux])
        
    return df


if __name__=="__main__":
    ids = obtener_ids()
    with open("ids_kavak.txt","w") as f:
        f.write(str(ids))
    df = obtener_datos_auto(ids)
    df.to_excel("kavak_result.xlsx")