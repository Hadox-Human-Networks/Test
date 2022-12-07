from flask import render_template
from ..helper import read_from_postgres, heatmap

def ml_controller(category):
    """Controller for machine learning dashboards for every category

    Args:
        category: category of the machine learning dashboard selected in the index form
    """
    if category == 'classifier':
        information = {}
        query = 'SELECT "Happy", "Sad", "Anger", "Surprise", "Neutral" FROM winkle_data.scenary_i'
        columns = ["Happy", "Sad", "Anger", "Surprise", "Neutral"]
        title = 'Correlation matrix - Emotions'

        df = read_from_postgres(query=query, columns_names=columns)
        corr_df = df.corr(method='pearson')

        heatmap_emotions = heatmap(corr_df, title=title, axis_name='Emotions')

        # Information
        information['category'] = category
        return render_template('dashboards/ml_classifier.html', graphJSON=heatmap_emotions, information=information)
    if category == 'regressor':
        information = {}
        query = 'SELECT "Happy", "Anger", "Sad", "Surprise", "Neutral", "Under_18", "Age18", "Age25", "Age35", "Age45", "Age55", "Age65", "ImpMale", "ImpFemale" FROM winkle_data.scenary_i'
        columns = ["Happy", "Anger", "Sad", "Surprise", "Neutral", "Under_18", "Age18", "Age25", "Age35", "Age45", "Age55", "Age65", "ImpMale", "ImpFemale"]
        df = read_from_postgres(query=query, columns_names=columns)

        ## Emotions
        title = 'Correlation matrix - Emotions'
        df_emotions = df[["Happy", "Anger", "Sad", "Surprise", "Neutral"]]
        corr_df = df_emotions.corr(method='pearson')
        heatmap_emotions = heatmap(corr_df, title=title, axis_name='Emotions')

        ## Age
        title = 'Correlation matrix - Age'
        df_age = df[["Under_18", "Age18", "Age25", "Age35", "Age45", "Age55", "Age65"]]
        corr_df = df_age.corr(method='pearson')
        heatmap_age = heatmap(corr_df, title=title, axis_name='Age')

        ## Sex
        title = 'Correlation matrix - Sex'
        df_sex = df[["ImpMale", "ImpFemale"]]
        corr_df = df_sex.corr(method='pearson')
        heatmap_sex = heatmap(corr_df, title=title, axis_name='Sex')

        # Information
        information['category'] = category
        return render_template('dashboards/ml_regressor.html', graphJSON1=heatmap_emotions, graphJSON2=heatmap_age, graphJSON3=heatmap_sex, information=information)
