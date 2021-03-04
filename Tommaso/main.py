import os
import json
from datetime import datetime


def metadata(file: str, nome: str):
    # name = os.path.basename(file)
    size = os.path.getsize(file)
    ultima_modifica = datetime.fromtimestamp(os.stat(file).st_mtime).strftime("%Y-%m-%d %I:%M:%S")
    data = {
        'nome': nome,
        'Dimensione': size,
        'DataUltimaModifica': ultima_modifica
    }
    if size > 20:
        return data
    else:
        return None


def json_cartella(dir: str):
    p = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if dir == root:
                p.append(f"{root}{name}")
            else:
                p.append(f"{root}\\{name}")
    data = []
    data.append(["file.txt","non la so"])
    data.append(["prova.py","2029"])
    for file in p:
        data.append(metadata(file, file.replace(dir, "")))
    #with open("file.json", "w") as outfile:
    #    json.dump(data, outfile, indent=4)


path = "..\\sim_storage\\LOCAL\\"
json_cartella(path)
"""
data = json.load(open("file.json"))
print(data["ciao.txt"]["DataUltimaModifica"])

"""
print("fine dell'algoritmo!")