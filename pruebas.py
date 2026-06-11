import csv
def lectura_completa(columna, formato):
    with open ('precios_surtidor_2024_2025_2026.csv', mode='r', encoding='utf-8') as file:
        lectura = csv.DictReader(file)
        columnaid = []
        for row in lectura:
            columnaid=columnaid+ [formato(row[columna])]
        return columnaid

#lectura_completa()

def gnc():
    gncid=lectura_completa('idproducto',int)
    gncprecio=lectura_completa('precio',float)
    total=0
    aparicion=0
    for x in range(0,len(gncid)):
        if gncid[x]==6:
            total+=gncprecio[x]
            aparicion+=1
    print (total/aparicion)
    return total/aparicion
gnc()