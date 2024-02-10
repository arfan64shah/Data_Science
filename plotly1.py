# import required libraries
import dash
from dash import html
from dash import dcc

# initiate app
app = dash.Dash()

# initiate layout
app.layout = html.Div([
    html.H1("Visualization Dashboard"),
    html.Div("This Dashboard is for visualization")
])

if (__name__ == '__main__'):
    app.run_server()