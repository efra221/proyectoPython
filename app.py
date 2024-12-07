from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Ruta para la página principal
@app.route("/")
def index():
    return render_template("chart.html")

# Ruta para generar la gráfica
@app.route("/chart")
def chart():
    # Cargar el archivo CSV
    csv_path = "1.csv"  
    data = pd.read_csv(csv_path)
    
    # Aplicar filtros
    filtered_data = data[(data["AÑO"] > 2011) & (data["CÓDIGO_DEPARTAMENTO"].isin([5, 8]))]
    
    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    plt.bar(filtered_data["AÑO"], filtered_data["CÓDIGO_DEPARTAMENTO"], color='blue', alpha=0.7, label="Departamentos 5 y 8")
    plt.title("Año vs Código de Departamento", fontsize=16)
    plt.xlabel("Año", fontsize=12)
    plt.ylabel("Código de Departamento", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    # Guardar la gráfica en la carpeta static
    chart_path = os.path.join("static", "chart.png")
    plt.savefig(chart_path)
    plt.close()

    return send_file(chart_path, mimetype="image/png")

@app.route("/chart_desercion")
def chart_desercion():
    csv_path = "1.csv"  
    data = pd.read_csv(csv_path)

    desercion = data[(data["AÑO"] > 2011) & (data["CÓDIGO_DEPARTAMENTO"].isin([5, 8]))]

    # Gráfica de desercion
    plt.figure(figsize=(12, 6))
    plt.plot(desercion["AÑO"], desercion["DESERCIÓN_TRANSICIÓN"], label="Transición", marker='o')
    plt.plot(desercion["AÑO"], desercion["DESERCIÓN_SECUNDARIA"], label="Secundaria", marker='^')
    plt.plot(desercion["AÑO"], desercion["DESERCIÓN_MEDIA"], label="Media", marker='d')
    plt.plot(desercion["AÑO"], desercion["DESERCIÓN_PRIMARIA"], label="Primaria", marker='s')
    plt.title("Deserción por Nivel Educativo (Departamentos 5 y 8)", fontsize=16)
    plt.xlabel("Año", fontsize=12)
    plt.ylabel("Tasa de Deserción (%)", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    chart_path = os.path.join("static", "chart_desercion.png")
    plt.savefig(chart_path)
    plt.close()

    return send_file(chart_path, mimetype="image/png")

@app.route("/chart_internet")
def chart_internet():
    csv_path = "1.csv"
    data = pd.read_csv(csv_path)

    Internet = data[(data["AÑO"] > 2011) & (data["CÓDIGO_DEPARTAMENTO"].isin([5, 8]))]

    # Grafica internet
    plt.figure(figsize=(12, 6))
    plt.bar(Internet["AÑO"], Internet["SEDES_CONECTADAS_A_INTERNET"], color='green', alpha=0.7, label="Sedes Conectadas a Internet")
    plt.plot(Internet["AÑO"], Internet["APROBACIÓN"], color='blue', marker='o', label="Tasa de Aprobación (%)")

    plt.title("Relación entre Conexión a Internet y Tasa de Aprobación", fontsize=16)
    plt.xlabel("Año", fontsize=12)
    plt.ylabel("Cantidad / Porcentaje", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    chart_path = os.path.join("static", "chart_internet.png")
    plt.savefig(chart_path)
    plt.close()

    return send_file(chart_path, mimetype="image/png")

@app.route("/chart_reprobacion")
def chart_reprobacion():
    csv_path = "1.csv"
    data = pd.read_csv(csv_path)

    Reprobacion = data[(data["AÑO"] == 2021) & (data["CÓDIGO_DEPARTAMENTO"].isin([5, 8]))]

    # Valore de la graficas
    categorias = ["TRANSICIÓN", "PRIMARIA", "SECUNDARIA", "MEDIA"]
    valores = [
        Reprobacion["REPROBACIÓN_TRANSICIÓN"].mean(),
        Reprobacion["REPROBACIÓN_PRIMARIA"].mean(),
        Reprobacion["REPROBACIÓN_SECUNDARIA"].mean(),
        Reprobacion["REPROBACIÓN_MEDIA"].mean(),
    ]

    # Grafica de reprobacion
    plt.figure(figsize=(8, 8))
    plt.pie(valores, labels=categorias, autopct="%1.1f%%", startangle=90, pctdistance=0.85, colors=["#ff9999","#66b3ff","#99ff99","#ffcc99"])
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    plt.gca().add_artist(centre_circle)
    plt.title("Distribución de la Reprobación por Nivel Educativo (2021)", fontsize=16)

    chart_path = os.path.join("static", "chart_reprobacion.png")
    plt.savefig(chart_path)
    plt.close()

    return send_file(chart_path, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)
