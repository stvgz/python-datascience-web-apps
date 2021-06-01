
import tushare as ts  # 获取股票信息
import dash # 设计网站
from datetime import datetime, timedelta
import dash_core_components as dcc #设计网站采用的核心插件库
import dash_bootstrap_components as dbc #设计网站采用的美化页面
import dash_html_components as html  #设计网站采用的核心插件库
from dash.dependencies import Input, Output, State # 完成用户点击响应
import plotly.graph_objects as go # 画出趋势图
from dash.exceptions import PreventUpdate
import pandas as pd

# ID definitions
id_button_update_a_share_list = 'id-button-update-a-share-list'
id_dpl_share_code = 'id-dpl-share-code'
id_date_picker_range = 'id-date-picker-range'
id_button_query_trend = 'id-button-query-trend'
id_graph_hist_trend_graphic = 'id-graph-hist-trend-graphic'

# create dash app
app = dash.Dash(__name__)

# layout design
header = html.H2("股票查询", className='text-center')
# update list button
update_a_share_button = dbc.Button(
    id=id_button_update_a_share_list,
    color='light',
    children='更新列表', outline=True)
# share select dropdown list
select_share = dcc.Dropdown(
    id=id_dpl_share_code,
    options=update_a_share_list()
)
# datetime picker
date_pick = dcc.DatePickerRange(
    id='id-date-picker-range',
    max_date_allowed=datetime.today(),
    start_date=datetime.today().date() - timedelta(days=60),
    end_date=datetime.today().date()
)
# query button
query_button = dbc.Button(
    "查询",
    color="warning",
    className="mr-1",
    id=id_button_query_trend,
    outline=False)

# make a better row/col layout
select_share_row = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [select_share],
                    className='col-5'),
                dbc.Col(
                    [update_a_share_button],
                    className='col-2')]),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [date_pick],
                    className='col-5'),
                dbc.Col(
                    [query_button],
                    className='col-1')])])

# get default figure
default_fig = plot_candlestick(
    get_trend_df(
        '000001.SZ',
        start_date='20200101',
        end_date='20200707'))
# graphic div
graphic_div = dbc.Container(
    [dcc.Graph(figure=default_fig, id=id_graph_hist_trend_graphic)])

# fully layout
app.layout = html.Div([
    header,
    select_share_row,
    html.Br(),
    graphic_div,
])


@app.callback(
    Output(id_graph_hist_trend_graphic, 'figure'),
    [Input(id_button_query_trend, 'n_clicks')],
    [State(id_dpl_share_code, 'value'),
     State(id_date_picker_range, 'start_date'),
     State(id_date_picker_range, 'end_date')]
)
def update_output_div(query, share, start, end):
    if query is not None:
        share_code = split_share_to_code(share)
        start_str = start.replace("-", "")
        end_str = end.replace("-", "")
        return plot_candlestick(
            get_trend_df(
                share_code,
                start_date=start_str,
                end_date=end_str))
    else:
        raise PreventUpdate