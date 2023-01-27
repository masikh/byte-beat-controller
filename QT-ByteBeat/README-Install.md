# Installing QT-Byte-beat on Ubuntu desktop for raspberry pi 4

What you’ll need

* microSD card (9GB minimum, 16GB recommended)
* computer with a microSD card drive
* Raspberry Pi 4
* micro USB-C power cable
* monitor with an HDMI interface
* micro HDMI cable
* USB keyboard
* Active internet cable attached to the raspberry pi (DHCP is assumed) 

#### step 1: Prepare the microSD card

Follow the steps on ubuntu.com for preparing the microSD card. This manual is based on Ubuntu-20.04-LTS-Desktop
    
    https://ubuntu.com/tutorials/how-to-install-ubuntu-desktop-on-raspberry-pi-4

When the image has been written to the microSD card stick it into the raspberry pi and boot from it. 
It's advisable to use a properly sized monitor, keyboard and mouse. 

#### step 2: First boot and setup your Ubuntu installation

Boot from the newly created microSD card and follow the on-screen questionnaire.

    Screen              Answer

    Welcome             English
    Keyboard layout     English (US) English (US)
    Where are you?      Amsterdam
    Who are you?        your name: Byte-Beat
                        Your computer's name: bytebeat
                        Pick a username: bytebeat
                        Choose a password: xxxxxxxxxx
                        Confirm your password: xxxxxxxxxx
                        (x) Log in automatically

After this questionnaire the computer will start to configure your system accordingly.
This will take a sure amount of time. It seems stuck on Applying changes (Waiting for unattended-upgr to exit.)
but it's actually doing something. For the Linux savvy among us (what are you doing here?) you
can switch to tty2 [ctrl-alt-f2] and login on that terminal and run ‘top‘ to monitor the progress.

Eventually it will start the Ubuntu desktop and after a while the ‘Software Updater‘ will ask
to install additional updates. Click ‘Install Now‘. When this is all finished, reboot and 
you're ready for the next steps...

#### step 3: Install software to build and fetch the project

Right-click your desktop and select 'open in terminal'. A terminal window will appear.

    bytebeat@bytebeat:~/Desktop$ sudo apt install git python3-pip pyqt5-dev python3-pyqt5 python3-pyqtgraph python3-pyaudio
    [sudo] password for bytebeat: xxxxxxxx
    ...
    Do you want to ccontinue? [Y/n] Y

Don't close your terminal, we will use it in the next steps too!

#### step 4: Checkout the git repository for retrieving the source-code

Lets checkout the git repository and create a convenient symbolic link to the correct directory.

    bytebeat@bytebeat:~/Desktop$ cd ~/  
    bytebeat@bytebeat:~$ git clone https://github.com/masikh/byte-beat-controller.git
    bytebeat@bytebeat:~$ ln -s byte-beat-controller/QT-Bytebeat .
    
Now you can jump to the QT-bytebeat source-code from any terminal by entering 'cd ~/QT-Bytebeat'.
In the directory ‘~/byte-beat-controller‘ you can find all the sources needed to build and
install the raspberry-pico microcontrollers and in the Docs you find a electrical schematic for 
wire-ing it all up.

#### step 5: Install required python packages for QT-Bytebeat

In you terminal jump to the QT-bytebeat directory and install the python requirements.

    bytebeat@bytebeat:~$ cd ~/QT-Bytebeat
    bytebeat@bytebeat:~/QT-Bytebeat$ sudo python3 -m pip install -r requirements.txt
    [sudo] password for bytebeat: xxxxxxxx
    ...

Check that there are no errors whilst installing the python packages. If there are any, please
be advised by google on how to solve these errors. Python and its packages are well maintained, it
should be easy to solve.

#### step 6: Set access rights for GPIO (/dev/mem)
    
In your terminal add the user to the ‘dialout‘ group

    bytebeat@bytebeat:~/QT-Bytebeat$ sudo adduser robert dialout
    [sudo] password for bytebeat: xxxxxxxx

#### step 7: First run of QT-Bytebeat

    bytebeat@bytebeat:~/QT-Bytebeat$ python3 ByteBeatUI.py

If all went well a window will open with QT-Bytebeat running. Congrats!!!

#### step 8: Make note of the ip-address and enable remote access

Install net-tools and openssh-server

    bytebeat@bytebeat:~/QT-Bytebeat$ sudo apt install net-tools openssh-server x11vnc
    [sudo] password for bytebeat: xxxxxxxx
    bytebeat@bytebeat:~/QT-Bytebeat$ ifconfig

Look up your ip-address either under eth0 (inet address), something like 192.168.1.12 or
under the wlan0 address if you also configured the wireless network. You can test if remote
access is working by opening a ssh-client on a remote machine and try to login to the 
raspberry pi.

    protocol: ssh
    username: bytebeat
    password: the password given during setup
    ip address: the one acquired above

If you can successfully login remotely, it's time to build the raspberry pi into a box and attach all the wires from 
the ‘circuit.png‘ in the ‘~/byte-beat-controller/Docs‘ directory.

#### step 9: Rotate the screen and setup system font

We use nano as editor of choice

    bytebeat@bytebeat:~/QT-Bytebeat$ sudo nano /boot/firmware/config.txt
    [sudo] password for bytebeat: xxxxxxxx

Add the following at the bottom of the file and save with [ctrl x, y]

    display_rotate=2
    lcd_rotate=2 # rotates the screen connected to the display port
    display_hdmi_rotate=2 # rotates the screen connected to the HDMI port
    display_lcd_rotate=2 # no idea what screen this applies to

    bytebeat@bytebeat:~/QT-Bytebeat$ sudo nano /boot/firmware/cmdline.txt
    [sudo] password for bytebeat: xxxxxxxx

Replace the line with and save with [ctrl x, y]

    zswap.enabled=1 zswap.zpool=z3fold zswap.compressor=zstd dwc_otg.lpm_enable=0 console=tty1 root=LABEL=writable rootfstype=ext4 rootwait fixrtc fbcon=rotate:2

We also fix the console font to be more readable

    bytebeat@bytebeat:~/QT-Bytebeat$ sudo dpkg-reconfigure console-setup
    [sudo] password for bytebeat: xxxxxxxx  
    > UTF-8 [ok]
    > Guess optimal character set [ok]
    > Terminus [ok]
    > 16x32 (framebuffer only) [ok]

Now reboot and check if the screen is correctly rotated and more readable. 

**Note I** The graphical user interface is still upside down. This is ok, we'll fix it later

**Note II** The first part during boot (before the flickering) is small font, the correct font is loaded after the flickering


#### Enable serial interface for UART

    bytebeat@bytebeat:~/QT-Bytebeat$ sudo apt install raspi-config
    [sudo] password for bytebeat: xxxxxxxx
    bytebeat@bytebeat:~/QT-Bytebeat$ raspi-config

####







