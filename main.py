#!/bin/python3

import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output, State, ctx
from data import decode_molecule, disease_infixes, mab_new_names
from dash.exceptions import PreventUpdate


encode_disease_infixes = {value:key for key, value in disease_infixes.items()}

# Define the GitHub link and icon
github_link = "https://github.com/kate-simonova/antibody-name-converter"

github_icon = html.A(
    href=github_link,
    children=[
        html.Img(src="https://img.icons8.com/material-rounded/48/000000/github.png", style={'width': '40px', 'height': '40px'})
    ],
    target="_blank",
    style={'margin-right': '10px'}
)

h6_element = html.H6(
    "Created by Ekaterina Simonova © 2024",
    style={'textAlign': 'center', 'color': '#333333', 'font-size': '15px', 'font-family': 'cursive', 'margin': '0'}
)

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

style_page = {
    'backdrop-filter': 'blur(10px)',
    'background-color': 'rgba(255, 255, 255, 0.5)',
    'padding': '10px',
    'margin': '20px auto',
    'border-radius': '10px',
    'width': '60%'
}

# Define the Dash app
app = Dash(__name__)
app._favicon = "antibodies.ico"
app.title = "MabNameDecoder"

# Create layout with tabs
app.layout = html.Div(
    html.Div(
        dcc.Tabs([
            # Decoder tab
            dcc.Tab(
                label='Decoder',
                children=[
                    # Content of the Decoder tab here
                    html.Div(
                        children=[
                            html.H1("Welcome to the Monoclonal Antibody Name Decoder", style={'textAlign': 'center', 'margin-bottom': '20px'}),
                            dcc.Input(id='input-antibody', type='text', placeholder='Enter antibody name here', maxLength=50, style={'margin': '10px', 'padding': '10px', 'width': '400px'}),
                            html.Button('Decode', id='decode-button', n_clicks=0, style={'margin': '10px', 'padding': '10px'}),
                            html.Div(id='syllabified-name', style={'margin': '10px', 'padding': '10px', 'font-weight': 'bold', 'fontSize': '18px'}),
                            dash_table.DataTable(
                                id='output-table',
                                columns=[
                                    {"name": "Part of Word", "id": "Part of Word"},
                                    {"name": "Meaning", "id": "Meaning"}
                                ],
                                data=[],
                                style_table={'margin': '10px', 'width': '33.33%'},
                                style_header={'display': 'none'},
                                style_cell={'textAlign': 'left', 'padding': '10px'},
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 0},
                                        'backgroundColor': '#83cec7',
                                        'fontWeight': 'bold'
                                    },
                                    {
                                        'if': {'column_id': 'Part of Word'},
                                        'textAlign': 'center'
                                    },
                                    {
                                        'if': {'column_id': 'Meaning'},
                                        'textAlign': 'left'
                                    }
                                ],
                            ),
                        ],
                        style= style_page,
                    ),
                ],
                style=tab_style,
                selected_style=tab_selected_style
            ),
            
            # Generator tab
            dcc.Tab(
                label='Generator',
                children=[
                    html.Div(
                        children=[
                            html.H1("Welcome to the Monoclonal Antibody Name Generator", style={'textAlign': 'center'}),
                            dcc.Input(id='prefix-input', type='text', placeholder='Input your prefix', maxLength=50, style={'margin': '15px 0 15px 25px', 'padding': '10px', 'width': '380px'}),
                            dcc.Dropdown(
                                id='infix-dropdown',
                                options=list(encode_disease_infixes.keys()),
                                placeholder='Select Infix for target class',
                                style={'margin': '10px', 'padding': '0px', 'width': '500px'}
                            ),
                            dcc.Dropdown(
                                id='suffix-dropdown',
                                options=list(mab_new_names.keys()),
                                placeholder='Select suffix based on the immunoglobulin variable domain',
                                style={'margin': '10px', 'padding': '0px', 'width': '500px'}
                            ),
                            html.Button('Generate', id='generate-button', n_clicks=0, style={'margin': '15px 0 15px 25px', 'padding': '10px'}),
                            html.Br(),
                            html.Div(id='antibody-name', style={'margin': '10px', 'padding': '10px', 'fontSize': '18px', "font-weight": "bold", 'display': 'inline-block'}),
                        ],
                        style= style_page,
                    ),
                ],
                style=tab_style,
                selected_style=tab_selected_style
            ),
        ]),
    ),
    style={
        'backgroundImage': "url('/assets/diginex.jpg')",
        'backgroundSize': 'cover',
        'padding': '20px',
        'border-radius': '0px',
        'border': 'none',
        'width': '100%',
        'minHeight': '100vh'
    }
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
def decode_antibody(n_clicks, antibody_name, existing_data):
    if n_clicks == 0 or not antibody_name:
        raise PreventUpdate

    decoded_data = decode_molecule(antibody_name)

    if decoded_data is None:
        return [], '', f"The provided monoclonal antibody name {antibody_name} is not valid!"

    # Convert the dictionary to a list of dictionaries for the DataTable
    new_data = [{'Part of Word': key, 'Meaning': value} for key, value in decoded_data.items()]

    # Syllabify the "Part of Word" column values and join them with hyphens
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

def generate_name(prefix, infix, suffix, n_clicks):

    if n_clicks == 0 or ctx.triggered_id != "generate-button":
        raise PreventUpdate

    if not prefix:
        return "Please input a prefix (it should contain at least one letter)"

    if not infix:
        return "Please select an infix"

    if not suffix:
        return "Please select a suffix"

    prefix = prefix.lower().capitalize()

    return f"Your monoclonal antibody name: {prefix + encode_disease_infixes[infix] + mab_new_names[suffix]}" 


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=9000, processes=2, threaded=False)
