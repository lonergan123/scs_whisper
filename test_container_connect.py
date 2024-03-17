#%%
import snowflake.connector
import requests

ctx = snowflake.connector.connect(
   authenticator="externalbrowser",
   user="kevin.lonergan@albertahealthservices.ca",
   account="ahsorg-ahsprod",
   database = 'DB_TEAM_JENKINS',
   schema = 'KL_TEST_JENKINS',
   session_parameters={
      'PYTHON_CONNECTOR_QUERY_RESULT_FORMAT': 'json'
   })

#%%
# Obtain a session token.
token_data = ctx._rest._token_request('ISSUE')
token_extract = token_data['data']['sessionToken']

#%%

# Create a request to the ingress endpoint with authz.
token = f'\"{token_extract}\"'
headers = {'Authorization': f'Snowflake Token={token}'}
# add content type to headers =application/json

#%%

# Set this to the ingress endpoint URL for the whisper service
url = 'https://gtj4aij-ahsorg-ahsprod.snowflakecomputing.app'

# Validate the connection.
response = requests.get(f'{url}', headers=headers)
print(response.text)

#%%
url = url + '/readstage'
response = requests.get(f'{url}', headers=headers)
print(response.text)
#%%
# try a post request
# set a varible called data equal to a json object with some sample data
datasend = {
        "audio_file_path" :"/audio_files/SampleMedDictation.mp3"
    }

url_post = url + "/transcripe_stage_audio"

response = requests.post(f'{url_post}', json=datasend, headers=headers)
print(response.text)

#works!

# %%
