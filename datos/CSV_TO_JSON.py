

import pandas

df = pandas.read_csv('../../Archivos/datosTrue02.csv', names=("FECHA","T1","T2","T3","T4","H1","H2","H3","H4","MO1","MO2","MO3","MO4","LUX1","LUX2","LUX3","LUX4"))

df.to_json('../../Archivos/json01.csv', orient='records')