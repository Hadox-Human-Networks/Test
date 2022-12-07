from ..helper import read_from_postgres, bar_chart, pie_chart, set_sex
from flask import render_template
import pandas as pd
import numpy as np


def data_controller(category):
    """Controller for data descriptors dashboards for every category

    Args:
        category: category of the data descriptors dashboard selected in the index form
    """
    if category == 'emotions':
        query = 'SELECT "Impressions", "Happy", "Sad", "Anger", "Surprise", "Neutral" FROM winkle_data.scenary_i'
        title_emotions = 'Quantity of weighted emotions detected'
        columns = ['Impressions','Happy', 'Sad', 'Anger', 'Surprise', 'Neutral' ]
        information = {}

        # Calculating weighted sum
        df = read_from_postgres(query=query, columns_names=columns)
        df['Happy (wg)'] = df.apply(lambda x: x.Impressions * x.Happy, axis=1)
        df['Sad (wg)'] = df.apply(lambda x: x.Impressions * x.Sad, axis=1)
        df['Anger (wg)'] = df.apply(lambda x: x.Impressions * x.Anger, axis=1)
        df['Surprise (wg)'] = df.apply(lambda x: x.Impressions * x.Surprise, axis=1)
        df['Neutral (wg)'] = df.apply(lambda x: x.Impressions * x.Neutral, axis=1)

        df = df.drop(columns=columns, axis=1)

        # Naming columns and sorting
        df_emotions = pd.DataFrame(df.sum(), columns=['Weighted sum'])
        df_emotions.index.name = 'Emotions'
        df_emotions =  df_emotions.sort_values('Weighted sum', ascending=False).reset_index()

        # Description
        max_values = df_emotions.values[:3]
        sum_values = df_emotions['Weighted sum'].sum()
        max_percent = [[round(i/sum_values * 100, 2)] for i in max_values[:,1].tolist()]
        values = np.insert(max_values, [2], max_percent, axis=1).tolist()
        information['category'] = category
        information['max_emotions'] = values

        graph_emotions = bar_chart(df_emotions, x_column='Emotions', y_column='Weighted sum', color_column='Emotions', title=title_emotions)
        return render_template('dashboards/data_emotions.html', information=information, graphJSON=graph_emotions)

# --------------------------------------------------------------------------------------------------------------------        
    elif category == 'age':
        information = {}
        query = 'SELECT "Impressions", "Under_18", "Age18", "Age25", "Age35", "Age45", "Age55", "Age65" FROM winkle_data.scenary_i'
        title_age = 'Percentage of weighted ages detected'
        columns = ['Impressions','Under_18', 'Age18', 'Age25', 'Age35', 'Age45', 'Age55', 'Age65']

        df = read_from_postgres(query=query, columns_names=columns)
        df['Under18_wg'] = df.apply(lambda x: x.Impressions * x.Under_18, axis=1)
        df['Age18_wg'] = df.apply(lambda x: x.Impressions * x.Age18, axis=1)
        df['Age25_wg'] = df.apply(lambda x: x.Impressions * x.Age25, axis=1)
        df['Age35_wg'] = df.apply(lambda x: x.Impressions * x.Age35, axis=1)
        df['Age45_wg'] = df.apply(lambda x: x.Impressions * x.Age45, axis=1)
        df['Age55_wg'] = df.apply(lambda x: x.Impressions * x.Age55, axis=1)
        df['Age65_wg'] = df.apply(lambda x: x.Impressions * x.Age65, axis=1)

        df = df.drop(columns=columns)

        df_age = pd.DataFrame(df.sum(), columns=['Sum_wg'])
        df_age.index.name = 'Age'

        graph_age = bar_chart(df_age.reset_index(), x_column='Age', y_column='Sum_wg', color_column='Age', title=title_age)

        information['category'] = category
        information['total'] = len(df)

        return render_template('dashboards/data_descriptors_age.html', category=category, graphJSON=graph_age, information=information)

# --------------------------------------------------------------------------------------------------------------------
    elif category == 'sex':
        information = {}
        query = 'SELECT "ImpMale", "ImpFemale" FROM winkle_data.scenary_i'
        title_sex = 'Percentage of people detected as male or female'
        columns = ['ImpMale', 'ImpFemale']

        df = read_from_postgres(query=query, columns_names=columns)
        df['Sex'] = df.apply(lambda x : set_sex(x.ImpFemale, x.ImpMale),axis=1)
        df_sex = df.groupby('Sex').count().reset_index()[['Sex', 'ImpMale']].rename(columns={'ImpMale': 'count'})

        graph_sex = pie_chart(df_sex, values='count', names='Sex', title=title_sex)
        information['category'] = category
        information['total'] = len(df)
        return render_template('dashboards/data_descriptors_sex.html', category=category, graphJSON=graph_sex, information=information)
    else:
        file_name = f'img/{category}.png'

        return render_template('dashboards.html', title='Data Descriptors', category=category, file_name=file_name)
