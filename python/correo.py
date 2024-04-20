import sys
import json
import ssl
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta

# ******************************************************************* #
# ***************************** FUNCIONES *************************** # 
# ******************************************************************* #
def verificar_argumentos():
    if len(sys.argv) < 4:
        print(json.dumps({"mensaje": "Algo ha salido mal"}))
        sys.exit(-1)
    return sys.argv[1], sys.argv[2], sys.argv[3]

def traduccion_mes(mesIngles):
    # Diccionario de nombres de meses en español
    traduccionMeses = {
        "January": "Xaneiro",
        "February": "Febreiro",
        "March": "Marzo",
        "April": "Abril",
        "May": "Maio",
        "June": "Xuño",
        "July": "Xullo",
        "August": "Agosto",
        "September": "Setembro",
        "October": "Outubro",
        "November": "Novembro",
        "December": "Decembro"
    }

    # Convertir el nombre del mes a español
    mesGalego = traduccionMeses.get(mesIngles, mesIngles)
    return mesGalego

# ******************************************************************* #
# ******************************* MAIN ****************************** # 
# ******************************************************************* #
def main():
    destinatario, rutaInformacion, nombreArchivo = verificar_argumentos()
    
    # Obtención del mes automática 
    mesDatos = (datetime.now() - timedelta(days=30)).strftime("%B")

    #Traducción del mes a español
    mesDatos = traduccion_mes(mesDatos)

    remitente = 'muundoGando@gmail.com'
    contraseña = 'dvhn oshh deig mvyd'
    #destinatario = 'carlos@fernandezdeus.es'

    asunto = "Resumo e Información de " + mesDatos
    cuerpo = """
        Hola!
        Dejamos adjunta la información del mes de """ + mesDatos + """."""

    # Crear objeto de mail:
    em = EmailMessage()
    em['From'] = remitente
    em['To'] = destinatario
    em['Subject'] = asunto
    em.set_content(cuerpo)

    # Adjuntar el archivo PDF
    with open(rutaInformacion, 'rb') as archivo_pdf:
        em.add_attachment(archivo_pdf.read(), maintype='application', subtype='pdf', filename=nombreArchivo)

    # Añadir SSL (extra de seguridad)
    context = ssl.create_default_context()

    # Iniciar sesión y enviar el mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(remitente, contraseña)
        smtp.sendmail(remitente, destinatario, em.as_string())


if __name__ == "__main__":
    main()
