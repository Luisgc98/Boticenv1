#!/bin/bash
defaultLocalPortal=http://localhost:5000

# this variables are dinamisourcey updated from portal
providedPortal=__PORTAL__
userSecret=[__USER_SECRET__]


configurePortal(){
    source ~/.bash_profile
    if [[ $AUTOMAGICA_PORTAL_URL != "" ]]
    then
        echo "Portal already configured, with value $AUTOMAGICA_PORTAL_URL, updating the value to $1"
        sed '/export AUTOMAGICA_PORTAL_URL/d' ~/.bash_profile >> ~/.bash_profile
    fi
    echo "export AUTOMAGICA_PORTAL_URL=$1" >> ~/.bash_profile
    export AUTOMAGICA_PORTAL_URL=$1
}

if [ $providedPortal == "" ]
then
    echo "No Portal URL provied, using default $defaultLocalPortal"
    configurePortal $defaultLocalPortal
else
    echo "To update Portal with URL: $providedPortal"
    configurePortal $providedPortal
fi

echo "Validating minimum required python version."
version=$(python3 -c 'import platform; major, minor, patch = platform.python_version_tuple(); print(major); print(minor); print(patch)')
version=(${version//./ })
if [[ ${version[0]} -lt 3 ]] || [[ ${version[0]} -eq 3 && ${version[1]} -lt 7 ]] || [[ ${version[0]} -eq 3 && ${version[1]} -eq 7 && ${version[2]} -lt 5 ]]; 
then
    if [[ $USER != "root" ]]; 
    then 
        echo "Python 3.7.5+ was not foud, plese run this script as root."
        exit
    else
        echo "Python 3.7.5+ was not foud, proceeding to install."
        curl -L -o 'python37.pkg' https://www.python.org/ftp/python/3.7.5/python-3.7.5-macosx10.9.pkg
        installer -pkg python37.pkg -target /Applications
        rm -rfd 'python37.pkg'
    fi
    #Install automagica module.
fi

#Validate if automagica module is installed.
automagica=$(python3 -c 'import pkgutil; print(1 if pkgutil.find_loader("automagica") else 0)')
if [[ $automagica -eq 1 ]]
then
    echo "Automagica's Python module is installed."
else    
    echo "Automagica's Python module is not installed. Proceeding to install."
    if eval "pip3 install automagica";
    then
        continue
    else
        echo "Error to install Automagica's Python module."
        exit 1
    fi
fi
# sets up the machine as bot
echo "entering setupAsBot"
if [ userSecret == "" ]
then
    echo "No user secret information provided, the process can not continue"
else
    # authenticate and register with the portal
    python3 -m automagica --connect $userSecret
    killall -9 python
    python3 -m automagica --bot
fi

echo "Configure portal ended"
exit 0