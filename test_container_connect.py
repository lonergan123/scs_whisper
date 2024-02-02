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
url = 'http://anhte-ahsorg-ahsprod.snowflakecomputing.app/api/detect_language'

# Validate the connection.
response = requests.get(f'{url}', headers=headers)
print(response.text)

# Insert your code to interact with the application here






# %%
