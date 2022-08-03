import numpy as np
import pandas as pd
import dash_leaflet as dl
import plotly.express as px
from classes.LoadData import LoadData
from classes.Graph import Graphs
from classes.Validation import Validations
from dash import dcc, html, dash, dash_table, Input, Output

#---------------------------------------------
# File: dash_graph.py
# Author: Wouter Abels (wouter.abels@rws.nl)
# Created: 21/02/22
# Last modified: 01/08/22
# Python ver: 3.10.4
#---------------------------------------------

## Load data ##
# JSON geodata of measurementobjects RWS
geo_data = LoadData.geo_data()

#MACEV data from 2015 till 2021
current_data, historic_data, unique_measurementobject, historic_and_current = LoadData.macev_data()


# Data for abundance plot
total_plot_data = Graphs.value_per_year(historic_and_current)


logo = ('IW_RW_Logo_online_pos_nl.png')
footer = 'Wouter Abels (wouterabels@rws.nl) 20 Juli 2022 Python 3.9.7'


## Build App ##
app = dash.Dash(__name__, title='Data Validatie')
app.layout = html.Div(id= 'app', children= [
    dcc.Location(id='url', refresh=False),
    html.Div(id='page_content')
    ]
)

# Index Page #
# Configure Index page and map with measurement locations
index_page = html.Div(
    id='index',
    children=[
        html.Div(
            id='navbar',
            children=[
                html.Header(
                    children=[
                        dcc.Link(
                            'Home', 
                            href='/', 
                            className='link_active'
                        ),
                        dcc.Link('Grafieken', 
                            href='/graphs', 
                            className='link'
                        ),
                        dcc.Link(   
                            'Validatie', 
                            href='/validation', 
                            className='link'
                        ),
                        dcc.Link(
                            'Statistiek', 
                            href='/statistics', 
                            className='link'
                        )
                    ]
                )
            ],
        ),
        html.Div(
            id='page',
            children=[
                html.Div(
                    id='index_text_map',
                    children=[
                        html.Div(
                            id='index_text',
                            children=[
                                html.H1(
                                    'Geautomatiseerde data-validatie van Macro-Evertebraten'
                                ),
                                html.P(
                                    'Dit rapport '
                                    'betreft de geautomatiseerde '
                                    'data-validatie methode '
                                    'voor het controleren van de '
                                    'data oplevering van '
                                    'perceel A, B '
                                    '(Randmeren en Trintelzand) en C (Maas).'
                                ),
                                html.P(
                                    'In dit rapport zijn de volgende '
                                    'validatie stappen uitgevoerd:'
                                ),
                                html.Ul(
                                    children=[
                                        html.Li(
                                            'Collectienummers zijn gevalideerd op '
                                            'notatie van het juiste jaartal.'
                                        ),
                                        html.Li(
                                            'Taxon statuscode van de gedetermineerde '
                                            'soorten worden gecontroleerd met de TWN lijst.'
                                        ),
                                        html.Li(
                                            'Voor de taxongroepen Oligochaeta en '
                                            'Chironomiden is er gevalideer '
                                            'of er wel minimaal 100 zijn gedetermineerd '
                                            'wanneer de berekende waarde 100 of hoger is.'
                                        ),
                                        html.Li(
                                            'Voor de resterende taxongroepen is een '
                                            'soortgelijke validatie uitgevoerd '
                                            'maar dan met minimaal 50 gedetermineerde '
                                            'individuen.'
                                        ),
                                        html.Li(
                                            'Er is gevalideerd wanneer er getallen met '
                                            'een factor worden doorgerekend '
                                            'of dit ook genoteerd is met een limietsymbool.'
                                        ),
                                        html.Li(
                                            'De nieuwe data wordt vergeleken met '
                                            'historische data van de afgelopen 6 jaar '
                                            'om te kijken of er soorten niet zijn '
                                            'gevonden bij deze metingen '
                                            'die wel in het verleden op de locaties '
                                            'zijn aangetroffen.'
                                        ),
                                        html.Li(
                                            'Ook wordt er gecontroleerd of er soorten '
                                            'zijn gevonden '
                                            'die nooit eerder op de meetlocaties zijn '
                                            'waargenomen.'
                                        ),
                                    ]
                                ),
                                html.P(
                                    'Verder is de data geplot, '
                                    'alle meetdata worden opgedeeld per taxongroep, '
                                    'meetjaar en op basis van meetlocatie. '
                                    'De verwerkte waarde worden omgerekend naar '
                                    'relatieve waarden '
                                    'om dit vervolgens tegen jaren uit te zetten in grafieken. '
                                    'Er wordt een overzichtsgrafiek geplot waar alle '
                                    'locatie bij elkaar worden genomen. '
                                    'Ook wordt alle data per meetlocatie geplot. In het '
                                    'totaal gaat het om 122 plots.'
                                ),
                                html.P('Wat er nog toegevoegd gaat worden:'),
                                html.Ul(
                                    children=[
                                        html.Li(
                                            'Controleren of de coördinaten van de '
                                            'meeting dichtbij genoeg zijn van het meetpunt.'
                                        ),
                                        html.Li(
                                            'Validatie van de sample volumes en oppervlaktes.'
                                        ),
                                        html.Li(
                                            'Statistische tests op de data uitvoeren,'
                                            ' om mogelijk wat te kunnen zeggen over '
                                            'correlaties door de jaren heen.'
                                        ),
                                        html.Li('Opmaak en leesbaarheid verbeteren.'),
                                    ]
                                ),
                            ],
                        ),
                        html.Div(
                            id='index_map',
                            children=[
                                dl.Map(
                                    center=[53, 5],
                                    zoom=7,
                                    children=[
                                        dl.TileLayer(),
                                        dl.GestureHandling(),
                                        dl.GeoJSON(
                                            data=geo_data,
                                            cluster=True,
                                            zoomToBoundsOnClick=True,
                                            superClusterOptions={
                                                'radius': 120,
                                                'extent': 250,
                                            },
                                        ),
                                    ],
                                )
                            ],
                        ),
                    ],
                ),
                html.Footer(footer),
                html.Img(id='logo', src=app.get_asset_url(logo)),
            ],
        ),
    ],
)


# Abbundance graphs page #
# Configure the page with the graphs
graph_page = html.Div(
    id='graph_page',
    children=[
        html.Div(
            id='navbar',
            children=[
                html.Header(
                    children=[
                        dcc.Link(
                            'Home', 
                            href='/', 
                            className='link'
                        ),
                        dcc.Link('Grafieken', 
                            href='/graphs', 
                            className='link_active'
                        ),
                        dcc.Link(   
                            'Validatie', 
                            href='/validation', 
                            className='link'
                        ),
                        dcc.Link(
                            'Statistiek', 
                            href='/statistics', 
                            className='link'
                        )
                    ]
                )
            ],
        ),
        html.Div(
            id='page',
            children=[
                html.Div(
                    id='graph_total',
                    children=[
                        html.H1('Macroevertebraten Abundantie'),
                        html.H2('2015-2021'),
                    ],
                ),
                html.H2('Grafieken'),
                html.Div(
                    id='abundance_radio',
                    children=[
                        dcc.RadioItems(
                            id='abundance_radio',
                            options=[
                                {
                                    'label': 'Totale Abundantie',
                                    'value': 'Totale Abundantie',
                                },
                                {
                                    'label': 'Relatieve Abundantie',
                                    'value': 'Relatieve Abundantie',
                                },
                            ],
                            value='Totale Abundantie',
                            labelStyle={'display': 'inline-block'},
                            style={'display': 'flex', 'justifyContent': 'center'},
                        )
                    ],
                ),
                dcc.Graph(id='abundance_graph'),
                html.H2('Abundantie per meetobject'),
                html.Div(
                    id='graph_dropdown_objects',
                    children=[
                        html.Div(
                            id='dropdown_objects',
                            children=[
                                dcc.Dropdown(
                                    id='object_dropdown',
                                    options=[
                                        {'label': i, 'value': i}
                                        for i in unique_measurementobject
                                    ],
                                    value=unique_measurementobject[0],
                                    clearable=False,
                                )
                            ],
                        ),
                        html.Div(
                            id='graph_objects', children=[dcc.Graph(id='object_graph')]
                        ),
                    ],
                ),
                html.Footer(footer),
                html.Img(id='logo', src=app.get_asset_url(logo)),
            ],
        ),
    ],
)

# App callback for the total or relative abundance graph
@app.callback(
    Output('abundance_graph', 'figure'),
    Input('abundance_radio', 'value'),
)

# Total abundace graph with its properties
def graph_total_update(dropdown_value):
    fig0 = px.bar(
        total_plot_data,
        color_discrete_map=Graphs.macev_taxongroup_colours,
        title='Totale Abundantie', template='simple_white',
        orientation='h',
        labels={
            'value': 'Totale Abundantie (n)', 
            'index': 'Jaar', 
            'Taxongroup': 'Taxongroep'
            }
    )
    fig1 = px.bar(
        total_plot_data.apply(lambda x: x*100/sum(x),axis=1),
        color_discrete_map=Graphs.macev_taxongroup_colours,
        title='Relatieve Abundantie',
        template='simple_white',
        orientation='h',
        labels={
            'value': 'Relatieve Abundantie (%)', 
            'index': 'Jaar', 
            'Taxongroup': 'Taxongroep'
            }
    )
    if dropdown_value == 'Totale Abundantie':
        return fig0
    elif dropdown_value == 'Relatieve Abundantie':
        return fig1

# App callback for the graphs dropdown and radio buttons
@app.callback(
    Output('object_graph', 'figure'),
    Input('object_dropdown', 'value'),
    Input('abundance_radio', 'value'),
)

# The properties of the graph per measurement object with abundance data
def graph_object_update(dropdown_object, dropdown_value):
    for object in unique_measurementobject:
        if dropdown_value =='Totale Abundantie':
            if object == dropdown_object:
                object_plot_data = Graphs.relative_data_location_per_year(
                    historic_and_current, dropdown_object)
                fig2 = px.bar(
                    object_plot_data,
                    color_discrete_map=Graphs.macev_taxongroup_colours,
                    title='Totale Abundantie meetobject: '+ str(dropdown_object),
                    template='simple_white',
                    orientation='h',
                    labels={
                        'value': 'Totale Abundantie (n)', 
                        'index': 'Jaar', 
                        'Taxongroup': 'Taxongroep'
                        }
                )
                return fig2
        elif dropdown_value == 'Relatieve Abundantie':
            if object == dropdown_object:
                object_plot_data = Graphs.relative_data_location_per_year(
                    historic_and_current, dropdown_object)
                fig3 = px.bar(
                    object_plot_data.apply(lambda x: x*100/sum(x),axis=1),
                    color_discrete_map=Graphs.macev_taxongroup_colours,
                    title='Relatieve Abundantie meetobject: '+ str(dropdown_object),
                    template='simple_white',
                    orientation='h',
                    labels={
                        'value': 'Relatieve Abundantie (%)', 
                        'index': 'Jaar', 
                        'Taxongroup': 'Taxongroep'
                        }
                )
                return fig3


# Data validation #
# Configure the validation page
validation_page = html.Div(
    children=[
        html.Div(
            id='navbar',
            children=[
                html.Header(
                    children=[
                        dcc.Link(
                            'Home', 
                            href='/', 
                            className='link'
                        ),
                        dcc.Link('Grafieken', 
                            href='/graphs', 
                            className='link'
                        ),
                        dcc.Link(   
                            'Validatie', 
                            href='/validation', 
                            className='link_active'
                        ),
                        dcc.Link(
                            'Statistiek', 
                            href='/statistics', 
                            className='link'
                        )
                    ]
                )
            ],
        ),
        html.Div(
            id='page',
            children=[
                html.H1('Macroevertebraten Abundantie'),
                html.H2('2015-2021'),
                html.H2('Validatie tabel'),
                html.Div(
                    id='dropdown_and_table',
                    children=[
                        dcc.Dropdown(
                            id='table_dropdown',
                            options=[
                                {
                                    'label': 'Collectienummer Validatie',
                                    'value': 'collection',
                                },
                                {
                                    'label': 'Taxonstatus Validatie',
                                    'value': 'taxonstatus',
                                },
                                {
                                    'label': 'Oligochaeten Validatie',
                                    'value': 'oligochaeta',
                                },
                                {
                                    'label': 'Chironomiden Validatie',
                                    'value': 'chironomidae',
                                },
                                {
                                    'label': 'Taxongroep Validatie',
                                    'value': 'taxongroup',
                                },
                                {
                                    'label': 'Factor Validatie', 
                                    'value': 'factor'
                                },
                                {
                                    'label': 'Missende Taxa',
                                    'value': 'missing'
                                },
                                {
                                    'label': 'Nieuwe Taxa', 
                                    'value': 'new'
                                },
                            ],
                            value='collection',
                        ),
                        dash_table.DataTable(     
                            id='table_object',
                            columns=[
                                {'name': i, 'id': i} for i in historic_and_current
                            ],
                            sort_action='native',
                            filter_action='native',
                            css=[
                                {
                                    'selector': '.previous-page, '
                                    '.next-page, .first-page, '
                                    '.last-page, .export, .show-hide',
                                    'rule': 'color: black;',
                                },
                                {
                                    'selector': '.current-page',
                                    'rule': 'padding-right: 5px;',
                                },
                            ],
                            style_cell={
                                'whiteSpace': 'normal',
                                'width': '100px',
                                'textAlign': 'center',
                                'height': '15px',
                                'padding-left': '10px',
                                'padding-right': '10px',
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                },
                            ],
                            style_table={
                                'height': 'auto',
                                'width': 'auto',
                                'overflowX': 'auto',
                                'overflowY': 'auto',
                            },
                            cell_selectable=False,
                            page_size=16,
                            style_as_list_view=True,
                        ),
                    ],
                ),
                html.Footer(footer),
                html.Img(id='logo', src=app.get_asset_url(logo)),
            ],
        ),
    ]
)

# Aap callback for the dropdown menu in validation page
@app.callback(
    Output('table_object', 'data'),
    Input('table_dropdown', 'value'),
)

# The table selections with validation data
def table_update(dropdown_value):
    current_data_validations = ['collection', 'taxonstatus', 'oligochaeta', 'chironomidae', 'taxongroup', 'factor']
    current_and_historic_data_validations = ['missing','new']
    if dropdown_value in current_data_validations:
        table_data = getattr(Validations, dropdown_value)
        return table_data(current_data).to_dict('records')
    elif dropdown_value in current_and_historic_data_validations:
        table_data = getattr(Validations, dropdown_value)
        return table_data(current_data, historic_data).to_dict('records')

statistics_page = html.Div(
    id='index',
    children=[
        html.Div(
            id='navbar',
            children=[
                html.Header(
                    children=[
                        dcc.Link(
                            'Home', 
                            href='/', 
                            className='link'
                        ),
                        dcc.Link('Grafieken', 
                            href='/graphs', 
                            className='link'
                        ),
                        dcc.Link(   
                            'Validatie', 
                            href='/validation', 
                            className='link'
                        ),
                        dcc.Link(
                            'Statistiek', 
                            href='/statistics', 
                            className='link_active'
                        )
                    ]
                )
            ],
        ),
        html.Div(
            id='page',
            children=[
                html.H1('Statistiek'),
                html.H2('In development')
        ]

        )
    ]
) 

## Pagination ##
# app callback for page selection in header
@app.callback(
    Output('page_content', 'children'),
    Input('url', 'pathname')
)


# Configure the multiple pages
def display_page(pathname):
    """Redirects webpage to selected page from navbar."""
    paths = {
        '/': index_page,
        '/graphs': graph_page,
        '/validation': validation_page,
        '/statistics': statistics_page,
    }
    return paths.get(pathname)

## Run app ##
if __name__ == '__main__':
    app.run_server()