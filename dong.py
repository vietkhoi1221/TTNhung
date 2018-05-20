import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
i =1
X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)
Z = deque(maxlen=20)
Z.append(1)


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    global i
    YY = []
    ZZ = []
    graph_data = open('example.txt','r').read()
    lines = graph_data.split("\n")
    for line in lines:
        if len(line) > 1:
            xs,ys,zs = line.split(',')
            YY.append(int(ys))
            ZZ.append(int(zs))
    X.append(X[-1]+1)
    Y.append(YY[i])
    Z.append(ZZ[i])
    i = i+1
    data1 = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Z),
            name='Độ ẩm',
            mode= 'lines+markers'
            )
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Nhiệt độ',
            mode= 'lines+markers'
            )

    return {'data': [data1,data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y)-10,max(Z)+10]),)}



if __name__ == '__main__':
    app.run_server(debug=True)