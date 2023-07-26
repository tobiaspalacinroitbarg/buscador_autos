#Imports
import bs4
import requests
from bs4 import BeautifulSoup

def obtener_links_meli():
    '''
    Función que busca los links de las publicaciones de todos los autos usados y nuevos en Mercado Libre
    '''
    # Inicializar lista vacía
    links:list[str] = []

    # Iterar, buscar link y agregar a la lista
    for pagina in range(0,42) :
        url = f'https://autos.mercadolibre.com.ar/autos_Desde_{pagina*49}_NoIndex_True'
        soup = bs4.BeautifulSoup(requests.get(url).text,'lxml')
        links_raw = soup.find_all('a', {'class': 'ui-search-item__group__element shops__items-group-details ui-search-link'}, href=True)
        for link in links_raw :
            links.append(link['href'])
        print(f"fin página {pagina+1}")

    # Exportar lista final a .txt
    with open('links.txt', 'w') as f:
        f.write(str(links))
