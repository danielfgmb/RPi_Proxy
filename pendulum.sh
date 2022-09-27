#!/bin/bash

# Check if gedit is running
# -x flag only match processes whose name (or command line if -f is
# specified) exactly match the pattern. 

echo `date`
# ruta
cd /home/pi/RPi_Proxy/

if ! pgrep -x "openvpn" > /dev/null
then
    # editar para concuerde con archivo pendulo
    echo activando openvpn 
    sudo openvpn /home/pi/pendulo1.ovpn > /dev/null 2>&1 &
else
    echo vpn corriendo
fi

if ! pgrep -x "python3" > /dev/null
then
    echo activando pendulo 

    sh start-hw-control.sh > xd3.txt 2>&1 &
else
    echo pendulo corriendo
fi

if ! pgrep -x "ffmpeg" > /dev/null
then
    echo activando transmision
    sudo nohup sh ./video-stream.sh > /dev/null 2>&1 &
else
    echo ffmpeg corriendo
fi
