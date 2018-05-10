#!/usr/bin/env bash

GREEN='\033[0;32m'
BLUEE='\033[0;34m'
ORANG='\033[0;33m'
NC='\033[0m'


echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"
echo -e "${GREEN}                                          [AWS Support]                                         ${NC}"
echo -e "${ORANG}                           This scripts installs AWS cli and configure it                          ${NC}"
echo -e "${ORANG}                                  E. Marinetto (nenetto@gmail.com)                              ${NC}"
echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"

echo -e "${GREEN}[AWS Support] ${ORANG}Creating log${NC}"
DIRECTORY=$(cd `dirname $0` && pwd)
LOGFILE=${DIRECTORY}'/installation.log'

#echo -e "${GREEN}[AWS Support] ${ORANG}Updating sources${NC}"
#apt-get update >> $LOGFILE 2>$LOGFILE && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends apt-utils >> $LOGFILE 2>$LOGFILE

#echo -e "${GREEN}[AWS Support] ${ORANG}Installing aws-cli${NC}"
#pip install awscli >> $LOGFILE

echo -e "${GREEN}[AWS Support] ${ORANG}Configuring aws${NC}"
printf "%s\n%s\neu-west-2\njson" "${AWS_KEY_ID}" "${AWS_SECRET_KEY}" | aws configure >> $LOGFILE


echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"
echo -e "${GREEN}                                         [AWS Support]                                          ${NC}"
echo -e "${GREEN}                                          FINISHED :D                                           ${NC}"
echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"