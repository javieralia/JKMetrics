import json
import os
import time
import requests
import sys
import csv
import datetime

CONFIG_FILE = os.path.realpath("./config.txt")
in_config_file = open (CONFIG_FILE, 'r')
lines = in_config_file.readlines()
if len(lines) != 4:
    sys.exit("Wrong credentials file. Expected 4 lines (0 -> user, 1-> password, 2-> url, 3-> jql)")
            
user= lines[0].strip()
password= lines[1].strip()
JQL_PATH = lines[2].strip()
jql = lines[3].strip()

header_params = {"Content-Type": "application/json"}
header = ['Tipo de incidencia','Clase de Servicio','Estado', 'Clave de Incidencia', 'ID de Incidencia', 'Creada', 'Resuelta']

query_params = {'jql': jql, 'startAt': 0, 'maxResults': 1000, 'expand' :'changelog'}

response = requests.get(url=JQL_PATH, headers=header_params, params=query_params, verify=False,
                        auth=(user, password))
if response.status_code == 200:
    json_data = json.loads(response.text)
    issues = json_data.get("issues")
    file = open('Resueltas.csv', 'a', newline ='')
    with file:
        try:
            if issues:
                write = csv.DictWriter(file,fieldnames=header)
                #write.writeheader()
                for issue in issues:
                    fechainiciopriorizacion=fechainicioready=equipoescalado=estadoanterior=estadoactual=fechainicioescalado=fechafinescalado=transportista=""
                    Clave = str(issue.get("key"))
                    IdJira = str(issue.get("id"))
                    FechaCreacion = issue.get("fields").get("created")[0:10]
                    TipoIssue=issue.get("fields").get("issuetype").get("name")
                    Prioridad = issue.get("fields").get("priority").get("name")
                    Estado=str(issue.get("fields").get("status").get("name"))
                    if issue.get("fields").get("resolutiondate") is not None:
                        FechaResolucion= issue.get("fields").get("resolutiondate")[0:10]
                    write.writerow({'Tipo de incidencia':TipoIssue, 'Clase de Servicio':Prioridad ,'Estado':Estado, 'Clave de Incidencia' : Clave,'ID de Incidencia':IdJira, 'Creada':FechaCreacion, 'Resuelta':FechaResolucion})
            else:
                print("Ha ocurrido un error o no hay issues en este momento")
        except : 
            print("Error escribiendo el fichero:Resueltas.csv")
else:
    print("Error al conectar a la URL: " + JQL_PATH + 
          "\nError Code: " + str(response.status_code))
