#!/bin/python3
import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output, State
from data import decode_molecule
from dash.exceptions import PreventUpdate


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

# Define the Dash app
app = Dash(__name__)
app._favicon = "antibodies.ico"
app.title = "MabNameDecoder"

# Define the app layout
app.layout = html.Div([
    html.Div(
        children=[
            # Header
            html.H1(
                "Welcome to the Antibody Name Decoder webpage",
                style={'textAlign': 'center', 'margin-bottom': '20px'}
            ),

            # Input window
            dcc.Input(
                id='input-antibody',
                type='text',
                placeholder='Enter antibody name here',
                style={'margin': '10px', 'padding': '10px', 'width': '400px'}
            ),

            # Decode button
            html.Button('Decode', id='decode-button', n_clicks=0, style={'margin': '10px', 'padding': '10px'}),

            # Syllabified antibody name
            html.Div(
                id='syllabified-name',
                style={'margin': '10px', 'padding': '10px', 'font-weight': 'bold'}
            ),

            # Output table
            dash_table.DataTable(
                id='output-table',
                columns=[
                    {"name": "Part of Word", "id": "Part of Word"},
                    {"name": "Meaning", "id": "Meaning"}
                ],
                data=[],
                style_table={'margin': '10px', 'width': '33.33%'},
                style_header={'display': 'none'},  # Hide table header
                style_cell={'textAlign': 'left', 'padding': '10px'},
                    style_data_conditional=[
                    # Style the first row (index 0) with a specific background color and bold text
                    {
                        'if': {'row_index': 0},
                        'backgroundColor': '#83cec7',
                        'fontWeight': 'bold'
                    },
                    # Center-align the "Part of Word" column
                    {
                        'if': {'column_id': 'Part of Word'},
                        'textAlign': 'center'
                    },
                    # Left-align the "Meaning" column
                    {
                        'if': {'column_id': 'Meaning'},
                        'textAlign': 'left'
                    }
                ],
            ),
        ],
        style={
            'backdrop-filter': 'blur(10px)',
            'background-color': 'rgba(255, 255, 255, 0.5)',
            'padding': '10px',
            'margin': '20px auto',
            'border-radius': '10px',
            'width': '60%'
        }
    ),
    
    # Footer with GitHub link and creator information
    html.Div(
        children=[
            github_icon,
            h6_element
        ],
        style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'margin-top': '20px'}
    )
], style={
    'backgroundImage': "url('/assets/diginex.jpg')",
    'backgroundSize': 'cover',
    'padding': '20px',
    'border-radius': '0px',
    'border': 'none',  
    'width': '100%',
    'minHeight': '100vh'
})

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
        return [], '', f"The provided antibody name {antibody_name} is not valid!"

    # Convert the dictionary to a list of dictionaries for the DataTable
    new_data = [{'Part of Word': key, 'Meaning': value} for key, value in decoded_data.items()]

    # Syllabify the "Part of Word" column values and join them with hyphens
    part_of_word_list = [item['Part of Word'] for item in new_data][1::]

    syllabified_name = '-'.join(part_of_word_list)

    updated_data = new_data

    return updated_data, '', syllabified_name


if __name__ == '__main__':
    app.run_server(debug=True)
