import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.subplots as sp
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json


def pie_chart(dataframe, values, names, title):
    """Pie chart with plotly

    Args:
        dataframe (pandas.DataFrame): Dataframe with the data
        values (String): Name of the column containing the value data
        names (String): Name of the column containing the names data
        title (String): Title of the chart

    Returns:
        String: String with plot in JSON
    """
    fig = px.pie(dataframe, values=values, names=names)
    fig.update_layout(title_text=title, title_x=0.5, titlefont=dict(size=22))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def bar_chart(dataframe, x_column, y_column, title, color_column, orientation='v', height=None):
    """Bar chart with plotly

    Args:
        dataframe (pandas.DataFrame): Dataframe with the data
        x_column (String): Name of the column containing the x-axis data
        y_column (String): Name of the column containing the y-axis data
        title (String): Title of the chart
        color_column (String): Values from this column are used to assign color to marks

    Returns:
        String: String with plot in JSON
    """
    fig = px.bar(dataframe, x=x_column, y=y_column, orientation=orientation,
            color=color_column,
            height=height)

    fig.update_layout(title_text=title, title_x=0.5, titlefont=dict(size=22))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def line_plot(dataframe, x_column, y_column, title):
    """Line plot with plotly

    Args:
        dataframe (pandas.DataFrame): Dataframe with the data
        x_column (String): Name of the column containing the x-axis data
        y_column (String): Name of the column containing the y-axis data
        title (String): Title of the chart

    Returns:
        String: String with plot in JSON
    """
    fig = px.line(dataframe, x=x_column, y=y_column, title=title)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def plot_advertising(x_col, y_col,
                     x_col2, y_col2, 
                     x_col3, y_col3, 
                     x_colp, y_colp, ):

    fig = make_subplots(rows=4, cols=1, subplot_titles=('Average exposure time of the advertising',  
                                                        'Average views of the advertising',
                                                        'Average play counts of the advertising',
                                                        'Average play counts of the advertising - Oaxaca'))

    fig.add_trace(go.Bar(x=x_col, y=y_col, name='AssetName'),
                    row=1, col=1)
    fig.add_trace(go.Bar(x=x_col2, y=y_col2, name='Views'),
                    row=2, col=1)
    fig.add_trace(go.Bar(x=x_col3, y=y_col3, name='DateHour'),
                    row=3, col=1)
    fig.add_trace(go.Line(x=x_colp, y=y_colp, name='UniqueVisitorId'),
                    row=4, col=1)

    fig['layout']['xaxis']['title']='AssetName'
    fig['layout']['xaxis2']['title']='AdExposure'
    fig['layout']['yaxis']['title']='AssetName'
    fig['layout']['yaxis2']['title']='Views'
    fig['layout']['xaxis3']['title']='AssetName'
    fig['layout']['xaxis4']['title']='AssetPlayCount'
    fig['layout']['yaxis3']['title']='DateHour'
    fig['layout']['yaxis4']['title']='UniqueVisitorId'

    fig.update_layout(height=1000, width=1250, title_text="Advertising information", title_x=0.5, titlefont=dict(size=35))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def heatmap(corr_df, title, axis_name):
    """Heatmap for correlation matrix

    Args:
        corr_df (Dataframe): Dataframe with correlation values
        title (String): Title of the heatmap graph
        axis_name (String): Name of both heatmap axis

    Returns:
        String: String with plot in JSON format
    """
    # The colorscale color can be changed with this
    colorscaleValue = [
        [0, 'rgb(255,0,0)'],
        [0.5, 'rgb(0,255,0)'],
        [1, 'rgb(0,0,255)'],
    ]

    fig = go.Figure(data=go.Heatmap(
        x=corr_df.columns.tolist(),
        y=corr_df.columns.tolist(),
        z=corr_df,
        colorscale = 'Earth',
        type = 'heatmap',
        text=corr_df.values.round(decimals=2).tolist(),
        texttemplate="%{text}",
        ))

    fig.data[0].update(zmin=-1, zmax=1)
    fig['layout']['xaxis']['title']=axis_name
    fig['layout']['yaxis']['title']=axis_name
    fig.update_layout(title_text=title)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def bar_chart_location(x_image, x_video, y_image, y_video, title, height=None):
    """Vertical stacked bar chart with 2 categories: Image and Video.
    This is for visitors' analytics dashboard

    Args:
        x_image (iterable): x-axis values for image
        x_video (iterable): x-axis values for video
        y_image (iterable): y-axis values for image
        y_video (iterable): y-axis values for video
        title (iterable): title of the bar chart
        height (int, optional): Height of the graph. Defaults to 800.
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_image, y=y_image, name='Image', orientation = 'h'))
    fig.add_trace(go.Bar(x=x_video, y=y_video, name='Video', orientation = 'h'))

    fig.update_layout(barmode='stack',
                title_text = title,
                yaxis={'categoryorder':'total ascending'},
                height=height)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
