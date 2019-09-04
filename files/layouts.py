import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

dff =  pd.read_csv('tmp/data.csv')

layout1 = html.Div([
    html.H1(
            'Upload Dataset (.csv)',
            id='uploadH1',
            style={
                'marginTop': '3%',
                'align': 'center',
                'fontSize': '2.1rem',
                'color': 'blue',
                'fontStyle': 'oblique'
            }),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ],
        style={'color': 'cornflowerblue'}),
        style={
            'width': '80%',
            'height': '70px',
            'textAlign': 'center',
            'fontSize': '17px',
            'fontStyle': 'italic',
            'lineHeight': '50px',
            'borderStyle': 'dashed',
            'borderColor': 'cornflowerblue',
            'borderWidth': '1.5px',
            'borderRadius': '10px',
            'margin': '5% 10%'
        },
        # Allow multiple files to be uploaded
        multiple=True,
        #Allow certain file types...
        #accept = "text/csv, application/vnd.ms-excel"
        ),
        html.Div(id='output-data-upload'),
    ],
    id = 'myBody'
    )


layout2 = html.Div([
                #Options
                html.Div([
                    html.H4('Chart Options'),
                    html.Div(
                        id='graphOptions',
                        children = [
                            html.Div([
                                html.Div([
                                    'X-axis:',
                                    dcc.Dropdown(
                                        id='dropdownValue1',
                                        options = [{'label': i, 'value': i} for i in dff.columns.unique()],
                                        placeholder='Select Value...',
                                        style={'width': '50%', 'margin': '3px'}
                                    ),
                                    'Y-axis:',
                                    dcc.Dropdown(
                                        id='dropdownValue2',
                                        options = [{'label': i, 'value': i} for i in dff.columns.unique()],
                                        placeholder='Select Value...',
                                        style={'width': '50%', 'margin': '3px'}
                                    )
                                ],
                                style={'display': 'flex'})
                                        
                            ])
                        ],
                        style={
                            'margin': '7px',
                            'borderStyle': 'solid',
                            'borderWidth': 'thin',
                            'borderRadius': '8px',
                            'borderColor': 'gray'
                            }
                    )
                ]),

                html.Hr(
                    style={
                        'width':'90%',
                        'backgroundColor':'darkslategrey',
                        'margin': '2% 5%'
                        }
                    ),

                #Graph Chart
                html.Div(
                    id='chartArea',
                    children = [
                        dcc.Graph(
                            id='lineGraph'
                        )
                    ]
                ),

                # Hidden div inside the app that stores the dataset values...
                html.Div(id='storageDiv', style={'display': 'none'}),
                
            ],
            id='myBody'
        )