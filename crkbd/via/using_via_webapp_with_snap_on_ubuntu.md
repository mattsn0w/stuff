# Summary 
Canonical created [Snap](https://snapcraft.io/about) in an effort to make general purpose and secure software packages by using [Linux Namespaces](https://en.wikipedia.org/wiki/Linux_namespaces).  
Container runtimes (_Docker, LXC, podman, Containerd, Nerdctl, Kubernetws_) makes extensive use of this Namespaces functionality along with other powerful security related system calls. [RedHat](https://www.redhat.com/sysadmin/building-container-namespaces) has a great blog post covering how to build containers by hand, aka, "containers the hard way".  


# Problem Statement
Because of the added software layer around a Snap'd applications by way of namespaces, specifically with filesystems, process separation, etc... ,
interaction with a computer's Human Input Devices (_aka, HID, like a keyboard or mouse_) are explicitly limited or do not work.
Web based Applications, such as the popular [VIA](https://usevia.app) for keyboard keymap configurations do not work. This breaks things for the [w3c webHID standard](https://wicg.github.io/webhid/) that enables cross-platform device configuration. 
I am using a Raspberry Pi 4 running Ubuntu 24.04 Desktop to build and configure qmk_firmware with VIA support for use on [Foostan's Corne v3 keyboard](https://github.com/foostan/crkbd/tree/v3-final), which I am building a small batch of.

## Debug pointers
* Browse to `chrome://device-log/` in Chromium or brave. You should see a permission error on one of the enumerated `/dev/hidrawN` devices.
  * `chrome://chrome-urls/` also has a list of interesting tools for diving deeper into Chromium based browser features, such as error handing(_chrome://network-errors/_) and the browser's DNS lookup (_chrome://net-internals/#dns_).  
* Check the permissions of the devices `/dev/hidraw*` and `/dev/input/event*`. 
* `lsusb` command is useful to see if the keyboard is visible to the kernel and USB driver.
* 

## Possible workarounds
1) Install the udev rule file from QMK for the supported devices.
  1) get the file from the [git repo](https://github.com/qmk/qmk_firmware/blob/master/util/udev/50-qmk.rules) ; copy it to ` /etc/udev/rules.d/`
  2) Add your username to the `plugdev` and `input` groups in `/etc/group` or with [usermod](https://manpages.ubuntu.com/manpages/noble/en/man8/usermod.8.html).
  3) Run `sudo udevadm control --reload-rules`
  4) Run `sudo udevadm trigger`
2) Execute the Chromium or Brave binary directly outside of the snap wrapper.
  1) `/snap/chromium/current/usr/lib/chromium-browser/chrome --user-data-dir=~/ChrUnsnapped --class="ChrUnsnapped" %U &` 
3) Browse to https://usevia.app and authorize the device.
4) Profit.



## Linux Specific Commands

```
# Brute force
# Plugin VIA enabled keyboard to Linux machine.
sudo chmod a+rwx /dev/hidraw*
sudo chmod a+rwx /dev/input/event*
# Run un-snapped Chromium.
/snap/chromium/current/usr/lib/chromium-browser/chrome --user-data-dir=~/ChrUnsnapped --class="ChrUnsnapped" %U &

sudo cp util/udev/50-qmk.rules /etc/udev/rules.d/
```

## 

### References
https://bbs.archlinux.org/viewtopic.php?id=285709
