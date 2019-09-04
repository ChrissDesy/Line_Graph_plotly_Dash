from flask import Flask, url_for, redirect
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from files.handlers import parse_contents
from files.layouts import layout1, layout2
import pandas as pd
#plotly imports...
import plotly.graph_objs as go

server = Flask(__name__)
app = dash.Dash(__name__, server= server, url_base_pathname='/home/')
vis = dash.Dash(__name__, server= server, url_base_pathname='/Visualize/')

vis.config['suppress_callback_exceptions']=True

app.layout = layout1
vis.layout = layout2

# ----------------- server handling ---------->

@server.route('/')
def home():
    return redirect('/home/')

@server.route('/view')
def viewData():
    return redirect('/Visualize/')

# ------------------ app callbacks ----------->
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children + [
        dcc.Link(
            html.Button(
                'Proceed',
                id='proBtn'
            ),
            refresh=True,
            href=url_for('viewData')
            #id='proBtn'
        ),

        html.Hr(id='hr2')]

# ----------------- vis callbacks ----------->

#load data for vis into system...
@vis.callback(Output('storageDiv', 'children'),[Input('myBody', 'children')])
def load_data2(children):
    try:
        df =  pd.read_csv('tmp/data.csv')
        print('dataset found')
        if df.empty != True:
            return df.to_json(date_format='iso', orient='split')

    except:
        print("Data not found..")
        return ''    


#update chart plot diagram (line)...
@vis.callback(Output('lineGraph', 'figure'),
              [Input('storageDiv', 'children'),
              Input('dropdownValue1', 'value'), Input('dropdownValue2', 'value')])
def update_line(data1, xValue, yValue):
    data = pd.read_json(data1, orient='split')

    plot = [go.Scatter(
                x=data[xValue],
                y=data[yValue],
                opacity=0.7
            )]

    figu = {
        'data': plot,

        'layout': go.Layout(
            xaxis={
                'title': xValue,
                'titlefont': dict(size=18, color='wheat'),
                'zeroline': False,
                'ticks': 'outside'
                },
            yaxis={
                'title': yValue,
                'titlefont': dict(size=18, color='wheat'),
                'ticks': 'outside'
                },
            margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            plot_bgcolor= '#27293d',
            paper_bgcolor='#27293d',
            font={'color':'#e14eca'},
            title='Your Dataset Analysis'
        )
    }

    return figu

if __name__ == '__main__':
    app.run_server(debug=True)