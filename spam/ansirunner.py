#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AnsibleRunner:

INTRO:

USAGE:

"""

import ansible.runner


class AnsibleRunner(object):
    '''
    Ansible Runner Wrapper class.
    '''
    def __init__(self, host_list=None, remote_user=None):
        '''
        Initialize AnsibleRunner.
        '''
        self.host_list = host_list
        self.remote_user = remote_user

    def validate_host_parameters(self, host_list, remote_user):
        '''
        Validate and set the host list and remote user parameters.
        '''
        if host_list is None:
            host_list = self.host_list

        if remote_user is None:
            remote_user = self.remote_user

        if host_list is None or remote_user is None:
            print "Host list [%s], remote user [%s] are required" % \
                  (host_list, remote_user)
            return (None, None)

        return (host_list, remote_user)

    def validate_results(self, results, checks=None):
        '''
        Valdiate results from the Anisble Run.
        '''
        results['status'] = 'PASS'
        failed_hosts = []

        ###################################################
        # First validation is to make sure connectivity to
        # all the hosts was ok.
        ###################################################
        if results['dark']:
            print "Host connectivity issues on %s",
            results['dark'].keys()
            failed_hosts.append(results['dark'].keys())
            results['status'] = 'FAIL'

        ##################################################
        # Now look for status 'failed'
        ##################################################
        for node in results['contacted'].keys():
            if 'failed' in results['contacted'][node]:
                if results['contacted'][node]['failed'] is True:
                    results['status'] = 'FAIL'

        #################################################
        # Check for the return code 'rc' for each host.
        #################################################
        for node in results['contacted'].keys():
            rc = results['contacted'][node].get('rc', None)
            if rc is not None and rc != 0:
                print "Operation 'return code' %s on host %s" % \
                    (results['contacted'][node]['rc'], node)
                failed_hosts.append(node)
                results['status'] = 'FAIL'

        ##################################################
        # Additional checks. If passed is a list of key/value
        # pairs that should be matched.
        ##################################################
        if checks is None:
            #print "No additional checks validated"
            return results, failed_hosts

        for check in checks:
            key = check.keys()[0]
            value = check.values()[0]
            for node in results['contacted'].keys():
                if key in results['contacted'][node].keys():
                    if results['contacted'][node][key] != value:
                        failed_hosts.append(node)
                        results['status'] = 'FAIL'

        return (results, failed_hosts)

    def ansible_perform_operation(self,
                                  host_list=None,
                                  remote_user=None,
                                  remote_pass=None,
                                  module=None,
                                  complex_args=None,
                                  module_args='',
                                  environment=None,
                                  check=False,
                                  sudo=False,
                                  sudo_user=None,
                                  sudo_pass=None,
                                  forks=20):
        '''
        Perform any ansible operation.
        '''
        (host_list, remote_user) = \
            self.validate_host_parameters(host_list, remote_user)
        if (host_list, remote_user) is (None, None):
            return None

        if module is None:
            print "ANSIBLE Perform operation: No module specified"
            return None

        runner = ansible.runner.Runner(
            module_name=module,
            host_list=host_list,
            remote_user=remote_user,
            remote_pass=remote_pass,
            module_args=module_args,
            complex_args=complex_args,
            environment=environment,
            check=check,
            sudo=sudo,
            sudo_user=sudo_user,
            sudo_pass=sudo_pass,
            forks=forks)

        results = runner.run()

        results, failed_hosts = self.validate_results(results)
        if results['status'] != 'PASS':
            print "ANSIBLE: [%s] operation failed [%s] [hosts: %s]" % \
                (module, complex_args, failed_hosts)

        return results, failed_hosts

    def ansible_get_dark_hosts(self,
                               ansible_result):
        '''
        Given the ansible result object, return the list of
        hosts that could not be contacted
        '''
        if not ansible_result['dark']:
            return []

        return ansible_result['dark'].keys()




