from flask import Flask, redirect, request, session, url_for
import json
import requests
import funcs

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

tparams = { 'client_id':'40ynv6ozsj0tf9cinqn7m0cui5nuyf',
         'redirect_uri':'http://127.0.0.1:5000/login/authorized',
         'response_type':'code',
         'scope':'user:read:email'}
r = requests.get('https://api.twitch.tv/kraken/oauth2/authorize', params=tparams)

@app.route('/')
def index():
    if 'code' and 'refresh_token' not in session:
        return ('<a href="%s">login here</a> forsenE' % url_for('login'))
    else:
        return ('welcome to my shitty test website %s!<br><a href="%s">logout</a>' % (funcs.getUser(funcs.getToken(session['refresh_token']), 'display_name'), url_for('logout')))
    return ''

@app.route('/login')
def login():
    return redirect(r.url)

@app.route('/login/authorized', methods=['GET', 'POST'])
def authorized():
    if 'error' and 'error_description' in request.args:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    if 'code' and 'scope' in request.args:
        session['code'] = request.args['code']
        session['scope'] = request.args['scope']
        twparams = {'client_id': '40ynv6ozsj0tf9cinqn7m0cui5nuyf',
                   'client_secret': 'cp5rpkc8qrv8xz8cr0hcfpjecrbli2',
                   'code': session['code'],
                   'grant_type': 'authorization_code',
                   'redirect_uri': 'http://127.0.0.1:5000/login/authorized'}
        twitch = requests.post('https://api.twitch.tv/api/oauth2/token', params=twparams)
        if 'refresh_token' and 'access_token' and 'expires_in' in twitch.text:
            print(twitch.text)
            ttext = json.loads(twitch.text)
            session['refresh_token'] = ttext['refresh_token']
            ##twitch.get('expires_in')
            return redirect(url_for('index'))
    return ''

@app.route('/logout')
def logout():
    session.pop('code')
    session.pop('refresh_token')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
