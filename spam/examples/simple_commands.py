#!/usr/bin/env python
# -*- coding: utf-8 -*-


import spam.ansirunner
import spam.plugins.rados as rados

host_list = ["11.111.11.1", "11.113.11.1", "11.111.11.13"]
remote_user = "wwot"
remote_pass = "wwwwwwwwww3"

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
    result = rados_handle.rados_df(host_list=["10.163.41.4"],
                                   remote_user=remote_user,
                                   remote_pass=remote_pass)

    #result, failed_hosts = rados_handle.perform_operation(
    #    host_list=["10.163.41.4"],
    #    remote_user=remote_user,
    #    remote_pass=remote_pass,
    #    cmd="rados df")
    print "RESULTS: ", result['contacted']['10.163.41.4']['parsed_results']



def main():
    '''
    Simple examples
    '''
    execute_ping()
    #execute_ls()
    #execute_rados_df()
    execute_rados_df2()


if __name__ == '__main__':
    main()
