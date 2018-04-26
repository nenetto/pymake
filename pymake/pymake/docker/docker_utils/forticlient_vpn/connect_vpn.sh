#!/usr/bin/env bash

if [ -z "$TERM" ]; then
    export TERM=xterm
    connect_vpn $1 $2 $3
else

    GREEN='\033[0;32m'
    REDDD='\033[0;31m'
    BLUEE='\033[0;34m'
    ORANG='\033[0;33m'
    NC='\033[0m'

    # Set parameters
    export VPNADDR=$1
    export VPNUSER=$2
    export VPNPASS=$3

    export VPNTIMEOUT=20

    echo ""
    echo -e "${BLUEE}--------------------------------------------------------------------------------${NC}"
    echo -e "${GREEN}                            [Start Forticlient]                                 ${NC}"
    echo -e "${ORANG}                This scripts starts Forticlient in your Debian 8                ${NC}"
    echo -e "${ORANG}                        E. Marinetto (nenetto@gmail.com)                        ${NC}"
    echo -e "${ORANG}          credits to https://github.com/AuchanDirect/docker-forticlient         ${NC}"
    echo -e "${BLUEE}--------------------------------------------------------------------------------${NC}"

    LOGFILE='/var/log/Forticlient.log'
    echo 'This is the log for [Forticlient]' >> $LOGFILE
    echo -e "${BLUEE}Log in ${GREEN}${LOGFILE} ${NC}"


    if [ -z "$VPNADDR" -o -z "$VPNUSER" -o -z "$VPNPASS" ]; then
      echo -e "${REDDD}[Start Forticlient] Variables VPNADDR, VPNUSER, VPNPASS must be provided.${NC}"; exit;
    fi

    # Setup masquerade, to allow using the container as a gateway
    #for iface in $(ip a | grep eth | grep inet | awk '{print $2}'); do
    #  iptables -t nat -A POSTROUTING -s "$iface" -j MASQUERADE
    #done

    echo -e "${BLUEE}------------ VPN Starts ------------${NC}"
    echo -e "${BLUEE}------------ Parameters ------------${NC}"
    echo -e "${BLUEE}-- ${ORANG}Server: ${GREEN}${VPNADDR}${NC}"
    echo -e "${BLUEE}-- ${ORANG}User  : ${GREEN}${VPNUSER}${NC}"
    echo -e "${BLUEE}-------------------------------------${NC}"
    echo -e "${BLUEE}----------- Kill previous -----------${NC}"
    pkill -f forticlient >> $LOGFILE
    echo -e "${BLUEE}-------------------------------------${NC}"
    /usr/bin/forticlient >> $LOGFILE ; sleep 10; echo -e "${BLUEE}-------------------------------------${NC}"

fi