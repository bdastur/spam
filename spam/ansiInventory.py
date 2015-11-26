#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AnsibleInventory:

INTRO:

USAGE:

"""

import os
import ansible.inventory


class AnsibleInventory(object):
    '''
    Ansible Inventory wrapper class.
    '''
    def __init__(self, inventory_filename):
        '''
        Initialize Inventory
        '''
        if not os.path.exists(inventory_filename):
            print "Provide a valid inventory filename"
            return

        self.inventory = ansible.inventory.InventoryParser(inventory_filename)

    def get_hosts(self, group=None):
        '''
        Get the hosts
        '''
        hostlist = []
        for group in self.inventory.groups:
            groupdict = {}
            groupdict['group'] = group
            groupdict['hostlist'] = []
            groupobj = self.inventory.groups.get(group)
            for host in groupobj.get_hosts():
                groupdict['hostlist'].append(host.name)
            hostlist.append(groupdict)

        return hostlist



