import pg8000
from datetime import datetime
from decimal import Decimal
cursor = pg8000.Cursor
con = pg8000.connect(                
    user="postgres",
    host="localhost",
    port=5433,
    database="juninpruebas",
    password="JUNINDATA",
    ssl=False,
)
cursor = con.cursor()
query="DELETE FROM public.produccion_c WHERE id_produccion_c = 4080;".format('public', 'produccion_c', 'produccion_c', '4080')
cursor.execute(query)
con.commit()