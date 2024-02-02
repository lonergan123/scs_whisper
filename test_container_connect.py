#%%
import snowflake.connector
import requests

ctx = snowflake.connector.connect(
   account='ahsorg-ahsprod',
   user='KEVIN.LONERGAN@ALBERTAHEALTHSERVICES.CA',
   role = 'RL_TEAM_JENKINS',
   warehouse = 'WH_SMALL',
   database = 'DB_TEAM_JENKINS',
   schema = 'KL_TEST_JENKINS',
   authenticator='externalbrowser',
   session_parameters={
      'PYTHON_CONNECTOR_QUERY_RESULT_FORMAT': 'json'
   })
#%%

# Obtain a session token.
token_data = ctx._rest._token_request('ISSUE')
token_extract = token_data['data']['sessionToken']

# Create a request to the ingress endpoint with authz.
token = f'\"{token_extract}\"'
headers = {'Authorization': f'Snowflake Token={token}'}

#%%
# Set this to the ingress endpoint URL for your service
url = 'https://anhtu-ahsorg-ahsprod.snowflakecomputing.app/echo'


# Validate the connection.
# set a varible called data equal to a json object with some sample data
datasend = {
    "data": [
        [0, "transcribe", "en-US", "audio.mp3", True],
        [1, "transcribe", "en-US", "audio1.mp3", True]
    ]
}

response = requests.post(f'{url}', data=datasend, headers=headers)
print(response.text)


# Insert your code to interact with the application here






# %%
