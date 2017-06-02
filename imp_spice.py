from pyzabbix import ZabbixAPI
import csv, sys

# Realiza a conexão no Zabbix
try:
	zapi = ZabbixAPI("http://zabbixsrv/zabbix")
	zapi.login("Admin", "zabbix")
	print("----> Conectado ao Zabbix!")
	
except:
	print("ERROR: Não foi possivel conectar ao Zabbix!")
	
try:
	if len(sys.argv) == 2:
		file = sys.argv[1]
	else:
		print("Argumento inválido!")
		exit()
	spice = csv.reader(open(file), delimiter=",")
	print("----> Arquivo importado!")
	for [host,ip,os] in spice:
		if os[0:7] == "Windows":
			host1 = zapi.host.get(filter={"host": host}, selectInterfaces=["interfaceid"])
			if host1:
				host_id = host1[0]["hostid"]
				print("--> HOST {0} ja existe!".format(host))
				continue
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
				"groups":[{
					
					"groupid": 5
				}],
				"templates": [{
					
					"templateid": 10081
				}]
				
			})
			print("---> HOST {0} adicionado!".format(host))
		else:
			print("Linux")
	
except csv.Error:
	print("Error!")
	sys.exit("Arquivo: {0}, linha {1}".format(file, spice.line_num))