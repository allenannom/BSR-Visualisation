import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import pycountry
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
country_filter_2017 = df['place_of_birth'].unique()
country_filter_2017 = np.insert(country_filter_2017,0,'All Countries')

#Chart dropdown options with filter by
all_options = {
    'Gender': ['Age Group','Region'],
    'Turban Wearing': ['Age Group','Region','Place of Birth',],
	'How voted in EU referendum 2016': ['Age Group','Region','Turban Wearing','View of  result of  referendum to leave  EU (Brexit)?']
}

all_options_2018 = {
    'Gender': ['Age Group','Region'],
    'Turban Wearing': ['Age Group','Region','Place of Birth',],
	'How often do you undertake spiritual practice?': ['Age Group','Gender','Turban Wearing']
}

#2018 Dataset and country headers
df_2018 = pd.read_csv('D:/Downloads/visualise/2018book.csv')
country_filter_2018 = df_2018['place_of_birth'].unique()
country_filter_2018 = np.insert(country_filter_2018,0,'All Countries')
#empty layout, app callback handles page change
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#home page 
index_page = html.Div(
	className="homepage", children=[
	html.H1('British Sikh Community'),
	html.Br(),
		html.Div([
			html.Div(
			className="image_header",
			children=[
				html.Img(src='/assets/logo1.png'),
				html.Br(),
				
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
                id='chart_name_2017',
                options=[{'label': i, 'value': i} for i in all_options],
                value='How voted in EU referendum 2016',),],
        style={'width': '25%', 'display': 'inline-block','padding':'0px 30px 20px 0px'}),
		html.Div([
			html.H3('Filter by'),
			dcc.Dropdown(id='chart_filter_2017'),
        ],
        style={'width': '25%', 'display': 'inline-block','padding':'0px 30px 20px 0px'}),
		
		html.Div([
			html.H3('Filter by Country'),
			dcc.Dropdown(
                id='country_dropdown_2017',
                options=[{'label': i, 'value': i} for i in country_filter_2017],
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
	#First chart
    dcc.Graph(id='indicator-graphic_2017'),
    html.Div(id='page-1-content'),
	#Second chart
	dcc.Graph(id='pie_chart'),
	html.Div(
	className="button_link",
	children=[dcc.Link('Go back to Home', href='/'),])
    

])

page_2_layout = html.Div([
    
	html.Div(
	className="navigation_bar",
	children=[

        html.Div([
		html.H3('Select Chart'),
            dcc.Dropdown(
                id='chart_name_2018',
                options=[{'label': i, 'value': i} for i in all_options_2018],
                value='Gender',),],
        style={'width': '25%', 'display': 'inline-block','padding':'0px 30px 20px 0px'}),
		html.Div([
			html.H3('Filter by'),
			dcc.Dropdown(id='chart_filter_2018'),
        ],
        style={'width': '25%', 'display': 'inline-block','padding':'0px 30px 20px 0px'}),
		
		html.Div([
			html.H3('Filter by Country'),
			dcc.Dropdown(
                id='country_dropdown_2018',
                options=[{'label': i, 'value': i} for i in country_filter_2018],
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
    dcc.Graph(id='indicator-graphic_2018'),
    html.Div(id='page-2-content'),
    dcc.Graph(id='pie_chart_2018'),
	html.Div(
	className="button_link",
	children=[dcc.Link('Go back to Home', href='/'),])

])

#populate filter by dropdown based on chart type
@app.callback(
    Output('chart_filter_2017', 'options'),
    [Input('chart_name_2017', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

#outputting filter by option dropdown	
@app.callback(
    Output('chart_filter_2017', 'value'),
    [Input('chart_filter_2017', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

#handles chart population and visualisation
@app.callback(
	Output(component_id='indicator-graphic_2017', component_property='figure'),
	[Input(component_id='chart_name_2017',component_property='value'),	
	Input('country_dropdown_2017', 'value'),
	Input('chart_filter_2017', 'value')])
def update_graph(input,selected_city,chart_filtering):
	#filter by country option
	df2 = df[df['place_of_birth']== selected_city ]
		
	if input =='Gender' and chart_filtering == 'Age Group':
		if selected_city == 'All Countries':
			df4 = df.groupby(["age_group", "gender"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["age_group", "gender"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()	
		femalevalue1 = df4.loc[df4['gender'] == 'Female']
		alllxfvalues = femalevalue1['age_group'].values
		alllyfvalues = femalevalue1['Percentage'].values

		malevalue1 = df4.loc[df4['gender'] == 'Male']
		alllxmvalues = malevalue1['age_group'].values
		alllymvalues = malevalue1['Percentage'].values
		
		gender_x_axis = 'Age Group'
		gender_name = 'Gender by Age Group'
	elif input =='Gender' and chart_filtering == 'Region':		
		#Need an option to display all country stats
		if selected_city == 'All Countries':
			df4 = df.groupby(["region", "gender"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["region", "gender"]).size().reset_index(name='count')
			
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()	
		femalevalue1 = df4.loc[df4['gender'] == 'Female']
		alllxfvalues = femalevalue1['region'].values
		alllyfvalues = femalevalue1['Percentage'].values

		malevalue1 = df4.loc[df4['gender'] == 'Male']
		alllxmvalues = malevalue1['region'].values
		alllymvalues = malevalue1['Percentage'].values
		
		gender_x_axis = 'Region'
		gender_name = 'Gender by Region'
	if input =='Turban Wearing' and chart_filtering == 'Age Group':
		if selected_city == 'All Countries':
			df4 = df.groupby(["turban_wearing", "age_group"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["turban_wearing", "age_group"]).size().reset_index(name='count')
		
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		newfemalevalue = df4.loc[df4['turban_wearing'] == 'No']
		newxfvalues = newfemalevalue['age_group'].values
		newyfvalues = newfemalevalue['Percentage'].values

		newmalevalue = df4.loc[df4['turban_wearing'] == 'Yes']
		newxmvalues = newmalevalue['age_group'].values
		newymvalues = newmalevalue['Percentage'].values
		
		turban_x_axis = 'Age Group'
		turban_name = 'Turban Wearing by Age Group'
	elif input =='Turban Wearing' and chart_filtering == 'Region':
		if selected_city == 'All Countries':
			df4 = df.groupby(["turban_wearing", "region"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["turban_wearing", "region"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		newfemalevalue = df4.loc[df4['turban_wearing'] == 'No']
		newxfvalues = newfemalevalue['region'].values
		newyfvalues = newfemalevalue['Percentage'].values

		newmalevalue = df4.loc[df4['turban_wearing'] == 'Yes']
		newxmvalues = newmalevalue['region'].values
		newymvalues = newmalevalue['Percentage'].values
		
		turban_x_axis = 'Region'
		turban_name = 'Turban Wearing by Region'
	elif input =='Turban Wearing' and chart_filtering == 'Place of Birth':
		if selected_city == 'All Countries':
			df4 = df.groupby(["turban_wearing", "place_of_birth"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["turban_wearing", "place_of_birth"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		newfemalevalue = df4.loc[df4['turban_wearing'] == 'No']
		newxfvalues = newfemalevalue['place_of_birth'].values
		newyfvalues = newfemalevalue['Percentage'].values

		newmalevalue = df4.loc[df4['turban_wearing'] == 'Yes']
		newxmvalues = newmalevalue['place_of_birth'].values
		newymvalues = newmalevalue['Percentage'].values
		
		turban_x_axis = 'Place of Birth'
		turban_name = 'Turban Wearing by Place of Birth'
	if input =='How voted in EU referendum 2016' and chart_filtering == 'Age Group':
		if selected_city == 'All Countries':
			df4 = df.groupby(["18. How voted in EU referendum 2016:", "age_group"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["18. How voted in EU referendum 2016:", "age_group"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		EU_no_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'Did not vote']
		no_xvalues = EU_no_vote['age_group'].values
		no_yvalues = EU_no_vote['Percentage'].values

		EU_leave_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK leaving the EU']
		leave_xvalues = EU_leave_vote['age_group'].values
		leave_yvalues = EU_leave_vote['Percentage'].values
		
		EU_stay_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK remaining a member of the EU']
		stay_xvalues = EU_stay_vote['age_group'].values
		stay_yvalues = EU_stay_vote['Percentage'].values
		
		eu_x_axis = 'Age Group'
		eu_name = 'Voted in EU Referendum 2016 by Age Group'
	elif input =='How voted in EU referendum 2016' and chart_filtering == 'Region':
		if selected_city == 'All Countries':
			df4 = df.groupby(["18. How voted in EU referendum 2016:", "region"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["18. How voted in EU referendum 2016:", "region"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		EU_no_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'Did not vote']
		no_xvalues = EU_no_vote['region'].values
		no_yvalues = EU_no_vote['Percentage'].values

		EU_leave_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK leaving the EU']
		leave_xvalues = EU_leave_vote['region'].values
		leave_yvalues = EU_leave_vote['Percentage'].values
		
		EU_stay_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK remaining a member of the EU']
		stay_xvalues = EU_stay_vote['region'].values
		stay_yvalues = EU_stay_vote['Percentage'].values
		
		eu_x_axis = 'Region'
		eu_name = 'Voted in EU Referendum 2016 by Region'
	elif input =='How voted in EU referendum 2016' and chart_filtering == 'Turban Wearing':
		if selected_city == 'All Countries':
			df4 = df.groupby(["18. How voted in EU referendum 2016:", "turban_wearing"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["18. How voted in EU referendum 2016:", "turban_wearing"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		EU_no_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'Did not vote']
		no_xvalues = EU_no_vote['turban_wearing'].values
		no_yvalues = EU_no_vote['Percentage'].values

		EU_leave_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK leaving the EU']
		leave_xvalues = EU_leave_vote['turban_wearing'].values
		leave_yvalues = EU_leave_vote['Percentage'].values
		
		EU_stay_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK remaining a member of the EU']
		stay_xvalues = EU_stay_vote['turban_wearing'].values
		stay_yvalues = EU_stay_vote['Percentage'].values
		
		eu_x_axis = 'Turban Wearing'
		eu_name = 'Voted in EU Referendum 2016 by Turban Wearing'
	elif input =='How voted in EU referendum 2016' and chart_filtering == 'View of  result of  referendum to leave  EU (Brexit)?':
		if selected_city == 'All Countries':
			df4 = df.groupby(["18. How voted in EU referendum 2016:", "19. View of  result of  referendum to leave  EU (Brexit)?"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["18. How voted in EU referendum 2016:", "19. View of  result of  referendum to leave  EU (Brexit)?"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		EU_no_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'Did not vote']
		no_xvalues = EU_no_vote['19. View of  result of  referendum to leave  EU (Brexit)?'].values
		no_yvalues = EU_no_vote['Percentage'].values

		EU_leave_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK leaving the EU']
		leave_xvalues = EU_leave_vote['19. View of  result of  referendum to leave  EU (Brexit)?'].values
		leave_yvalues = EU_leave_vote['Percentage'].values
		
		EU_stay_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK remaining a member of the EU']
		stay_xvalues = EU_stay_vote['19. View of  result of  referendum to leave  EU (Brexit)?'].values
		stay_yvalues = EU_stay_vote['Percentage'].values
		
		eu_x_axis = 'View of  result of  referendum to leave  EU (Brexit)?'
		eu_name = 'Voted in EU Referendum 2016 by View of Result'
	if input == 'Turban Wearing':
		return {
			'data': [
				{'x': newxfvalues, 'y': newyfvalues, 'type': 'bar', 'name': 'No',},
				{'x': newxmvalues, 'y': newymvalues, 'type': 'bar', 'name': 'Yes'},
				
			],
			'layout': {
				'title': turban_name,
				'yaxis':{
                     'title':'Percentage'},
					 'xaxis': {'title': turban_x_axis},
			}
			
			
		}
	elif input == 'Gender':
		return {
			'data': [
			   {'x': alllxfvalues, 'y': alllyfvalues, 'type': 'bar', 'name': 'Female'},
				{'x': alllxmvalues, 'y': alllymvalues, 'type': 'bar', 'name': 'Male'},
			],
			'layout': {
				'title': gender_name,
				'yaxis':{
                     'title':'Percentage'},
					 'xaxis': {'title': gender_x_axis},
			}
		}
	elif input == 'How voted in EU referendum 2016':
		return {
			'data': [
			   {'x': no_xvalues, 'y': no_yvalues, 'type': 'bar', 'name': 'Did Not Vote'},
				{'x': leave_xvalues, 'y': leave_yvalues, 'type': 'bar', 'name': 'Voted to Leave'},
				{'x': stay_xvalues, 'y': stay_yvalues, 'type': 'bar', 'name': 'Voted to Stay'},
				
			],
			'layout': {
				'title': eu_name,
				'yaxis':{
                     'title':'Percentage'},
				'xaxis': {'title': eu_x_axis},
			}
		}

#Second chart functions		
@app.callback(
	Output(component_id='pie_chart', component_property='figure'),
	[Input(component_id='chart_name_2017',component_property='value'),	
	Input('country_dropdown_2017', 'value'),
	Input('chart_filter_2017', 'value')])
def update_graph_2017(input,selected_city,chart_filtering):
	#filter by country option
	df2 = df[df['place_of_birth']== selected_city ]

		
	if input =='Gender' and chart_filtering == 'Age Group':
		if selected_city == 'All Countries':
			df4 = df.groupby(["age_group", "gender"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["age_group", "gender"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()	
		femalevalue1 = df4.loc[df4['gender'] == 'Female']
		alllxfvalues = femalevalue1['age_group'].values
		alllyfvalues = femalevalue1['Percentage'].values

		malevalue1 = df4.loc[df4['gender'] == 'Male']
		alllxmvalues = malevalue1['age_group'].values
		alllymvalues = malevalue1['Percentage'].values
		
		gender_name = 'Gender by Age Group'
	elif input =='Gender' and chart_filtering == 'Region':
		if selected_city == 'All Countries':
			df4 = df.groupby(["region", "gender"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["region", "gender"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()	
		femalevalue1 = df4.loc[df4['gender'] == 'Female']
		alllxfvalues = femalevalue1['region'].values
		alllyfvalues = femalevalue1['Percentage'].values

		malevalue1 = df4.loc[df4['gender'] == 'Male']
		alllxmvalues = malevalue1['region'].values
		alllymvalues = malevalue1['Percentage'].values
		
		gender_name = 'Gender by Region'
	elif input =='Turban Wearing' and chart_filtering == 'Place of Birth':		
		#Need an option to display all country stats
		if selected_city == 'All Countries':
			df4 = df.groupby(["turban_wearing", "place_of_birth"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["turban_wearing", "place_of_birth"]).size().reset_index(name='count')
			
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		df4.place_of_birth = df4.place_of_birth.replace({"England": "United Kingdom"})		

		newfemalevalue = df4.loc[df4['turban_wearing'] == 'No']
		names = newfemalevalue['place_of_birth'].values
		newyfvalues = newfemalevalue['Percentage'].values

		newmalevalue = df4.loc[df4['turban_wearing'] == 'Yes']
		newxmvalues = newmalevalue['place_of_birth'].values
		newymvalues = newmalevalue['Percentage'].values
		
		#convert country name to country code
		def get_country_code(name):
			for co in list(pycountry.countries):
				if name in co.name:
					return co.alpha_3
			return None

		def c_code():
			codes = []
			for name in names:
				codes.append(get_country_code(name))
			return codes
		#country codes saved in this variable
		codes = c_code()
		
		turban_name = 'Turban Wearing by Place of Birth'
	elif input =='Turban Wearing' and chart_filtering == 'Age Group':	
		if selected_city == 'All Countries':
			df4 = df.groupby(["turban_wearing", "age_group"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["turban_wearing", "age_group"]).size().reset_index(name='count')
		
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		femalevalue1 = df4.loc[df4['turban_wearing'] == 'No']
		alllxfvalues = femalevalue1['age_group'].values
		alllyfvalues = femalevalue1['Percentage'].values

		malevalue1 = df4.loc[df4['turban_wearing'] == 'Yes']
		alllxmvalues = malevalue1['age_group'].values
		alllymvalues = malevalue1['Percentage'].values
		
		turban_name = 'Turban Wearing by Age Group'
	elif input =='Turban Wearing' and chart_filtering == 'Region':	
		if selected_city == 'All Countries':
			df4 = df.groupby(["turban_wearing", "region"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["turban_wearing", "region"]).size().reset_index(name='count')
		
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		femalevalue1 = df4.loc[df4['turban_wearing'] == 'No']
		alllxfvalues = femalevalue1['region'].values
		alllyfvalues = femalevalue1['Percentage'].values

		malevalue1 = df4.loc[df4['turban_wearing'] == 'Yes']
		alllxmvalues = malevalue1['region'].values
		alllymvalues = malevalue1['Percentage'].values
		
		turban_name = 'Turban Wearing by Region'
	elif input =='How voted in EU referendum 2016' and chart_filtering == 'Age Group':
		if selected_city == 'All Countries':
			df4 = df.groupby(["18. How voted in EU referendum 2016:", "age_group"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["18. How voted in EU referendum 2016:", "age_group"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		EU_no_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'Did not vote']
		no_xvalues = EU_no_vote['age_group'].values
		no_yvalues = EU_no_vote['Percentage'].values

		EU_leave_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK leaving the EU']
		leave_xvalues = EU_leave_vote['age_group'].values
		leave_yvalues = EU_leave_vote['Percentage'].values
		
		EU_stay_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK remaining a member of the EU']
		stay_xvalues = EU_stay_vote['age_group'].values
		stay_yvalues = EU_stay_vote['Percentage'].values
		
		EU_title = 'Brexit Votes by Age Group'
		EU_name = 'Age Group'
	elif input =='How voted in EU referendum 2016' and chart_filtering == 'Region':
		if selected_city == 'All Countries':
			df4 = df.groupby(["18. How voted in EU referendum 2016:", "region"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["18. How voted in EU referendum 2016:", "region"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		EU_no_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'Did not vote']
		no_xvalues = EU_no_vote['region'].values
		no_yvalues = EU_no_vote['Percentage'].values

		EU_leave_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK leaving the EU']
		leave_xvalues = EU_leave_vote['region'].values
		leave_yvalues = EU_leave_vote['Percentage'].values
		
		EU_stay_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK remaining a member of the EU']
		stay_xvalues = EU_stay_vote['region'].values
		stay_yvalues = EU_stay_vote['Percentage'].values
		
		EU_title = 'Brexit Votes by Region'
		EU_name = 'Region'
	elif input =='How voted in EU referendum 2016' and chart_filtering == 'Turban Wearing':
		if selected_city == 'All Countries':
			df4 = df.groupby(["18. How voted in EU referendum 2016:", "turban_wearing"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["18. How voted in EU referendum 2016:", "turban_wearing"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		EU_no_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'Did not vote']
		no_xvalues = EU_no_vote['turban_wearing'].values
		no_yvalues = EU_no_vote['Percentage'].values

		EU_leave_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK leaving the EU']
		leave_xvalues = EU_leave_vote['turban_wearing'].values
		leave_yvalues = EU_leave_vote['Percentage'].values
		
		EU_stay_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK remaining a member of the EU']
		stay_xvalues = EU_stay_vote['turban_wearing'].values
		stay_yvalues = EU_stay_vote['Percentage'].values
		
		EU_title = 'Brexit Vote by Turban Wearing'
		EU_name = 'Turban Wearing'
	elif input =='How voted in EU referendum 2016' and chart_filtering == 'View of  result of  referendum to leave  EU (Brexit)?':
		if selected_city == 'All Countries':
			df4 = df.groupby(["18. How voted in EU referendum 2016:", "19. View of  result of  referendum to leave  EU (Brexit)?"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["18. How voted in EU referendum 2016:", "19. View of  result of  referendum to leave  EU (Brexit)?"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		EU_no_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'Did not vote']
		no_xvalues = EU_no_vote['19. View of  result of  referendum to leave  EU (Brexit)?'].values
		no_yvalues = EU_no_vote['Percentage'].values

		EU_leave_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK leaving the EU']
		leave_xvalues = EU_leave_vote['19. View of  result of  referendum to leave  EU (Brexit)?'].values
		leave_yvalues = EU_leave_vote['Percentage'].values
		
		EU_stay_vote = df4.loc[df4['18. How voted in EU referendum 2016:'] == 'In favour of the UK remaining a member of the EU']
		stay_xvalues = EU_stay_vote['19. View of  result of  referendum to leave  EU (Brexit)?'].values
		stay_yvalues = EU_stay_vote['Percentage'].values
		
		EU_title = 'View of  result of  referendum to leave  EU (Brexit)?'
		EU_name = 'View of Brexit'
	if input == 'Gender':
		return {
			  'data': [
                go.Pie(
                    labels=alllxfvalues,
                    values=alllyfvalues,
                    hoverinfo='label+percent+name',
					name=gender_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 0},
					title='Female',
                ),
				go.Pie(
                    labels=alllxmvalues,
                    values=alllymvalues,
                    hoverinfo='label+percent+name',  
					name=gender_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 1},
					title='Male',
                )
            ],
            'layout': {
				'title': gender_name,
				'grid': {'rows': 1, 'columns': 2},
			}
		}
	
	elif input == 'Turban Wearing' and chart_filtering != 'Place of Birth':
		return {
			  'data': [
                go.Pie(
                    labels=alllxfvalues,
                    values=alllyfvalues,
                    hoverinfo='label+percent+name', 
                    name=turban_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 0},
					title='Female',
                ),
				go.Pie(
                    labels=alllxmvalues,
                    values=alllymvalues,
                    hoverinfo='label+percent+name',   
                    name=turban_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 1},
					title='Male',
                )
            ],
            'layout': {
				'title': turban_name,
				'grid': {'rows': 1, 'columns': 2},
			}
		}
		
	elif input == 'Turban Wearing' and chart_filtering == 'Place of Birth': 
		data = [go.Choropleth(
		locations = codes,
		z = newyfvalues,
		colorscale = [
			[0, "rgb(5, 10, 172)"],
			[0.35, "rgb(40, 60, 190)"],
			[0.5, "rgb(70, 100, 245)"],
			[0.6, "rgb(90, 120, 245)"],
			[0.7, "rgb(106, 137, 247)"],
			[1, "rgb(220, 220, 220)"]
		],
		autocolorscale = False,
		reversescale = True,
		marker = go.choropleth.Marker(
			line = go.choropleth.marker.Line(
				color = 'rgb(180,180,180)',
				width = 0.5
			)),
		colorbar = go.choropleth.ColorBar(
			tickprefix = '%',
			title = 'Percentage of Non Turban Wearing'),
		)]

		layout = go.Layout(
			#width=1600,
			#height= 450,
			title = go.layout.Title(
				text = 'Turban Wearing by Place of Birth'
			),
			geo = go.layout.Geo(
				showframe = False,
				showcoastlines = True,
				showland = True,
				projection = go.layout.geo.Projection(
					type = 'equirectangular'
				)
			),
			)
		fig = go.Figure(data = data, layout = layout)
		return fig

	elif input == 'How voted in EU referendum 2016':
		return {
			  'data': [
                go.Pie(
                    labels=no_xvalues,
                    values=no_yvalues,
                    hoverinfo='label+percent+name',   
                    name=EU_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 0},
					title='No Vote',
                ),
				go.Pie(
                    labels=leave_xvalues,
                    values=leave_yvalues,
                    hoverinfo='label+percent+name',   
                    name=EU_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 1},
					title='Vote to Leave',
                ),
				go.Pie(
                    labels=stay_xvalues,
                    values=stay_yvalues,
                    hoverinfo='label+percent+name',   
                    name=EU_name,
                    hole=.3,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 2},
					title='Vote to Stay',
                )
            ],
            'layout': {
				'title': EU_title,
				'grid': {'rows': 1, 'columns': 3},
				'yaxis': {
					'tickformat': ',.1%',
					
				  }
			}
		}
	
#2018 python code - trying to split up the code into other python files without errors		
#populate filter by dropdown based on chart type
@app.callback(
    Output('chart_filter_2018', 'options'),
    [Input('chart_name_2018', 'value')])
def set_cities_options_2018(selected_country_2018):
    return [{'label': i, 'value': i} for i in all_options_2018[selected_country_2018]]

#outputting filter by option dropdown	
@app.callback(
    Output('chart_filter_2018', 'value'),
    [Input('chart_filter_2018', 'options')])
def set_cities_value_2018(available_options_2018):
    return available_options_2018[0]['value']

#handles chart population and visualisation
@app.callback(
	Output(component_id='indicator-graphic_2018', component_property='figure'),
	[Input(component_id='chart_name_2018',component_property='value'),	
	Input('country_dropdown_2018', 'value'),
	Input('chart_filter_2018', 'value')])
def update_graph_2018(input_2018,selected_city_2018,chart_filtering_2018):
	#filter by country option
	
	df2 = df_2018[df_2018['place_of_birth']== selected_city_2018 ]
		
	if input_2018 =='Gender' and chart_filtering_2018 == 'Age Group':
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["age_group", "gender"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["age_group", "gender"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()	
		femalevalue1 = df4.loc[df4['gender'] == 'Female']
		alllxfvalues = femalevalue1['age_group'].values
		alllyfvalues = femalevalue1['Percentage'].values

		malevalue1 = df4.loc[df4['gender'] == 'Male']
		alllxmvalues = malevalue1['age_group'].values
		alllymvalues = malevalue1['Percentage'].values

	elif input_2018 =='Gender' and chart_filtering_2018 == 'Region':		
		#Need an option to display all country stats
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["region", "gender"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["region", "gender"]).size().reset_index(name='count')
			
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()	
		femalevalue1 = df4.loc[df4['gender'] == 'Female']
		alllxfvalues = femalevalue1['region'].values
		alllyfvalues = femalevalue1['Percentage'].values

		malevalue1 = df4.loc[df4['gender'] == 'Male']
		alllxmvalues = malevalue1['region'].values
		alllymvalues = malevalue1['Percentage'].values
		
	if input_2018 =='Turban Wearing' and chart_filtering_2018 == 'Age Group':
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["turban_wearing", "age_group"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["turban_wearing", "age_group"]).size().reset_index(name='count')
		
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		newfemalevalue = df4.loc[df4['turban_wearing'] == 'No']
		newxfvalues = newfemalevalue['age_group'].values
		newyfvalues = newfemalevalue['Percentage'].values

		newmalevalue = df4.loc[df4['turban_wearing'] == 'Yes']
		newxmvalues = newmalevalue['age_group'].values
		newymvalues = newmalevalue['Percentage'].values
	elif input_2018 =='Turban Wearing' and chart_filtering_2018 == 'Region':
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["turban_wearing", "region"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["turban_wearing", "region"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		newfemalevalue = df4.loc[df4['turban_wearing'] == 'No']
		newxfvalues = newfemalevalue['region'].values
		newyfvalues = newfemalevalue['Percentage'].values

		newmalevalue = df4.loc[df4['turban_wearing'] == 'Yes']
		newxmvalues = newmalevalue['region'].values
		newymvalues = newmalevalue['Percentage'].values
	elif input_2018 =='Turban Wearing' and chart_filtering_2018 == 'Place of Birth':
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["turban_wearing", "place_of_birth"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["turban_wearing", "place_of_birth"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		newfemalevalue = df4.loc[df4['turban_wearing'] == 'No']
		newxfvalues = newfemalevalue['place_of_birth'].values
		newyfvalues = newfemalevalue['Percentage'].values

		newmalevalue = df4.loc[df4['turban_wearing'] == 'Yes']
		newxmvalues = newmalevalue['place_of_birth'].values
		newymvalues = newmalevalue['Percentage'].values
	if input_2018 =='How often do you undertake spiritual practice?' and chart_filtering_2018 == 'Age Group':
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["18. How often undertake spiritual practice such as reading Bani?", "age_group"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["18. How often undertake spiritual practice such as reading Bani?", "age_group"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		spritual_everyday = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Everyday']
		everyday_xvalues = spritual_everyday['age_group'].values
		everyday_yvalues = spritual_everyday['Percentage'].values
		
		spritual_few = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'A few times a week']
		few_xvalues = spritual_few['age_group'].values
		few_yvalues = spritual_few['Percentage'].values

		spritual_weekly = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Weekly']
		weekly_xvalues = spritual_weekly['age_group'].values
		weekly_yvalues = spritual_weekly['Percentage'].values
		
		spritual_monthly = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Monthly']
		monthly_xvalues = spritual_monthly['age_group'].values
		monthly_yvalues = spritual_monthly['Percentage'].values
		
		spritual_need_to = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'When I need to']
		need_to_xvalues = spritual_need_to['age_group'].values
		need_to_yvalues = spritual_need_to['Percentage'].values
		
		
		spritual_never = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Never']
		never_xvalues = spritual_never['age_group'].values
		never_yvalues = spritual_never['Percentage'].values
		
		spritual_title = 'Spritual Practice by Age Group'
	elif input_2018 =='How often do you undertake spiritual practice?' and chart_filtering_2018 == 'Gender':
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["18. How often undertake spiritual practice such as reading Bani?", "gender"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["18. How often undertake spiritual practice such as reading Bani?", "gender"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		spritual_everyday = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Everyday']
		everyday_xvalues = spritual_everyday['gender'].values
		everyday_yvalues = spritual_everyday['Percentage'].values
		
		spritual_few = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'A few times a week']
		few_xvalues = spritual_few['gender'].values
		few_yvalues = spritual_few['Percentage'].values

		spritual_weekly = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Weekly']
		weekly_xvalues = spritual_weekly['gender'].values
		weekly_yvalues = spritual_weekly['Percentage'].values
		
		spritual_monthly = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Monthly']
		monthly_xvalues = spritual_monthly['gender'].values
		monthly_yvalues = spritual_monthly['Percentage'].values
		
		spritual_need_to = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'When I need to']
		need_to_xvalues = spritual_need_to['gender'].values
		need_to_yvalues = spritual_need_to['Percentage'].values
		
		
		spritual_never = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Never']
		never_xvalues = spritual_never['gender'].values
		never_yvalues = spritual_never['Percentage'].values
		
		spritual_title = 'Spritual Practice by Gender'
	
	elif input_2018 =='How often do you undertake spiritual practice?' and chart_filtering_2018 == 'Turban Wearing':
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["18. How often undertake spiritual practice such as reading Bani?", "turban_wearing"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["18. How often undertake spiritual practice such as reading Bani?", "turban_wearing"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		spritual_everyday = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Everyday']
		everyday_xvalues = spritual_everyday['turban_wearing'].values
		everyday_yvalues = spritual_everyday['Percentage'].values
		
		spritual_few = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'A few times a week']
		few_xvalues = spritual_few['turban_wearing'].values
		few_yvalues = spritual_few['Percentage'].values

		spritual_weekly = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Weekly']
		weekly_xvalues = spritual_weekly['turban_wearing'].values
		weekly_yvalues = spritual_weekly['Percentage'].values
		
		spritual_monthly = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Monthly']
		monthly_xvalues = spritual_monthly['turban_wearing'].values
		monthly_yvalues = spritual_monthly['Percentage'].values
		
		spritual_need_to = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'When I need to']
		need_to_xvalues = spritual_need_to['turban_wearing'].values
		need_to_yvalues = spritual_need_to['Percentage'].values
		
		
		spritual_never = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Never']
		never_xvalues = spritual_never['turban_wearing'].values
		never_yvalues = spritual_never['Percentage'].values
		
		spritual_title = 'Spritual Practice by Turban Wearing'

	if input_2018 == 'Turban Wearing':
		return {
			'data': [
				{'x': newxfvalues, 'y': newyfvalues, 'type': 'bar', 'name': 'No'},
				{'x': newxmvalues, 'y': newymvalues, 'type': 'bar', 'name': 'Yes'},
			],
			'layout': {
				'title': ' Turban Wearing',
				'yaxis':{
                     'title':'Percentage'
                },
			}
			
			
		}
	elif input_2018 == 'Gender':
		return {
			'data': [
			   {'x': alllxfvalues, 'y': alllyfvalues, 'type': 'bar', 'name': 'Female'},
				{'x': alllxmvalues, 'y': alllymvalues, 'type': 'bar', 'name': 'Male'},
			],
			'layout': {
				'title': 'Gender',
				'yaxis':{
                     'title':'Percentage'
                },
			}
		}
	elif input_2018 == 'How often do you undertake spiritual practice?':
		return {
			'data': [
			   {'x': everyday_xvalues, 'y': everyday_yvalues, 'type': 'bar', 'name': 'Everyday'},
				{'x': few_xvalues, 'y': few_yvalues, 'type': 'bar', 'name': 'A few times a Week'},
				{'x': weekly_xvalues, 'y': weekly_yvalues, 'type': 'bar', 'name': 'Weekly'},
				{'x': monthly_xvalues, 'y': monthly_yvalues, 'type': 'bar', 'name': 'Monthly'},
				{'x': need_to_xvalues, 'y': need_to_yvalues, 'type': 'bar', 'name': 'When I need to'},
				{'x': never_xvalues, 'y': never_yvalues, 'type': 'bar', 'name': 'Never'},
				
			],
			'layout': {
				'title': spritual_title,
				'yaxis':{
                     'title':'Percentage'
                },
			}
		}
		
#Second chart functions	2018 DATASET	
@app.callback(
	Output(component_id='pie_chart_2018', component_property='figure'),
	[Input(component_id='chart_name_2018',component_property='value'),	
	Input('country_dropdown_2018', 'value'),
	Input('chart_filter_2018', 'value')])
def update_graph_second_chart(input_2018,selected_city_2018,chart_filtering_2018):
	#filter by country option
	df2 = df_2018[df_2018['place_of_birth']== selected_city_2018 ]
	
	if input_2018 =='Gender' and chart_filtering_2018 == 'Age Group':
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["age_group", "gender"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["age_group", "gender"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()	
		femalevalue1 = df4.loc[df4['gender'] == 'Female']
		alllxfvalues = femalevalue1['age_group'].values
		alllyfvalues = femalevalue1['Percentage'].values

		malevalue1 = df4.loc[df4['gender'] == 'Male']
		alllxmvalues = malevalue1['age_group'].values
		alllymvalues = malevalue1['Percentage'].values
		
		gender_name = 'Gender by Age Group'
	elif input_2018 =='Gender' and chart_filtering_2018 == 'Region':
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["region", "gender"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["region", "gender"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()	
		femalevalue1 = df4.loc[df4['gender'] == 'Female']
		alllxfvalues = femalevalue1['region'].values
		alllyfvalues = femalevalue1['Percentage'].values

		malevalue1 = df4.loc[df4['gender'] == 'Male']
		alllxmvalues = malevalue1['region'].values
		alllymvalues = malevalue1['Percentage'].values
		
		gender_name = 'Gender by Region'
	elif input_2018 =='Turban Wearing' and chart_filtering_2018 == 'Place of Birth':		
		#Need an option to display all country stats
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["turban_wearing", "place_of_birth"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["turban_wearing", "place_of_birth"]).size().reset_index(name='count')
			
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		df4.place_of_birth = df4.place_of_birth.replace({"England": "United Kingdom"})		

		newfemalevalue = df4.loc[df4['turban_wearing'] == 'No']
		names = newfemalevalue['place_of_birth'].values
		newyfvalues = newfemalevalue['Percentage'].values

		newmalevalue = df4.loc[df4['turban_wearing'] == 'Yes']
		newxmvalues = newmalevalue['place_of_birth'].values
		newymvalues = newmalevalue['Percentage'].values
		
		#convert country name to country code
		def get_country_code(name):
			for co in list(pycountry.countries):
				if name in co.name:
					return co.alpha_3
			return None

		def c_code():
			codes = []
			for name in names:
				codes.append(get_country_code(name))
			return codes
		#country codes saved in this variable
		codes = c_code()
		
		turban_name = 'Turban Wearing by Place of Birth'
	elif input_2018 =='Turban Wearing' and chart_filtering_2018 == 'Age Group':	
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["turban_wearing", "age_group"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["turban_wearing", "age_group"]).size().reset_index(name='count')
		
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		femalevalue1 = df4.loc[df4['turban_wearing'] == 'No']
		alllxfvalues = femalevalue1['age_group'].values
		alllyfvalues = femalevalue1['Percentage'].values

		malevalue1 = df4.loc[df4['turban_wearing'] == 'Yes']
		alllxmvalues = malevalue1['age_group'].values
		alllymvalues = malevalue1['Percentage'].values
		
		turban_name = 'Turban Wearing by Age Group'
	elif input_2018 =='Turban Wearing' and chart_filtering_2018 == 'Region':	
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["turban_wearing", "region"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["turban_wearing", "region"]).size().reset_index(name='count')
		
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		femalevalue1 = df4.loc[df4['turban_wearing'] == 'No']
		alllxfvalues = femalevalue1['region'].values
		alllyfvalues = femalevalue1['Percentage'].values

		malevalue1 = df4.loc[df4['turban_wearing'] == 'Yes']
		alllxmvalues = malevalue1['region'].values
		alllymvalues = malevalue1['Percentage'].values
		
		turban_name = 'Turban Wearing by Region'
		
	elif input_2018 =='How often do you undertake spiritual practice?' and chart_filtering_2018 == 'Age Group':
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["18. How often undertake spiritual practice such as reading Bani?", "age_group"]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["18. How often undertake spiritual practice such as reading Bani?", "age_group"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		spritual_everyday = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Everyday']
		everyday_xvalues = spritual_everyday['age_group'].values
		everyday_yvalues = spritual_everyday['Percentage'].values
		
		spritual_few = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'A few times a week']
		few_xvalues = spritual_few['age_group'].values
		few_yvalues = spritual_few['Percentage'].values

		spritual_weekly = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Weekly']
		weekly_xvalues = spritual_weekly['age_group'].values
		weekly_yvalues = spritual_weekly['Percentage'].values
		
		spritual_monthly = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Monthly']
		monthly_xvalues = spritual_monthly['age_group'].values
		monthly_yvalues = spritual_monthly['Percentage'].values
		
		spritual_need_to = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'When I need to']
		need_to_xvalues = spritual_need_to['age_group'].values
		need_to_yvalues = spritual_need_to['Percentage'].values
		
		
		spritual_never = df4.loc[df4['18. How often undertake spiritual practice such as reading Bani?'] == 'Never']
		never_xvalues = spritual_never['age_group'].values
		never_yvalues = spritual_never['Percentage'].values
		
		spritual_title = 'Spritual Practice by Age Group'
		spritual_name = 'Spritual Practice'
		
	elif input_2018 =='How often do you undertake spiritual practice?' and chart_filtering_2018 == 'Gender':
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["gender", "18. How often undertake spiritual practice such as reading Bani?" ]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["gender", "18. How often undertake spiritual practice such as reading Bani?"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		spritual_female = df4.loc[df4['gender'] == 'Female']
		spritual_f_xvalues = spritual_female['18. How often undertake spiritual practice such as reading Bani?'].values
		spritual_f_yvalues = spritual_female['Percentage'].values

		spritual_male = df4.loc[df4['gender'] == 'Male']
		spritual_m_xvalues = spritual_male['18. How often undertake spiritual practice such as reading Bani?'].values
		spritual_m_yvalues = spritual_male['Percentage'].values
		
		spritual_title = 'Spritual Practice by Gender'
		spritual_name = 'Spritual Practice'
		
	elif input_2018 =='How often do you undertake spiritual practice?' and chart_filtering_2018 == 'Turban Wearing':
		if selected_city_2018 == 'All Countries':
			df4 = df_2018.groupby(["turban_wearing", "18. How often undertake spiritual practice such as reading Bani?" ]).size().reset_index(name='count')
		else:
			df4 = df2.groupby(["turban_wearing", "18. How often undertake spiritual practice such as reading Bani?"]).size().reset_index(name='count')
		df4['Percentage'] = 100 * df4['count']  / df4['count'].sum()
		spritual_female = df4.loc[df4['turban_wearing'] == 'No']
		spritual_f_xvalues = spritual_female['18. How often undertake spiritual practice such as reading Bani?'].values
		spritual_f_yvalues = spritual_female['Percentage'].values

		spritual_male = df4.loc[df4['turban_wearing'] == 'Yes']
		spritual_m_xvalues = spritual_male['18. How often undertake spiritual practice such as reading Bani?'].values
		spritual_m_yvalues = spritual_male['Percentage'].values
		
		spritual_title = 'Spritual Practice by Turban Wearing'
		spritual_name = 'Spritual Practice'
	if input_2018 == 'Gender':
		return {
			  'data': [
                go.Pie(
                    labels=alllxfvalues,
                    values=alllyfvalues,
                    hoverinfo='label+percent+name',
					name=gender_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 0},
					title='Female',
                ),
				go.Pie(
                    labels=alllxmvalues,
                    values=alllymvalues,
                    hoverinfo='label+percent+name',  
					name=gender_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 1},
					title='Male',
                )
            ],
            'layout': {
				'title': gender_name,
				'grid': {'rows': 1, 'columns': 2},
			}
		}
	
	elif input_2018 == 'Turban Wearing' and chart_filtering_2018 != 'Place of Birth':
		return {
			  'data': [
                go.Pie(
                    labels=alllxfvalues,
                    values=alllyfvalues,
                    hoverinfo='label+percent+name', 
                    name=turban_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 0},
					title='Female',
                ),
				go.Pie(
                    labels=alllxmvalues,
                    values=alllymvalues,
                    hoverinfo='label+percent+name',   
                    name=turban_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 1},
					title='Male',
                )
            ],
            'layout': {
				'title': turban_name,
				'grid': {'rows': 1, 'columns': 2},
			}
		}
		
	elif input_2018 == 'Turban Wearing' and chart_filtering_2018 == 'Place of Birth': 
		data = [go.Choropleth(
		locations = codes,
		z = newyfvalues,
		colorscale = [
			[0, "rgb(5, 10, 172)"],
			[0.35, "rgb(40, 60, 190)"],
			[0.5, "rgb(70, 100, 245)"],
			[0.6, "rgb(90, 120, 245)"],
			[0.7, "rgb(106, 137, 247)"],
			[1, "rgb(220, 220, 220)"]
		],
		autocolorscale = False,
		reversescale = True,
		marker = go.choropleth.Marker(
			line = go.choropleth.marker.Line(
				color = 'rgb(180,180,180)',
				width = 0.5
			)),
		colorbar = go.choropleth.ColorBar(
			tickprefix = '%',
			title = 'Percentage of Non Turban Wearing'),
		)]

		layout = go.Layout(
			#width=1600,
			#height= 450,
			title = go.layout.Title(
				text = 'Turban Wearing by Place of Birth'
			),
			geo = go.layout.Geo(
				showframe = False,
				showcoastlines = True,
				showland = True,
				projection = go.layout.geo.Projection(
					type = 'equirectangular'
				)
			),
			)
		fig = go.Figure(data = data, layout = layout)
		return fig

	elif input_2018 == 'How often do you undertake spiritual practice?' and chart_filtering_2018 == 'Age Group':
		return {
			  'data': [
                go.Pie(
                    labels=everyday_xvalues,
                    values=everyday_yvalues,
                    hoverinfo='label+percent+name',   
                    name=spritual_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 0},
					title='Everday',
                ),
				go.Pie(
                    labels=few_xvalues,
                    values=few_yvalues,
                    hoverinfo='label+percent+name',   
                    name=spritual_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 1},
					title='Few times a Week',
                ),
				go.Pie(
                    labels=weekly_xvalues,
                    values=weekly_yvalues,
                    hoverinfo='label+percent+name',   
                    name=spritual_name,
                    hole=.3,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 2},
					title='Weekly',
                ),
				go.Pie(
                    labels=monthly_xvalues,
                    values=monthly_yvalues,
                    hoverinfo='label+percent+name',   
                    name=spritual_name,
                    hole=.3,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 3},
					title='Monthly',
                ),
				go.Pie(
                    labels=need_to_xvalues,
                    values=need_to_yvalues,
                    hoverinfo='label+percent+name',   
                    name=spritual_name,
                    hole=.3,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 4},
					title='When I need to',
                ),
				go.Pie(
                    labels=never_xvalues,
                    values=never_yvalues,
                    hoverinfo='label+percent+name',   
                    name=spritual_name,
                    hole=.3,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 5},
					title='Never',
                )
				
            ],
            'layout': {
				'title': spritual_title,
				'grid': {'rows': 1, 'columns': 6},
				'yaxis': {
					'tickformat': ',.1%',
					
				  }
			}
		}
	elif input_2018 == 'How often do you undertake spiritual practice?' and chart_filtering_2018 != 'Age Group':
		return {
			  'data': [
                go.Pie(
                    labels=spritual_f_xvalues,
                    values=spritual_f_yvalues,
                    hoverinfo='label+percent+name',   
                    name=spritual_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 0},
					title='Female',
                ),
				go.Pie(
                    labels=spritual_m_xvalues,
                    values=spritual_m_yvalues,
                    hoverinfo='label+percent+name',   
                    name=spritual_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 1},
					title='Male',
                ),
				
				
            ],
            'layout': {
				'title': spritual_title,
				'grid': {'rows': 1, 'columns': 2},
				'yaxis': {
					'tickformat': ',.1%',
					
				  }
			}
		}
	elif input_2018 == 'How often do you undertake spiritual practice?' and chart_filtering_2018 == 'Turban Wearing':
		return {
			  'data': [
                go.Pie(
                    labels=spritual_f_xvalues,
                    values=spritual_f_yvalues,
                    hoverinfo='label+percent+name',   
                    name=spritual_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 0},
					title='No',
                ),
				go.Pie(
                    labels=spritual_m_xvalues,
                    values=spritual_m_yvalues,
                    hoverinfo='label+percent+name',   
                    name=spritual_name,
                    hole=.4,
                    pull=.1,
                    textposition='outside',
					domain= {'column': 1},
					title='Yes',
                ),
				
				
            ],
            'layout': {
				'title': spritual_title,
				'grid': {'rows': 1, 'columns': 2},
				'yaxis': {
					'tickformat': ',.1%',
					
				  }
			}
		}
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