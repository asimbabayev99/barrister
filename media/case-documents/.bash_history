git clone https://github.com/Soltanali-J/SINAM.git
git clone https://github.com/azad-mammedov/Lusoft.git
git config --global user.name "azad-mammedov"
git config --global user.email "azad.mammedov6@gmail.com"
git clone https://github.com/asimbabayev99/LuaProject.git
git clone https://github.com/asimbabayev99/LuaProject.git
#!/bin/sh
# Copyright 2011 Dvir Volk <dvirsk at gmail dot com>. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL Dvir Volk OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
################################################################################
#
# Service installer for redis server, runs interactively by default.
#
# To run this script non-interactively (for automation/provisioning purposes),
# feed the variables into the script. Any missing variables will be prompted!
# Tip: Environment variables also support command substitution (see REDIS_EXECUTABLE)
#
# Example:
#
# sudo REDIS_PORT=1234 \
# 		 REDIS_CONFIG_FILE=/etc/redis/1234.conf \
# 		 REDIS_LOG_FILE=/var/log/redis_1234.log \
# 		 REDIS_DATA_DIR=/var/lib/redis/1234 \
# 		 REDIS_EXECUTABLE=`command -v redis-server` ./utils/install_server.sh
#
# This generates a redis config file and an /etc/init.d script, and installs them.
#
# /!\ This script should be run as root
#
################################################################################
die () { 	echo "ERROR: $1. Aborting!"; 	exit 1; }
#Absolute path to this script
SCRIPT=$(readlink -f $0)
#Absolute path this script is in
SCRIPTPATH=$(dirname $SCRIPT)
#Initial defaults
_REDIS_PORT=6379
_MANUAL_EXECUTION=false
echo "Welcome to the redis service installer"
echo "This script will help you easily set up a running redis server"
echo
#check for root user
if [ "$(id -u)" -ne 0 ] ; then 	echo "You must run this script as root. Sorry!"; 	exit 1; fi
git clone https://github.com/Soltanali-J/Lua-Group.git
git clone https://github.com/azad-mammedov/Luamarket.git
git clone https://github.com/asimbabayev99/LuaProject.git
git clone https://github.com/asimbabayev99/barrister.git
git clone https://github.com/asimbabayev99/barrister.git
git clone https://github.com/asimbabayev99/barrister.git
git clone https://github.com/asimbabayev99/barrister.git
git clone https://github.com/asimbabayev99/arimas.git
git clone https://github.com/asimbabayev99/merdan-argo.git
git pull https://github.com/Soltanali-J/SINAM.git
git pull https://github.com/Soltanali-J/SINAM
