# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 16:37:32 2022

@author: Prateek

Dashboard to view Greater Sydney property market stats
"""

import sqlite3
import numpy as np
import math
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


con = sqlite3.connect('Suburb_names.db')
suburbs = pd.read_sql('SELECT * FROM SubNames' , con)
sydney_subs = suburbs[suburbs['SA4 Name'].str.contains('Sydney - ')].reset_index(drop=True)

suburb_dict = dict(zip( sydney_subs['Locality']+ ' [' +sydney_subs['Postcode'].astype(str)+']' , '['+sydney_subs['Locality']+']'))


bedrooms = pd.DataFrame([['1 Bedroom', '1'],['2 Bedrooms', '2'],
                         ['3 Bedrooms', '3'],['4 Bedrooms', '4'],
                         ['5 Bedrooms', '5']],
                         columns=['Label', 'Value'])

bed_dict = dict(zip(bedrooms['Label'], bedrooms['Value']))

type_dict = {"Apartment": "Unit", "House": "House"}

demo_dict = {'Modes of Transport to Work':'Transport','Occupation':'Occupation',
             'Weekly Rent ($)':'Rent','Religion':'Religion',
             'Weekly Household Income ($)':'Income',
             'Age':'Age','Marital Status':'MaritalStatus',
             'Country of Birth':'CountryOfBirth','Education':'Education',
             'Type of Occupancy':'Occupancy'}

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    
    dbc.Row([dbc.Col(html.Hr(style={"height":"1px",
                                    "color":"rgb(37,202,160)",
                                    "background": "rgb(37,202,160)",
                                    "margin-left":"20%",
                                    'width':'60%',
                                    "margin-bottom":"15px",
                                    "margin-top":"40px"}))]),
    
    dbc.Row([dbc.Col(html.H2('Greater Sydney Property Market Dashboard', 
                             style = {'font-family':"Candara",
                                      'font-size': '26px',
                                      "text-align": "center"}))]),
    
    dbc.Row([dbc.Col(html.Hr(style={"height":"2px",
                                    "color":"rgb(249,91,58)",
                                    "margin-left":"34%",
                                    'width':'32%',
                                    "margin-top":"5px",
                                    "margin-bottom":"50px"}))]),
    
    dbc.Row([
        dbc.Col([ html.Label(['Select Suburb'], 
                             style={'font-family':"Candara",
                                    'font-size': '20px',
                                    "text-align": "center",
                                    "marginLeft":'20px'})]),
        dbc.Col([ html.Label(['Select Number of Bedrooms'], 
                             style={'font-family':"Candara",
                                    'font-size': '20px', 
                                    "text-align": "center",
                                    "marginLeft":'20px'})]),
        dbc.Col([ html.Label(['Select Property Type'], 
                             style={'font-family':"Candara",
                                    'font-size': '20px', 
                                    "text-align": "center",
                                    "marginLeft":'20px'})]),
        ],justify = 'center'),
    
    dbc.Row([
        dbc.Col([ dcc.Dropdown(
                id='dropdown1',
                options=[{'label':label, 'value': value} for label, value in suburb_dict.items()], 
                value = '[Alexandria]',
                placeholder="Select Suburb",
                
                style=dict(
                    verticalAlign="middle",
                    marginLeft ='10px',
                    width='95%',
                    )),
                ]),
        
        dbc.Col([ dcc.Dropdown(
                id='dropdown2',
                options=[{'label':label, 'value': value} for label, value in bed_dict.items()], 
                value = '2',
                placeholder="Select Bedrooms",
                style=dict(
                    verticalAlign="middle",
                    marginLeft ='10px',
                    width='95%'
                    )),
                ]),
        
        dbc.Col([ dcc.Dropdown(
                id='dropdown3',
                options=[{'label':label, 'value': value}for label, value in type_dict.items()], 
                value = 'Unit',
                placeholder="Select Property Type",
                style=dict(
                    verticalAlign="middle",
                    marginLeft ='10px',
                    width='95%'
                    ))
                ]),
            ],justify = 'start'),
          

        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id="graph_price")],
                    style = {'float':'left', 
                             'width':'95%',
                             "margin-top":"30px"})
                ]),
        
            dbc.Col([
                html.Div([
                    dcc.Graph(id="graph_rent")],
                    style = {'float':'right',
                             "margin-right":"15px",
                             'width':'90%',
                             "margin-top":"30px"})
                ]),
            ]),
        
        
        dbc.Row([dbc.Col(html.H2('Demographic Information (2021 Census)', 
                                 style = {'font-family':"Candara",
                                          'font-size': '22px',
                                          "text-align": "center",
                                          "margin-bottom":"50px",
                                          "margin-top":"30px"}))]),
        
        
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                        id='dropdown4',
                        options=[{'label':label, 'value': value} for label, value in demo_dict.items()], 
                        value = 'Rent',
                        placeholder="Select Demographic Information",
                        style=dict(
                            verticalAlign="middle",
                            marginLeft ='12%',
                            width='70%'
                            ))
                ]),
        
            dbc.Col([
                dcc.Dropdown(
                        id='dropdown5',
                        options=[{'label':label, 'value': value} for label, value in demo_dict.items()], 
                        value = 'Income',
                        placeholder="Select Demographic Information",
                        style=dict(
                            verticalAlign="middle",
                            marginLeft ='15%',
                            width='70%'
                            ))
                ]),
            ]),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id="graph_demo1")],
                    style = {'float':'left', 
                             'width':'95%',
                             "margin-bottom":"50px"})
                ]),
        
            dbc.Col([
                html.Div([
                    dcc.Graph(id="graph_demo2")],
                    style = {'float':'right', 
                             'width':'95%',
                             "margin-bottom":"50px",
                             "margin-left":"50px"})
                ]),
            ]),
        
        dbc.Row([dbc.Col(html.Hr(style={"height":"1px",
                                        "color":"rgb(37,202,160)",
                                        "background": "rgb(37,202,160)",
                                        "margin-left":"20%",
                                        'width':'60%',
                                        "margin-top":"15px"}))]),
        
])

@app.callback(
    Output("graph_price", "figure"), 
    [Input('dropdown1', 'value'),
    Input('dropdown2', 'value'),
    Input('dropdown3', 'value')
    ])

def price_plot(dropdown1, dropdown2, dropdown3):
    locality = dropdown1
    bedrooms = dropdown2
    prop_type = dropdown3
    
    if prop_type == 'Unit':
        conn = sqlite3.connect('Unit_Data.db')
    else:
        conn = sqlite3.connect('House_Data.db')
    
    query = f'SELECT * FROM {locality}  WHERE bedrooms IS {bedrooms}'    
    df = pd.read_sql(query , conn)
    
    fig = fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index[:], 
                             y=df['medianSoldPrice'], 
                             mode='lines+markers', 
                             name="Median Sold Price",
                             line_color = 'rgb(37,202,160)')),
    
    fig.add_trace(go.Scatter(x=df.index[:], 
                             y=df['medianSaleListingPrice'],
                             mode='lines+markers',
                             name="Median Listing Price",
                             line=dict(color='rgb(37,202,160)',
                                       dash='dot'))),
    
    fig.add_trace(go.Scatter(x=df.index[:], 
                             y=df['75thPercentileSoldPrice'],
                             mode='lines+markers',
                             name="75th Percentile Price",
                             line_color = 'rgb(279,179,71)')),
    fig.add_trace(go.Scatter(x=df.index[:], 
                             y=df['95thPercentileSoldPrice'],
                             mode='lines+markers',
                             name="95th Percentile Price",
                             line_color = 'rgb(249,91,58)')),
    

    
    fig.update_layout(
        autosize=True,
        height=500,
        title='Prices',
        title_x=0.4,
        titlefont = dict(size=22),
        yaxis_title='Price ($)',
        plot_bgcolor='rgba(51,61,71,0)',
        font_family="Candara",
        legend = dict(
            font = dict(size = 16)),
        yaxis = dict(
            tickfont = dict(size=16),
            titlefont = dict(size=18),
            linecolor='rgba(51,61,71,0.4)',
            gridcolor='rgba(51,61,71,0.1)',
            showline=True,
            mirror=True,
            linewidth=2,
            gridwidth = 1
            ),
        xaxis = dict(
            tickfont = dict(size=16),
            tickvals = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
            ticktext = ['2019 [Q1]','2019 [Q2]','2019 [Q3]','2019 [Q4]',
                        '2020 [Q1]','2020 [Q2]', '2020 [Q3]','2020 [Q4]',
                        '2021 [Q1]','2021 [Q2]', '2021 [Q3]','2021 [Q4]',
                        '2022 [Q1]','2022 [Q2]', '2022 [Q3]','2022 [Q4]'],
            linecolor='rgba(51,61,71,0.4)',
            gridcolor='rgba(51,61,71,0.1)',
            showline=True,
            mirror=True,
            linewidth=2,
            gridwidth = 1,
            range=[0, 15]
            ),
        )
    
    return fig

@app.callback(
    Output("graph_rent", "figure"), 
    [Input('dropdown1', 'value'),
    Input('dropdown2', 'value'),
    Input('dropdown3', 'value')
    ])

def rent_plot(dropdown1, dropdown2, dropdown3):
    locality = dropdown1
    bedrooms = dropdown2
    prop_type = dropdown3
    
    if prop_type == 'Unit':
        conn = sqlite3.connect('Unit_Data.db')
    else:
        conn = sqlite3.connect('House_Data.db')
    
    query = f'SELECT * FROM {locality}  WHERE bedrooms IS {bedrooms}'
    df = pd.read_sql(query , conn)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index[:], 
                             y=df['medianRentListingPrice'], 
                             mode='lines+markers', 
                             name="Median Rent",
                             line_color = 'rgb(37,202,160)')),
    
    fig.add_trace(go.Scatter(x=df.index[:], 
                             y=df['highestRentListingPrice'],
                             mode='lines+markers',
                             name="Highest Rent",
                             line_color = 'rgb(249,91,58)')),
    
    
    fig.update_layout(
        autosize = True,
        height = 500,
        title ='Rents',
        title_x = 0.42,
        titlefont = dict(size=22),
        yaxis_title ='Weekly Rent ($)',
        plot_bgcolor ='rgba(51,61,71,0)',
        font_family ="Candara",
        legend = dict(
            font = dict(size = 16)),
        yaxis = dict(
            tickfont = dict(size=16),
            titlefont = dict(size=18),
            linecolor ='rgba(51,61,71,0.4)',
            gridcolor ='rgba(51,61,71,0.1)',
            showline = True,
            mirror=True,
            linewidth=2,
            gridwidth = 1
            ),
        xaxis = dict(
            linecolor ='rgba(51,61,71,0.4)',
            gridcolor ='rgba(51,61,71,0.1)',
            showline = True,
            mirror=True,
            linewidth=2,
            gridwidth = 1,
            range=[0, 15],
            tickfont = dict(size=16),
            tickvals = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
            ticktext = ['2019 [Q1]','2019 [Q2]', '2019 [Q3]','2019 [Q4]',
                        '2020 [Q1]','2020 [Q2]', '2020 [Q3]','2020 [Q4]',
                        '2021 [Q1]','2021 [Q2]', '2021 [Q3]','2021 [Q4]',
                        '2022 [Q1]','2022 [Q2]', '2022 [Q3]','2022 [Q4]']
            ),
        )
    
    return fig

@app.callback(
    Output("graph_demo1", "figure"), 
    [Input('dropdown1', 'value'),
    Input('dropdown4', 'value')
    ])

def demo_plot1(dropdown1,dropdown4):
    
    locality = dropdown1[1:-1].upper()
    demo = dropdown4
    conn = sqlite3.connect('Demographic_data.db')
    query = f'SELECT * FROM {demo}'
    df = pd.read_sql(query , conn)
    df = df[df['suburb']==f'{locality}']
    df = df.drop(['suburb'], axis=1).reset_index(drop = 
                                                 True).sort_values(by=0, 
                                                                   ascending=False, 
                                                                   axis=1)
    if len(df.columns)>9:
        new_df = df.iloc[:,:9]
        others = list(df.sum(axis=1) - new_df.sum(axis=1))[0]
        new_df.insert(loc=9, column='Others', value=others)
        labels = (list(new_df.columns))
        values = (list(new_df.values[0]))
    else:
        labels = (list(df.columns))
        values = (list(df.values[0]))
    
    colors = ['#20a9ca','#1eb2be','#1dbbb2','#1bc3a5','#67be88','#b3b86a',
              '#ffb24c','#ff9944','#ff803c','#ff6633']
    
    if demo == 'CountryOfBirth':
        name = 'Country<br>of<br>Birth'
    elif demo == 'MaritalStatus':
        name = 'Marital<br>Status'
    elif demo == 'Income':
        name = 'Weekly<br>Household<br>Income ($)'
    elif demo == 'Rent':
        name = 'Weekly<br>Rent ($)'
    elif demo == 'Transport':
        name = 'Mode of<br>Transport<br>to Work'
    elif demo == 'Occupancy':
        name = 'Type<br>of<br>Occupancy'
    else:
        name = f'{demo}'
    
    colors_divider = math.floor(len(colors)/(len(labels)))
    
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=labels, 
                         values=values,
                         text = [f'({i} %)' for i in (np.round((values/sum(values))*100))],
                         textinfo='label+text', 
                         textposition='outside',
                         name = name,
                         textfont=dict(size=16),
                         hole = 0.4,
                         marker=dict(colors=colors[0::colors_divider],
                                     line=dict(color='#ffffff', width=3)),
                         sort=False,
                         showlegend=False,
                         hoverinfo="label+percent+name"
                         )),
    
    fig.update_layout(
        autosize = False,
        width = 650,
        height=650,
        margin = {"r":150,"l":150,"t":150, "b":150},
        font_family = "Candara",
        uniformtext_minsize=16, 
        uniformtext_mode='hide',
        annotations=[dict(text=name, 
                          x=0.5, 
                          y=0.5, 
                          font_size=18, 
                          showarrow=False,
                          font_family ="Candara")]
        )
    
    
    return fig

@app.callback(
    Output("graph_demo2", "figure"), 
    [Input('dropdown1', 'value'),
    Input('dropdown5', 'value')
    ])

def demo_plot2(dropdown1,dropdown5):
    
    locality = dropdown1[1:-1].upper()
    demo = dropdown5
    conn = sqlite3.connect('Demographic_data.db')
    query = f'SELECT * FROM {demo}'
    df = pd.read_sql(query , conn)
    df = df[df['suburb']==f'{locality}']
    df = df.drop(['suburb'], axis=1).reset_index(drop = 
                                                 True).sort_values(by=0, 
                                                                   ascending=False, 
                                                                   axis=1)
    
    if len(df.columns)>9:
        new_df = df.iloc[:,:9]
        others = list(df.sum(axis=1) - new_df.sum(axis=1))[0]
        new_df.insert(loc=9, column='Others', value=others)
        labels = (list(new_df.columns))
        values = (list(new_df.values[0]))
    else:
        labels = (list(df.columns))
        values = (list(df.values[0]))
    
    colors = ['#20a9ca','#1eb2be','#1dbbb2','#1bc3a5','#67be88','#b3b86a',
              '#ffb24c','#ff9944','#ff803c','#ff6633']
    
    colors_divider = math.floor(len(colors)/(len(labels)))
    
    if demo == 'CountryOfBirth':
        name = 'Country<br>of<br>Birth'
    elif demo == 'MaritalStatus':
        name = 'Marital<br>Status'
    elif demo == 'Income':
        name = 'Weekly<br>Household<br>Income ($)'
    elif demo == 'Rent':
        name = 'Weekly<br>Rent ($)'
    elif demo == 'Transport':
        name = 'Mode of<br>Transport<br>to Work'
    elif demo == 'Occupancy':
        name = 'Type<br>of<br>Occupancy'
    else:
        name = f'{demo}'
    
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=labels, 
                         values=values,
                         text = [f'({i} %)' for i in (np.round((values/sum(values))*100))],
                         textinfo='label + text', 
                         textposition='outside',
                         textfont=dict(size=16),
                         name = name,
                         hole = 0.4,
                         marker=dict(colors=colors[0::colors_divider],
                                     line=dict(color='#ffffff', width=3)),
                         sort=False,
                         showlegend=False,
                         hoverinfo="label+percent+name"
                         )),
    
    fig.update_layout(
        autosize = False,
        width = 650,
        height=650,
        margin = {"r":150,"l":150,"t":150, "b":150},
        font_family = "Candara",
        uniformtext_minsize=12, uniformtext_mode='hide',
        annotations=[dict(text=name, 
                          x=0.5, 
                          y=0.5, 
                          font_size=18, 
                          showarrow=False,
                          font_family ="Candara")]
        )
    
    return fig

app.run_server(debug=True)

