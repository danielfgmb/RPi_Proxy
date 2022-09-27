#!/bin/bash

# Check if gedit is running
# -x flag only match processes whose name (or command line if -f is
# specified) exactly match the pattern. 


if ! pgrep -x "openvpn" > /dev/null || ! pgrep -f "python3 main.py" > /dev/null || ! pgrep -x "ffmpeg" > /dev/null
then
    # editar para concuerde con archivo pendulo
    sudo nohup openvpn /home/pi/pendulo1.ovpn ; python3 main.py ; sh video-stream.sh
fi
