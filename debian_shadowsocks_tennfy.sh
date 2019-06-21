#! /bin/bash
#===============================================================================================
#   System Required:  debian or ubuntu (32bit/64bit)
#   Description:  Install Shadowsocks(libev) for Debian or Ubuntu
#   Author: tennfy <admin@tennfy.com>
#   Intro:  http://www.tennfy.com
#===============================================================================================
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
clear
echo '-----------------------------------------------------------------'
echo '   Install Shadowsocks(libev) for debian or ubuntu (32bit/64bit) '
echo '   Intro:  http://www.tennfy.com                                 '
echo '   Author: tennfy <admin@tennfy.com>                             '
echo '-----------------------------------------------------------------'

#Variables
ShadowsocksType='shadowsocks-libev'
ShadowsocksDir='/opt/shadowsocks'

#Version
ShadowsocksVersion=''
LIBUDNS_VER='0.4'
LIBSODIUM_VER='1.0.13'
MBEDTLS_VER='2.6.0'

#ciphers
Ciphers=(
chacha20-ietf-poly1305
aes-256-gcm
aes-192-gcm
aes-128-gcm
)

#color
CEND="\033[0m"
CMSG="\033[1;36m"
CFAILURE="\033[1;31m"
CSUCCESS="\033[32m"
CWARNING="\033[1;33m"

function Die()
{
	echo -e "${CFAILURE}[Error] $1 ${CEND}"
	exit 1
}
function CheckSanity()
{
	# Do some sanity checking.
	if [ $(/usr/bin/id -u) != "0" ]; then
		Die 'Must be run by root user'
	fi

	if [ ! -f /etc/debian_version ]; then
		Die "Distribution is not supported"
	fi
}
function PackageInstall()
{
    for package in $*; do  
		echo "[${package} Installing] ************************************************** >>"
		apt-get install -y --force-yes $package 
		if [ $? -ne 0 ]; then
			 Die "${package} install failed"
		fi
    done  
}
function Download()
{
	wget --no-check-certificate -c $1
	if [ $? -ne 0 ]; then
		Die "File download failed"
	fi
}
function GetDebianVersion()
{
	if [ -f /etc/debian_version ]; then
		local main_version=$1
		local debian_version=`cat /etc/debian_version|awk -F '.' '{print $1}'`
		if [ "${main_version}" == "${debian_version}" ]; then
		    return 0
		else 
			return 1
		fi
	else
		Die "Distribution is not supported"
	fi    	
}
function GetSystemBit()
{
	ldconfig
	if [ $(getconf WORD_BIT) = '32' ] && [ $(getconf LONG_BIT) = '64' ] ; then
		if [ '64' = $1 ]; then
		    return 0
		else
		    return 1
		fi			
	else
		if [ '32' = $1 ]; then
		    return 0
		else
		    return 1
		fi		
	fi
}
function CheckServerPort()
{
    if [ $1 -ge 1 ] && [ $1 -le 65535 ]; then 
	    return 0
	else
	    return 1
	fi
}
function GetLatestShadowsocksVersion()
{
	local shadowsocksurl=`curl -s https://api.github.com/repos/shadowsocks/shadowsocks-libev/releases/latest | grep tag_name | cut -d '"' -f 4`
	
	if [ $? -ne 0 ]; then
	    Die "Get latest shadowsocks version failed!"
	else
	    ShadowsocksVersion=`echo $shadowsocksurl|sed 's/v//g'`
	fi
}
function InstallLibudns()
{
    Download http://www.corpit.ru/mjt/udns/udns-$LIBUDNS_VER.tar.gz
    tar -zxvf udns-$LIBUDNS_VER.tar.gz -C ${ShadowsocksDir}/packages
	rm -f udns-$LIBUDNS_VER.tar.gz
	
    pushd ${ShadowsocksDir}/packages/udns-$LIBUDNS_VER	
    ./configure && make && \
	cp udns.h /usr/include/ && \
	cp libudns.a /usr/lib/ 
    if [ $? -ne 0 ]; then
    #failure indication
        Die "Libudns installation failed!"
    fi
    popd
    ldconfig	
}
function InstallLibsodium()
{
    Download https://github.com/jedisct1/libsodium/releases/download/$LIBSODIUM_VER/libsodium-$LIBSODIUM_VER.tar.gz
    tar -zxvf libsodium-$LIBSODIUM_VER.tar.gz -C ${ShadowsocksDir}/packages
	rm -f libsodium-$LIBSODIUM_VER.tar.gz
	
    pushd ${ShadowsocksDir}/packages/libsodium-$LIBSODIUM_VER
    ./configure --prefix=/usr && make && make install
	if [ $? -ne 0 ]; then
    #failure indication
        Die "Libsodium installation failed!"
    fi
    popd
    ldconfig	
}
function InstallMbedtls()
{
    Download https://tls.mbed.org/download/mbedtls-$MBEDTLS_VER-gpl.tgz
	tar -zxvf mbedtls-$MBEDTLS_VER-gpl.tgz -C ${ShadowsocksDir}/packages
	rm -f mbedtls-$MBEDTLS_VER-gpl.tgz
	
    pushd ${ShadowsocksDir}/packages/mbedtls-$MBEDTLS_VER	
    make SHARED=1 CFLAGS=-fPIC && make DESTDIR=/usr install
	if [ $? -ne 0 ]; then
    #failure indication
        Die "Mbedtls installation failed!"
    fi
    popd
    ldconfig	
}
function InstallShadowsocksCore()
{
    #install
    PackageInstall gettext build-essential autoconf libtool libpcre3-dev libev-dev libc-ares-dev automake curl
	
    #install Libsodium
    InstallLibsodium 
    #install MbedTLS
    InstallMbedtls
	
    #get latest shadowsocks-libev release version
	GetLatestShadowsocksVersion
	
    #download latest release version of shadowsocks-libev
    Download https://github.com/shadowsocks/shadowsocks-libev/releases/download/v${ShadowsocksVersion}/shadowsocks-libev-${ShadowsocksVersion}.tar.gz
    tar zxvf shadowsocks-libev-${ShadowsocksVersion}.tar.gz -C ${ShadowsocksDir}/packages
	rm -f shadowsocks-libev-${ShadowsocksVersion}.tar.gz 
	
	mv ${ShadowsocksDir}/packages/shadowsocks-libev-${ShadowsocksVersion} ${ShadowsocksDir}/packages/shadowsocks-libev
    pushd ${ShadowsocksDir}/packages/shadowsocks-libev
    ./configure --prefix=/usr --disable-documentation && make && make install
	if [ $? -ne 0 ]; then
    #failure indication
        Die "Shadowsocks-libev installation failed!"
    fi	
    mkdir -p /etc/${ShadowsocksType}
    cp ./debian/shadowsocks-libev.init /etc/init.d/${ShadowsocksType}
    cp ./debian/shadowsocks-libev.default /etc/default/${ShadowsocksType}
	
	#fix bind() problem without root user
	sed -i '/nobody/i\USER="root"' /etc/init.d/${ShadowsocksType}
	sed -i '/nobody/i\GROUP="root"' /etc/init.d/${ShadowsocksType}
	sed -i '/nobody/d' /etc/init.d/${ShadowsocksType}
	sed -i '/nogroup/d' /etc/init.d/${ShadowsocksType}
	
    chmod +x /etc/init.d/${ShadowsocksType}
	popd	
}
function UninstallShadowsocksCore()
{
    #stop shadowsocks-libev process
    /etc/init.d/${ShadowsocksType} stop

	#uninstall shadowsocks-libev
	update-rc.d -f ${ShadowsocksType} remove 

    #change the dir to shadowsocks-libev
    pushd ${ShadowsocksDir}/packages/shadowsocks-libev
	make uninstall
    make clean
	popd
	
    #delete all install files
	rm -rf ${ShadowsocksDir}   

    #delete configuration file
    rm -rf /etc/${ShadowsocksType}

    #delete shadowsocks-libev init file
    rm -f /etc/init.d/${ShadowsocksType}
    rm -f /etc/default/${ShadowsocksType}
}
function Init()
{	
	#init system
	apt-get update
	
	cd /root
	
    #create packages and conf directory
	if [ -d ${ShadowsocksDir} ]; then 
	    rm -rf ${ShadowsocksDir}	
	fi
	mkdir ${ShadowsocksDir}
	mkdir ${ShadowsocksDir}/packages
	mkdir ${ShadowsocksDir}/conf
}
############################### install function##################################
function InstallShadowsocks()
{
	#initialize
    Init
	
    #install shadowsocks core program
	InstallShadowsocksCore
	
    # Get IP address(Default No.1)	
    ip=`curl -s checkip.dyndns.com | cut -d' ' -f 6  | cut -d'<' -f 1`
    if [ -z $ip ]; then
        ip=`curl -s ifconfig.me/ip`
    fi

    #config setting
	clear
    echo '-----------------------------------------------------------------'
    echo '          Please setup your shadowsocks server                   '
    echo '-----------------------------------------------------------------'
    echo ''
	#input server port
	while :; do
        read -p "input server port(443 is default): " server_port
		[ -z "$server_port" ] && server_port=443
        if CheckServerPort $(($server_port)); then
		    break
		else
		    echo -e "${CFAILURE}[Error] The server port should be between 1 to 65535! ${CEND}"
		fi
	done
	
	echo ''
	echo '-----------------------------------------------------------------'
	echo ''
	
	#select encrypt method
	while :; do
		echo 'Please select encrypt method:'
        i=1
		for var in "${Ciphers[@]}"; do
            echo -e "\t${CMSG}${i}${CEND}. ${var}"
			let i++
        done
		read -p "Please input a number:(Default 1 press Enter) " encrypt_method_num
		[ -z "$encrypt_method_num" ] && encrypt_method_num=1
		if [[ ! $encrypt_method_num =~ ^[1-${#Ciphers[@]}]$ ]]; then
			echo -e "${CWARNING} input error! Please only input number 1~${#Ciphers[@]} ${CEND}"
		else
		    let encrypt_method_num=encrypt_method_num-1
			encrypt_method=${Ciphers[$encrypt_method_num]}			
			break
		fi
	done
	
	echo ''
	echo '-----------------------------------------------------------------'
	echo ''
	while :; do
        read -p "input password: " shadowsocks_pwd
	    if [ -z ${shadowsocks_pwd} ]; then
		    echo -e "${CFAILURE}[Error] The password is null! ${CEND}"
		else
            break
		fi
	done	
         

	echo ''
	echo '-----------------------------------------------------------------'
	echo ''

    #config shadowsocks
cat > /etc/${ShadowsocksType}/config.json<<-EOF
{
    "server":"${ip}",
    "server_port":${server_port},
    "local_port":1080,
    "password":"${shadowsocks_pwd}",
    "timeout":60,
    "method":"${encrypt_method}"
}
EOF

    #add system startup
    update-rc.d ${ShadowsocksType} defaults

    #start service
    /etc/init.d/${ShadowsocksType} start

    #if failed, start again --debian8 specified
    if [ $? -ne 0 ]; then
    #failure indication
	    echo ''
        echo '-----------------------------------------------------------------'
		echo ''
        echo -e "${CFAILURE}Sorry, shadowsocks-libev install failed!${CEND}"
        echo -e "${CFAILURE}Please contact with admin@tennfy.com${CEND}"
		echo ''
		echo '-----------------------------------------------------------------'
    else	
        #success indication
		echo ''
        echo '-----------------------------------------------------------------'
		echo ''
        echo -e "${CSUCCESS}Congratulations, ${ShadowsocksType} install completed!${CEND}"
        echo -e "Your Server IP: ${ip}"
        echo -e "Your Server Port: ${server_port}"
        echo -e "Your Password: ${shadowsocks_pwd}"
        echo -e "Your Local Port: 1080"
        echo -e "Your Encryption Method:${encrypt_method}"
		echo ''
		echo '-----------------------------------------------------------------'
    fi
}
############################### uninstall function##################################
function UninstallShadowsocks()
{
    UninstallShadowsocksCore
    echo -e "${CSUCCESS}${ShadowsocksType} uninstall success!${CEND}"
}
############################### update function##################################
function UpdateShadowsocks()
{
    UninstallShadowsocks
    InstallShadowsocks
    echo -e "${CSUCCESS}${ShadowsocksType} update success!${CEND}"
}
############################### Initialization##################################
CheckSanity

action=$1
[ -z $1 ] && action=install
case "$action" in
install)
    InstallShadowsocks
    ;;
uninstall)
    UninstallShadowsocks
    ;;
update)
    UpdateShadowsocks
    ;;	
*)
    echo "Arguments error! [${action} ]"
    echo "Usage: `basename $0` {install|uninstall|update}"
    ;;
esac
