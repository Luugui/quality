from pyzabbix import ZabbixAPI
import csv, os, getpass

# Função para adicionar Hosts

def add_host(host, ip, os):
    if os == "Windows":
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
                "groupid": 5

            }],
            "templates": [{
                "templateid": "10081"

            }]

        })
        print("--> Host {0} adicionado!".format(host))

    elif os == "Linux":
        if host1:
            host_id = host1[0]["hostid"]
            print("Host {0} ja existe!".format(host))
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
                "groupid": 5

            }],
            "templates": [{

                "templateid": "10001"
                

            }]

        })
        print("--> Host {0} adicionado!".format(host))

    elif os == "Server":
        if host1:
            host_id = host1[0]["hostid"]
            print("--> Host {0} ja existe!".format(host))
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
                "groupid": 36

            }],
            "templates": [{

                "templateid": "10081"

            }]

        })
        print("--> Host {0} adicionado!".format(host))



m = 0

while m == 0:
    URL = input("Insira a url do Zabbix: ")
    USER = input("Usuario: ")
    PASS = getpass.getpass("Senha: ")
    try:
        zapi = ZabbixAPI(URL)
        zapi.login(USER,PASS)
        print("-> Zabbix Conectado!")
        m = 1
    except:
        print("Não foi possivel conectar ao Zabbix!")
        os.system("pause")
        os.system("cls")
        m = 0

n = 1

# Realizando a adição do arquivo CSV

while n == 1:
    try:
        file = input("Nome do arquivo .csv: ")
        lista = csv.reader(open(file), delimiter=",")
        print("-> Arquivo importado!")
        n = 0
    except:
        print("Arquivo não encontrado!")
        n = 1
        os.system("pause")
        os.system("cls")
        print("-> Zabbix Conectado!")
        print("1- Verifique se especificou a extensao '.csv' no arquivo")
        print("2- Verifique se o arquivo esta na mesma pasta do script")


# Realizando a adição dos Hosts no Zabbix
add = 0
ext = 0

for[host,ip,os] in lista:
    if "Server" in os:
        host1 = zapi.host.get(filter={"host": host}, selectInterfaces=["interfaceid"])
        if host1:
            host_id = host1[0]["hostid"]
            print("--> Host {0} ja existe!".format(host))
            ext += 1
            continue
        add_host(host,ip,"Server")
        add += 1
    if "Linux" in os:
        host1 = zapi.host.get(filter={"host": host}, selectInterfaces=["interfaceid"])
        if host1:
            host_id = host1[0]["hostid"]
            print("--> Host {0} ja existe!".format(host))
            ext += 1
            continue
        add_host(host,ip,"Linux")
        add += 1
    if "Windows" in os:
        host1 = zapi.host.get(filter={"host": host}, selectInterfaces=["interfaceid"])
        if host1:
            host_id = host1[0]["hostid"]
            print("--> Host {0} ja existe!".format(host))
            ext += 1
            continue
        add_host(host,ip,"Windows")
        add += 1
print("Foram adicionados {0} Hosts e {1} Hosts ja existiam".format(add,ext))