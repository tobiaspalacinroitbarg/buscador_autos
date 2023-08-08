#Imports
import bs4
import requests
from bs4 import BeautifulSoup
from aux_funcs import calcular_fecha
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time 

def element_exists(driver:webdriver, by, ref:str, time=3, refresh=True):
    ret = False
    try:    # Check si existen más opciones que las del inicio - hacer click en caso de existir
        ret = WebDriverWait(driver, time).until(EC.presence_of_element_located((by,ref)))
        if refresh == True:
            driver.refresh()
        try:
            ret = WebDriverWait(driver, time).until(EC.presence_of_element_located((by,ref)))
        except :
            pass
    except TimeoutException:
        pass
    return ret


def obtener_descr_carac(url, driver):
    """
    Función que obtiene la descripción y características
    """
    driver.get(url)
    driver.execute_script("window.scrollTo(0, 1000)")
    element_exists(driver, By.XPATH, '//*[@id="highlighted_specs_attrs"]/div[3]/div/span').click()
    descripcion = element_exists(driver, By.XPATH, '//p[@class="ui-pdp-description__content"]').text
    titulos_caracteristicas_raw = driver.find_elements(By.XPATH, '//tr[@class="andes-table__row ui-vpp-striped-specs__row"]')
    titulos_caracteristicas = [caracteristica.get_attribute('innerText').split("\n")[0] for caracteristica in titulos_caracteristicas_raw]
    caracteristicas_raw = driver.find_elements(By.XPATH, '//td[@class="andes-table__column andes-table__column--left ui-vpp-striped-specs__row__column"]')
    caracteristicas = [caracteristica.get_attribute('innerText') for caracteristica in caracteristicas_raw]
    caracteristicas_final = {}
    for index, caracteristica in enumerate(caracteristicas):
        caracteristicas_final[titulos_caracteristicas[index]] = [caracteristica]
    df = pd.DataFrame(caracteristicas_final)
    return descripcion, df

def fotos_auto(soup):
    """
    Función que busca todas las fotos de un auto
    """
    fotos = []
    i:int = 0
    while True:
        try:
            if i==0:
                foto:str = soup.find('img', {'data-index':str(i)})['src']
            else:
                foto:str = soup.find('img', {'data-index':str(i)})['data-src']
            fotos.append(foto)
            i += 1
        except TypeError:
            break
    return fotos

def obtener_ids_meli():
    '''
    Función que busca los links de las publicaciones de todos los autos usados y nuevos en Mercado Libre
    '''
    # Inicializar lista vacía
    ids:list[str] = []
    # Iterar, buscar link y agregar a la lista
    for pagina in range(0,42) :
        url:str  = f'https://autos.mercadolibre.com.ar/autos_Desde_{pagina*49}_NoIndex_True'
        soup = bs4.BeautifulSoup(requests.get(url).text,'lxml')
        links_raw = soup.find_all('a', {'class': 'ui-search-item__group__element shops__items-group-details ui-search-link'}, href=True)
        for link in links_raw :
            id:str = str(link['href'].split("-")[1])
            ids.append(id)
        print(f"fin página {pagina+1}")
    # Return lista final
    with open("ids_meli.txt","w") as f:
        f.write(str(ids))
    return

def obtener_datos_auto(ids, driver):
    """
    Función que obtiene los datos de una oferta
    """
    df_final = pd.DataFrame()
    for id in ids:
        # URL
        url:str = f"https://auto.mercadolibre.com.ar/MLA-{id}"
        # Soup
        soup = bs4.BeautifulSoup(requests.get(url).text,'lxml')
        try:
            # Datos
            precio:str = soup.find('span', {'class':'andes-money-amount__fraction'}).text
            moneda:str = soup.find('span', {'class':'andes-money-amount__currency-symbol'}).text
            fecha = calcular_fecha(soup.find('span', {'class':'ui-pdp-subtitle'}).text.split("·")[-1])
            link_vendedor:str = soup.find('a', {'class': 'ui-vip-profile-info__info-link'}, href=True)['href']
            vendedor:str = soup.find('a', {'class': 'ui-vip-profile-info__info-link'}).text
            ubicacion:str = soup.find_all('p', {'class': 'ui-seller-info__status-info__subtitle'})[-1].text
            fotos = fotos_auto(soup)
            descripcion, df_caracteristicas = obtener_descr_carac(url, driver)
            datos = {"id":[id],"precio":[precio],"moneda": [moneda], "descripcion":[descripcion], "fecha":[fecha], "link_vendedor":[link_vendedor],"vendedor_nombre": [vendedor], "ubicacion_auto":[ubicacion], "links_fotos":[fotos]} 
            df_datos = pd.DataFrame(datos)
            df_auto = pd.concat([df_datos, df_caracteristicas], axis=1)
            df_final = pd.concat([df_final, df_auto])
        except:
            continue
    return df_final


# Al ejecutar...
if __name__=='__main__':
    # Obtener ids
    #obtener_ids_meli()
    # Leer id's
    with open ("./ids_meli.txt","r") as f:
        ids = eval(f.read())
    # Crear driver
    driver = webdriver.Chrome()
    # Obtener datos
    df = obtener_datos_auto(ids, driver)
    # Exportar
    df.to_excel("meli8-8-23.xlsx")
