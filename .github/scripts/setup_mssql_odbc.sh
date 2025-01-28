#!/usr/bin/env bash

set -xve
#Repurposed from https://github.com/Yarden-zamir/install-mssql-odbc

curl -sSL -O https://packages.microsoft.com/config/ubuntu/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)/packages-microsoft-prod.deb

sudo dpkg -i packages-microsoft-prod.deb
#rm packages-microsoft-prod.deb

sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18

