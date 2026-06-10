import streamlit as st
import csv
#print ("Hola")
#with open ('precios_surtidor_2024_2025_2026.csv', mode='r', encoding='utf-8') as file:
#    lectura = csv.DictReader(file)
#    for row in lectura:
#      print(row['producto'], row['empresabandera'])


with open ('precios_surtidor_2024_2025_2026.csv', mode='r', encoding='utf-8') as file:
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
st.button("Hola")       
st.bar_chart({"data": [cant_nafta_super, cant_nafta_premium, cant_nafta_GNC, cant_nafta_gasoilG2, cant_nafta_gasoilG3]})

#python -m streamlit run proyecto.py (hostear proyecto)