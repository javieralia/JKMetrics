import json
import time
import requests
import sys
import csv
import datetime

JQL_PATH = "https://axinic.central.inditex.grp/jira/rest/api/2/search"
user=""
password=""
header_params = {"Content-Type": "application/json"}
header = ['Tipo de incidencia','Tipo de Trabajo','Clase de Servicio','Estado', 'Clave de Incidencia', 'ID de Incidencia', 'Creada', 'Actualizada', 'Fecha Inicio Escalado', 'Fecha Fin Escalado', 'Transportista','Resuelta']


# Cerradas

jql= "project = <proyecto> AND 'Equipo Asignado' = jsdsoportetrackingtec and status in (Done,Cerrado,Closed,Resolved) and (Resolved >= startOfMonth(-12) AND resolved <= endOfMonth(-12))"
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
                    if issue.get("fields").get("customfield_24960") is not None:
                        Sintoma1=issue.get("fields").get("customfield_24960").get("value") #tipo de servicio
                    if issue.get("fields").get("customfield_24961") is not None:
                        Sintoma2=issue.get("fields").get("customfield_24961").get("value")#tipo de servicio
                    TServicio=Sintoma1 + "-" + Sintoma2
                    if issue.get("fields").get("resolutiondate") is not None:
                        FechaResolucion= issue.get("fields").get("resolutiondate")[0:10]
                    if issue.get("fields").get("customfield_18963") is not None:
                        transportista=issue.get("fields").get("customfield_18963")

                    transiciones = issue.get("changelog").get("histories")
                    for transicion in transiciones:
                        for i in range(len(transicion.get("items"))):
                            if transicion.get("items")[i].get("field")=="status":
                                estadoanterior = transicion.get("items")[i].get("fromString")
                                estadoactual = transicion.get("items")[i].get("toString")
                                if estadoactual=="Escalado":
                                    fechainicioescalado=transicion.get("created")[0:10]
                                if estadoanterior=="Escalado":
                                    fechafinescalado=transicion.get("created")[0:10]
                    write.writerow({'Tipo de incidencia':TipoIssue, 'Tipo de Trabajo': TServicio ,'Clase de Servicio':Prioridad ,'Estado':Estado, 'Clave de Incidencia' : Clave,'ID de Incidencia':IdJira, 'Creada':FechaCreacion, 'Actualizada':Actualizada,'Fecha Inicio Escalado':fechainicioescalado,'Fecha Fin Escalado':fechafinescalado, 'Transportista':transportista, 'Resuelta':FechaResolucion})
            else:
                print("Ha ocurrido un error o no hay issues en este momento")
        except : 
            print("Error escribiendo el fichero:Resueltas.csv")
else:
    print("Error al conectar a la URL: " + JQL_PATH + 
          "\nError Code: " + str(response.status_code))
