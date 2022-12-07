from flask_login import logout_user
from flask import redirect, flash, url_for

def logout_controller():
    logout_user()
    flash('You have been logged out.') 
    return redirect(url_for('auth.login'))
