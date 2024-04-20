def traduccion_mes(mesIngles):
    # Diccionario de nombres de meses en español
    traduccionMeses = {
        "January": "enero",
        "February": "febrero",
        "March": "marzo",
        "April": "abril",
        "May": "mayo",
        "June": "junio",
        "July": "julio",
        "August": "agosto",
        "September": "septiembre",
        "October": "octubre",
        "November": "noviembre",
        "December": "diciembre"
    }

    # Convertir el nombre del mes a español
    mesEspanol = traduccionMeses.get(mesIngles, mesIngles)
    return mesEspanol
