#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SPAM Rados Module
"""

import spam.ansirunner
import re


class Rados(object):
    """
    SPAM Rados class
    """
    def __init__(self):
        """
        Initialize Rados class.
        """
        self.runner = spam.ansirunner.AnsibleRunner()

    def rados_df(self,
                 host_list=None,
                 remote_user=None,
                 remote_pass=None):
        '''
        Invoked the rados df command and return output to user
        '''
        result, failed_hosts = self.runner.ansible_perform_operation(
            host_list=host_list,
            remote_user=remote_user,
            remote_pass=remote_pass,
            module="command",
            module_args="rados df")

        parsed_result = self.rados_parse_df(result)

        return parsed_result

    def rados_parse_df(self,
                       result):
        '''
        Parse the result from ansirunner module and save it as a json
        object
        '''
        parsed_results = []
        HEADING = r".*(pool name) *(category) *(KB) *(objects) *(clones)" + \
            " *(degraded) *(unfound) *(rd) *(rd KB) *(wr) *(wr KB)"

        HEADING_RE = re.compile(HEADING,
                                re.IGNORECASE)

        dict_keys = ["pool_name", "category", "size_kb", "objects",
                     "clones", "degraded", "unfound", "rd", "rd_kb",
                     "wr", "wr_kb"]

        if result['contacted'].keys():
            for node in result['contacted'].keys():
                df_result = {}
                nodeobj = result['contacted'][node]
                df_output = nodeobj['stdout']
                for line in df_output.splitlines():
                    print "Line: ", line
                    # Skip the heading line.
                    reobj = HEADING_RE.match(line)
                    if not reobj:
                        row = line.split()
                        if len(row) != len(dict_keys):
                            print "line not match: ", line
                            continue

                        key_count = 0
                        for column in row:
                            df_result[dict_keys[key_count]] = column
                            key_count += 1
                        print "df_result: ", df_result
                        parsed_results.append(df_result)

                    nodeobj['parsed_results'] = parsed_results

        return result

