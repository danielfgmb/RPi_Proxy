#!/bin/bash

# Check if gedit is running
# -x flag only match processes whose name (or command line if -f is
# specified) exactly match the pattern. 


if ! pgrep -x "openvpn" > /dev/null
then
    # editar para concuerde con archivo pendulo
    sudo openvpn /home/pi/pendulo1.ovpn > /dev/null 2>&1 &
fi

if ! pgrep -f "python3 main.py" > /dev/null
then
    sudo python3 main.py > /dev/null 2>&1 &
fi

if ! pgrep -x "ffmpeg" > /dev/null
then
    sh ./video-stream.sh > /dev/null 2>&1 &
fi
