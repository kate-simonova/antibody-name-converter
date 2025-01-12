#!/bin/python3

import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output, State, ctx
from data import decode_molecule, disease_infixes, mab_new_names, encode_disease_infixes
from dash.exceptions import PreventUpdate


# Define the GitHub link and icon
github_link = 'https://github.com/kate-simonova/antibody-name-converter'

github_icon = html.A(href='https://github.com/kate-simonova', children=[
    html.Img(className='github-icon', src='https://img.icons8.com/material-rounded/48/000000/github.png')
], className='github-icon')

footer = html.H2('Created by Ekaterina Simonova © 2024')


# Define style for tabs
tab_style = {
    'backgroundColor': '#78b2ab',
    'color': '#333333',
    'font-size': '16px',
    'cursor': 'pointer',
    'fontWeight': 'bold',
    'borderBottom': '1px solid black',
}

tab_selected_style = {
    'backgroundColor': '#83cec7',
    'borderTop': '1px solid black',
    'borderLeft': '1px solid black',
    'borderRight': '1px solid black',
    'borderBottom': '1px solid black',
    'color': 'black',
    'font-size': '20px',
    'cursor': 'pointer',
    'fontWeight': 'bold',
}


# Define the Dash app
app = Dash(__name__)
app._favicon = 'antibodies.ico'
app.title = 'MabNameConverter'

# Create layout with tabs
app.layout = html.Div(
    html.Div(
        dcc.Tabs([
            # Decoder tab
            dcc.Tab(
                label='Decoder',
                children=[
                    html.Div(
                        children=[
                            html.H1('Welcome to the Monoclonal Antibody Name Decoder'),
                            dcc.Input(id='input-antibody', type='text', placeholder='Enter antibody name here', maxLength=50),
                            html.Button('Decode', id='decode-button', n_clicks=0),
                            html.Div(id='syllabified-name'),
                            dash_table.DataTable(
                                id='output-table',
                                data=[],
                            ),
                        ],
                        className='style-page',
                    ),
                html.Div(
                    children=[
                        github_icon,
                        footer
                    ],
                    className='footer-style'
                )],
                style=tab_style,
                selected_style=tab_selected_style
            ),
            
            # Generator tab
            dcc.Tab(
                label='Generator',
                children=[
                    html.Div(
                        children=[
                            html.H1('Welcome to the Monoclonal Antibody Name Generator'),
                            dcc.Input(id='prefix-input', type='text', placeholder='Input your prefix', maxLength=50),
                            dcc.Dropdown(
                                id='infix-dropdown',
                                options=list(encode_disease_infixes.keys()),
                                placeholder='Select Infix for target class',
                                className='generator-dropdown',
                            ),
                            dcc.Dropdown(
                                id='suffix-dropdown',
                                options=list(mab_new_names.keys()),
                                placeholder='Select suffix based on the immunoglobulin variable domain',
                                className='generator-dropdown'
                            ),
                            html.Button('Generate', id='generate-button', n_clicks=0),
                            html.Br(),
                            html.Div(id='antibody-name', className='gen-out'),
                        ],
                        className='style-page',
                    ),
                html.Div(
                    children=[
                        github_icon,
                        footer
                    ],
                    className='footer-style'
                )],
                style=tab_style,
                selected_style=tab_selected_style
            ),
        ]),
    ),
    className='layout-style',
)

# Callback function
@app.callback(
    [Output('output-table', 'data'),
     Output('input-antibody', 'value'),
     Output('syllabified-name', 'children')],
     Input('decode-button', 'n_clicks'),
     State('input-antibody', 'value'),
     State('output-table', 'data')
)

def decode_antibody_name(n_clicks, antibody_name, existing_data):
    if n_clicks == 0 or not antibody_name:
        raise PreventUpdate

    decoded_data = decode_molecule(antibody_name)

    if decoded_data is None:
        return [], '', f'The provided monoclonal antibody name {antibody_name} is not valid!'

    new_data = [{'Part of Word': key, 'Meaning': value} for key, value in decoded_data.items()]

    part_of_word_list = [item['Part of Word'] for item in new_data][1::]

    syllabified_name = '-'.join(part_of_word_list)

    updated_data = new_data

    return updated_data, '', syllabified_name


@app.callback(
    Output('antibody-name', 'children'),
    Input('prefix-input', 'value'),
    Input('infix-dropdown', 'value'),
    Input('suffix-dropdown', 'value'),
    Input('generate-button', 'n_clicks')
)

def encode_antibody_name(prefix, infix, suffix, n_clicks):

    if n_clicks == 0 or ctx.triggered_id != 'generate-button':
        raise PreventUpdate

    if not prefix:
        return 'Please input a prefix (it should contain at least one letter)'

    if not infix:
        return 'Please select an infix'

    if not suffix:
        return 'Please select a suffix'

    prefix = prefix.lower().capitalize()

    return f'Your monoclonal antibody name: {prefix + encode_disease_infixes[infix] + mab_new_names[suffix]}' 


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=9000, processes=1, threaded=False)