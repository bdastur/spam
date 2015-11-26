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
        if not group:
            return self.inventory.hosts.keys()

        groupobj = self.inventory.groups.get(group, None)
        if not groupobj:
            return None

        hostobjs = groupobj.get_hosts()
        hostlist = []
        for host in hostobjs:
            hostlist.append(host.name)

        return hostlist



