nm-applet &
xrandr --auto --output HDMI1 --mode 1920x1080 --rate 60 --right-of eDP1
lxpolkit &
/usr/lib/xfce4/notifyd/xfce4-notifyd &
# plank &
compton &
sleep 2 && tint2 &
sleep 1 && tint2 -c /home/piotr/.config/tint2/bottom-personal-icons.tint2rc &
#nitrogen --restore &
~/.fehbg
obhud --touchpad off &
light -S 20 &
redshift -m randr -l 52.25:22.12 &
numlockx on &
setxkbmap pl &
ksuperkey -e 'Super_L=Alt_L|F1' &
ksuperkey -e 'Super_R=Alt_L|F1' &

