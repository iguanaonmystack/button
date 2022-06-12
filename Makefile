all: 
	mount /mnt/usbkey
	cp code.py /mnt/usbkey/code.py
	sync
	umount /mnt/usbkey

boot:
	mount /mnt/usbkey
	cp boot.py /mnt/usbkey/boot.py
	sync
	umount /mnt/usbkey
