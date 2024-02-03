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

# Set this to the ingress endpoint URL for your service
url = 'https://anhue-ahsorg-ahsprod.snowflakecomputing.app'

# Validate the connection.
response = requests.get(f'{url}', headers=headers)
print(response.text)

#%%
# try a post request
# set a varible called data equal to a json object with some sample data
datasend = {
    "data" :"John"
    ,"something_else" :"doe"
}

url = 'https://anhue-ahsorg-ahsprod.snowflakecomputing.app/echo'

response = requests.post(f'{url}', json=datasend, headers=headers)
print(response.text)

#works!
