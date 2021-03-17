#Importación de librerías
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px


df2018 = pd.read_csv("https://raw.githubusercontent.com/dphi-official/Datasets/master/IT_Salary_Survey_EU_18-20/Survey_2018.csv")
df2019 = pd.read_csv("https://raw.githubusercontent.com/dphi-official/Datasets/master/IT_Salary_Survey_EU_18-20/Survey_2019.csv")
df2020 = pd.read_csv("https://raw.githubusercontent.com/dphi-official/Datasets/master/IT_Salary_Survey_EU_18-20/Survey_2020.csv")

app = dash.Dash()
server = app.server

app.layout = html.Div([
                    html.Div([
                    html.Label('Escoger año'),
                    dcc.Dropdown(id='selector',
                        options=[{'label': '2018', 'value': '2018'},
                                 {'label': '2019', 'value': '2019'},
                                 {'label': '2020', 'value': '2020'}],
                        value='2018'
                    )],style={'width': '100%', 'display': 'inline-block'}),
                  
                    html.Div([
                    dcc.Graph(id='tecnologia')
                    ],style={'width': '100%'}),


                    html.Div([
                    dcc.Graph(id='tipos_empresa')
                    ],style={'width': '50%', 'float': 'left', 'display': 'inline-block'}),

                    html.Div([
                    dcc.Graph(id='genero')
                    ],style={'width': '50%', 'float': 'right', 'display': 'inline-block'})

                    ])

@app.callback(Output('tipos_empresa', 'figure'),
              [Input('selector', 'value')])
def actualizar_empresa(seleccion):
    
    if seleccion == '2018':
        seleccion = df2018
    elif seleccion == '2019':
        seleccion = df2019
    else:
        seleccion = df2020
        
    df = seleccion.groupby("Company type")["Company type"].count().head(3)
    df = pd.DataFrame(df)
    fig = px.pie(df,values="Company type", names=df.index, title ="Tipos de Empresas( TOP 3 )")

    return fig

@app.callback(Output('genero', 'figure'),
              [Input('selector', 'value')])
def actualizar_genero(seleccion):
    if seleccion == '2018':
        seleccion = df2018
    elif seleccion == '2019':
        seleccion = df2019
    else:
        seleccion = df2020
        
    df = seleccion.groupby("Gender")["Gender"].count()
    fig = px.pie(df,values="Gender", names=df.index, title ="Género")

    return fig

@app.callback(Output('tecnologia', 'figure'),
              [Input('selector', 'value')])
def actualizar_tecnologia(seleccion):
    if seleccion == '2018':
        df2018.rename(columns={'Main language at work':'Your main technology / programming language'},
                  inplace=True)
        seleccion = df2018

    elif seleccion == '2019':
        seleccion = df2019
    else:
        seleccion = df2020
        
    df = seleccion.groupby("Your main technology / programming language")["Your main technology / programming language"].count()
    df = pd.DataFrame(df)
    df.rename(columns={'Your main technology / programming language':'Total'},
              inplace=True)
    df.sort_values(by="Total",ascending=False,inplace=True)
    df.sort_values(by="Your main technology / programming language", axis=0)
    df = df.head(5)
    fig = px.bar(df, x=df.index, y=df["Total"],title ="Idioma ( 2008 ) / Tipo de Tecnología ( 2019 - 2020 )")
    
    return fig

if __name__ == '__main__':
    app.run_server(port=7200)
