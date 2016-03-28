#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from ansible.utils.vault import VaultEditor


class AnsiVault(object):
    '''
    A python wrapper for Ansible Vault
    '''
    HEADER = '$ANSIBLE_VAULT'

    def __init__(self):
        print "init"
        self.vault_password = os.environ.get("PYANSI_VAULT_PASSWORD", None)

    def is_file_encrypted(self, filename):
        '''
        Given a file. Check if it is already encrypted.
        '''
        if not os.path.exists(filename):
            print "Invalid filename %s. Does not exist" % filename
            return False

        fhandle = open(filename, "rb")
        data = fhandle.read()
        fhandle.close()

        if data.startswith(AnsiVault.HEADER):
            return True
        else:
            return False

    def encrpyt_file(self, filename):
        '''
        Encrypt File
        Args:
            filename: Pass the filename to encrypt.
        Returns:
            No return.
        '''
        if not os.path.exists(filename):
            print "Invalid filename %s. Does not exist" % filename
            return

        if self.vault_password is None:
            print "ENV Variable PYANSI_VAULT_PASSWORD not set"
            return

        if self.is_file_encrypted(filename):
            # No need to do anything.
            return

        cipher = 'AES256'
        vaulteditor = VaultEditor(cipher, self.vault_password, filename)
        vaulteditor.encrypt_file()

    def decrypt_file(self, filename):
        '''
        Decrypt File
        Args:
            filename: Pass the filename to encrypt.
        Returns:
            No return.
        '''
        if not os.path.exists(filename):
            print "Invalid filename %s. Does not exist" % filename
            return

        if self.vault_password is None:
            print "ENV Variable PYANSI_VAULT_PASSWORD not set"
            return

        if not self.is_file_encrypted(filename):
            # No need to do anything.
            return

        cipher = 'AES256'
        vaulteditor = VaultEditor(cipher, self.vault_password, filename)
        vaulteditor.decrypt_file()


