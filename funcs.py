from flask import session
import requests, json


def getToken(refresh_token):
    twparams = {'client_id': '40ynv6ozsj0tf9cinqn7m0cui5nuyf',
                'client_secret': 'cp5rpkc8qrv8xz8cr0hcfpjecrbli2',
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
                }
    twitch = requests.post('https://api.twitch.tv/kraken/oauth2/token', params=twparams)
    tokendata = json.loads(twitch.text)
    session['refresh_token'] = tokendata['refresh_token']
    return tokendata['access_token']

def getUser(access_token, udata):
    headers = {'Client-ID' : '40ynv6ozsj0tf9cinqn7m0cui5nuyf', 'Authorization': 'Bearer %s' % access_token}
    r = requests.get("https://api.twitch.tv/helix/users", headers=headers)
    print (r.text)
    uddata = json.loads(r.text)
    return uddata['data'][0][udata]