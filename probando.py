import streamlit as st
import csv
import matplotlib.pyplot as plt
def todos_datos():
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


def grafico_cantcombustibles(datos):
    cant_nafta_super= 0
    cant_nafta_premium= 0
    cant_nafta_GNC= 0 
    cant_nafta_gasoilG2= 0
    cant_nafta_gasoilG3= 0
    for producto in datos["idproducto"]:
        if producto == "2":
            cant_nafta_super += 1
        elif producto == "3":
            cant_nafta_premium += 1
        elif producto == "6":
            cant_nafta_GNC += 1
        elif producto == "19":
            cant_nafta_gasoilG2 += 1
        elif producto == "21":
            cant_nafta_gasoilG3 += 1   
    combustible = {"Nafta Super": cant_nafta_super, 
               "Nafta Premium": cant_nafta_premium, 
               "GNC": cant_nafta_GNC, 
               "Gasoil G2": cant_nafta_gasoilG2, 
               "Gasoil G3": cant_nafta_gasoilG3}
    st.bar_chart(combustible, sort="value")


def seleccionador_provincia(datos):

    provincias = ["TODO"] + sorted(set(datos["provincia"]))
    seleccionador = st.selectbox(
        "Selecciona una Provincia", provincias)
    return seleccionador

def seleccionador_empresa(datos):
    lista = ["TODAS"] + sorted(set(datos["empresabandera"]))
    empresa = st.sidebar.selectbox(
        "¿En qué empresa está interesado?",
        lista
    )
    return empresa

def mapa(datos):
    provincia = seleccionador_provincia(datos)
    empresa = seleccionador_empresa(datos)
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

def main():
    datos = todos_datos()
    grafico_cantcombustibles(datos)
    mapa(datos)
main()

