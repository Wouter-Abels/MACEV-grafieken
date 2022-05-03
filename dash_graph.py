import plotly.express as px
from dash import dcc, html, dash
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

#---------------------------------------------
# File: dash_test.ipynb
# Author: Wouter Abels (wouter.abels@rws.nl)
# Created: 21/02/22
# Last modified: 04/04/22
# Python ver: 3.9.7
#---------------------------------------------

# Load data
total_plot_data = pd.read_csv('aquadash_v2/assets/total_plot_data.csv')
historic_and_data = pd.read_csv('aquadash_v2/assets/historic_and_data.csv')
unique_measurementobject = np.sort(pd.unique(historic_and_data['measurementobjectname']))
macev_taxongroup_colours = {
    'Annelida/Platyhelminthes - Hirudinea':'aqua', \
    'Annelida/Platyhelminthes - Polychaeta':'skyblue', \
    'Annelida/Platyhelminthes - Oligochaeta':'dodgerblue', \
    'Annelida/Platyhelminthes - Turbellaria':'darkblue', \
    'Arachnida':'dimgray', \
    'Bryozoa - Hydrozoa - Porifera':'lightgrey', \
    'Crustacea - Amphipoda':'pink', \
    'Crustacea - Decapoda':'magenta', \
    'Crustacea - Isopoda':'violet', \
    'Crustacea - Mysida':'purple', \
    'Crustacea - Remaining':'blueviolet', \
    'Echinodermata':'ivory', \
    'Insecta (Diptera) - Chironomidae':'orange', \
    'Insecta (Diptera) - Remaining':'limegreen', \
    'Insecta (Diptera) - Simuliidae':'green', \
    'Insecta - Coleoptera':'lawngreen', \
    'Insecta - Ephemeroptera':'seagreen', \
    'Insecta - Heteroptera':'darkolivegreen', \
    'Insecta - Lepidoptera':'mediumspringgreen', \
    'Insecta - Odonata':'greenyellow', \
    'Insecta - Remaining':'palegreen', \
    'Insecta - Trichoptera':'yellowgreen', \
    'Marien - Remaining':'dimgrey', \
    'Mollusca - Bivalvia':'yellow', \
    'Mollusca - Gastropoda':'gold', \
    'Collembola':'black'
    }

# Divide dataset per year and calculate relative distribution per year, return te values from series to a dataframe and reset the first column to index and add column titles remove empty columns with only 0 values
def value_per_year(relative_data_location_year):
    years = ['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']
    dataperyear = {}
    for year in years:
        dataperyear[year] = relative_data_location_year[relative_data_location_year['collectiondate']\
            .str\
            .contains(year)]\
            .groupby('name_tg')['calculatedvalue']\
            .sum()\
            .astype(int)\
            .to_frame()\
            .rename_axis('Taxongroup')\
            .rename(columns={'calculatedvalue':year})
    dataperyear = pd.concat(dataperyear, join='outer', axis=1)\
        .fillna(0)\
        .astype(int)
    dataperyear = dataperyear.loc[:, (dataperyear!=0)\
        .any(axis=0)]
    dataperyear.columns = dataperyear.columns.droplevel()
    dataperyear = dataperyear.T
    return dataperyear

# Divide data per location
def data_location(historic_and_data, object):
    datalocation = historic_and_data[historic_and_data["measurementobjectname"].str.contains(object)]
    return datalocation


def relative_data_location_per_year(object, historic_and_data):
    relative_data_location_year = data_location(object, historic_and_data) 
    relative_data_location_year = value_per_year(relative_data_location_year)
    relative_data_location_year = relative_data_location_year
    return relative_data_location_year

# Build App
app = dash.Dash(__name__)
app.layout =html.Div([
        html.H1('MACEV data 2015-2021'),
        dcc.RadioItems(id='abundance_radio', options= [{'label': 'Totale Abundantie', 'value':'Totale Abundantie'},{'label': 'Relatieve Abundantie', 'value': 'Relatieve Abundantie',}], value= 'Totale Abundantie', labelStyle={'display': 'inline-block'}),
        dcc.Graph(id= 'abundance_graph'),
        dcc.Dropdown(id= 'object_dropdown', options=[{'label': i, 'value': i} for i in unique_measurementobject], value= unique_measurementobject[0]),
        dcc.Graph(id= 'object_graph')
        ])

@app.callback(
    Output('abundance_graph', 'figure'),
    Input('abundance_radio', 'value'),
    )

def graph_total_update(dropdown_value):
    fig = px.bar(total_plot_data, color_discrete_map=macev_taxongroup_colours, title='Totale Abundantie', template='simple_white', orientation='h', labels={'value': 'Totale Abundantie (n)', 'index': 'Jaar', 'Taxongroup': 'Taxongroep'})
    fig1 = px.bar(total_plot_data.apply(lambda x: x*100/sum(x),axis=1), color_discrete_map=macev_taxongroup_colours, title='Relatieve Abundantie MACEV 2021-2015', template='simple_white', orientation='h', labels={'value': 'Relatieve Abundantie (%)', 'index': 'Jaar', 'Taxongroup': 'Taxongroep'})
    if dropdown_value == 'Totale Abundantie':
        return fig
    elif dropdown_value == 'Relatieve Abundantie':
        return fig1

@app.callback(
    Output('object_graph', 'figure'),
    Input('object_dropdown', 'value'),
    Input('abundance_radio', 'value'),
    )

def graph_object_update(dropdown_object, dropdown_value):
    for object in unique_measurementobject:
        if dropdown_value =='Totale Abundantie':
            if object == dropdown_object:
                object_plot_data = relative_data_location_per_year(historic_and_data, dropdown_object)
                fig2 = px.bar(object_plot_data, color_discrete_map=macev_taxongroup_colours, title='Totale Abundantie meetobject: '+ str(dropdown_object), template='simple_white', orientation='h', labels={'value': 'Totale Abundantie (n)', 'index': 'Jaar', 'Taxongroup': 'Taxongroep'})
                return fig2
        if dropdown_value == 'Relatieve Abundantie':
            if object == dropdown_object:
                object_plot_data = relative_data_location_per_year(historic_and_data, dropdown_object)
                fig3 = px.bar(object_plot_data.apply(lambda x: x*100/sum(x),axis=1), color_discrete_map=macev_taxongroup_colours, title='Relatieve Abundantie meetobject: '+ str(dropdown_object), template='simple_white', orientation='h', labels={'value': 'Relatieve Abundantie (%)', 'index': 'Jaar', 'Taxongroup': 'Taxongroep'})
                return fig3

# Run app
app.run_server(debug=True)