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


alerts_query = gql(
    """ 
query alerts(
  $alertCodes: [ID!],
  $carCodes: [ID!],
  $page: Int,
  $limit: Int,
  $startDate: BaseDate,
  $endDate: BaseDate,
  $dateType: DateTypes,
  $startSize: Float,
  $endSize: Float,
  $territoryIds: [Int!],
  $territoryCategory: String,
  $statusName: String,
  $sources: [SourceTypes!],
  $intersectWithCar: Boolean,
  $isInEmbargoedArea: Boolean,
  $isInAuthorizedArea: Boolean,
  $deforestationClasses: [DeforestationTypes!],
  $actionTypesIds: [Int!],
  $boundingBox: [Float!],
  $sortField: AlertSortField,
  $sortDirection: SortDirection
) {
  alerts(
    alertCodes: $alertCodes,
    carCodes: $carCodes,
    page: $page,
    limit: $limit,
    startDate: $startDate,
    endDate: $endDate,
    dateType: $dateType,
    startSize: $startSize,
    endSize: $endSize,
    territoryIds: $territoryIds,
    territoryCategory: $territoryCategory,
    statusName: $statusName,
    sources: $sources,
    intersectWithCar: $intersectWithCar,
    isInEmbargoedArea: $isInEmbargoedArea,
    isInAuthorizedArea: $isInAuthorizedArea,
    deforestationClasses: $deforestationClasses,
    actionTypesIds: $actionTypesIds,
    boundingBox: $boundingBox,
    sortField: $sortField,
    sortDirection: $sortDirection
  ) {
    collection {
      ...AlertDataFragment
    }
    metadata {
      ...CollectionMetadataFragment
    }
    rankingByBiome {
      ...AlertRankingByBiomeFragment
    }
    rankingByCity {
      ...AlertRankingByCityFragment
    }
    rankingByState {
      ...AlertRankingByStateFragment
    }
    summary {
      ...QuerySummaryFragment
    }
  }
}
    """
)

alerts_variables = {
    "alertCodes": ["4"],
    "carCodes": ["4"],
    "page": 1,
    "limit": 100,
    "startDate": "2019-01-01",
    "endDate": "2020-01-01",
    "dateType": "DetectedAt",
    "startSize": 0,
    "endSize": 999999.9,
    "territoryIds": [""],
    "territoryCategory": None,
    "statusName": "published",
    "sources": ["All"],
    "intersectWithCar": None,
    "isInEmbargoedArea": None,
    "isInAuthorizedArea": None,
    "deforestationClasses": ["All"],
    "actionTypesIds": [""],
    "boundingBox": [""],
    "sortField": "DETECTED_AT",
    "sortDirection": "DESC"
}

authorized_transport = RequestsHTTPTransport(
    url=endpoint,
    headers={"Authorization": f"Bearer {token}"},
    verify=True,
    retries=3,
)
authorized_client = Client(
    transport=authorized_transport,
    fetch_schema_from_transport=True,
)

alerts_result = authorized_client.execute(
    alerts_query, variable_values=alerts_variables)
