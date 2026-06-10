import streamlit as st
import csv
import matplotlib.pyplot as plt

#print ("Hola")
#with open ('precios_surtidor_2024_2025_2026.csv', mode='r', encoding='utf-8') as file:
#    lectura = csv.DictReader(file)
#    for row in lectura:
#      print(row['producto'], row['empresabandera'])


with open ('precios_surtidor_2024_2025_2026.csv', mode='r', encoding='utf-8') as file: 
    #lectura= lo usamos para leer el csv, utilizamos el modulo: csv
    #Cantidad de nafta:
    #cant_nafta_"tipo de nafta": Lo usamos para contabilizar cada tipo de nafta que hay en argentina,
    #utilizamos un contador, por iteracion va sumando 1 al tipo de nafta, por el 'idproducto' correspondiente.
    #Nafta Super = idproducto 2
    #Nafta Premium = idproducto 3
    #Nafta GNC = idproducto 6
    #Nafta Gasoil Grado 2 = idproducto 19
    #Nafta Gasoil Grado 2 = idproducto 21

    lectura = csv.DictReader(file)
    cant_nafta_super= 0
    cant_nafta_premium= 0
    cant_nafta_GNC= 0 
    cant_nafta_gasoilG2= 0
    cant_nafta_gasoilG3= 0

    for row in lectura:
        if row['idproducto'] == '2':
            cant_nafta_super +=1
        elif row['idproducto'] == '3':
            cant_nafta_premium +=1
        elif row['idproducto'] == '6':
            cant_nafta_GNC +=1
        elif row['idproducto'] == '19':
            cant_nafta_gasoilG2 +=1
        else:
            cant_nafta_gasoilG3 +=1
#st.button("Hola")     #Boton de prueba
#st.bar_chart({"data": [cant_nafta_super, cant_nafta_premium, cant_nafta_GNC, cant_nafta_gasoilG2, cant_nafta_gasoilG3]}) #Grafico de barras pero con indices 0,1,2,3,4

combustible = {"Nafta Super": cant_nafta_super, 
               "Nafta Premium": cant_nafta_premium, 
               "GNC": cant_nafta_GNC, 
               "Gasoil G2": cant_nafta_gasoilG2, 
               "Gasoil G3": cant_nafta_gasoilG3}
def main():
    #Grafico que muestra, la cantidad de combustible por tipo
    st.bar_chart(combustible)
main()

#python -m streamlit run proyecto.py (hostear proyecto)