import dash
import plotly.graph_objs as go
from dash.dependencies import Output
from dash.dependencies import Input, Output
from app import app, df, all_options

#populate filter by dropdown based on chart type
@app.callback(
    Output('chart_filter', 'options'),
    [Input('chart_name', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

#outputting filter by option dropdown	
@app.callback(
    Output('chart_filter', 'value'),
    [Input('chart_filter', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

#handles chart population and visualisation
@app.callback(
	Output(component_id='indicator-graphic', component_property='figure'),
	[Input(component_id='chart_name',component_property='value'),	
	Input('country_dropdown', 'value'),
	Input('chart_filter', 'value')])
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

	if input == 'Turban Wearing':
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
	elif input == 'Gender':
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
	elif input == 'How voted in EU referendum 2016':
		return {
			'data': [
			   {'x': no_xvalues, 'y': no_yvalues, 'type': 'bar', 'name': 'Did Not Vote'},
				{'x': leave_xvalues, 'y': leave_yvalues, 'type': 'bar', 'name': 'Voted to Leave'},
				{'x': stay_xvalues, 'y': stay_yvalues, 'type': 'bar', 'name': 'Voted to Stay'},
				
			],
			'layout': {
				'title': 'Voted in EU referendum 2016',
				'yaxis':{
                     'title':'Percentage'
                },
			}
		}
	