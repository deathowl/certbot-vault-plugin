"""Vault Let's Encrypt installer plugin."""

from __future__ import print_function

import os
import logging

import zope.interface

import hvac

from certbot import interfaces
from certbot.plugins import common


logger = logging.getLogger(__name__)

class Installer(common.Plugin):
    zope.interface.implements(interfaces.IInstaller)
    zope.interface.classProvides(interfaces.IPluginFactory)

    description = "Vault Cert Installer"

    @classmethod
    def add_parser_arguments(cls, add):
        add("vault-token", default=os.getenv('VAULT_TOKEN'),
            help="CloudFront distribution id")
        add("vault-url", default=os.getenv('VAULT_URL'),
            help="CloudFront distribution id")

    def __init__(self, *args, **kwargs):
        super(Installer, self).__init__(*args, **kwargs)
        self.hvac_client = hvac.Client(self.conf('vault-url'), token=self.conf('vault-token'))



    def prepare(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return ""

    def get_all_names(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def deploy_cert(self, domain, cert_path, key_path, chain_path, fullchain_path):
        """
        Upload Certificate to Vault
        """

        name = "certificates/le-%s" % domain
        body = open(cert_path).read()
        key = open(key_path).read()
        chain = open(chain_path).read()

        self.hvac_client.write(path=name, body=body, key=key, chain=chain)

    def enhance(self, domain, enhancement, options=None):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def supported_enhancements(self):  # pylint: disable=missing-docstring,no-self-use
        return []  # pragma: no cover

    def get_all_certs_keys(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def save(self, title=None, temporary=False):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def rollback_checkpoints(self, rollback=1):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def recovery_routine(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def view_config_changes(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def config_test(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def restart(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover