#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SPAM Rados Module
"""

import spam.ansirunner

class Rados(object):
    """
    SPAM Rados class
    """
    def __init__(self):
        """
        Initialize Rados class.
        """
        self.runner = spam.ansirunner.AnsibleRunner()

    def perform_operation(self,
                          host_list=None,
                          remote_user=None,
                          remote_pass=None,
                          cmd="rados --help"):
        """
        Execute Rados operations.
        """
        print "BRD: here 1"

        result, failed_hosts = self.runner.ansible_perform_operation(
            host_list=host_list,
            remote_user=remote_user,
            remote_pass=remote_pass,
            module="command",
            module_args=cmd)

        return (result, failed_hosts)



