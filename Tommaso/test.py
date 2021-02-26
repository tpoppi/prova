from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json

transport = RequestsHTTPTransport(url='http://127.0.0.1:8080/')

client = Client(transport=transport)

query = gql("""
query {
    GetAllFiles {
        Nome
        Dimensione
        DataUltimaModifica
    }
}
""")

# risultato = client.execute(query)

risultato = {
    "data": {
        "GetAllFiles": [
            {
                "nome": ".gitignore",
                "Dimensione": 14,
                "DataUltimaModifica": "2021-02-17 06:45:01"
            },
            {
                "nome": "ciao.txt",
                "Dimensione": 22,
                "DataUltimaModifica": "2021-02-26 05:03:16"
            },
            {
                "nome": "ciao\\dentro.txt",
                "Dimensione": 0,
                "DataUltimaModifica": "2021-02-25 06:18:32"
            },
            {
                "nome": "ciao\\hey.txt",
                "Dimensione": 0,
                "DataUltimaModifica": "2022-02-25 06:20:25"
            },
            {
                "nome": "ciao\\file.txt",
                "Dimensione": 0,
                "DataUltimaModifica": "2022-02-25 06:20:25"
            }
        ]
    }
}
with open("test.json", "w") as outfile:
    json.dump(risultato, outfile, indent=4)

data_server = json.load(open("test.json"))
data_client = json.load(open("file.json"))
print(data_server["data"]["GetAllFiles"])
print(data_client)

#file che son nel client e non sono nel server
newFilesClient=[]
#file che son nel server e non sono nel client
newFilesServer=[]
#file nel client che sono più aggiornati rispetto a quelli nel server
updateFilesClient=[]
#file nel server che sono più aggiornati rispetto a quelli nel client
updateFileServer=[]

# controllo che tutti i file del server siano uguali a quelli del client
for i in data_server["data"]["GetAllFiles"]:
    nome = i["nome"]
    trovato = False
    for y in data_client:
        if i["nome"] == y["nome"]:
            if i["DataUltimaModifica"] != y["DataUltimaModifica"]:
                if i["DataUltimaModifica"] > y["DataUltimaModifica"]:
                    print(f"{nome} è stato modificato nel server")
                    updateFileServer.append(nome)
                else:
                    print(f"{nome} è stato modificato nel client")
                    updateFilesClient.append(nome)
            trovato = True
            break
    if not trovato:
        print(f"Il file {nome} non è presente nel client")
        newFilesServer.append(nome)

# controllo che tutti i file nel client sono uguali al quelli nel server
for i in data_client:
    nome = i["nome"]
    trovato = False
    for y in data_server["data"]["GetAllFiles"]:
        if i["nome"] == y["nome"]:
            trovato = True
            break
    if not trovato:
        print(f"Il file {nome} non è presente nel server")

print(newFilesClient)
print(newFilesServer)
print(updateFilesClient)
print(updateFileServer)