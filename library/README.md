# Collections Plugins Directory

Only one module is provided in this directory, the [`config_txt_facts`](config_txt_facts.py) module. This module gathers specific facts for the [Raspberry Pi OS](https://www.raspberrypi.org/documentation/configuration/config-txt/); on any other system most values will be blank. Most of the values come from various functions defined in the [`raspi-config` script](https://github.com/RPi-Distro/raspi-config/blob/master/raspi-config).

Assuming you have the following playbook file saved as `example.yml`:

```yaml
- hosts: localhost
  tasks:
    - config_txt_facts:
    - ansible.builtin.debug: var=ansible_facts.config
```

```sh
$ ansible-playbook example.yml

PLAY [localhost] **********************************************************************************

TASK [Gathering Facts] ****************************************************************************
ok: [localhost]

TASK [config_txt_facts] *****************************************************
ok: [localhost]

TASK [ansible.builtin.debug] **********************************************************************
ok: [localhost] => {
    "ansible_facts.config": {
        "autologin": "1",
        "blanking": "0",
        "boot_cli": "1",
        "boot_splash": "1",
        "boot_wait": "0",
        "bootro_conf": "",
        "bootro_now": "",
        "camera": "1",
        "can_expand": "0",
        "fan": "1",
        "fan_gpio": "14",
        "fan_temp": "80",
        "hostname": "raspberrypi",
        "i2c": "1",
        "keyboard_layout": "gb",
        "leds": "-1",
        "locale": "en_GB.UTF-8",
        "net_names": "1",
        "onewire": "1",
        "overlay_conf": "",
        "overlay_now": "",
        "overscan": "0",
        "pi4video": "0",
        "pi_type": "0",
        "pixdub": "1",
        "rgpio": "1",
        "serial": "0",
        "serial_hw": "1",
        "spi": "1",
        "timezone": "Europe/London",
        "vnc": "1"
    },
    "changed": false
}
```
