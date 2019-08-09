import requests, json, sys

URL_P = sys.argv[2]
URL_A = sys.argv[3]


URL_AGENT = "{URL_P}/aeengine/rest/{URL_A}/monitoring/agents".format(URL_P=URL_P,URL_A=URL_A)
URL_LOGIN = "{URL_P}/aeengine/rest/authenticate".format(URL_P=URL_P)
USER = sys.argv[4]
PASS = sys.argv[5]

payload = {
    "username": USER,
    "password": PASS
}

auth = requests.post(URL_LOGIN, params=payload)
j = json.loads(auth.content)

Token = j['sessionToken']

headers = {
    "X-session-token": Token,
    "Content-Type": "application/json"
}

agent = requests.get(URL_AGENT, headers=headers)
jagent = json.loads(agent.content)


def check_agent(aindex):
	if jagent[aindex]['agentState'] == "RUNNING":
		print(1)
	else:
		print(0)


def discovery_agent():
	result = {"data":[]}
	i = 0
	while i < len(jagent):
		result["data"].append(
			{"{#AGENTINDEX}": i,"{#AGENTID}": jagent[i]['id'], "{#AGENTNAME}": jagent[i]['agentName']}
		)
		i += 1
	obj = json.dumps(result)
	print(obj)



if sys.argv[1] != "discovery":
	INDEX = int(sys.argv[1])
	check_agent(INDEX)
elif sys.argv[1] == "discovery":
	discovery_agent()
