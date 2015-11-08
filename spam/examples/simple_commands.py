#!/usr/bin/env python
# -*- coding: utf-8 -*-


import ansirunner


def execute_ping():
    '''
    Execute ls on some hosts
    '''
    runner = ansirunner.AnsibleRunner()
    host_list = ["10.163.41.4"]
    remote_user = "root"
    result, failed_hosts = runner.ansible_perform_operation(
        host_list=host_list,
        remote_user=remote_user,
        module="ping")

    print result, failed_hosts

def main():
    '''
    Simple examples
    '''
    execute_ping()

if __name__ == '__main__':
    main()
