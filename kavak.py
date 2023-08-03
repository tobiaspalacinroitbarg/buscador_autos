# Imports
import http.client
import requests
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd
import json

def obtener_ids()->list[str]:
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
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        'access-token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbm9ueW1vdXMiOnRydWUsInVzZXJBZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTQuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImlwQWRkcmVzcyI6IjE5MC4xOC42Ni43MyIsInVzZXJJZCI6bnVsbCwidXNlckVtYWlsIjpudWxsLCJ1c2VyVW5pcXVlSWQiOm51bGwsImFsbG93VXNlclN1YnN0aXR1dGlvbiI6ZmFsc2UsImVwb2NoIjoxNjg1OTc0Mzg1MTA5LCJqdGkiOiI1MTRhNGEzNi1mYzg4LTRiZjEtOThkYy02NTI2ZWQ3OGJiNjgiLCJpYXQiOjE2ODU5NzQzODUsImV4cCI6MTY4ODU2NjM4NSwiaXNzIjoia2F2YWsuY29tIn0.iYlccfe0NKjFmtOjPgTC76hA4vgaAr7NZPiB9ylBuoQ",
        'kavak-country-acronym': "ar",
        'refreshToken': "",
        'sec-ch-ua': "^\^Not/A",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "^\^Windows^^"
        }
    ids:list[str] = []
    for pagina in range(0,30):
        conn.request("GET", f"/advanced-search/advanced-search?page={pagina}&loan_limit=true", payload, headers)
        res = conn.getresponse()
        data = res.read()
        for car in json.loads(data.decode("utf-8"))["cars"]:
            ids.append(car["id"])
    with open("ids_kavak.txt","w") as f:
        f.write(str(ids))



    
def obtener_datos_auto(ids:list[str])->pd.DataFrame:
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
    
    df = pd.DataFrame(columns=["n_pagina","car_id","car_make","car_year","km","region_id","car_model","price","monthly_payment","car_trim","promotion_price","promotion_name","body_type","transmission","filter_status","ext_color","location_filter","fuel_type","financing_only","status","filter_status_code"])
    pag = 0
    for iter, id in enumerate(ids):
        conn.request("GET", f"/drago-vip/dynamic?stockId={id}", payload, headers)
        res = conn.getresponse()
        data = res.read() 
        try:
            dicc = json.loads(data.decode("utf-8"))["data"]["mainResult"]
            for key, value in dicc.items():
                dicc[key] = [value]
            df_temp = pd.DataFrame(dicc)
            df_temp["n_pagina"] = pag
            df = pd.concat([df, df_temp])
        except:
            continue
        if iter % 30 == 0:
            pag = round(iter/30)
            print(f"fin página {pag}")

    return df


if __name__=="__main__":
    # Obtener id's
    obtener_ids()
    # Leer id's
    with open ("./ids_kavak.txt","r") as f:
        ids = eval(f.read())
    # Obtener datos de todos los autos
    df = obtener_datos_auto(ids)
    # Exportar
    df.to_excel("kavak_result.xlsx")