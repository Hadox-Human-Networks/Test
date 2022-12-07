from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


"""
TODO: Give unique name to dashboards images to avoid confusion
"""
class DashboardAnalytics(FlaskForm):
    category = SelectField('Analytics Dashboards', choices=[('asset', 'Asset'), ('customer', 'Customer'), ('visitors', 'Visitors'), ('advertising', 'Advertising')])
    submit = SubmitField('Go to Analytics Dash!')

class DashboardData(FlaskForm):
    category = SelectField('Data Descriptors Dashboards', choices=[('emotions', 'Emotions'), ('age', 'Age'),  ('sex', 'Sex')])
    submit = SubmitField('Go to Data Dash!')

class DashboardML(FlaskForm):
    category = SelectField('Machine Learning Dashboards', choices=[('classifier', 'Classifier'), ('regressor', 'Regressor')])
    submit = SubmitField('Go to ML Dash!')

