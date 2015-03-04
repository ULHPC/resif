# Lmod install

## Overview

This document provides indications to follow in order to install Lmod on CentOS and Debian.

## Install on CentOS

**Prerequisites:** You need to have the EPEL testing repositories in the sources list. (Do not enable it by default):

    yum install epel-release -y

Then install the Lmod package using this repo:

    yum install --enable-repo=epel-testing Lmod

You can now use Lmod in a version compatible with EasyBuild.

## Install on Debian

**Prerequisites:** You need to have the sid repository in your sources list (the lmod package from jessie is too old and therefore not compatible with EasyBuild). And we are going to make sure that this repo is not going to be used for anything else except if we specify it directly.

1) Add the sid repository to your sources list:  
    1) Create a file named debian-sid.list in /etc/apt/sources.list.d
    2) Write the following content inside it:  
    
        # sid repository - main, contrib and non-free branches
        deb http://http.us.debian.org/debian sid main non-free contrib
        deb-src http://http.us.debian.org/debian sid main non-free contrib
3) Set your default Debian release. Create or modify /etc/apt/apt.conf.d/99defaultrelease to match the following content:

    APT::Default-Release "wheezy"
Eventually replacing _wheezy_ with the name of your release if different.
2) Install the lmod package using this repository:
   
    apt-get update
    apt-get install -y -t sid lmod

You can now use Lmod in a version compatible with EasyBuild.