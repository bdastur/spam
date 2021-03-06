#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import pyansible.ansirunner
import pyansible.plugins.virsh as virsh
import pyansible.ansivault as ansivault
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
        self.username = os.environ.get("PYANSI_USERNAME", None)
        self.password = os.environ.get("PYANSI_PASSWORD", None)
        self.serveriplist = self.fhandler.get_server_ssh_ips()
        self.virshrunner = virsh.Virsh(
            host_list=self.serveriplist,
            remote_user=self.username,
            remote_pass=self.password,
            sudo=True,
            sudo_pass=self.password,
            sudo_user='root')

    def test_ping(self):
        print "basic test"
        print self.username
        print self.serveriplist
        runner = pyansible.ansirunner.AnsibleRunner()
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

    def test_virsh_version_3(self):
        virshrunner = virsh.Virsh(
            host_list=self.serveriplist,
            remote_user=self.username,
            remote_pass=self.password,
            sudo=True,
            sudo_pass=self.password,
            sudo_user='root')

        cmd = "virsh version"
        virsh_result = virshrunner.execute_virsh_command(cmd=cmd,
                                                         delimiter=":",
                                                         output_type="LRVALUE",
                                                         sudo=True)
        self.failUnless(virsh_result is not None)
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(virsh_result)

    def test_virsh_list(self):
        virshrunner = virsh.Virsh(
            host_list=self.serveriplist,
            remote_user=self.username,
            remote_pass=self.password,
            sudo=True,
            sudo_pass=self.password,
            sudo_user='root')

        virsh_result = virshrunner.virsh_list(sudo=True)
        self.failUnless(virsh_result is not None)
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(virsh_result)

    def test_virsh_list_2(self):

        cmd = "virsh list"
        fields = ["Id", "Name", "state"]
        virsh_result = self.virshrunner.execute_virsh_command(
            cmd=cmd,
            output_type="TABLE",
            fields=fields,
            sudo=True)

        self.failUnless(virsh_result is not None)
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(virsh_result)

    def test_virsh_per_domain_info(self):
        virsh_result = self.virshrunner.virsh_per_domain_info(sudo=True)
        self.failUnless(virsh_result is not None)
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(virsh_result)

    def create_test_file(self, filename):
        '''
        Create a test file
        '''
        fhandle = open(filename, "w")
        fhandle.write("This is a test file")
        fhandle.close()

    def test_encrypt_file(self):
        filename = "/tmp/testfile.txt"
        self.create_test_file(filename)
        vault = ansivault.AnsiVault()
        vault.encrpyt_file(filename)

        # Read the data again after decrypting.
        vault.decrypt_file(filename)

        fhandle = open(filename, "r")
        data = fhandle.read()
        print "data: ", data

        # cleanup after test
        os.remove(filename)

    def test_encrypt_invalid(self):

        #1. File does not exist.
        filename = "/tmp/testinvalid.txt"
        vault = ansivault.AnsiVault()
        vault.encrpyt_file(filename)

        #2. Try encrypting encrypted file.
        filename = "/tmp/testfile.txt"
        self.create_test_file(filename)

        vault = ansivault.AnsiVault()
        vault.encrpyt_file(filename)

        if vault.is_file_encrypted(filename):
            print "File encrypted"

        vault.encrpyt_file(filename)
        vault.encrpyt_file(filename)

        os.remove(filename)

        #3. Try decrypting a non encrypted file.
        filename = "/tmp/testfile.txt"
        self.create_test_file(filename)

        vault = ansivault.AnsiVault()
        vault.decrypt_file(filename)




