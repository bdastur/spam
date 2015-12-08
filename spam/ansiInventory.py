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
        self.inventory = None
        if not os.path.exists(inventory_filename):
            print "Provide a valid inventory filename"
            return

        self.inventory = ansible.inventory.InventoryParser(inventory_filename)

    def get_hosts(self, group=None):
        '''
        Get the hosts
        '''
        hostlist = []

        if group:
            groupobj = self.inventory.groups.get(group)
            if not groupobj:
                print "Group [%s] not found in inventory" % group
                return None

            groupdict = {}
            groupdict['hostlist'] = []
            for host in groupobj.get_hosts():
                groupdict['hostlist'].append(host.name)
            hostlist.append(groupdict)
        else:
            for group in self.inventory.groups:
                groupdict = {}
                groupdict['group'] = group
                groupdict['hostlist'] = []
                groupobj = self.inventory.groups.get(group)
                for host in groupobj.get_hosts():
                    groupdict['hostlist'].append(host.name)
                hostlist.append(groupdict)

        return hostlist



