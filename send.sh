#!/bin/bash
sshpass -p "raspberry" rsync -a ./registration_pattern.goo pi@elegoo.local:/mnt/usb_share --rsync-path="sudo rsync" --no-o --no-g
