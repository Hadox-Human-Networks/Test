from flask import render_template, session, redirect, flash, url_for
from ..forms import DashboardAnalytics, DashboardData, DashboardML


def index_controller():
    """Home page with 3 forms to select the category of the desired dashboard.
    Each form redirects to the respective endpoint of the dashboard
    """
    analytics_form = DashboardAnalytics()
    data_form = DashboardData()
    ml_form = DashboardML()
    if analytics_form.validate_on_submit():
        category = analytics_form.category.data
        return redirect(url_for('dashboards.analytics', category=category))
    if data_form.validate_on_submit():
        category = data_form.category.data
        return redirect(url_for('dashboards.data', category=category))
    if ml_form.validate_on_submit():
        category = ml_form.category.data
        return redirect(url_for('dashboards.ml', category=category))
    return render_template('index.html', form1=analytics_form, form2=data_form, form3=ml_form)

