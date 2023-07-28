# Import
from datetime import datetime, timedelta

def calcular_fecha(texto):
    """
    Función que busca extraer el número de días del texto 'publicado hace {x} días
    """
    # Quedarse con el número
    dias = int(texto.split()[2])  

    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Calcular la fecha anterior restando los días
    fecha_publicacion = fecha_actual - timedelta(days=dias)
    
    fecha_publicacion = fecha_publicacion.strftime("%d/%m/%Y")

    return fecha_publicacion