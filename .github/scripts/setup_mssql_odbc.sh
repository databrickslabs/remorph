#!/usr/bin/env bash

set -xve
#Repurposed from https://github.com/Yarden-zamir/install-mssql-odbc

VERSION_ID="$(awk -F= '$1=="VERSION_ID"{gsub(/\"/, "", $2); print $2}' /etc/os-release)"

declare -A known_hashes=(
  [20.04]='3edd2ff1b9e18ca3bc93f46893b755400d1f22f4fb4c077c9d5882cd60d837b8'
  [22.04]='b8713c36d3e6f6b2520830180cf6b5779e48410ad5d5e1b192635b0c7359fcc6'
  [24.04]='607d2033f90d1e58ed3cb3593c9b83881f6b3cb3627ab7d00952f1c04199c3a1'
)
if [ ! -v "known_hashes[${VERSION_ID}]" ]
then
  printf "Unsupported Ubuntu version: %s\n" "${VERSION_ID}"
  exit 1
fi
expected_hash="${known_hashes[${VERSION_ID}]}"

curl -sSL -O "https://packages.microsoft.com/config/ubuntu/${VERSION_ID}/packages-microsoft-prod.deb"
printf "%s *packages-microsoft-prod.deb\n" "${expected_hash}" | sha256sum -c -

sudo dpkg -i packages-microsoft-prod.deb
#rm packages-microsoft-prod.deb

sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
