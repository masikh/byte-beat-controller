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