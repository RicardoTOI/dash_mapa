import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import folium
from dash.dash_table import FormatTemplate
money = FormatTemplate.money(0)
import locale
locale.setlocale( locale.LC_ALL, '' )

#Leer datos de mysql
import mysql

conexion = mysql.connector.connect(
    user='root', password='TOIFELIZ2022', host='localhost',database='inmuebles24', port=3306)

#Creamos un objeto cursor
cursor= conexion.cursor()
#Usamos toda la sql
cursor.execute("SELECT * from casas_departamentos")
#Lo ponemos en una df
df = pd.DataFrame(cursor.fetchall())
conexion.close()
#df=df.iloc[:,1:]

#df= pd.read_csv('df_dash.csv', encoding='utf8')
df=df.iloc[:,1:]
df.columns = ['Precios','Moneda','Metros_totales','Metros_construidos','Baños','Estacionamientos','Recamaras','Medio_baño','Antiguedad','Estado','Municipio','Zona','Tipo','Direcciones','Latitud','Longitud']
print(df.dtypes)
for feature in df:
    if df[feature].dtype == "object":
        df[feature] = df[feature].fillna("None")
    else: 
        df[feature] = df[feature].fillna(1.3)
    
app = dash.Dash()

app.layout = html.Div([

    html.Div([

    html.Img(src=app.get_asset_url('toi.png'), style = {'width':'100px','float': 'left', 'margin-left':'20px'}),
    html.H1(
        children="Casas y departamentos en venta",
        style={'color': '#D65F00','margin': '4px auto','text-align': 'center'}
    )
    ], style={'background-color':'#f5f5f5','padding':'3px','border-radius':'7px','font-size':'15px', "border":"1px #D65F00 solid", 'height':'50px'}),

    
    html.Br(),
    html.Iframe(
        open('casas_depas.html','r',encoding="utf-8-sig").read(),
        id='map',
        height='550',
        style={'width':'65%','float': 'right','padding':'5px'} ),
    
    html.Div([ 
    html.Label('Estado', style={'color':'black','font-size':'20px' }), 
    dcc.Dropdown(
        options=df['Estado'].unique().tolist(),
        value =[' Ciudad de México'],
        id = "estado_mexico",
        multi=True,
        style={'background-color':'#f5f5f5', 'border-radius':'5px'}
    )
    ], style={'width':'30%', 'margen':'10px'} ),


    html.Div([
    html.Hr(),
    html.Label('Municipio', style={'color':'black','font-size':'20px' }), 
    dcc.Dropdown( 
        id='municipio_mexico',
        multi=True,
        style={'background-color':'#f5f5f5', 'border-radius':'5px'}      
    )
    ], style={'width':'30%'} ),

    html.Div([
    html.Hr(),
    html.Label('Zona', style={'color':'black','font-size':'20px' }), 
    dcc.Dropdown(
        id='zona_mexico',
        multi=True,
        style={'background-color':'#f5f5f5', 'border-radius':'5px'}
    )
    ], style={'width':'30%'} ),

    html.Div([
    html.Br(),
    html.Label('Precio', style={'color':'black','font-size':'17px' }),
    dcc.RangeSlider( 
        0,
        30000000, 
        value=[df['Precios'].min(),3000000],
        tooltip={"placement": "bottom", "always_visible": True},
        id='precio'
    )
    ], style={'width':'30%'} ),

    html.Div([
    html.Br(),

    html.Div([
    html.Label('Habitaciones', style={'color':'black','font-size':'17px' }), 
    dcc.Slider(0, 10, 1, 
    value=4,
    id='habitacion',
    tooltip={"placement": "bottom", "always_visible": True}
    )], style={'width':'48%','float': 'left','display': 'inline-block'} ),
    
    html.Div([
    html.Label('Baños', style={'color':'black','font-size':'17px' }), 
    dcc.Slider(0, 10, 1, 
    value=4,
    id='tipo_baño',
    tooltip={"placement": "bottom", "always_visible": True}
    )],style={'width':'48%','float': 'right'} ),

    ], style={'width':'30%'} ),

    html.Div([
    html.Br(),

    html.Div([
    html.Label('Antiguedad', style={'color':'black','font-size':'17px' }), 
    dcc.Slider(0, 30, 3, 
    value=9,
    id='antiguedad',
    tooltip={"placement": "bottom", "always_visible": True}
    )], style={'width':'48%','float': 'left','display': 'inline-block'} ),
    
    html.Div([
    html.Label('Estacionamientos', style={'color':'black','font-size':'17px' }), 
    dcc.Slider(0, 10, 1, 
    value=3,
    id='estacionamientos',
    tooltip={ "placement": "bottom", "always_visible": True}
    )],style={'width':'48%','float': 'right'} ),

    ], style={'width':'30%'} ),

    html.Div([
    html.Br(),
    html.Label('Totales metros cuadrados', style={'color':'black','font-size':'17px' }),
    dcc.RangeSlider( 
        df['Metros_totales'].min(),
        1000, 
        value=[df['Metros_totales'].min(),100],
        tooltip={"placement": "bottom", "always_visible": True},
        id='mtotales',     
    ),
    ], style={'width':'30%'} ),

    html.Div([
    html.Br(),
    html.Label('Construidos metros cuadrados', style={'color':'black','font-size':'17px' }),
    dcc.RangeSlider( 
        df['Metros_construidos'].min(),
        1000, 
        value=[df['Metros_construidos'].min(),100],
        tooltip={"placement": "bottom", "always_visible": True},
        id='mconstruidos',     
    )
    ], style={'width':'30%'} )


], style={'background-color':'#f5f5f5',})


#Escoger municipio
@app.callback(
    Output('municipio_mexico', 'options'),
    [Input('estado_mexico', 'value')])
def municipios_func(estados_disponibles):   
    df_est = df.query(f'Estado =={estados_disponibles}')["Municipio"].unique().tolist()
    return df_est

#Escoger zona
@app.callback(
    Output('zona_mexico', 'options'),
    Input('estado_mexico', 'value'),
    Input('municipio_mexico', 'value'))
def zonas_func(estado_selec, municipio_selec):   
    df_est= df.query(f'Estado =={estado_selec}')
    df_mun = df_est.query(f'Municipio =={municipio_selec}')["Zona"].unique().tolist()
    return df_mun

#Mapa
@app.callback(
    Output('map', 'srcDoc'),
    [Input('estado_mexico', 'value'),
    Input('municipio_mexico', 'value'),
    Input('zona_mexico', 'value'),
    Input('mtotales', 'value'),
    Input('mconstruidos', 'value'),
    Input('precio', 'value'),
    Input('tipo_baño', 'value'),
    Input('habitacion', 'value'),
    Input('antiguedad', 'value'),
    Input('estacionamientos', 'value')
    ])
def mapa(est_selec, mun_selec, zona_selec,m_totales, m_construidos, precio_, tipo_baño_, habitacion, antiguedad, estacionamientos):
    Mexico = [23.634501, -102.552784]
    map = folium.Map(Mexico, zoom_start = 5)
    map.save("casas_depas.html")
    
    
    #Habitaciones
    df1 = df.query(f'Recamaras<={habitacion}')
    df2 = df1.query(f'Baños<={tipo_baño_}' )
    #Filtro precio
    df3 = df2.query(f'Precios<={precio_[1]}')
    df4 = df3.query(f'Precios>={precio_[0]}')
    #Filtro metros construidos
    df5 = df4.query(f'Metros_construidos<={m_construidos[1]}')
    df6 = df5.query(f'Metros_construidos>={m_construidos[0]}')

    #Filtro metros totales
    df7 = df6.query(f'Metros_totales<={m_totales[1]}')
    df8 = df7.query(f'Metros_totales>={m_totales[0]}')

    #Antigueadad
    df9 = df8.query(f'Antiguedad<={antiguedad}')
    df10 = df9.query(f'Estacionamientos<={estacionamientos}')


   
    
    if zona_selec:
        
        for zona in zona_selec:
            zona_selec = zona
            
            df11 = df10.query(f'Estado == "{est_selec[0]}"')
            df12 = df11.query(f'Municipio == "{mun_selec[0]}"')
            df13 = df12.query(f'Zona == "{zona_selec}"')
            list_lat = df13["Latitud"].tolist()
            list_long = df13["Longitud"].tolist()
            
            #Marcamos en el mapa
            tipo = df11['Tipo'].tolist()    
            precio = df11['Precios'].tolist() 
            moneda = df11['Moneda'].tolist() 


            habitaciones = df11['Recamaras'].tolist()
            baños = df11['Baños'].tolist()
            totm2=df11['Metros_totales'].tolist()
            constm2=df11['Metros_construidos'].tolist()
            direccion = df11['Direcciones'].tolist()
            antiguedad=df11['Antiguedad'].tolist()
            estacionamientos = df11['Estacionamientos'].tolist()


            for i in range(len(list_lat)):
                
                if habitaciones[i] == 1.3:
                    habitaciones[i] = 'No disponible'
                else:
                    habitaciones[i] =int(habitaciones[i])
                if baños[i] == 1.3:
                    baños[i] = 'No dispinoble'
                else:
                    baños[i]=int(baños[i])
                if totm2[i] == 1.3:
                    totm2[i] = 'No disponible'
                else:
                    totm2[i]= str(int(totm2[i]))+' m²'
                if constm2[i] == 1.3:
                    constm2[i] = 'No disponible'
                else:
                    constm2[i]=str(int(constm2[i])) + ' m²'
                if antiguedad[i] == 1.3:
                    antiguedad[i] = 'No disponible'
                else:
                    antiguedad[i]=str(int(antiguedad[i])) + ' años'
                if estacionamientos[i] == 1.3:
                    estacionamientos[i] = 'No disponible'
                else:
                    estacionamientos[i]=int(estacionamientos[i])

                if tipo[i] == 'Casa':
                    folium.Marker([list_lat[i], list_long[i]],popup = f'<h1>{locale.currency( precio[i], grouping=True )}{moneda[i]}</h1> <br> <h2>Casa</h2> <h4>Metros totales: {totm2[i]} </h4> <h4>Metros construidos: {constm2[i]} </h4> <h4>Antiguedad: {antiguedad[i]} </h4> <h4>Estacionamientos: {estacionamientos[i]} </h4> <h4>Habitaciones: {habitaciones[i]}</h4> <h4>Baños: {baños[i]}</h4> <h6>{direccion[i]}</h6> ', icon = folium.Icon(color = "red")).add_to(map)
                if tipo[i]=='Departamento':
                    folium.Marker([list_lat[i], list_long[i]],popup = f'<h1>{locale.currency(precio[i], grouping=True )}{moneda[i]}</h1> <br> <h2>Departamento</h2> <h4>Metros totales: {totm2[i]} </h4> <h4>Metros construidos: {constm2[i]} </h4> <h4>Antiguedad: {antiguedad[i]} </h4> <h4>Estacionamientos: {estacionamientos[i]} </h4> <h4>Habitaciones: {habitaciones[i]}</h4> <h4>Baños: {baños[i]}</h4> <h6>{direccion[i]}</h6> ', icon = folium.Icon(color = "darkblue")).add_to(map)
            map.save("casas_depas.html")
        return open('casas_depas.html','r',encoding="utf-8-sig").read()    
  

    
    map.save("casas_depas.html")
    return open('casas_depas.html','r',encoding="utf-8-sig").read()


if __name__=="__main__":
    app.run_server(debug=True)