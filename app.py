from dotenv import load_dotenv
import os
import base64
import requests
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
print(client_id,client_secret)


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),'utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content_Type" : "application/x-www-form-urlencoded"


    }
    data = {
        "grant_type":"client_credentials"
    }
    result = requests.post(url,headers = headers,data =data)
    json_content = json.loads(result.content)
    token = json_content['access_token']
    return token

def get_auth_header(token):
    return {"Authorization" : "Bearer " +token}


def search_for_artist(token,artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist,track&limit=1"
    query_url = url +query
    result = requests.get(query_url,headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if(len(json_result)) == 0:
        print("no artist present")
        return None
    return json_result

def get_artist_top_tracks(token,artist_id):
    url = "https://api.spotify.com/v1/artists/{}/top-tracks?country=IN".format(artist_id)
    headers = get_auth_header(token)
    result = requests.get(url,headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result


token = get_token()
result =search_for_artist(token,"JOHN SUMMIT")
artist_name = result[0]['name']
artist_id = result[0]['id']
ans = get_artist_top_tracks(token,artist_id)
for i in ans:
    print(i['name'])
print(artist_name,artist_id)
# print(ans)
