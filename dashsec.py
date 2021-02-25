import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

data = pd.read_csv('ASHO20.csv', header=None, skiprows=[0])
data.columns = ['del', 'Date', 'Values']
data.tail()

st = data.drop(['del'], axis=1)
st.dropna(axis=0, how='any', inplace=True)
st['Date'] = pd.to_datetime(st['Date'], format='%Y-%m-%d')
st.tail()

dates = ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01',
         '2020-05-01', '2020-06-01', '2020-07-01', '2020-08-01', '2020-09-01', '2020-10-01', '2020-11-01', '2020-12-21']

dates_m = ['Jan', 'Feb', 'March', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
date_mark = {i: dates[i] for i in range(0, 12)}
date_mark_m = {i: dates_m[i] for i in range(0, 12)}

trace_1 = go.Scatter(x=st.Date, y=st['Values'],
                     name='A',
                     line=dict(width=1,
                               color='rgb(229, 151, 50)'))
layout = go.Layout(title='Time Series Plot',
                   hovermode='closest')
figure = go.Figure(data=[trace_1], layout=layout)
figure.update_xaxes(
    ticklabelmode="period", rangeslider_visible=True, autorange=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="day", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    ))

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Graph(id='plot', figure=figure),

    html.P([
        html.Label("Time Period"),
        dcc.RangeSlider(id='slider',
                        marks=date_mark_m,
                        min=0,
                        max=11,
                        value=[0, 5])
    ], style={'width': '80%',
              'fontSize': '20px',
              'padding-left': '100px',
              'display': 'inline-block'})
])


@app.callback(Output('plot', 'figure'),
              [Input('slider', 'value')])
def update_figure(X):
    st2 = st[(st.Date > dates[X[0]]) & (st.Date < dates[X[1]])]
    trace_1 = go.Scatter(x=st2.Date, y=st2['Values'],
                         name='A',
                         line=dict(width=1,
                                   color='rgb(229, 151, 50)'))
    figure = go.Figure(data=[trace_1], layout=layout)
    figure.update_xaxes(
        dtick="M1",
        tickformat="%m\n%Y",
        ticklabelmode="period",
        rangeslider_visible=True, autorange=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ))
    return figure


if __name__ == '__main__':
    app.run_server()
