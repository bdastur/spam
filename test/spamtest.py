#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import spam.ansirunner
import spam.plugins.virsh as virsh
import yaml
import pprint


class FileHandler(object):
    '''
    Class handles reading the setup yaml file
    '''
    def __init__(self, filename="./setup.yaml"):
        self.yamlfile = filename
        self.parsed = None
        try:
            fhandle = open(self.yamlfile)
        except IOError:
            print "Failed to read %s" % self.yamlfile
            return

        try:
            self.parsed = yaml.safe_load(fhandle)
        except yaml.parser.ParserError as parse_err:
            print "Failed to parse %s [%s] " % (self.yamlfile, parse_err)
            return


    def get_parsed_data(self, keys):
        '''
        Given a list of keys, get the parsed data.
        '''
        if not isinstance(keys, list):
            print "Expected a list of keys"
            msg = """ Example:
                Given a yaml construct:
                    SERVERS:
                        server1:
                            ssh_ip: 1.1.1.1
                If looking for ssh_ip for server1, the keys would
                be ["SERVERS", "server1", "ssh_ip"]
                """
            print msg
            return None

        parsed = self.parsed
        for key in keys:
            parsed = parsed.get(key)

        return parsed

    def get_server_ssh_ips(self, role=None):
        '''
        Return a list of server ssh ips for a specific role.
        if role is None, return all
        '''
        serveriplist = []
        servers = self.get_parsed_data(["SERVERS"])
        for server in servers:
            serveriplist.append(server['ssh_ip'])

        return serveriplist


class SPAMUT(unittest.TestCase):
    '''
    Main unit test class.
    '''
    def __init__(self, *args, **kwargs):
        '''
        Initialize UT.
        '''
        super(SPAMUT, self).__init__(*args, **kwargs)

    def setUp(self):
        self.fhandler = FileHandler()
        self.username = self.fhandler.get_parsed_data(["USERNAME"])
        self.password = self.fhandler.get_parsed_data(["PASSWORD"])
        self.serveriplist = self.fhandler.get_server_ssh_ips()

    def test_ping(self):
        print "basic test"
        print self.username
        print self.serveriplist
        runner = spam.ansirunner.AnsibleRunner()
        result, failed_hosts = runner.ansible_perform_operation(
            host_list=self.serveriplist,
            remote_user=self.username,
            remote_pass=self.password,
            sudo=False,
            sudo_pass=None,
            sudo_user=None,
            module="ping")

    def test_virsh_version(self):
        virshrunner = virsh.Virsh()
        virsh_result = virshrunner.virsh_version(
            host_list=self.serveriplist,
            remote_user=self.username,
            remote_pass=self.password,
            sudo=True,
            sudo_pass=self.password,
            sudo_user='root')

        self.failUnless(virsh_result is not None)
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(virsh_result)

    def test_virsh_version_2(self):
        virshrunner = virsh.Virsh(
            host_list=self.serveriplist,
            remote_user=self.username,
            remote_pass=self.password,
            sudo=True,
            sudo_pass=self.password,
            sudo_user='root')

        virsh_result = virshrunner.virsh_version(sudo=True)
        self.failUnless(virsh_result is not None)
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(virsh_result)

    def test_basic1(self):
        print "basic1 test"
        print self.username

