from dotenv import load_dotenv
import requests
import tweepy
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# GitHub app credentials
client_id = os.getenv('GH_CLIENT_ID')
client_secret = os.getenv('GH_CLIENT_SECRET')
access_token_url = 'https://github.com/login/oauth/access_token'
api_url = 'https://api.github.com'

# Twitter app credentials from environment variables
consumer_key = os.getenv('TW_API_KEY')
consumer_secret = os.getenv('TW_API_SECRET_KEY')
access_token = os.getenv('TW_ACCES_TOKEN')
access_token_secret = os.getenv('TW_ACCES_SECRET')

# Authenticate GitHub app and get access token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
data = {
    'grant_type': 'client_credentials',
}
headers = {
    'Accept': 'application/json',
}
response = requests.post(access_token_url, auth=auth, data=data, headers=headers)
access_token = response.json()['access_token']

# Get list of repositories for authenticated user
headers = {
    'Authorization': f'token {access_token}',
    'Accept': 'application/vnd.github.v3+json',
}
response = requests.get(f'{api_url}/user/repos', headers=headers)
repos = response.json()

# Authenticate Twitter app
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret)

# Post tweet for each commit message that contains the keyword "#twittle"
for repo in repos:
    response = requests.get(f'{api_url}/repos/{repo["full_name"]}/commits', headers=headers)
    commits = response.json()
    for commit in commits:
        if '#twittle' in commit['commit']['message']:
            tweet_text = commit['commit']['message'].replace('#twittle', '').strip()
            api = tweepy.API(auth)
            api.update_status(tweet_text)
