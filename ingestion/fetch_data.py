import os

from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

load_dotenv()

username = os.environ.get('EMAIL')
pwd = os.environ.get('PASSWORD')
assert username and pwd, 'Missing credentials. Check .env file.'

endpoint = "https://plataforma.alerta.mapbiomas.org/api/v2/graphql"
transport = RequestsHTTPTransport(
    url=endpoint,
    verify=True,
    retries=3,
)

client = Client(
    transport=transport, fetch_schema_from_transport=True)

login_query = gql(
    """
    mutation signIn(
  $email: String!,
  $password: String!
) {
  signIn(
    email: $email,
    password: $password
  ) {
    token
  }
}
    """
)
login_variables = {
    "email": username,
    "password": pwd,
}

result = client.execute(login_query, variable_values=login_variables)
assert 'signIn' in result, 'Error logging in'
token = result['signIn'].get('token')
