from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from Dashboard import app, db, login, oauth, google, twitter
from Dashboard.models import User
from flask_login import current_user, login_user, logout_user, login_required
import uuid

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('board'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('board'))

    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        account = User.query.filter_by(username=userName).first()
        if account:
            if account.password == password:
                login_user(account)
                return redirect(url_for('board'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        account = User.query.filter_by(username=userName).first()
        if account:
            return redirect(url_for('signup'))
        else:
            uuid_var = uuid.uuid1()
            new = User(str(uuid_var), userName, password)
            db.session.add(new)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signUp.html')

@app.route('/DashBoards', methods=['GET', 'POST'])
@login_required
def board():
    if request.method == 'POST':

        if request.form.get('Widget1'):
            if current_user.widget1:
                current_user.widget1 = False
                db.session.commit()
                return redirect(url_for('board'))
            else:
                current_user.widget1 = True
                db.session.commit()
                return redirect(url_for('board'))

        if request.form.get('Widget2'):             
            if current_user.widget2:         
                current_user.widget2 = False
                db.session.commit()
                return redirect(url_for('board')) 
            else:
                current_user.widget2 = True 
                db.session.commit()
                return redirect(url_for('board'))

        if request.form.get('Widget3'):
            if current_user.widget3:         
                current_user.widget3 = False
                db.session.commit()
                return redirect(url_for('board')) 
            else:
                current_user.widget3 = True 
                db.session.commit()
                return redirect(url_for('board'))

        if request.form.get('google_Widget1'):
            if current_user.google_widget1:         
                current_user.google_widget1 = False
                db.session.commit()
                return redirect(url_for('board')) 
            else:
                current_user.google_widget1 = True 
                db.session.commit()
                return redirect(url_for('board'))

        if request.form.get('google_Widget2'):    
            if current_user.google_widget2:  
                current_user.google_widget2 = False
                db.session.commit()
                return redirect(url_for('board')) 
            else:
                current_user.google_widget2 = True
                db.session.commit()
                return redirect(url_for('board'))

        if request.form.get('twitter_Widget1'):
            if current_user.twitter_widget1: 
                current_user.twitter_widget1 = False
                db.session.commit()
                return redirect(url_for('board'))
            else:  
                current_user.twitter_widget1 = True
                db.session.commit()
                return redirect(url_for('board'))

    return render_template('Dashboard.html')

@app.route('/Dashboards/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')

@app.route('/Dashboards/settings/google_login', methods=['GET', 'POST'])
@login_required
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/Dashboards/settings/google_login/authorize', methods=['GET', 'POST'])
@login_required
def google_authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    current_user.google_accessToken = token['access_token']
    current_user.is_googleConnected = True
    db.session.commit()
    return redirect(url_for('board'))

@app.route('/Dashboards/settings/twitter_login', methods=['GET', 'POST'])
@login_required
def twitter_login():
    twitter = oauth.create_client('twitter')
    redirect_uri = url_for('twitter_authorize', _external=True)
    return twitter.authorize_redirect(redirect_uri)

@app.route('/Dashboards/settings/twitter_login/authorize', methods=['GET', 'POST'])
@login_required
def twitter_authorize():
    twitter = oauth.create_client('twitter')  # create the google oauth client
    token = twitter.authorize_access_token()  # Access token from google (needed to get user info)
    resp = twitter.get('account/verify_credentials.json')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    print(user_info)
    current_user.twitter_accessToken = token['oauth_token']
    current_user.twitter_accessTokenSecret = token['oauth_token_secret']
    current_user.is_twitterConnected = True
    db.session.commit()
    return redirect(url_for('board'))

@app.route('/about.json')
def about(): 
    ip_address = request.remote_addr
    about_json = {
        'client': {
            'host': ip_address
        },
        'server': {
        'current_time': 250 ,
        'services': [{
            'name': "weather",
            'widgets': [{
                'name': "city_temperature",
                'description': "Display temperature for a city",
                'params': [{
                    'name': "city",
                    'type': "string"
                }]
            }]
        }, {
            'name': 'map' ,
            'widgets': [{
                'name': "google_map" ,
                'description': "Displaying an google map" ,
                'params': [{
                    'name': "Departure" ,
                    'type': "Geo-Localisation"
                }, {
                    'name': "Arrival" ,
                    'type': "Geo-Localisation"
                }]
            }]
            }]
        }
    }
    return jsonify(about_json)

if __name__ == "__main__":
    app.run()
