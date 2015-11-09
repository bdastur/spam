#!/usr/bin/env python
# -*- coding: utf-8 -*-


import spam.ansirunner
import spam.plugins.rados as rados


host_list = ["11.111.11.1", "12.122.21.2", "12.123.21.22"]
remote_user = "eoot"
remote_pass = "eeeeeeeeee3"


def execute_ping():
    '''
    Execute ls on some hosts
    '''
    runner = spam.ansirunner.AnsibleRunner()
    result, failed_hosts = runner.ansible_perform_operation(
        host_list=host_list,
        remote_user=remote_user,
        remote_pass=remote_pass,
        module="ping")

    print result, failed_hosts
    dark_hosts = runner.ansible_get_dark_hosts(result)
    print "dark hosts: ", dark_hosts


def execute_ls():
    '''
    Execute any adhoc command on the hosts.
    '''
    runner = spam.ansirunner.AnsibleRunner()
    result, failed_hosts = runner.ansible_perform_operation(
        host_list=host_list,
        remote_user=remote_user,
        remote_pass=remote_pass,
        module="command",
        module_args="ls -1")

    print "Result: ", result


def execute_rados_df():
    runner = spam.ansirunner.AnsibleRunner()
    result, failed_hosts = runner.ansible_perform_operation(
        host_list=host_list,
        remote_user=remote_user,
        remote_pass=remote_pass,
        module="command",
        module_args="rados df")

    print "Result: ", result


def execute_rados_df2():
    rados_handle = rados.Rados()
    result, failed_hosts = rados_handle.perform_operation(
        host_list=["11.111.11.1"],
        remote_user=remote_user,
        remote_pass=remote_pass,
        cmd="rados df")

    print "Rados result: ", result


def main():
    '''
    Simple examples
    '''
    execute_ping()
    execute_ls()
    execute_rados_df()
    execute_rados_df2()


if __name__ == '__main__':
    main()
