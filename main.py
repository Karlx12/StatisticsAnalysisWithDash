import pandas as pd
from dash import Dash, html, dash_table, dcc
import plotly.express as px

df = pd.read_csv("./notas_1u.csv", sep=",")

stats_grouped = (
    df.groupby("Tipo_Examen")["Nota"].agg(["mean", "median", "std"]).reset_index()
)
stats_grouped = stats_grouped.round(2)


# Initialize the app
app = Dash(__name__)

# Create figures for visualizations
histogram_fig = px.histogram(
    df,
    x="Nota",
    color="Tipo_Examen",
    title="Distribución de Notas",
    labels={"Nota": "Calificación", "Tipo_Examen": "Tipo de Examen"},
    opacity=0.7,
    barmode="overlay",
)

boxplot_fig = px.box(
    df,
    x="Tipo_Examen",
    y="Nota",
    title="Comparación de Notas por Tipo de Examen",
    labels={"Nota": "Calificación", "Tipo_Examen": "Tipo de Examen"},
    color="Tipo_Examen",
)

barplot_fig = px.bar(
    stats_grouped,
    x="Tipo_Examen",
    y="mean",
    title="Promedio de Notas por Tipo de Examen",
    labels={"mean": "Promedio", "Tipo_Examen": "Tipo de Examen"},
    color="Tipo_Examen",
)

# App layout
app.layout = html.Div(
    [
        html.H1(children="Notas de alumnos Primera Unidad"),
        html.Div(
            [
                html.H2("Tabla de datos"),
                dash_table.DataTable(
                    data=[
                        {str(k): v for k, v in row.items()}
                        for row in df.to_dict("records")
                    ],
                    columns=[
                        {"name": "Alumno", "id": "Alumno"},
                        {"name": "Nota", "id": "Nota"},
                        {"name": "Tipo Examen", "id": "Tipo_Examen"},
                    ],
                    page_size=10,
                    sort_action="native",
                    filter_action="native",
                    style_table={"overflowX": "auto"},
                    style_header={
                        "backgroundColor": "rgb(230, 230, 230)",
                        "fontWeight": "bold",
                        "color": "#333333",
                    },
                    style_cell={
                        "textAlign": "left",
                        "padding": "12px",
                        "fontFamily": "Arial, sans-serif",
                    },
                    style_data={
                        "whiteSpace": "normal",
                        "height": "auto",
                        "lineHeight": "15px",
                    },
                ),
            ],
            style={"margin": "30px 30px"},
        ),
        html.Div(
            [
                html.H2("Visualizaciones"),
                html.Div(
                    [dcc.Graph(figure=histogram_fig, style={"height": "500px"})],
                    style={"margin": "20px 0px"},
                ),
                html.Div(
                    [dcc.Graph(figure=boxplot_fig, style={"height": "500px"})],
                    style={"margin": "20px 0px"},
                ),
                html.Div(
                    [dcc.Graph(figure=barplot_fig, style={"height": "500px"})],
                    style={"margin": "20px 0px"},
                ),
            ]
        ),
        html.Div(
            [
                html.H2("Estadísticas por Tipo de Examen"),
                dash_table.DataTable(
                    data=[
                        {str(k): v for k, v in row.items()}
                        for row in stats_grouped.to_dict("records")
                    ],
                    columns=[
                        {"name": "Tipo de Examen", "id": "Tipo_Examen"},
                        {"name": "Media", "id": "mean"},
                        {"name": "Mediana", "id": "median"},
                        {"name": "Desviación Estándar", "id": "std"},
                    ],
                ),
            ]
        ),
    ]
)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
