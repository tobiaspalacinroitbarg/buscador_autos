import scrapy
from gc import callbacks
from ..func_aux import calcular_fecha

class BooksSpider(scrapy.Spider):
    name = 'meli_spider'
    allowed_domains = ['autos.mercadolibre.com.ar', 'auto.mercadolibre.com.ar']
    start_urls = ['https://autos.mercadolibre.com.ar/autos-usados_ITEM*CONDITION_2230581_NoIndex_True']

    def parse(self, response):
        autos = response.css('div.ui-search-result__wrapper')
        
        for auto in autos :
            url_auto = auto.css('a.ui-search-item__group__element').attrib['href']
            yield response.follow(url_auto, callback=self.parse_publicacion_auto)
        
        next_page_url = response.css('li.andes-pagination__button--next a').attrib['href']

        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_publicacion_auto(self, response):
        subtitulo = response.css('span.ui-pdp-subtitle::text').get()
        yield {
            'titulo': response.css('h1.ui-pdp-title::text').get(),
            'fecha_publicacion' : calcular_fecha(subtitulo.split("·")[-1]),
            'año_auto': subtitulo.split()[0],
            'km_recorridos': subtitulo.split()[2],
            'precio': response.css('span.andes-money-amount__currency-symbol::text').get() + response.css('span.andes-money-amount__fraction::text').get(),
            'fotos': fotos_auto(response),
        }
    
def fotos_auto(response):
    """
    Función que busca todas las fotos de un auto
    """
    fotos = []
    i:int = 0
    while True:
        try:
            if i==0:
                foto = response.xpath('//img[@data-index=0]').attrib['src']
            else:
                foto = response.xpath(f'//img[@data-index={i}]').attrib['data-src']
            fotos.append(foto)
            i += 1
        except KeyError:
            break
    return fotos

    
    