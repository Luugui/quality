from pyzabbix import ZabbixAPI


zapi = ZabbixAPI("http://IP-ZABBIX/zabbix")
zapi.login("USUARIO","SENHA")
print("Conectado com sucesso!")

r = open("ATIVOS.txt", "w")


for h in zapi.host.get(output="extend"):
    for i in zapi.hostinterface.get(output="extend",hostids=h):
        for g in zapi.hostgroup.get(output="extend", hostids=h):
            ativos = {'Host':h['host'], 'IP':i['ip'], 'DNS':i['dns'], 'GRUPO':g['name']}
            print(ativos)
            r.write("{0}, {1}, {2}, {3}\n".format(ativos['Host'],ativos['IP'],ativos['DNS'],ativos['GRUPO']))
        
r.close()
