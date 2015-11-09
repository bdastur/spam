#!/usr/bin/env python
# -*- coding: utf-8 -*-


import ansirunner


def execute_ping():
    '''
    Execute ls on some hosts
    '''
    runner = ansirunner.AnsibleRunner()
    host_list = ["11.111.11.1", "11.122.22.2", "12.133.31.32"]
    remote_user = "3444"
    remote_pass = "4eeeeeel1e3"
    result, failed_hosts = runner.ansible_perform_operation(
        host_list=host_list,
        remote_user=remote_user,
        remote_pass=remote_pass,
        module="ping")

    print result, failed_hosts
    dark_hosts = runner.ansible_get_dark_hosts(result)
    print "dark hosts: ", dark_hosts


def main():
    '''
    Simple examples
    '''
    execute_ping()

if __name__ == '__main__':
    main()
