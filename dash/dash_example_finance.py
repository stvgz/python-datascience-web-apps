# a finanace app showing stock prices and predictions with simple ARIMA
import datetime
from datetime import date
import dash
import dash.dependencies as dd
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import dash_extensions as de 
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame


import dash_table
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import os,sys
import datetime
import re

# 1. Make app
# app = dash.Dash(__name__,requests_pathname_prefix='/example-finance/')
app= dash.Dash(__name__)


# some config 
# make title (if applicable)
app.title='APP_NAME'

# 2. make content
# Contet-----------------------------------------------------------------------
content_list=[

    # some hidden components
    dcc.Store(id='memory'), # used to store data in memory and pass them between call backs
    Download(id='download'),  #used to download data

    dcc.Markdown(""" ### 最近12个月股价 Stock Price of Last 12 Months"""),
    dcc.Loading([
        dcc.Graph(
            id='chart_1',
            figure={
                'data': [],
                'layout': dict(
                    xaxis={'title': 'Time'},
                    yaxis={'title': 'Output'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest')
            }
        )

    ]),
    # dcc.Markdown(""" ##  Table"""),

    # dash_table.DataTable(
    #     id='table',
    #     columns=[],
    #     style_cell={  # use 
    #     'whiteSpace': 'normal',
    #     'height': 'auto',
    #     },
    #     style_table={'overflowX': 'auto'},  # use x scroll

    #     # page_current=0,
    #     # page_size=20,
    #     # page_action='native', #front end
    #     # sort_mode='single',
    #     # filter_action='native',
    #     # sort_action='native',

    # ),

]


#make sidebar
sidebar_list=[
    dcc.Markdown(""" # 请选择公司 Please Select Company Name"""),
    dcc.Dropdown(
        id='dropdown_name_selector',
        options=[
            {'label':'TESLA特斯拉','value':'TSLA'},
            {'label':'APPLE苹果公司','value':'AAPL'},
            # {'label':'AMAZON亚马逊','value':'AMZN'},
        ],
    multi=False,
    value='AAPL' # default Value
    )
    

]

sidebar=html.Div(
    # style=sidebar_content_style,
    sidebar_list
)

# compose page content
content=[html.Div(
        # style=content_style_bg,
        children=[
        dbc.Row(
            [
                # dbc.Col(content,width=2),
                # dbc.Col(sidebar,width=3),
                dbc.Col(sidebar,width=3,
                        # style=sidebar_content_style
                        )
                        ,
                dbc.Col(content_list,
                # style=content_style_inner
                )
            ]
        )
    ])]

app.layout = html.Div(content)

def get_stock(stock_name,source='csv',start='all',end='all'):
    """
    Get stock values from local files or internet
    """

    # base_dir = os.getcwd()
    file_dir = os.path.abspath(__file__)
    base_dir = os.path.dirname(file_dir)

    if source=='web':
        import pandas_datareader.data as web
        import yfinance as yf
        yf.pdr_override()

        start=datetime.datetime.now()-datetime.timedelta(days=360)
        end=datetime.datetime.now()
        df=web.get_data_yahoo(stock_name,start,end)

    elif source=='csv':
        if stock_name=="AAPL":
            df = pd.read_csv(os.path.join(base_dir,'AAPL.csv'))
        if stock_name =='TSLA':
            df = pd.read_csv(os.path.join(base_dir,'TSLA.csv'))
            # pass
    else:
        df=pd.DataFrame()
    return df

# update from some input
@app.callback(dd.Output('chart_1','figure'),
              [dd.Input('dropdown_name_selector','value')],
              [dd.State('dropdown_name_selector','value')])
def update(n,stock_name):
    
    df=get_stock(stock_name=stock_name)
    df=df.reset_index()

    df = df.rename(columns={'trade_date':'Date'})
    # df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].apply(lambda x: datetime.datetime.strptime(str(x),'%Y%m%d'))

    df = df.head(360)

    fig=go.Figure()
    fig.add_trace(go.Candlestick(x=df.Date,open=df.open,close=df.close,high=df.high,low=df.low))

    fig.update_layout(height=600)
    # fig.add_trace()
    
    return fig


if __name__ == '__main__':
    
    # app.run_server(debug=True)
    app.run_server(host="0.0.0.0", port=8050)

    # app.run_server(host="0.0.0.0",port=9999)
    # app.run_server(host="0.0.0.0",port=8050)