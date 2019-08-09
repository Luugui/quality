import requests, json, sys, time
from datetime import datetime

URL_P = sys.argv[3]


URL_AGENT = "{URL_P}/aeengine/rest/workflowinstances".format(URL_P=URL_P)
URL_LOGIN = "{URL_P}/aeengine/rest/authenticate".format(URL_P=URL_P)
USER = sys.argv[4]
PASS = sys.argv[5]

payload = {
    "username": USER,
    "password": PASS
}

params = {
	"offset": 0,
	"size": 10
}

data = {
	"filter": [
		{
            "columnName": "status",
            "displayName": "Status",
            "columnType": "string",
            "visibility": "true",
            "comparator": "eq",
            "values": [
                "Failure"
            ],
            "error": {
                "hasError": "false",
                "message": ""
            }
        }
	 ]
}

auth = requests.post(URL_LOGIN, params=payload)
j = json.loads(auth.content)

Token = j['sessionToken']

headers = {
    "X-session-token": Token,
    "Content-Type": "application/json"
}

agent = requests.post(URL_AGENT, headers=headers, params=params, json=data)

jagent = json.loads(agent.content)

def check_workflowstatus(aindex):
	if jagent['data'][aindex]['status'] == "Complete":
		print(1)
	else:
		print(0)


def discovery_workflow():
	result = {"data":[]}
	i = 0
	while i < len(jagent['data']):
		dt = int(jagent['data'][i]['executionStartTime'])/1000
		data = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(dt))
		result["data"].append(
			{"{#WORKFLINDEX}": i,"{#WORKFLID}": jagent['data'][i]['workflowConfiguration']['id'], "{#WORKFLNAME}": jagent['data'][i]['workflowConfiguration']['name'], "{#WORKFEXECUTE}": data}
		)
		i += 1
	obj = json.dumps(result)
	print(obj)

def workfl_data_execute(aindex):
	dt = int(jagent['data'][aindex]['executionStartTime'])/1000
	data = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(dt))
	print(data)

def workfl_data_create(aindex):
	dt = int(jagent['data'][aindex]['createdDate'])/1000
	data = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(dt))
	print(data)
	
def workfl_agent_name(aindex):
	ag_nome = jagent['data'][aindex]['agentName']
	print(ag_nome)

def workfl_name(aindex):
	ag_nome = jagent['data'][aindex]['workflowName']
	print(ag_nome)
	

if sys.argv[1] == "check":
	INDEX = int(sys.argv[2])
	check_workflowstatus(INDEX)
elif sys.argv[1] == "discovery":
	discovery_workflow()
elif sys.argv[1] == "dt_ex":
	INDEX = int(sys.argv[2])
	workfl_data_execute(INDEX)
elif sys.argv[1] == "dt_ct":
	INDEX = int(sys.argv[2])
	workfl_data_create(INDEX)
elif sys.argv[1] == "wf_ag":
	INDEX = int(sys.argv[2])
	workfl_agent_name(INDEX)
elif sys.argv[1] == "wf_nm":
	INDEX = int(sys.argv[2])
	workfl_name(INDEX)
else:
	print("ZBX_NOTSUPPORTED")

