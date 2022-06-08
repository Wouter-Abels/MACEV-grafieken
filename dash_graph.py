import plotly.express as px
from dash import dcc, html, dash, dash_table
import numpy as np
import pandas as pd
import datetime
from assets.graph import graphs
from assets.validation import validations
from dash.dependencies import Input, Output

#---------------------------------------------
# File: dash_graph.py
# Author: Wouter Abels (wouter.abels@rws.nl)
# Created: 21/02/22
# Last modified: 08/06/22
# Python ver: 3.9.7
#---------------------------------------------

# Load data
historic_and_current = pd.read_csv('assets/historic_and_data.csv')
historic_and_current['externalreference'] = historic_and_current['externalreference'].astype(str)
current_data = historic_and_current.loc[historic_and_current['measurementdate'] >= '2021']
historic_data = historic_and_current.loc[historic_and_current['measurementdate'] <= '2021']
total_plot_data = graphs.value_per_year(historic_and_current)
unique_measurementobject = np.sort(pd.unique(historic_and_current['measurementobjectname']))

# Build App
app = dash.Dash(__name__, title='MACEV Grafieken')
app.layout =html.Div([
        html.H1('Macroevertebraten Abundantie'),
        html.H2('2015-2021'),
        dcc.RadioItems(id= 'abundance_radio',
        options= [
            {'label': 'Totale Abundantie', 'value': 'Totale Abundantie'},
            {'label': 'Relatieve Abundantie', 'value': 'Relatieve Abundantie',}],
            value= 'Totale Abundantie',
            labelStyle={'display': 'inline-block'},
            style= dict(display='flex',
            justifyContent='center')),
        dcc.Graph(id= 'abundance_graph'),
        html.P('Abundantie per meetobject'),
        dcc.Dropdown(id= 'object_dropdown',
        options= [
            {'label': i, 'value': i} for i in unique_measurementobject], value= unique_measurementobject[0]),
        dcc.Graph(id= 'object_graph'),
        html.P('Validatie tabellen'),
        dcc.Dropdown(id= 'table_dropdown',
        options= [
            {'label': 'Collectienummer Validatie', 'value': 'collectie'},
            {'label': 'Taxonstatus Validatie', 'value': 'taxonstatus'},
            {'label': 'Oligochaeten Validatie', 'value': 'oligochaeten'},
            {'label': 'Chironomiden Validatie', 'value': 'chironomiden'},
            {'label': 'Taxongroep Validatie', 'value': 'taxongroep'},
            {'label': 'Factor Validatie', 'value': 'factor'},
            {'label': 'Missende Taxa', 'value': 'missend'},
            {'label': 'Nieuwe Taxa', 'value': 'nieuw'}],
            value='collectie'),
        dash_table.DataTable(id= 'table_object',
        columns=[{'name': i, 'id':i} for i in historic_and_current.columns],
        sort_action='native',
        filter_action='native'),
        html.Footer('Wouter Abels (wouterabels@rws.nl) 24 Mei 2022 Python 3.9.7')
        ])

@app.callback(
    Output('abundance_graph', 'figure'),
    Input('abundance_radio', 'value'),
    )

def graph_total_update(dropdown_value):
    fig = px.bar(total_plot_data, color_discrete_map=graphs.macev_taxongroup_colours, title='Totale Abundantie', template='simple_white', orientation='h', labels={'value': 'Totale Abundantie (n)', 'index': 'Jaar', 'Taxongroup': 'Taxongroep'})
    fig1 = px.bar(total_plot_data.apply(lambda x: x*100/sum(x),axis=1), color_discrete_map=graphs.macev_taxongroup_colours, title='Relatieve Abundantie', template='simple_white', orientation='h', labels={'value': 'Relatieve Abundantie (%)', 'index': 'Jaar', 'Taxongroup': 'Taxongroep'})
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
                object_plot_data = graphs.relative_data_location_per_year(historic_and_current, dropdown_object)
                fig2 = px.bar(object_plot_data,
                color_discrete_map=graphs.macev_taxongroup_colours,
                title='Totale Abundantie meetobject: '+ str(dropdown_object),
                template='simple_white',
                orientation='h',
                labels={'value': 'Totale Abundantie (n)', 'index': 'Jaar', 'Taxongroup': 'Taxongroep'})
                return fig2
        elif dropdown_value == 'Relatieve Abundantie':
            if object == dropdown_object:
                object_plot_data = graphs.relative_data_location_per_year(historic_and_current, dropdown_object)
                fig3 = px.bar(object_plot_data.apply(lambda x: x*100/sum(x),axis=1),
                color_discrete_map=graphs.macev_taxongroup_colours,
                title='Relatieve Abundantie meetobject: '+ str(dropdown_object),
                template='simple_white',
                orientation='h',
                labels={'value': 'Relatieve Abundantie (%)', 'index': 'Jaar', 'Taxongroup': 'Taxongroep'})
                return fig3

@app.callback(
    Output('table_object', 'data'),
    Input('table_dropdown', 'value'),
)

def table_update(dropdown_value):
    if dropdown_value == 'collectie':
        return validations.collection(current_data).to_dict('records')
    elif dropdown_value == 'taxonstatus':
        return validations.taxonstatus(current_data).to_dict('records')
    elif dropdown_value == 'oligochaeten':
        return validations.oligochaeta(current_data).to_dict('records')
    elif dropdown_value == 'chironomiden':
        return validations.chironomidae(current_data).to_dict('records')
    elif dropdown_value == 'taxongroep':
        return validations.taxongroup(current_data).to_dict('records')
    elif dropdown_value == 'factor':
        pass
    elif dropdown_value == 'missend':
        pass
    elif dropdown_value == 'nieuw':
        pass

# Run app
if __name__ == '__main__':
    app.run_server()