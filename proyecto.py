import streamlit as st
import csv
import matplotlib.pyplot as plt

#ordenamos la pagina en 2 columnas
col1, col2 = st.columns(2, width=1000)
def todos_datos():
    #datos = diccionario con listas vacias de todas las columnas "importantes" que vamos a utilizar dentro de todo el programa, cada vez que
    #necesitemos llamar a los datos del archivo, llamaremos directamente a "datos" sin abrir de vuelta el csv. por ejemplo:
    #print (datos["precio"]) y mostrara todos los precios
    #lectura= lo usamos para leer el csv, utilizamos el modulo: csv, utilizamos DictReader para poder leer el archivo usando los nombres
    #de las columnas
    #for row in lectura: recorre todas las filas del csv, por cada iteracion se guarda una fila distinta en cada columna o row
    #También verificamos que la latitud y longitud no estén vacías, ya que algunas estaciones no tienen coordenadas y no podrían
    #mostrarse correctamente en el mapa.
    datos = {
        "provincia": [],
        "idproducto": [],
        "precio": [],
        "idempresabandera": [],
        "latitud": [],
        "longitud": [],
        "empresabandera": [],
        "producto": []
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
            datos["producto"].append(row["producto"])
            
    return datos

def contar_combustible(datos, id_combustible):
    #Cuenta la cantidad de tipo de combustible que hay en el pais
    #Recibe id_combustible y cuando encuentra una coincidencia, suma 1 al contador
    #devuelve la cantidad total
    cantidad = 0
    for producto in datos["idproducto"]:
        if producto == id_combustible:
            cantidad += 1
    return cantidad

def grafico_cantcombustibles(datos):
    #Tomando contar_combustible(), genera un grafico que muestra la cantidad de
    #tipos de combustible que hay en el pais
    #Guarda los resultados en un diccionario donde la clave es el nombre
    #del combustible y el valor es la cantidad de ese tipo de combustible.
    combustible = {
        "Nafta Super": contar_combustible(datos, "2"),
        "Nafta Premium": contar_combustible(datos, "3"),
        "GNC": contar_combustible(datos, "6"),
        "Gasoil G2": contar_combustible(datos, "19"),
        "Gasoil G3": contar_combustible(datos, "21")
    }
    st.write(":bar_chart: Cantidad de combustible en todo el país :bar_chart:")
    st.bar_chart(combustible,sort= "value")

def seleccionador_provincia(datos):
    #Esto es parte de todo el mapa, sirve para seleccionar en que provincia queremos visualizar
    #las empresas, el combustible, y el promedio de precios por tipo de combustible
    #Utiliza set() para eliminar provincias repetidas y sorted()para ordenarlas alfabéticamente.
    provincias = ["TODO"] + sorted(set(datos["provincia"]))
    seleccionador = st.sidebar.selectbox(
        "Selecciona una Provincia", provincias)
    return seleccionador

def seleccionador_empresa(datos):
    #Esto es parte de todo el mapa, sirve para seleccionar que empresa queremos buscar, se puede
    #acompañar seleccionando una provincia para tener datos mas exactos
    #utilizando set() y las ordena alfabéticamente.
    #la opcion "TODAS" permite no aplicar ningún filtro por empresa en el mapa
    lista = ["TODAS"] + sorted(set(datos["empresabandera"]))
    empresa = st.sidebar.selectbox(
        "¿En qué empresa está interesado?",
        lista
    )
    return empresa

def seleccionador_combustible(datos):
    #Esto es parte de todo el mapa, sirve para seleccionar que tipo de combustibles queremos buscar
    #se puede acompañar por la provincia y por la empresa para tener datos mas exactos
    #La opción "TODO" permite mostrar estaciones sin filtrar
    #por combustible.
    lista = ["TODO"] + sorted(set(datos["producto"]))
    combustible = st.sidebar.selectbox(
        "Elegir combustible",
        lista
    )
    return combustible

def mapa_interactivo(datos,provincia, empresa, combustible):
    #Este es el mapa principal.
    #Permite filtrar por provincia, empresa y tipo de combustible(Gracias a los seleccionadores)
    #Recorre todas las estaciones del archivo y compara los datos con los filtros seleccionados por el usuario:
    #provincia, empresa y combustible.
    #el st.warning nos indica que si no encuentra estaciones que coincidan con los filtros,muestra un mensaje de advertencia.
    #st.map() para representar todas las estaciones seleccionadas en el mapa.
    longitudes = []
    latitudes = []
    for x in range(len(datos["provincia"])):
        if datos["provincia"][x] == provincia or provincia == "TODO":
            if empresa == datos["empresabandera"][x] or empresa == "TODAS":
                if combustible == datos["producto"][x] or combustible == "TODO":
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
    #Calcula el promedio del precio de un tipo de combustible
    #Recibe una provincia y un id de combustible.
    #Recorre todas las estaciones y suma los precios solamente cuando coinciden con la provincia y el combustible seleccionado.
    #cuenta la cantidad de estaciones encontradas para poder realizar el promedio.
    #Si encuentra estaciones devuelve el promedio del precio. En caso contrario devuelve 0 para evitar errores.
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
    #Muestra el promedio de cada tipo de combustible
    #Utiliza promedio_combustible, por cada tipo de combustible a consultar
    st.write("### Promedios en", provincia)
    comb_nombre = [("2", "Nafta Super"), ("3", "Nafta Premium"), ("6", "GNC"), ("19", "Gasoil G2"), ("21", "Gasoil G3")]
    for id_combustible, nombre in comb_nombre:
        promedio = promedio_combustible(datos, provincia, id_combustible)
        st.write(nombre,"$", round(promedio, 2))
    

def grafico_gnc_barato(datos):
    #Este grafico muestra las empresas con combustible GNC, mas barato
    #suma_empresa: almacena la suma de todos los precios de GNC de cada empresa.
    #cantidad_empresa: almacena la cantidad de estaciones de GNC que tiene cada empresa.
    #Recorre todas las estaciones y solamente toma aquellas cuales idproducto corresponde al GNC.
    #calcula el promedio dividiendo la suma de preciosentre la cantidad de estaciones.
    #Color amarillo para diferenciar del fondo y del grafico de arriba
    suma_empresa = {}
    cantidad_empresa = {}

    for x in range(len(datos["idproducto"])):
        if datos["idproducto"][x] == "6":
            empresa = datos["empresabandera"][x]

            if empresa not in suma_empresa:
                suma_empresa[empresa] = 0
                cantidad_empresa[empresa] = 0

            suma_empresa[empresa] += float(datos["precio"][x])
            cantidad_empresa[empresa] += 1

    promedio_empresa = {}

    for empresa in suma_empresa:
        promedio_empresa[empresa] = round(suma_empresa[empresa] / cantidad_empresa[empresa], 2)

    st.write("Promedio del precio del GNC por empresa")
    st.bar_chart(promedio_empresa, sort="value", color="yellow")
    
def main():
    #Función principal del programa
    #Obtiene los datos del archivo
    #Llama a todos los seleccionadores, mapas, interfaces
    datos = todos_datos()
    provincia = seleccionador_provincia(datos)
    empresa = seleccionador_empresa(datos)
    combustible = seleccionador_combustible(datos)
    with col2:
        grafico_cantcombustibles(datos)
        grafico_gnc_barato(datos)
    with col1:
        mapa_interactivo(datos, provincia,empresa,combustible)
        mostrar_promedios(datos,provincia)
        
main()

#python -m streamlit run proyecto.py (hostear proyecto)
