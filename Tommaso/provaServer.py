from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json

transport = RequestsHTTPTransport(url='http://20.56.176.12/')

client = Client(transport=transport)

query = gql("""
query {
    GetAllFiles {
        Nome
        DataUltimaModifica
    }
}
""")

risultato = client.execute(query)["GetAllFiles"]
print(risultato)