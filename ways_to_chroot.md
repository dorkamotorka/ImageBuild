## chroot

This command may be used directly as root, but normal users are not able to use this command. 

## schroot

schroot allows access to chroots for normal users using the same mechanism, but with permissions checking and allowing additional automated setup of the chroot environment, such as mounting additional filesystems and other configuration tasks.

## dchroot

dchroot is and earlier version and is being deprecated in favour of schroot.

## arch-chroot 

arch-chroot is a shell script that prepares a new "root directory" with the necessary system mounts (/proc, /sys, /dev, etc.) and files (/etc/resolv.conf), then does a chroot into it.

Instal on Ubuntu with: 

	sudo apt install arch-install-scripts
