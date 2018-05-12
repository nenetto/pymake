#!/usr/bin/env bash

GREEN='\033[0;32m'
BLUEE='\033[0;34m'
ORANG='\033[0;33m'
NC='\033[0m'


echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"
echo -e "${GREEN}                                              [Pymake]                                          ${NC}"
echo -e "${ORANG}                                 This scripts installs MSSQL drivers                            ${NC}"
echo -e "${ORANG}                                  E. Marinetto (nenetto@gmail.com)                               ${NC}"
echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"

echo -e "${GREEN}[Datalab Utils] ${ORANG}Creating log${NC}"
DIRECTORY=$(cd `dirname $0` && pwd)
LOGFILE=$DIRECTORY'/installation.log'

echo -e "${GREEN}[Datalab Utils] ${ORANG}Updating sources${NC}"
apt-get update >> $LOGFILE 2>$LOGFILE && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends apt-utils >> $LOGFILE 2>$LOGFILE

echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing unixodbc-dev${NC}"
DEBIAN_FRONTEND=noninteractive apt-get -y install unixodbc-dev >> $LOGFILE

echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing apt-transport-https${NC}"
DEBIAN_FRONTEND=noninteractive apt-get -y install apt-transport-https curl >> $LOGFILE

echo -e "${GREEN}[Datalab Utils] ${ORANG}Adding key${NC}"
curl https://packages.microsoft.com/keys/microsoft.asc 2>$LOGFILE | apt-key add - >> $LOGFILE 2>$LOGFILE

#Download appropriate package for the OS version
#Choose only ONE of the following, corresponding to your OS version

#Debian 8
echo -e "${GREEN}[Datalab Utils] ${ORANG}Adding sources${NC}"
curl https://packages.microsoft.com/config/debian/8/prod.list > /etc/apt/sources.list.d/mssql-release.list 2>$LOGFILE

#Debian 9
#curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list

echo -e "${GREEN}[Datalab Utils] ${ORANG}Updating sources${NC}"
apt-get update >> $LOGFILE
echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing msodbcsql13${NC}"
DEBIAN_FRONTEND=noninteractive ACCEPT_EULA=Y apt-get -y install msodbcsql >> $LOGFILE

# optional: for bcp and sqlcmd
echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing mssql-tools13${NC}"
DEBIAN_FRONTEND=noninteractive ACCEPT_EULA=Y apt-get -y install mssql-tools >> $LOGFILE

# optional: for unixODBC development headers
echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing  unixodbc-dev${NC}"
DEBIAN_FRONTEND=noninteractive apt-get install -y unixodbc-dev >> $LOGFILE

echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing  libssl1.0.0${NC}"
echo "deb http://security.debian.org/debian-security jessie/updates main" >> /etc/apt/sources.list
apt-get update >> $LOGFILE
DEBIAN_FRONTEND=noninteractive apt-get install libssl1.0.0 >>$LOGFILE

echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing  python-pyodbc${NC}"
DEBIAN_FRONTEND=noninteractive apt-get -y install python-pyodbc >> $LOGFILE

echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing  locales${NC}"
DEBIAN_FRONTEND=noninteractive apt-get -y install locales >> $LOGFILE
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
locale-gen >> $LOGFILE

echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"
echo -e "${GREEN}                                           [Pymake]                                             ${NC}"
echo -e "${GREEN}                                          FINISHED :D                                           ${NC}"
echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"