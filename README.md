# byte-beat-controller

```
cd build
cmake ..
make
```

# python test

Edit byte-beat-json-decoder.py and set your tty for serial connection

```
cd python-test
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 byte-beat-json-decoder.py
```

# Linux setup

```
sudo dpkg-reconfigure console-setup
> UTF-8 [ok]
> Guess optimal character set [ok]
> Terminus [ok]
> 16x32 (framebuffer only) [ok]
reboot
```

vim /boot/firmware/config.txt and add at the bottom of the file

```
enable_uart=1
display_rotate=2
lcd_rotate=2 # rotates the screen connected to the display port
display_hdmi_rotate=2 # rotates the screen connected to the HDMI port
display_lcd_rotate=2 # no idea what screen this applies to
```

vim /boot/firmware/cmdline.txt and add change the line into

```
zswap.enabled=1 zswap.zpool=z3fold zswap.compressor=zstd dwc_otg.lpm_enable=0 console=tty1 root=LABEL=writable rootfstype=ext4 rootwait fixrtc fbcon=rotate:2
```

# pin layout

## PICO

```
button 0 knob: gpio 14 (pin 19) led: gpio 17 (pin 22)
button 1 knob: gpio 15 (pin 20) led: gpio 16 (pin 21)
pot 0: gpio 26 (pin 31), 3v3 out (pin 36), ground (pin 33)
pot 1: gpio 27 (pin 32), 3v3 out (pin 36), ground (pin 33)
uart: RX: gpio 4 (pin 4), TX: gpio 5 (pin 7), ground (pin 8)
power: vsys 5.0v (pin 39), ground (pin 38)
```

## Raspberry pi 4

```
power lcd: 3.3v (pin 1), 5.0v (pin 2), gpio 2 (pin 3), 5.0v (pin 4)
uart: RX: gpio 14 (pin 4), TX: gpio 15 (pin 6), ground (pin 6)
button 1: ground (pin 14), gpio 23 (pin 16)
button 1: ground (pin 20), gpio 24 (pin 18)
power: usb c connect
lcd: hdmi 1
```