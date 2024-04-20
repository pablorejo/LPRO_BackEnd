import pandas as pd
from conf import *

query = "SELECT * FROM gps;"
df_datos_jesus = pd.read_sql_query(query,obtener_engine())
df_datos_jesus.to_csv('datos_gps_jesus.csv',index=False)

