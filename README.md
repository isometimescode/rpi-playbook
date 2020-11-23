# Raspberry Pi Collection and Playbook

This repository contains a collection with a fact gathering module and a series of roles for working with both fresh installs of Rapsberry Pi OS and existing hosts on the network.

## Prerequisites

### Installing Rapsberry Pi OS

1. Create an SD card following the directions from [Raspbian](https://www.raspberrypi.org/software/).
2. With your SD card mounted on your local machine, manually copy some additional files to the `boot` directory before you eject the card. This is needed for a headless pi that we connect to via `ssh`.
- An empty file called `ssh`; this will automatically turn on `sshd` at boot.
```
touch /path/to/your/card/boot/ssh
```
- A file called `wpa_supplicant.conf` with your appropriate wifi settings so the pi will join your network automatically. The contents typically look like:
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
  scan_ssid=1
  ssid="YOUR_NETWORK_NAME"
  psk="YOUR_NETWORK_PASSWORD"
  key_mgmt=WPA-PSK
}
```
3. Install your SD card on your device and turn it on.


### Installing Ansible

There are [official Ansible steps](https://docs.ansible.com/ansible/latest/installation_guide/index.html) to install the Ansible CLI on your local machine (or any other machine) you will be using as a controller node.

Another option is to use a [Docker image](https://github.com/isometimescode/docker-ansible-playbook):

```
docker pull isometimescode/ansible-playbook:latest
docker run -it --rm -v $(pwd)/playbook:/playbook isometimescode/ansible-playbook /playbook/yourplaybook.yml
```
