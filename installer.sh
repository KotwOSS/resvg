#! /usr/bin/bash

# ░█▀▀█ █▀▀ ░█▀▀▀█ ░█  ░█ ░█▀▀█
# ░█▄▄▀ █▀▀  ▀▀▀▄▄  ░█░█  ░█ ▄▄
# ░█ ░█ ▀▀▀ ░█▄▄▄█   ▀▄▀  ░█▄▄█
#
# ReSVG is a advanced SVG compiler which includes many features.
#
# It is licensed under the MIT license.
#
# (c) Copyright 2022 KotwOSS
#
# https://github.com/KotwOSS/ReSVG


####################################################
## █ █▄░█ █▀ ▀█▀ ▄▀█ █░░ █░░ █▀ █▀▀ █▀█ █ █▀█ ▀█▀ ##
## █ █░▀█ ▄█ ░█░ █▀█ █▄▄ █▄▄ ▄█ █▄▄ █▀▄ █ █▀▀ ░█░ ##
####################################################
#   This script allows an easy installation and    #
#           deinstallation of ReSVG.               #


version='0.0.0alpha1'


red='\033[38;2;255;100;100m'
dark_red='\033[38;2;230;40;40m'
blue='\033[38;2;100;100;255m'
orange='\033[38;2;255;150;0m'
yellow='\033[38;2;255;205;50m'
gray='\033[38;2;140;140;140m'
green='\033[38;2;130;255;130m'
reset='\033[0m'

function print_logo() {
    printf '\n'
    printf $orange'░█▀▀█ █▀▀ ░█▀▀▀█ ░█  ░█ ░█▀▀█'$reset'\n'
    printf $orange'░█▄▄▀ █▀▀  ▀▀▀▄▄  ░█░█  ░█ ▄▄'$reset'\n'
    printf $orange'░█ ░█ ▀▀▀ ░█▄▄▄█   ▀▄▀  ░█▄▄█'$reset'\n'
    printf '\n'
    printf 'ReSVG installer version '$blue$version$reset'\n'
    printf '\n'
}

function install() {
    printf 'Installing...\n'

    if [ ! -f 'resvg' ]; then
        ln __main__.py resvg
    fi
    chmod +x resvg

    echo '# RESVG INSTALL' >> "/home/$user/.bashrc"
    echo 'export PATH="'$install_path':$PATH"' >> "/home/$user/.bashrc"
    echo '# END RESVG INSTALL' >> "/home/$user/.bashrc"

    printf '\n'
    printf 'Successfully '$green'installed '$reset'resvg!\n'
}

function uninstall() {
    printf 'Uninstalling...\n'
    
    if [ -f 'resvg' ]; then
        rm resvg
    fi
    sed -i '/RESVG INSTALL/,/# END RESVG INSTALL/d' "/home/$user/.bashrc"

    printf '\n'
    printf 'Successfully '$red'uninstalled '$reset'resvg!\n'
}

function check() {
    installed=$(cat /home/$user/.bashrc | grep -Eo '# RESVG INSTALL')

    if [ -z "$installed" ]; then
        printf 'Do you really want to '$orange'install '$reset'ReSVG?\n'
        printf '['$orange'Y'$reset'/'$gray'n'$reset']: '
        read answer
        printf '\n'
        if [ "$answer" == 'Y' ]; then
            install
        else
            printf $yellow'not installing'$reset'\n'
        fi
        printf '\n'
    else
        printf $dark_red'WARNING '$reset'Already installed! Do you want to '$red'uninstall'$reset'?\n'
        printf '['$red'Y'$reset'/'$gray'n'$reset']: '
        read answer
        printf '\n'
        if [ "$answer" == 'Y' ]; then
            uninstall
        else
            printf $yellow'not uninstalling'$reset'\n'
        fi
        printf '\n'
    fi
}

function main() {
    cd resvg
    user=$(whoami)
    install_path=$(pwd)

    print_logo
    check
}

main
