# import required libraries
import dash
from dash import dash_core_components as dcc
from dash import html

# initiate app
app = dash.Dash()

# start layout
app.layout = html.Div([
    html.H1("Dashboard"),
    html.Div("This is a new dashboard")
])

# start app
if (__name__ == '__main__'):
    app.run_server()