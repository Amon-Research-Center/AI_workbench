#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

apt update && apt -y dist-upgrade
sudo apt install nala wajig
wajig install apache2 nginx samba gnucash zsh fonts-powerline fonts-font-awesome wget curl
eval "chsh -s /usr/bin/zsh"
eval "zsh"

# echo "eklectic  ALL=(ALL) NOPASSWD:ALL" >> /dev/null | sudo tee /etc/sudoers

# direcetories
mkdir -p /home/nfs/wip
mkdir -p /home/nfs/git
mkdir -p /home/nfs/programs
mkdir -p /home/nfs/ek_data
mkdir -p /home/nfs/stoall
mkdir -p /home/nfs/backups
mkdir -p /home/nfs/pxe

rm -vfrd /etc/nanorc
ln -s /home/nfs/ek_data/ek_nanorc /etc/nanorc

rm -vfrd /etc/sudoers
ln -s /home/nfs/ek_data/ek_sudoers /etc/sudoers

rm -vfrd /etc/ntpsec/
ln -s /home/nfs/ek_data/ek_ntp.conf /etc/ntpsec/ntp.conf

rm -vfrd /etc/apache2
ln -s /home/nfs/ek_data/ek_apache2 /etc/apache2

rm -vfrd /etc/nginx
ln -s /home/nfs/ek_data/ek_nginx //etc/nginx

rm -vfrd /etc/samba
ln -s /home/nfs/ek_data/ek_samba /etc/nginx

rm -vfrd /etc/gnucash
ln -s home/nfs/ek_data/ek_gnucash /etc/gnucash

rm -vfrd /var/www
ln -s /home/nfs/ek_data/ek_wwww

rm -vfrd /home/eklectic/.zshrc
ln -s /home/nfs/ek_data/ek_zshrc /home/eklectic/.zshrc

rm -vfrd /home/eklectic/.ohmyzsh
ln -s /home/nfs/ek_data/ek_oh-my-zsh /home/eklectic/.oh-my-zsh

rm -vfrd /home/eklectic/.oh-my-zsh.sh
ln -s /home/nfs/ek_data/ek_oh-my-zsh.sh /home/eklectic/.oh-my-zsh.sh

rm -vfrd /home/eklectic/.p10k.zsh
ln -s /home/nfs/ek_data/ek_p10k.zsh /home/eklectic/.p10k.ek_zshrc

rm -vfrd /home/eklectic/.powerlevel10k
ln -s /home/nfs/ek_data/ek_powerlevel10k /home/eklectic/.powerlevel10k

rm -vfrd /home/eklectic/.ssh
ln -s /home/nfs/ek_data/ek_ssh /home/eklectic/.ssh





