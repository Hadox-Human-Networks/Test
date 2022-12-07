from flask import render_template
from ..helper import read_from_postgres, pie_chart, bar_chart, line_plot
from ..helper import plot_advertising, bar_chart_location
import pandas as pd

def analytics_controller(category):
    """Controller for analytics dashboards for every category

    Args:
        category: category of the analytics dashboard selected in the index form
    """
    if category == 'customer':
        """TODO: Add filter by region"""
        information = {}
        query = 'SELECT "Customer", "EndpointId", "DateHour" FROM winkle_data.scenary_i'
        columns = ['Customer', 'EndpointId', 'DateHour']
        title = 'Percentage of customers'

        df = read_from_postgres(query=query, columns_names=columns)
        df_customer = df.groupby(by=['Customer']).count()

        graph_customer = pie_chart(df_customer.reset_index(), values='EndpointId', names='Customer', title=title)

        # Information
        max_value = df_customer.EndpointId.values.max()
        max_percent = max_value / df_customer.EndpointId.sum()
        max_customer = df_customer[df_customer['EndpointId']==max_value].index.values[0]
        min_date = pd.to_datetime(df['DateHour']).dt.date.min()
        max_date = pd.to_datetime(df['DateHour']).dt.date.max()
        information['category'] = category
        information['max_value'] = max_value
        information['max_percent'] = round(max_percent * 100, 2)
        information['max_customer'] = max_customer
        information['min_date'] = min_date
        information['max_date'] = max_date

        return render_template('dashboards/analytics_customer.html', graphJSON=graph_customer, information=information)

        
    elif category == 'asset':
        information = {}
        query = 'SELECT "Source", "EndpointId", "AssetTypeName", "DateHour" FROM winkle_data.scenary_i'
        columns = ['Source', 'EndpointId', 'AssetTypeName', 'DateHour']
        title = 'Percentage of records with and specific OS and Asset Type'
        df = read_from_postgres(query=query, columns_names=columns)
        
        df_asset = df.groupby(by=['Source', 'AssetTypeName']).count().reset_index()

        graph_asset = bar_chart(df_asset, x_column='EndpointId', y_column='Source', title=title,
                         color_column='AssetTypeName', orientation='h')

        max_value = df_asset.groupby('Source').sum().max().values[0]
        max_value_asset = df_asset.groupby('AssetTypeName').sum().max().values[0]

        aux_df = df_asset.sort_values(by='Source')
        max_source = aux_df['Source'][0]

        aux_df_asset = df_asset.sort_values(by='AssetTypeName')
        max_asset = aux_df_asset['AssetTypeName'][0]

        min_date = pd.to_datetime(df['DateHour']).dt.date.min()
        max_date = pd.to_datetime(df['DateHour']).dt.date.max()
        aux_info = aux_df.sort_values(by=['Source','EndpointId'])

        information['category'] = category
        information['max_source'] = max_source
        information['max_value'] = max_value
        information['max_asset'] = max_asset
        information['max_value_asset'] = max_value_asset
        information['min_date'] = min_date
        information['max_date'] = max_date
        information['Linux_info'] = aux_info['AssetTypeName'].values[1]
        information['Windows_info'] = aux_info['AssetTypeName'].values[3]
        return render_template('dashboards/analytics_asset.html', graphJSON=graph_asset, 
                                information=information, category=category)

    elif category == 'visitors':
        information = {}
        query = 'SELECT "Location", "UniqueVisitorId", "AssetTypeName", "DateHour" FROM winkle_data.scenary_i WHERE "AdExposure" > 60'
        columns = ['Location', 'UniqueVisitorId', 'AssetTypeName', 'DateHour']
        title = 'Number of visitors showing interest in an advertisement'

        df = read_from_postgres(query=query, columns_names=columns)
        
        df_visitors = df.groupby(by=['Location', 'AssetTypeName']).count().sort_values('UniqueVisitorId').reset_index()
        df_image = df_visitors.loc[df_visitors['AssetTypeName']=='Image']
        df_video = df_visitors.loc[df_visitors['AssetTypeName']=='Video']
        df_image.set_index('Location', inplace=True)
        df_video.set_index('Location', inplace=True)

        graph_visitors = bar_chart_location(x_image=df_image.UniqueVisitorId,
                                    y_image=df_image.index,
                                    x_video=df_video.UniqueVisitorId,
                                    y_video=df_video.index,
                                    title=title,
                                    height=800)

        # Information
        max_value = df_visitors.groupby('Location').sum().max().values[0]
        df_visitors_sorted = df_visitors.groupby('Location').sum().sort_values('UniqueVisitorId')
        max_state = df_visitors_sorted[df_visitors_sorted['UniqueVisitorId']==int(max_value)].index.values[0]
        max_percent = max_value / df_visitors.UniqueVisitorId.sum()
        min_date = pd.to_datetime(df['DateHour']).dt.date.min()
        max_date = pd.to_datetime(df['DateHour']).dt.date.max()
        information['category'] = category
        information['max_value'] = max_value
        information['max_percent'] = round(max_percent * 100, 2)
        information['max_state'] = max_state
        information['min_date'] = min_date
        information['max_date'] = max_date
        return render_template('dashboards/analytics_visitors.html', graphJSON=graph_visitors, information=information)


    elif category == 'advertising':
        query = 'SELECT "AssetName", "AdExposure", "Views", "AssetPlayCount", "DateHour", "UniqueVisitorId", "Location" FROM winkle_data.scenary_i'
        columns = ['AssetName', 'AdExposure', 'Views', 'AssetPlayCount', 'DateHour', 'UniqueVisitorId', 'Location']

        df = read_from_postgres(query=query, columns_names=columns)


        # Bar chart for exposure time (Graph #1)
        title_exposure = 'Average exposure time of the advertising'
        df_exposure = df.drop(['Views', 'AssetPlayCount', 'DateHour', 'UniqueVisitorId'], axis=1)
        df_exposure = df.groupby('AssetName') \
                        .mean() \
                        .sort_values('AdExposure', ascending=False) \
                        .reset_index()
        # df_exposure,x_column='AssetName',y_column='AdExposure',title=title_exposure,color_column='AssetName'

        # Bar chart for views (Graph #2)
        title_views = 'Average views of the advertising'
        df_views = df.drop(['AdExposure', 'AssetPlayCount', 'DateHour', 'UniqueVisitorId'], axis=1)
        df_views = df.groupby('AssetName') \
                        .mean() \
                        .sort_values('Views', ascending=False) \
                        .reset_index()
        #(df_views,x_column="AssetName",y_column="Views",title=title_views,color_column='AssetName')

        # Bar chart for play counts (Graph #3)
        title_play_count = 'Average play counts of the advertising'
        df_play_count = df.drop(['AdExposure', 'Views', 'DateHour', 'UniqueVisitorId'], axis=1)
        df_play_count = df.groupby('AssetName') \
                        .mean() \
                        .sort_values('AssetPlayCount', ascending=False) \
                        .reset_index()
        #df_play_count,x_column="AssetName",y_column="AssetPlayCount",title=title_play_count,color_column='AssetName')

        # Line plot for average play counts (Graph #4)
        location = 'Oaxaca'
        title_oaxaca = f'Average play counts of the advertising - {location}'
        
        
        df_oaxaca = df[df['Location'] == location]
        df_oaxaca = df_oaxaca.drop(['AdExposure', 'Views', 'AssetPlayCount', 'AssetName'], axis=1)
        df_oaxaca = df_oaxaca.groupby(['Location', 'DateHour'])[['UniqueVisitorId']].count().reset_index()
        df_oaxaca['DateHour'] = pd.to_datetime(df_oaxaca['DateHour'])
        df_oaxaca = df_oaxaca.resample('12H', on='DateHour').sum().reset_index()
        #df_oaxaca,x_column='DateHour',y_column="UniqueVisitorId",title=title_oaxaca)

        graph = plot_advertising(x_col=df_exposure['AssetName'],y_col=df_exposure['AdExposure'],
                                 x_col2=df_views["AssetName"],y_col2=df_views["Views"],
                                 x_col3=df_play_count["AssetName"],y_col3=df_play_count["AssetPlayCount"],
                                 x_colp=df_oaxaca['DateHour'],y_colp=df_oaxaca["UniqueVisitorId"])

        return render_template('dashboards/analytics.html', category=category, 
                                graphJSON=[graph])#, graph_views#    , graph_play_count, graph_oaxaca])
    else:
        file_name = f'img/{category}.png'
        return render_template('dashboards/dashboards.html', title='Data Descriptors', category=category, file_name=file_name)
