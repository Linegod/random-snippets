# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    author: Unknown (!UNKNOWN) (modified by J.P. Pasnak, CD)
    name: syslog_json_splunk_format
    type: notification
    requirements:
      - whitelist in configuration
    short_description: sends JSON events to syslog in a format suitable for Splunk
    description:
      - This plugin logs ansible-playbook and ansible runs to a syslog server in JSON format suitable for Splunk
      - This plugin has been adapted from the the syslog_json plugin - https://github.com/ansible-collections/community.general/blob/main/plugins/callback/syslog_json.py
      - The syslog msg information has been adjusted to be key=value pairs
      - The task name has been added to the logged information
      - Before Ansible 2.9 only environment variables were available for configuration
    options:
      server:
        description: syslog server that will receive the event
        env:
        - name: SYSLOG_SERVER
        default: localhost
        ini:
          - section: callback_syslog_json_splunk_format
            key: syslog_server
      port:
        description: port on which the syslog server is listening
        env:
          - name: SYSLOG_PORT
        default: 514
        ini:
          - section: callback_syslog_json_splunk_format
            key: syslog_port
      facility:
        description: syslog facility to log as
        env:
          - name: SYSLOG_FACILITY
        default: user
        ini:
          - section: callback_syslog_json_splunk_format
            key: syslog_facility
      setup:
        description: Log setup tasks.
        env:
          - name: ANSIBLE_SYSLOG_SETUP
        type: bool
        default: true
        ini:
          - section: callback_syslog_json_splunk_format
            key: syslog_setup
        version_added: 4.5.0
'''

import os
import json

import logging
import logging.handlers

import socket

from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    """
    logs ansible-playbook and ansible runs to a syslog server in json format
    """

    CALLBACK_VERSION = 1.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'syslog_json_splunk_format'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):

        super(CallbackModule, self).__init__()

    def set_options(self, task_keys=None, var_options=None, direct=None):

        super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)

        syslog_host = self.get_option("server")
        syslog_port = int(self.get_option("port"))
        syslog_facility = self.get_option("facility")

        self.logger = logging.getLogger('ansible logger')
        self.logger.setLevel(logging.DEBUG)

        self.handler = logging.handlers.SysLogHandler(
            address=(syslog_host, syslog_port),
            facility=syslog_facility
        )
        self.logger.addHandler(self.handler)
        self.hostname = socket.gethostname().split('.', 1)[0]

    def v2_runner_on_failed(self, result, ignore_errors=False):
        res = result._result
        hostname = result._host.get_name()
        task_name = result._task.name
        self.logger.error('self_hostname="%s" ansible-command="task" execution="FAILED" hostname="%s" task="%s" message="%s"', self.hostname, hostname, task_name, self._dump_results(res))

    def v2_runner_on_ok(self, result):
        res = result._result
        hostname = result._host.get_name()
        task_name = result._task.name
        if result._task.action != "gather_facts" or self.get_option("setup"):
            self.logger.info('self_hostname="%s" ansible-command="task" execution="OK" hostname="%s" task="%s" message="%s"', self.hostname, hostname, task_name, self._dump_results(res))

    def v2_runner_on_skipped(self, result):
        hostname = result._host.get_name()
        task_name = result._task.name
        self.logger.info('self_hostname="%s" ansible-command="task" execution="SKIPPED" hostname="%s" message="%s"', self.hostname, hostname, task_name, 'skipped')

    def v2_runner_on_unreachable(self, result):
        res = result._result
        hostname = result._host.get_name()
        task_name = result._task.name
        self.logger.error('self_hostname="%s" ansible-command="task" execution="UNREACHABLE" hostname="%s" message="%s"', self.hostname, hostname, task_name, self._dump_results(res))

    def v2_runner_on_async_failed(self, result):
        res = result._result
        hostname = result._host.get_name()
        task_name = result._task.name
        jid = result._result.get('ansible_job_id')
        self.logger.error('self_hostname="%s" ansible-command="task" execution="FAILED" hostname="%s" message="%s"', self.hostname, hostname, task_name, self._dump_results(res))

    def v2_playbook_on_import_for_host(self, result, imported_file):
        hostname = result._host.get_name()
        self.logger.info('self_hostname="%s" ansible-command="playbook" execution="IMPORTED" hostname="%s" message="imported file %s"', self.hostname, hostname, imported_file)

    def v2_playbook_on_not_import_for_host(self, result, missing_file):
        hostname = result._host.get_name()
        self.logger.info('self_hostname="%s" ansible-command="playbook" execution="NOT IMPORTED" hostname="%s" message="missing file %s"', self.hostname, hostname, missing_file)
