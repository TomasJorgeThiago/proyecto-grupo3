import csv
def lectura_completa(columna, formato):
    with open ('precios_surtidor_2024_2025_2026.csv', mode='r', encoding='utf-8') as file:
        lectura = csv.DictReader(file)
        columnaid = []
        for row in lectura:
            columnaid=columnaid+ [formato(row[columna])]
        return columnaid

#lectura_completa()

def promedio_precio(num):
    id_nafta=lectura_completa('idproducto',int)
    precio_nafta=lectura_completa('precio',float)
    total=0
    aparicion=0
    for x in range(0,len(id_nafta)):
        if id_nafta[x]==num:
            total+=precio_nafta[x]
            aparicion+=1
    print (total/aparicion)
    return total/aparicion
#promedio_precio()

def main():
    promedio_precio(2)
    promedio_precio(3)
    promedio_precio(6)
    promedio_precio(19)
    promedio_precio(21)
main()    
