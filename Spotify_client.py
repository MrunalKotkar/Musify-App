import base64
import datetime
from urllib.parse import urlencode
import random
import string
import urllib
import requests

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        } 
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
        
        
    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')
    
    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')
    
    def base_search(self, query_params): # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()
    
    '''def search(self, query=None, operator=None, operator_query=None, search_type='artist' ):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type.lower()})
        print(query_params)
        return self.base_search(query_params)
    '''

    def search(self, query, search_type='artist'):  # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": search_type.lower()})
        # print(query)
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()


    def get_random_tracks(self):
        access_token = self.get_access_token()
        #%f%
        wildcard = f'%{random.choice(string.ascii_lowercase)}%'
        query = urllib.parse.quote(wildcard)
        offset = random.randint(0, 2000)

        url = f'https://api.spotify.com/v1/search?q={query}&offset={offset}&type=track'

        response = requests.get(
            url,
            headers = {
                "Content-Type" : "application/json",
                "Authorization" : f"Bearer {access_token}"
            }
        )
        response_json = response.json()
        print(response_json['tracks']['items'][1])
        tracks = [track for track in response_json['tracks']['items']]

        print(f'Found {len(tracks)} from your search')

        return tracks

    def add_tracks_to_library(self, track_ids):
        access_token = self.get_access_token()
        url = 'https://api.spotify.com/v1/me/tracks'
        #print(access_token)
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            json = {
                'ids' : 'track_ids'
            }
        )

        return response.ok

    def get_audio_track(self):

        endpoint = f"https://api.spotify.com/v1/tracks/{track_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_top_value(self, top_value_type='artists'):
        if top_value_type == None:
            raise Exception("Type is required")
        # query_params = urlencode({"type": top_value_type})
        headers = self.get_resource_header()
        endpoint = f"https://api.spotify.com/v1/me/top/{top_value_type}"
        # lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(endpoint, headers=headers)
        print(r)
        if r.status_code not in range(200, 299):
            return {}

        return r.json()

    def get_users_profile(self, user_id):
        print(user_id)
        headers = self.get_resource_header()
        endpoint = f"https://api.spotify.com/v1/users/{user_id}"
        r = requests.get(endpoint, headers=headers)
        print(r)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_tracks(self, track_ids):
        endpoint = "https://api.spotify.com/v1/tracks"
        headers = self.get_resource_header()
        query_params = ",".join(track_ids)
        lookup_url = f"{endpoint}?ids={query_params}"
        print(lookup_url)
        r = requests.get(lookup_url, headers=headers)
        print(r)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_albums_of_artist(self, artist_id):
        headers = self.get_resource_header()
        endpoint = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        r = requests.get(endpoint, headers=headers)
        print(r)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()