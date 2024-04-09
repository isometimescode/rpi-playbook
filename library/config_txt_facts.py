#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2020, Toni Wells (@isometimescode)
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: config_txt_facts

short_description: This module collects facts for the Rapsberry Pi OS.

version_added: "1.0.0"

description: The facts from this module not only includes OS-specific info like timezone and encoding
             but also information about enabled pins and all of the other configuration listed in
             https://www.raspberrypi.org/documentation/configuration/config-txt/
             https://github.com/RPi-Distro/raspi-config/blob/master/raspi-config

author:
    - Toni Wells (@isometimescode)
'''

EXAMPLES = r'''
- name: Return ansible_facts
  raspberrypi.configure.config_txt_facts:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
ansible_facts.config:
  description: Facts to add to ansible_facts.
  returned: always
  type: dict
  contains:
    timezone:
      description: The timezone name for this host (can be empty)
      type: str
      returned: always
      sample: 'Europe/London'
    keyboard_layout:
      description: The layout for the keyboard (can be empty)
      type: str
      returned: always
      sample: 'gb'
    locale:
      description: The locale for the system (can be empty)
      type: str
      returned: always
      sample: 'en_GB.UTF-8'
    autologin:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 1
    blanking:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 0
    boot_cli:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 1
    boot_splash:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 1
    boot_wait:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 0
    bootro_conf:
      description: The raspi-config value for this key (can be empty)
      type: str
      returned: always
      sample: ''
    bootro_now:
      description: The raspi-config value for this key (can be empty)
      type: str
      returned: always
      sample: ''
    camera:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 1
    can_expand:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 0
    fan:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 1
    fan_gpio:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 14
    fan_temp:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 80
    hostname:
      description: The raspi-config value for this key (can be empty)
      type: str
      returned: always
      sample: 'raspberrypi'
    i2c:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 1
    leds:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: '-1'
    net_names:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 1
    onewire:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 1
    overlay_conf:
      description: The raspi-config value for this key (can be empty)
      type: str
      returned: always
      sample: ''
    overlay_now:
      description: The raspi-config value for this key (can be empty)
      type: str
      returned: always
      sample: ''
    overscan:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 0
    pi4video:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 0
    pi_type:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 0
    pixdub:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 1
    rgpio:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 1
    serial:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 0
    serial_hw:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 1
    spi:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 1
    vnc:
      description: The raspi-config value for this key (can be empty)
      type: int
      returned: always
      sample: 1
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess
import os


def get_file_contents(filename):
    """Return the contents of the specified file or empty string if not found."""
    try:
        with open(filename, 'r') as f:
            return f.read().replace('\n', '')
    except IOError:
        return ''


def run_command(cmd, stripped=True):
    """Run a shell command to retrieve a value or empty string on failure."""
    try:
        with open(os.devnull, 'w') as devnull:
            output = subprocess.check_output(cmd, shell=True, universal_newlines=True, stderr=devnull)
            return output.replace('/n', '').strip() if stripped else output
    except subprocess.CalledProcessError:
        return ''


def get_locales():
    """Run the localectl command for locale info"""
    output = run_command('localectl', False)
    lines = dict(l.strip().split(': ') for l in output.splitlines() if l)
    return {
        'locale': lines.get('System Locale', '').split('=')[-1],
        'keyboard_layout': lines.get('X11 Layout', '')
    }


def get_raspi_configs():
    """Get all the configs from raspi-configs"""
    result = dict()
    configs = [
        'pi_type', 'can_expand', 'overscan', 'blanking', 'pixdub', 'hostname', 'vnc', 'spi', 'i2c',
        'serial', 'serial_hw', 'pi4video', 'boot_cli', 'autologin', 'leds', 'fan', 'fan_gpio',
        'fan_temp', 'boot_wait', 'boot_splash', 'rgpio', 'camera', 'onewire', 'net_names',
        'overlay_now', 'overlay_conf', 'bootro_now', 'bootro_conf']
    for name in configs:
        result[name] = run_command('raspi-config nonint get_' + name)
    # TODO get_config_var gpu_mem_1024 $CONFIG for all memory sizes
    return result


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict()

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        ansible_facts=dict(),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['ansible_facts']['config'] = {
        'timezone': get_file_contents('/etc/timezone'),
    }

    result['ansible_facts']['config'].update(get_locales())
    result['ansible_facts']['config'].update(get_raspi_configs())

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
