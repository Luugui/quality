from pyzabbix import ZabbixAPI
import os, csv

zapi = ZabbixAPI("http://10.3.10.76/zabbix/")
zapi.login("Admin","zabbix")


file = input("Insira o nome do arquivo: ")
lista = csv.reader(open(file), delimiter=";")


def get_group_id(groupname):
	group = zapi.hostgroup.get(output="extend",filter={"name": groupname})
	if len(group) == 0:
		grupo = zapi.hostgroup.create({"name": groupname})
		id = grupo["groupids"][0]
	else:
		id = group[0]["groupid"]
	return id
		
def create_host(host,ip,grupo):
	host_create = zapi.host.create({
				"host": host,
				"status": 0,
				"interfaces": [{
					"type": 1,
					"main": 1,
					"useip": 1,
					"ip": ip,
					"dns": "",
					"port": 10050
				}],
				"groups": [{
					"groupid": grupo

				}],
				"templates": [{

					"templateid": "10186"

				}]

			})
	
def atualiza_grupo(host,grupo):
	
	gid = get_group_id(grupo)
	grupos = []
	for g in zapi.host.get(output=["hostid"], selectGroups=["groupid"], filter={"host": host}):
		for i in g['groups']:
			grupos.append(i['groupid'])
	
	grupos.append(gid)
	hid = zapi.host.get(output=["hostid"], filter={"host": host})
	gupdate = zapi.host.update(hostid=hid[0]['hostid'], groups=grupos)
	

	
for [grupo,host,ip] in lista:
	host1 = zapi.host.get(filter={"host": host}, selectInterfaces=["interfaceid"])
	if host1:
		host_id = host1[0]["hostid"]
		atualiza_grupo(host,grupo)
		print("--> Host {0} ja existe adicionado ao grupo {1}".format(host,grupo))
	else:
		gid = get_group_id(grupo)
		create_host(host,ip,gid)
		print("--> Host {0} criado e adicionado ao grupo {1}".format(host,grupo))
































