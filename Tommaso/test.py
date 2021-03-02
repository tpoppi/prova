from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
from enum import Enum
import os
import json
from datetime import datetime
from server import Server
"""
transport = RequestsHTTPTransport(url='http://127.0.0.1:8080/')

client = Client(transport=transport)


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
"""

class Policy(Enum):
    Client = 1
    Server = 2
    lastUpdate = 3


class metaData:
    def __init__(self):
        # file che son nel client e non sono nel server
        self.newFilesClient : list= []
        # file che son nel server e non sono nel client
        self.newFilesServer = []
        # file nel client che sono più aggiornati rispetto a quelli nel server
        self.updateFilesClient = []
        # file nel server che sono più aggiornati rispetto a quelli nel client
        self.updateFileServer = []
        """percorso cartella locale"""
        self.directory = "..\\sim_storage\\LOCAL\\"
        #metadata dei file nel client
        self.metaClient = self.createJson(self.directory)
        """metadata dei file nel server"""
        self.metaServer = self.getDataServer()

    def getDataServer(self) -> None:
        server = Server()
        return server.getAllFiles()

    def updateDiff(self):
        # controllo che tutti i file del server siano uguali a quelli del client
        for i in self.metaServer:
            ciao = i["nome"]
            ultimaModifica = i["DataUltimaModifica"]
            trovato = False
            for y in self.metaClientclient:
                if i["nome"] == y["nome"]:
                    if i["DataUltimaModifica"] != y["DataUltimaModifica"]:
                        if i["DataUltimaModifica"] > y["DataUltimaModifica"]:
                            print(f"{nome} è stato modificato nel server")
                            self.updateFileServer.append(nome)
                        else:
                            print(f"{nome} è stato modificato nel client")
                            self.updateFilesClient.append(nome)
                    trovato = True

            if not trovato:
                print(f"Il file {nome} non è presente nel client")
                self.newFilesServer.append([nome, ultimaModifica])

        # controllo che tutti i file nel client sono uguali al quelli nel server
        for i in self.metaClient:
            nome = i["nome"]
            ultimaModifica= i["DataUltimaModifica"]
            trovato = False
            ciao=True
            for y in self.metaServer:
                if i["nome"] == y["nome"]:
                    trovato = True
                    break
            if not trovato:
                print(f"Il file {nome} non è presente nel server")
                self.newFilesClient.append([nome, ultimaModifica])

        print(self.newFilesClient)
        print(self.newFilesServer)
        print(self.updateFilesClient)
        print(self.updateFileServer)

    def applyChangeServer(self):
        """aggiorno il client:
             -aggiungo i nuovi file presenti nel server
             -elimino i file che non son presenti nel server
             -aggiorno nel client tutti i file che hanno DataUltimaModifica differente dal server (anche se hanno una data di ultima modifica maggiore vince il server)"""
        server = Server()
        for i in self.newFilesServer:
            server.sendToServer(i[0],i[1])
            print(f"aggiunto al server il file {i[0]}")
        for i in self.metaClient:
            for y in self.newFilesClient:
                if i["nome"] == y["nome"]:
                    server.removeFileByName(i["nome"])
                    nome=i["nome"]
                    print(f"rimosso nel client il file {nome}")
        for y in self.updateFileServer:
            #devo cancellare i file nel client con nome y["nome] e esportare dal server il file y["nome"] e caricarlo nel client
            ''
        for y in self.updateFileServer:
            #stessa cosa di sopra
            ''

    def applyChanges(policy: Policy):
        switcher = {
            Policy.Client: '',
            Policy.Server: '',
            Policy.lastUpdate: ''
        }
        return switcher.get(policy, "Invalid policy")

    def metadata(self, file: str, nome: str):
        # name = os.path.basename(file)
        size = os.path.getsize(file)
        ultima_modifica = datetime.fromtimestamp(os.stat(file).st_mtime).strftime("%Y-%m-%d %I:%M:%S")
        data = {
            'nome': nome,
            'Dimensione': size,
            'DataUltimaModifica': ultima_modifica
        }
        return data

    def createJson(self, dir: str):
        """"""
        p = []
        for root, dirs, files in os.walk(dir):
            for name in files:
                if dir == root:
                    p.append(f"{root}{name}")
                else:
                    p.append(f"{root}\\{name}")
        data = []
        for file in p:
            data.append(self.metadata(file, file.replace(dir, "")))
        #with open("file.json", "w") as outfile:
        #    json.dump(data, outfile, indent=4)
        return data


metadata= metaData()
print(metadata.metaClient)
print(metadata.metaServer)
server = Server()
server.sendToServer("C:\\Users\Poppi\Desktop\codice\project-SSD\src\sim_storage\LOCAL\ciao\dentro.txt","2022-02-25 06:20:25")
print(metadata.metaServer)
metadata.updateFileServer()
print(metadata.metaServer)
