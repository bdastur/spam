#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import getpass
import spam.ansirunner
import spam.plugins.rados as rados


def execute_ping(host_list, remote_user, remote_pass,
                 sudo=False, sudo_user=None, sudo_pass=None):
    '''
    Execute ls on some hosts
    '''
    runner = spam.ansirunner.AnsibleRunner()
    result, failed_hosts = runner.ansible_perform_operation(
        host_list=host_list,
        remote_user=remote_user,
        remote_pass=remote_pass,
        sudo=sudo,
        sudo_pass=sudo_pass,
        sudo_user=sudo_user,
        module="ping")

    print result, failed_hosts
    dark_hosts = runner.ansible_get_dark_hosts(result)
    print "dark hosts: ", dark_hosts


def execute_ls(host_list, remote_user, remote_pass):
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


def execute_rados_df(host_list, remote_user, remote_pass):
    runner = spam.ansirunner.AnsibleRunner()
    result, failed_hosts = runner.ansible_perform_operation(
        host_list=host_list,
        remote_user=remote_user,
        remote_pass=remote_pass,
        module="command",
        module_args="rados df")

    print "Result: ", result


def execute_rados_df2(host_list, remote_user, remote_pass):
    rados_handle = rados.Rados()
    result = rados_handle.rados_df(host_list=host_list,
                                   remote_user=remote_user,
                                   remote_pass=remote_pass)

    print "RESULTS: ", result['contacted']



def print_description():
    description = \
        '''
        simple_commands.py.
        Ansible Runner usage examples
        -----------------------------
        ./simple_commands.py  --hosts xyz.com abc.com \
         --username behzad_dastur --askpass --asksudopass
        '''

    return description


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="simple_commands.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=print_description())

    parser.add_argument("--hosts",
                        help="Hosts to execute operations on",
                        nargs='+',
                        required=True)
    parser.add_argument("--username",
                        help="Username for remote hosts",
                        required=True)
    parser.add_argument("--askpass",
                        help="Ansible operation will prompt for user password",
                        action="store_true")
    parser.add_argument("--asksudopass",
                        help="Ansible operation will prompt for sudo password",
                        action="store_true")

    args = parser.parse_args()
    return args


def main():
    '''
    Simple examples
    '''
    args = parse_arguments()
    if args.askpass:
        password = getpass.getpass("Password: ")
    else:
        password = None

    if args.asksudopass:
        sudo = True
        sudo_pass = getpass.getpass("Sudo password[default ssh password]: ")
        if len(sudo_pass) == 0:
            sudo_pass = password
        sudo_user = 'root'
    else:
        sudo = False
        sudo_pass = None
        sudo_user = None

    if not args.username:
        username = getpass.getuser()
    else:
        username = args.username

    host_list = args.hosts
    os.environ["ANSIBLE_HOST_KEY_CHECKING"] = "False"

    execute_ping(host_list, username, password,
                 sudo=sudo, sudo_user=sudo_user, sudo_pass=sudo_pass)
    #execute_ls()
    #execute_rados_df()
    #execute_rados_df2(host_list, username, password)


if __name__ == '__main__':
    main()
