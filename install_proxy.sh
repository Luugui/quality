# Instala os repositórios
rpm -Uvh https://repo.zabbix.com/zabbix/4.2/rhel/8/x86_64/zabbix-release-4.2-2.el8.noarch.rpm

# Instala os pacotes do Zabbix Proxy
dnf clean all
dnf install zabbix-proxy-sqlite3

# Cria a pasta do Banco de Dados
mkdir /var/zabbix
chown zabbix:zabbix /var/zabbix

# Cria o arquivo do Banco de Dados
cd /var/zabbix
zcat /usr/share/doc/zabbix-proxy-sqlite3*/schema.sql.gz | sqlite3 zabbix.db
chown zabbix:zabbix zabbix.db

# Alterando o arquivo de configuração
sed -i 's/Server=127.0.0.1/Server=noc.quality.com.br/g' /etc/zabbix/zabbix_proxy.conf
sed -i 's/Hostname=Zabbix proxy/Hostname=zabbix-proxy-tereos/g' /etc/zabbix/zabbix_proxy.conf
sed -i 's/DBName=zabbix_proxy/DBName=/var/zabbix/zabbix.db/g' /etc/zabbix/zabbix_proxy.conf

# Iniciando o serviço e habilitando o inicio automatico
systemctl enable --now zabbix-proxy