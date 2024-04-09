# Raspberry Pi Collection and Playbook

This repository contains a collection with a fact gathering module and a series of roles for working with both fresh installs of Rapsberry Pi OS and existing hosts on the network.

## Prerequisites

### Installing Rapsberry Pi OS

1. Create an SD card use the Raspberry Pi Imager from [Raspberry Pi OS](https://www.raspberrypi.org/software/) to load a new OS on to your SD card.
2. Make sure to set the settings for:
  * a new user & password
  * a new SSH key
  * the desired hostname
3. Install your SD card on your device and turn it on.
4. Make sure your chosen hostname is listed in the `inventory.yml` file

### Installing Ansible

There are [official Ansible steps](https://docs.ansible.com/ansible/latest/installation_guide/index.html) to install the Ansible CLI on your local machine (or any other machine) you will be using as a controller node.

### Running the Playbook

`ansible-playbook playbook.yml`

Alternatively, you can use tags:

`ansible-playbook -t software playbook.yml` --> to install software only

`ansible-playbook --skip-tags init playbook.yml` --> to run everything except the initial rpi provisioning
