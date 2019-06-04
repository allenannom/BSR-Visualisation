import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True
df = pd.read_csv('D:/Downloads/visualise/completebook.csv')

#filter by country dropdown options
country_filter = df['place_of_birth'].unique()
country_filter = np.insert(country_filter,0,'All Countries')

#Chart dropdown options with filter by
all_options = {
    'Gender': ['Age Group','Region'],
    'Turban Wearing': ['Age Group','Region','Place of Birth',],
	'How voted in EU referendum 2016': ['Age Group','Region','Turban Wearing','View of  result of  referendum to leave  EU (Brexit)?']
}

#2018 Dataset and country headers
df_2018 = pd.read_csv('D:/Downloads/visualise/2018book.csv')
country_filter_2018 = df_2018['1. Place of birth'].unique()
country_filter_2018 = np.insert(country_filter_2018,0,'All Countries')
#empty layout, app callback handles page change
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#home page 
index_page = html.Div([
	html.H1('BRITISH SIKH CHARITY'),
		html.Div([
			html.Div(
			className="image_header",
			children=[
				html.Img(src='/assets/logo1.png'),
				
			]),
			
		]),
		html.Div([
			html.Div(
			className="button_link",
			children=[
				dcc.Link('2017 Data', href='/page-1'),
				html.A("BSR Home Page", href='http://www.britishsikhreport.org/', target="_blank"),	
			dcc.Link('2018 Data', href='/page-2'),
			]),
			
		]),
    

])

#2017 Dataset page
page_1_layout = html.Div([
    
	html.Div(
	className="navigation_bar",
	children=[

        html.Div([
		html.H3('Select Chart'),
            dcc.Dropdown(
                id='chart_name',
                options=[{'label': i, 'value': i} for i in all_options],
                value='How voted in EU referendum 2016',),],
        style={'width': '25%', 'display': 'inline-block','padding':'0px 30px 20px 0px'}),
		html.Div([
			html.H3('Filter by'),
			dcc.Dropdown(id='chart_filter'),
        ],
        style={'width': '25%', 'display': 'inline-block','padding':'0px 30px 20px 0px'}),
		
		html.Div([
			html.H3('Filter by Country'),
			dcc.Dropdown(
                id='country_dropdown',
                options=[{'label': i, 'value': i} for i in country_filter],
                value='All Countries',
            ),
        ],style={'width': '25%', 'display': 'inline-block','padding':'0px 0px 20px 0px'}),
		html.Div(
		className="grouped_logo",
		children=[
			html.H1('2017 BSR'),
			html.Img(src='/assets/logo1.png'),
        ],style={'width': '20%', 'display': 'inline-block', 'position':'relative', 'text-align':'right'}),
    ]),
	html.Hr(),
    dcc.Graph(id='indicator-graphic'),
    html.Div(id='page-1-content'),
    html.Br(),
	html.Div(
	className="button_link",
	children=[dcc.Link('Go back to Home', href='/'),])
    

])

page_2_layout = html.Div([
    
	html.H1('2017 BSR'),

])

from callbacks_2017 import *	

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
	if pathname == '/page-1':
		return page_1_layout
	elif pathname == '/page-2':
		return page_2_layout
	else:
		return index_page
    # You could also return a 404 "URL not found" page here



if __name__ == '__main__':
    app.run_server(debug=True)