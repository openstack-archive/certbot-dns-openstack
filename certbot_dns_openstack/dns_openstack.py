# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import logging

import zope.interface

from certbot import interfaces
from certbot import errors
from certbot.plugins import dns_common

from openstack.config import loader
from openstack import connection

LOG = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for OpenStack

    This Authenticator uses the OpenStack v2 DNS API to fulfill a
    dns-01 challenge.
    """

    description = 'Obtain certificates using a DNS TXT record.'
    ttl = 60

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=30)
        add('config', help='OpenStack Client Config file.')
        add('cloud', help='OpenStack to use.')

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return 'This plugin configures a DNS TXT record to respond to a ' + \
               'dns-01 challenge using the OpenStack DNS API.'

    def _setup_credentials(self):
        config_file = self.conf('config') or ''
        config = loader.OpenStackConfig(
            config_files=loader.CONFIG_FILES + [config_file])
        self.cloud = connection.Connection(
            config=config.get_one(
                self.conf('cloud')
            )
        )

    def _perform(self, domain, validation_name, validation):
        domain_name_guesses = dns_common.base_domain_name_guesses(domain)
        for domain in domain_name_guesses:
            self.zone = self.cloud.get_zone(domain + '.')
            if self.zone is not None:
                break
        if self.zone is None:
            raise errors.PluginError(
                'Unable to determine zone identifier for {0} using '
                'zone names: {1}'.format(domain, domain_name_guesses))
        self.recordset = self.cloud.create_recordset(
            self.zone['id'], validation_name + '.', "TXT", [validation])

    def _cleanup(self, domain, validation_name, validation):
        if getattr(self, 'recordset', False):
            self.cloud.delete_recordset(
                self.zone['id'], self.recordset['id'])
