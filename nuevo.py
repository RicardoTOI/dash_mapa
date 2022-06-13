import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import folium
import locale
import math
locale.setlocale( locale.LC_ALL, '' )
#pd.set_option('display.max_colwidth', None)

#Leer datos de mysql
import mysql.connector


conexion = mysql.connector.connect(
    user='toicommx_science', password='TOIFELIZ2022', host='51.79.35.184',
    database='toicommx_inmobiliaria', port=3306, auth_plugin='mysql_native_password')

#Creamos un objeto cursor
cursor= conexion.cursor()
#Usamos toda la sql
cursor.execute("SELECT * from casas_departamentos")
#Lo ponemos en una df
df = pd.DataFrame(cursor.fetchall())
conexion.close()


#df= pd.read_csv('df_final_110622.csv', encoding='utf8')
df=df.iloc[:,1:]
df.columns = ['Precios','Moneda','Metros_totales','Metros_construidos','Baños','Estacionamientos','Recamaras','Medio_baño','Antiguedad','Estado','Municipio','Zona','Tipo','Direcciones','Latitud','Longitud']

app = dash.Dash()
server = app.server

app.layout = html.Div([

    html.Div([


    html.Img(src='https://toi.com.mx/images/toi-expertos-hipotecarios-logo-color.svg', style = {'width':'100px','float': 'left', 'margin-left':'20px'}),
    html.H1(
        children="Geolocalización de casas y departamentos en venta",
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
        value =[' Nuevo León'],
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
        #marks={i: f'(format({i}, ",d"))' for i in range(0, 30000001)},
        value=[df['Precios'].min(),3000000],
        tooltip={"placement": "bottom", "always_visible": True},
        id='precio',

    )
    ], style={'width':'30%'} ),

    html.Div([
    html.Br(),

    html.Div([
    html.Label('Habitaciones', style={'color':'black','font-size':'17px' }), 
    dcc.RangeSlider(0, 10, 1,
    value=[0,4],
    id='habitacion',
    tooltip={"placement": "bottom", "always_visible": True}
    )], style={'width':'48%','float': 'left','display': 'inline-block'} ),
    
    html.Div([
    html.Label('Baños', style={'color':'black','font-size':'17px' }), 
    dcc.RangeSlider(0, 10, 1,
    value=[0,4],
    id='tipo_baño',
    tooltip={"placement": "bottom", "always_visible": True}
    )],style={'width':'48%','float': 'right'} ),

    ], style={'width':'30%'} ),

    html.Div([
    html.Br(),

    html.Div([
    html.Label('Antiguedad', style={'color':'black','font-size':'17px' }), 
    dcc.RangeSlider(0, 30, 3,
    value=[0,10],
    id='antiguedad',
    tooltip={"placement": "bottom", "always_visible": True}
    )], style={'width':'48%','float': 'left','display': 'inline-block'} ),
    
    html.Div([
    html.Label('Estacionamientos', style={'color':'black','font-size':'17px' }), 
    dcc.RangeSlider(0, 10, 1,
    value=[0,4],
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

    df1 = df[ (df['Recamaras'].isnull()) | (df['Recamaras'] <= habitacion[1]) ]
    df2 = df1[ (df1['Recamaras'].isnull()) | (df1['Recamaras'] >= habitacion[0]) ]
    df3 = df2[ (df2['Baños'].isnull()) | (df2['Baños'] <= tipo_baño_[1]) ]
    df4 = df3[(df3['Baños'].isnull()) | (df3['Baños'] >= tipo_baño_[0])]
    df5 = df4[ (df4['Precios'].isnull()) | (df4['Precios'] <= precio_[1]) ]
    df6 = df5[ (df5['Precios'].isnull()) | (df5['Precios'] >= habitacion[0]) ]
    df7 = df6[ (df6['Metros_construidos'].isnull()) | (df6['Metros_construidos'] <= m_construidos[1]) ]
    df8 = df7[ (df7['Metros_construidos'].isnull()) | (df7['Metros_construidos'] >= m_construidos[0]) ]
    df9 = df8[ (df8['Metros_totales'].isnull()) | (df8['Metros_totales'] <= m_totales[1]) ]
    df10 = df9[ (df9['Metros_totales'].isnull()) | (df9['Metros_totales'] >= m_totales[0]) ]
    df11 = df10[ (df10['Antiguedad'].isnull()) | (df10['Antiguedad'] <= antiguedad[1]) ]
    df12 = df11[(df11['Antiguedad'].isnull()) | (df11['Antiguedad'] >= antiguedad[0])]
    df13 = df12[ (df12['Estacionamientos'].isnull()) | (df12['Estacionamientos'] <= estacionamientos[1]) ]
    df14 = df13[(df13['Estacionamientos'].isnull()) | (df13['Estacionamientos'] >= estacionamientos[1])]

    if zona_selec:
        
        for zona in zona_selec:
            zona_selec = zona
            
            df15 = df14[ df14['Estado'] == f'{est_selec[0]}']
            df16 = df15[ df15['Municipio'] == f'{mun_selec[0]}' ]
            df17 = df16[df16['Zona'] == f'{zona_selec}']
            list_lat = df17["Latitud"].tolist()
            list_long = df17["Longitud"].tolist()
            
            #Marcamos en el mapa
            tipo = df17['Tipo'].tolist()
            precio = df17['Precios'].tolist()
            habitaciones = df17['Recamaras'].tolist()
            baños = df17['Baños'].tolist()
            totm2 = df17['Metros_totales'].tolist()
            constm2 = df17['Metros_construidos'].tolist()
            direccion = df17['Direcciones'].tolist()
            antiguedad = df17['Antiguedad'].tolist()
            estacionamientos = df17['Estacionamientos'].tolist()

            for i in range(len(list_lat)):


                if math.isnan(habitaciones[i]) == True:
                    habitaciones[i] = 'No disponible'
                else:
                    habitaciones[i] =int(habitaciones[i])
                if math.isnan(baños[i]) == True:
                    baños[i] = 'No dispinoble'
                else:
                    baños[i]=int(baños[i])
                if math.isnan(totm2[i]) == True:
                    totm2[i] = 'No disponible'
                else:
                    totm2[i]=str(int(totm2[i]))+' m²'
                if math.isnan(constm2[i]) == True:
                    constm2[i] = 'No disponible'
                else:
                    constm2[i]=str(int(constm2[i]))+' m²'
                if math.isnan(antiguedad[i]) == True:
                    antiguedad[i] = 'No disponible'
                else:
                    antiguedad[i]=str(int(antiguedad[i])) + ' años'
                if math.isnan(estacionamientos[i]) == True:
                    estacionamientos[i] = 'No disponible'
                else:
                    estacionamientos[i]=int(estacionamientos[i])

                if tipo[i] == 'Casa':
                    folium.Marker([list_lat[i], list_long[i]],popup = f'<h1>{locale.currency( precio[i], grouping=True )} MXN</h1> <br> <h2>Casa</h2> <h4>Metros totales: {totm2[i]} </h4> <h4>Metros construidos: {constm2[i]} </h4> <h4>Antiguedad: {antiguedad[i]} </h4> <h4>Estacionamientos: {estacionamientos[i]} </h4> <h4>Habitaciones: {habitaciones[i]}</h4> <h4>Baños: {baños[i]}</h4> <h6>{direccion[i]}</h6> ', icon = folium.Icon(color = "red")).add_to(map)
                if tipo[i]=='Departamento':
                    folium.Marker([list_lat[i], list_long[i]],popup = f'<h1>{locale.currency(precio[i], grouping=True )} MXN</h1> <br> <h2>Departamento</h2> <h4>Metros totales: {totm2[i]} </h4> <h4>Metros construidos: {constm2[i]} </h4> <h4>Antiguedad: {antiguedad[i]} </h4> <h4>Estacionamientos: {estacionamientos[i]} </h4> <h4>Habitaciones: {habitaciones[i]}</h4> <h4>Baños: {baños[i]}</h4> <h6>{direccion[i]}</h6> ', icon = folium.Icon(color = "darkblue")).add_to(map)
            map.save("casas_depas.html")

        return open('casas_depas.html','r',encoding="utf-8-sig").read()
  

    
    map.save("casas_depas.html")
    return open('casas_depas.html','r',encoding="utf-8-sig").read()


if __name__=="__main__":
    app.run_server(debug=True)