import pandas as pd
from datetime import datetime

data = pd.read_csv('datos.csv')
with open('datos.sql','w') as file:
    for i in range(0, len(data)):
        row = data.iloc[i]
        fecha = datetime.strptime(row['fecha'], "%Y-%m-%d %H:%M:%S.%f")
        fecha_final_str = "\'" +  fecha.strftime("%Y-%m-%d %H:%M:%S") + "\'"

        numero_pendiente =  str(1000 + int(row['Numero pendiente']))
        if (i == len(data)-1):
            file.write(f"({numero_pendiente},1, {row['latitude']}, {row['longitude']},{fecha_final_str});\n")
        else:
            file.write(f"({numero_pendiente},1, {row['latitude']}, {row['longitude']},{fecha_final_str}),\n")
            