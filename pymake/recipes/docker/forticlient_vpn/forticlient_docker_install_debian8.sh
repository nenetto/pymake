#!/usr/bin/env bash

REEED='\033[0;31m'
GREEN='\033[0;32m'
BLUEE='\033[0;34m'
ORANG='\033[0;33m'
NC='\033[0m'



echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"
echo -e "${GREEN}                                          [Forticlient]                                         ${NC}"
echo -e "${ORANG}                        This scripts installs Forticlient in your Debian 8                      ${NC}"
echo -e "${ORANG}                               E. Marinetto (nenetto@gmail.com)                                 ${NC}"
echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"

echo -e "${GREEN}[Forticlient] ${ORANG}Creating log${NC}"
DIRECTORY=$(cd `dirname $0` && pwd)
LOGFILE=$DIRECTORY'/installation.log'
echo 'This is the log for [Forticlient]' >> $LOGFILE

echo -e "${GREEN}[Forticlient] ${ORANG}Updating sources${NC}"
apt-get update >> $LOGFILE 2>$LOGFILE && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends apt-utils >> $LOGFILE 2>$LOGFILE


echo -e "${GREEN}[Forticlient] ${ORANG}Installing expect${NC}"
# https://askubuntu.com/questions/506158/unable-to-initialize-frontend-dialog-when-using-ssh
DEBIAN_FRONTEND=noninteractive apt-get -y install expect >> $LOGFILE

echo -e "${GREEN}[Forticlient] ${ORANG}Installing ipppd${NC}"
DEBIAN_FRONTEND=noninteractive apt-get -y install ipppd >> $LOGFILE

echo -e "${GREEN}[Forticlient] ${ORANG}Clean apt lists${NC}"
rm -rf /var/lib/apt/lists/* >> $LOGFILE

echo -e "${GREEN}[Forticlient] ${ORANG}Installing Forticlient from https://hadler.me/linux/forticlient-sslvpn-deb-packages/${NC}"
wget 'https://hadler.me/files/forticlient-sslvpn_4.4.2333-1_amd64.deb' -O forticlient-sslvpn_amd64.deb >> $LOGFILE 2>$LOGFILE
dpkg -x forticlient-sslvpn_amd64.deb /usr/share/forticlient >> $LOGFILE

echo -e "${GREEN}[Forticlient] ${ORANG}Running Forticlient setup${NC}"
$DIRECTORY/forticlient_setup >> $LOGFILE

echo -e "${GREEN}[Forticlient] ${ORANG}Copying files${NC}"
cp $DIRECTORY/forticlient.sh /usr/bin/forticlient
cp $DIRECTORY/connect_vpn.sh /usr/bin/connect_vpn

echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"
echo -e "${GREEN}                                        [Forticlient]                                           ${NC}"
echo -e "${GREEN}                                          FINISHED :D                                           ${NC}"
echo -e "${BLUEE}################################################################################################${NC}"
echo -e "${REEED}Remember to run ${GREEN}connect_vpn ${ORANG}<IP>:<PORT> <USERNAME> <PASSWORD>${REEED} to connect your vpn${NC}"
echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"