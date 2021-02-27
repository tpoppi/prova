from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
#from settings import Settings


class Server:

    def __init__(self):
        #self.url: str = Settings["HOST"]
        #self.port: int = Settings["PORT"]

        transport = RequestsHTTPTransport(url='http://20.56.176.12/')
        self.client: Client = Client(transport=transport)

    def sendToServer(self, filePath: str, lastUpdate: str) -> None:
        """Richiede il percorso del file e l'orario di ultima modifica"""
        query = gql('''
                mutation SingleUpload($file: Upload!, $datetime: String!) {
                    singleUpload(file: $file, datetime: $datetime) {
                        filename
                        mimetype
                        encoding
                    }
                }
                ''')

        with open(filePath, "rb") as f:
            params = {
                "file": f,
                "datetime": lastUpdate
            }

            result = self.client.execute(
                query, variable_values=params, upload_files=True
            )

            print(result)

    def getAllFiles(self):
        """Restituisce il nome dei file con l'ultima modifica"""
        query = gql('''
                query {
                    GetAllFiles {
                        Nome
                        DataUltimaModifica
                    }
                }
                ''')
        #response = self.client.execute(query)["GetAllFiles"]
        #result: dict[str, str] = {}
        #for items in response:
        #    result[items["Nome"]] = items["DataUltimaModifica"]

        return self.client.execute(query)["GetAllFiles"]

    def removeFileByName(self, fileName: str) -> None:
        """Rimuove il file dal cloud"""
        query = gql('''
                mutation RemoveFile($fileName: String!) {
                    removeFile(fileName: $fileName) {
                        Nome
                        DataUltimaModifica
                    }
                }
                ''')

        params = {
            "fileName": fileName
        }

        result = self.client.execute(query, variable_values=params)

        print(result)
