# Imports
import http.client


def obtener_datos_auto():
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

    conn.request("GET", "/drago-vip/dynamic?stockId=248528", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))