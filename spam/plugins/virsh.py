#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SPAM virsh Module
The module interfaces with virsh commands to get hypervisor and VM stats.
"""

import spam.ansirunner
import rex


class Virsh(object):
    """
    SPAM Virsh class
    """
    def __init__(self,
                 host_list=None,
                 remote_user=None,
                 remote_pass=None,
                 sudo=False,
                 sudo_user=None,
                 sudo_pass=None):
        '''
        Initialize virsh.
        '''
        self.host_list = host_list
        self.remote_user = remote_user
        self.remote_pass = remote_pass
        self.sudo = sudo
        self.sudo_user = sudo_user
        self.sudo_pass = sudo_pass
        self.runner = spam.ansirunner.AnsibleRunner()


    def get_validated_params(self,
                             host_list, remote_user, remote_pass,
                             sudo, sudo_user, sudo_pass):
        if host_list is None:
            host_list = self.host_list

        if remote_user is None:
            remote_user = self.remote_user

        if remote_pass is None:
            remote_pass = self.remote_pass

        if sudo:
            if sudo_user is None:
                sudo_user = self.sudo_user
            if sudo_pass is None:
                sudo_pass = self.sudo_pass

        return(host_list, remote_user, remote_pass,
               sudo, sudo_user, sudo_pass)

    def virsh_version(self,
                      host_list=None,
                      remote_user=None,
                      remote_pass=None,
                      sudo=False,
                      sudo_user=None,
                      sudo_pass=None):
        '''
        Get the virsh version
        '''
        host_list, remote_user, remote_pass, \
            sudo, sudo_user, sudo_pass = self.get_validated_params(
                host_list, remote_user, remote_pass, sudo, sudo_user,
                sudo_pass)

        result, failed_hosts = self.runner.ansible_perform_operation(
            host_list=host_list,
            remote_user=remote_user,
            remote_pass=remote_pass,
            module="command",
            module_args="virsh version",
            sudo=sudo,
            sudo_user=sudo_user,
            sudo_pass=sudo_pass)

        virsh_result = None

        if result['contacted'].keys():
            virsh_result = {}
            for node in result['contacted'].keys():
                nodeobj = result['contacted'][node]
                jsonoutput = rex.parse_lrvalue_string(nodeobj['stdout'], ":")
                virsh_result[node] = {}
                virsh_result[node]['result'] = jsonoutput

        return virsh_result


