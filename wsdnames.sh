#!/usr/bin/env bash
# config: exec_always /home/piotr/PycharmProjects/swayinfo/wsdnames.sh

# Do not forget to change the path according to the script location!
pkill -f "python3 /home/piotr/PycharmProjects/swayinfo/wsdnames-i3ipc-2.0.1.py"
/home/piotr/PycharmProjects/swayinfo/wsdnames.py &
