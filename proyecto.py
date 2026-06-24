import streamlit as st
import csv
import matplotlib.pyplot as plt

#Cambios y Correcciones:

# 1- Hicimos la funcion principal de lectura , para que solo se lea una vez, esta consta de un diccionario con listas vacias, que luego dentro
# del for, se ira rellenando con su respectiva columna, por cada iteracion. El if utilizado lo pusimos porque nos dimos cuenta que hay un par de
# coordenadas que estan vacias, entonces simplemente las salteamos, no hay errores ya que es la latitud y la longitud de 2 estaciones.
# 2- Ordenamos el grafico de combustibles: Nos pedian que ordenemos de menor a mayor los valores del grafico, utilizamos simplemente uno de los
# parametros de la funcion st.bar, "sort" que permite Ordenar por valor. Reeutilizamos la funcion principal del grafico.
#PREGUNTA DINAMICA: ¿Cuántas estaciones se encuentran disponibles según la provincia?

# 3- Agregar mapa interactivo + Seleccionador: Agregamos un mapa interactivo que nos muestra todas las estaciones de servicio en la provincia que
# seleccionamos. El Seleccionador esta ordenado alfabeticamente con el parametro "sorted". Utilizamos un set, para que las provincias no se repitan.

#para tomar nota: Hay un par de provincias, como por ejemplo "Buenos Aires" que tienen algunas sus latitudes y longitudes en otro lugar del pais. Tomamos esto
#como un error del dataset y esperamos instrucciones de como seguir.

#-----------------------------------------
def todos_datos():
    #datos = diccionario con listas vacias de todas las columnas "importantes" que vamos a utilizar dentro de todo el programa, cada vez que
    #necesitemos llamar a los datos del archivo, llamaremos directamente a "datos" sin abrir de vuelta el csv. por ejemplo:
    #print (datos["precio"]) y mostrara todos los precios
    #lectura= lo usamos para leer el csv, utilizamos el modulo: csv, utilizamos DictReader para poder leer el archivo usando los nombres
    #de las columnas
    #for row in lectura: recorre todas las filas del csv, por cada iteracion se guarda una fila distinta en cada columna o row
    datos = {
        "provincia": [],
        "idproducto": [],
        "precio": [],
        "idempresabandera": [],
        "latitud": [],
        "longitud": [],
        "empresabandera": []
    }
    with open("precios_surtidor_2024_2025_2026.csv", mode="r",encoding="utf-8") as archivo:
        lectura = csv.DictReader(archivo)
        for row in lectura:
            if row["latitud"] == "" or row["longitud"] == "":
                continue
            datos["provincia"].append(row["provincia"])
            datos["idproducto"].append(row["idproducto"])
            datos["precio"].append(row["precio"])
            datos["idempresabandera"].append(row["idempresabandera"])
            datos["empresabandera"].append(row["empresabandera"])
            datos["latitud"].append(float(row["latitud"]))
            datos["longitud"].append(float(row["longitud"]))
            
    return datos

def contar_combustible(datos, id_combustible):
    cantidad = 0
    for producto in datos["idproducto"]:
        if producto == id_combustible:
            cantidad += 1
    return cantidad

def grafico_cantcombustibles(datos):
    combustible = {
        "Nafta Super": contar_combustible(datos, "2"),
        "Nafta Premium": contar_combustible(datos, "3"),
        "GNC": contar_combustible(datos, "6"),
        "Gasoil G2": contar_combustible(datos, "19"),
        "Gasoil G3": contar_combustible(datos, "21")
    }
    st.write(":bar_chart: Cantidad de combustible por tipo en todo el país :bar_chart:")
    st.bar_chart(combustible,sort= "value")


def seleccionador_provincia(datos):
    provincias = ["TODO"] + sorted(set(datos["provincia"]))
    seleccionador = st.sidebar.selectbox(
        "Selecciona una Provincia", provincias)
    return seleccionador

def seleccionador_empresa(datos):
    lista = ["TODAS"] + sorted(set(datos["empresabandera"]))
    empresa = st.sidebar.selectbox(
        "¿En qué empresa está interesado?",
        lista
    )
    return empresa

def mapa_interactivo(datos,provincia, empresa):
    longitudes = []
    latitudes = []
    for x in range(len(datos["provincia"])):
        if datos["provincia"][x] == provincia or provincia == "TODO":
            if empresa == datos["empresabandera"][x] or empresa == "TODAS":
                longitudes.append(datos["longitud"][x])
                latitudes.append(datos["latitud"][x])

    if len(latitudes) == 0:
        st.warning("No hay estaciones para mostrar.")
    else:
        datos_mapa = {
        "lat": latitudes,
        "lon": longitudes,
        "zoom": 13
    }
        st.map(datos_mapa)
        
        
def promedio_combustible(datos, provincia, id_combustible):
    total = 0
    cantidad = 0
    for x in range(len(datos["provincia"])):
        if datos["provincia"][x] == provincia or provincia == "TODO":
            if datos["idproducto"][x] == id_combustible:
                total += float(datos["precio"][x])
                cantidad += 1
    if cantidad > 0:
        return total / cantidad
    return 0

def mostrar_promedios(datos, provincia):
    st.write("Promedios en", provincia)
    st.write("Nafta Super:",round(promedio_combustible(datos, provincia, "2"), 2))
    st.write("Nafta Premium:",round(promedio_combustible(datos, provincia, "3"), 2))
    st.write("GNC:",round(promedio_combustible(datos, provincia, "6"), 2))
    st.write("Gasoil G2:",round(promedio_combustible(datos, provincia, "19"), 2))
    st.write("Gasoil G3:",round(promedio_combustible(datos, provincia, "21"), 2))     
    return provincia

def main():
    #llamamos a la funcion datos y a todos los graficos o mapas
    datos = todos_datos()
    provincia = seleccionador_provincia(datos)
    empresa = seleccionador_empresa(datos)
    mapa_interactivo(datos, provincia,empresa)
    mostrar_promedios(datos,provincia)
    grafico_cantcombustibles(datos)
main()

#python -m streamlit run proyecto.py (hostear proyecto)
