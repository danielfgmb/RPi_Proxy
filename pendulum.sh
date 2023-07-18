#!/bin/bash

# Check if gedit is running
# -x flag only match processes whose name (or command line if -f is
# specified) exactly match the pattern. 

. ./datos_servidor.ini

echo `date`
echo v10
# ruta


if ! pgrep -x "openvpn" > /dev/null
then
    # editar para concuerde con archivo pendulo
    echo activando openvpn 
    sudo openvpn $ubicacion_ovpn_file > /dev/null 2>&1 &
    echo durmiendo por 30s
    sleep 20
else
    echo vpn corriendo
fi

if ! pgrep -x "python3" > /dev/null
then
    echo activando pendulo 
    killall python3
    cd $ubicacion_proxy  && python3 main.py > /dev/null 2>&1 &

else
    echo pendulo corriendo
fi

if ! pgrep -x "ffmpeg" > /dev/null
then
    echo nada ffmpeg $video_frame $video_width\x$video_height $usb_camera $video_server/$stream_key
    sudo ffmpeg -f v4l2 -framerate $video_frame -video_size $video_width\x$video_height -i $usb_camera -c:v libx264 -preset veryfast -tune zerolatency -pix_fmt yuv420p -an -f flv $video_server/$stream_key > /dev/null 2>&1 &

    # echo activando transmision
    # cd /home/pi/RPi_Proxy/ && sudo nohup sh video-stream.sh > /dev/null 2>&1 &
else
    echo ffmpeg corriendo
fi
