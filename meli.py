#Imports
import bs4
import requests
from bs4 import BeautifulSoup
from aux_funcs import calcular_fecha

def intentar_descripcion(url):
    for iter in range(0,3):
        try:
            soup = bs4.BeautifulSoup(requests.get(url).text,'lxml')
            descripcion = soup.find('p', {'class':'ui-pdp-description__content'}).text
            return descripcion
        except AttributeError:
            continue
    return None


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
    return ids

def obtener_datos_auto(ids):
    """
    Función que obtiene los datos de una oferta
    """
    for id in ids:
        # URL
        url:str = f"https://auto.mercadolibre.com.ar/MLA-{id}"
        # Soup
        soup = bs4.BeautifulSoup(requests.get(url).text,'lxml')
        # Datos
        precio:str = soup.find('span', {'class':'andes-money-amount__fraction'}).text
        moneda:str = soup.find('span', {'class':'andes-money-amount__currency-symbol'}).text
        fecha = calcular_fecha(soup.find('span', {'class':'ui-pdp-subtitle'}).text.split("·")[-1])
        descripcion:str = intentar_descripcion(url)
        link_vendedor:str = soup.find('a', {'class': 'ui-vip-profile-info__info-link'}, href=True)['href']
        vendedor:str = soup.find('a', {'class': 'ui-vip-profile-info__info-link'}).text
        ubicacion:str = soup.find_all('p', {'class': 'ui-seller-info__status-info__subtitle'})[-1].text
        fotos = fotos_auto(soup)
        caracteristicas = soup.find('div', {'class':'ui-pdp-collapsable__container'})
        # Print
        print({"precio":precio,"moneda": moneda,"fecha":fecha, "descripcion":descripcion, "link_vendedor":link_vendedor,"vendedor_nombre": vendedor, "ubicacion_auto":ubicacion, "links_fotos":fotos})  
        


# Al ejecutar...
if __name__=='__main__':
    #ids:list[str] = obtener_ids_meli()
    #obtener_datos_auto(ids)
    obtener_datos_auto(["1378559369","1378549243","1378509935","1373263027","1452321150","1454308006","1459701372","1379772407","1434333980","1373685851","1373710437","1373657097","1433454096","1373263027","1432267566"])
