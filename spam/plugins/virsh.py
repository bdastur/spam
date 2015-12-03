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

    def execute_virsh_command(self,
                              **kwargs):
        '''
        common virsh execution function
        '''
        host_list = kwargs.get('host_list', None)
        remote_user = kwargs.get('remote_user', None)
        remote_pass = kwargs.get('remote_pass', None)
        sudo = kwargs.get('sudo', False)
        sudo_user = kwargs.get('sudo_user', None)
        sudo_pass = kwargs.get('sudo_pass', None)

        host_list, remote_user, remote_pass, \
            sudo, sudo_user, sudo_pass = self.get_validated_params(
                host_list, remote_user,
                remote_pass, sudo,
                sudo_user, sudo_pass)

        if 'cmd' not in kwargs.keys():
            print "Require a command to execute"
            return None
        cmd = kwargs['cmd']

        if 'delimiter' not in kwargs.keys():
            delimiter = ":"
        else:
            delimiter = kwargs['delimiter']

        if 'output_type' not in kwargs.keys():
            output_type = "LRVALUE"
        else:
            output_type = kwargs['output_type']

        if output_type == "TABLE":
            if 'fields' not in kwargs.keys():
                print "Require to pass fields"
                return None

        fields = kwargs['fields']

        result, failed_hosts = self.runner.ansible_perform_operation(
            host_list=host_list,
            remote_user=remote_user,
            remote_pass=remote_pass,
            module="command",
            module_args=cmd,
            sudo=sudo,
            sudo_user=sudo_user,
            sudo_pass=sudo_pass)

        virsh_result = None
        if result['contacted'].keys():
            virsh_result = {}
            for node in result['contacted'].keys():
                nodeobj = result['contacted'][node]
                if output_type == "LRVALUE":
                    jsonoutput = rex.parse_lrvalue_string(nodeobj['stdout'],
                                                          delimiter)
                elif output_type == "TABLE":
                    jsonoutput = rex.parse_tabular_string(nodeobj['stdout'],
                                                          fields)
                else:
                    pass
                virsh_result[node] = {}
                virsh_result[node]['result'] = jsonoutput

        return virsh_result

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

    def virsh_list(self,
                   host_list=None,
                   remote_user=None,
                   remote_pass=None,
                   sudo=False,
                   sudo_user=None,
                   sudo_pass=None):
        '''
        Get virsh list --state-running
        <TODO>: Add an options argument for different options to
        collect the virsh list output. Need a fix to  rex module
        tabular before that.
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
            module_args="virsh list --state-running",
            sudo=sudo,
            sudo_user=sudo_user,
            sudo_pass=sudo_pass)

        virsh_result = None

        fields = ["Id", "Name", "state"]

        if result['contacted'].keys():
            virsh_result = {}
            for node in result['contacted'].keys():
                nodeobj = result['contacted'][node]
                jsonoutput = rex.parse_tabular_string(nodeobj['stdout'],
                                                      fields)
                virsh_result[node] = {}
                virsh_result[node]['result'] = jsonoutput

        return virsh_result

    def virsh_per_domain_info(self,
                              **kwargs):
        '''
        Get per domain stats from each hosts passed as hostlist.
        '''
        host_list = kwargs.get('host_list', self.host_list)
        remote_user = kwargs.get('remote_user', self.remote_user)
        remote_pass = kwargs.get('remote_pass', self.remote_pass)
        sudo = kwargs.get('sudo', self.sudo)
        sudo_user = kwargs.get('sudo_user', self.sudo_user)
        sudo_pass = kwargs.get('sudo_pass', self.sudo_pass)

        result, failed_hosts = self.runner.ansible_perform_operation(
            host_list=host_list,
            remote_user=remote_user,
            remote_pass=remote_pass,
            module="command",
            module_args="virsh list",
            sudo=sudo,
            sudo_user=sudo_user,
            sudo_pass=sudo_pass)

        virsh_result = None

        fields = ["Id", "Name", "state"]

        if result['contacted'].keys():
            virsh_result = {}
            for node in result['contacted'].keys():
                nodeobj = result['contacted'][node]
                jsonoutput = rex.parse_tabular_string(nodeobj['stdout'],
                                                      fields)
                virsh_result[node] = {}
                virsh_result[node]['result'] = jsonoutput

        print virsh_result


        return virsh_result


