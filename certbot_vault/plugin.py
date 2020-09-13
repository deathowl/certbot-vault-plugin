"""Vault Let's Encrypt installer plugin."""

from __future__ import print_function

import os
import logging

import zope.interface

import hvac

from certbot import interfaces
from certbot.plugins import common


logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IInstaller)
@zope.interface.provider(interfaces.IPluginFactory)
class VaultInstaller(common.Plugin):
    description = "Vault Cert Installer"

    @classmethod
    def add_parser_arguments(cls, add):
        add("vault-token",
            default=os.getenv('VAULT_TOKEN'),
            help="Vault access token"
        )
        add("vault-addr",
            default=os.getenv('VAULT_ADDR'),
            help="Vault URL"
        )
        add("vault-path",
            default=os.getenv('VAULT_PATH'),
            help="Vault Path"
        )

    def __init__(self, *args, **kwargs):
        super(VaultInstaller, self).__init__(*args, **kwargs)
        self.hvac_client = hvac.Client(self.conf('vault-addr'), token=self.conf('vault-token'))

    def prepare(self):  # pylint: disable=missing-docstring,no-self-use
        """
        Prepare the plugin
        """
        pass  # pragma: no cover

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        """
        Human-readable string to help understand the module
        """
        return (
            "Hashicorp Vault Plugin",
            "Vault: %s Path: %" % (
                self.conf('vault-addr'),
                self.conf('vault-path')
            )
        )

    def get_all_names(self):  # pylint: disable=missing-docstring,no-self-use
        return []

    def deploy_cert(self, domain, cert_path, key_path, chain_path, fullchain_path):
        """
        Upload Certificate to Vault

        :param str domain: domain to deploy certificate file
        :param str cert_path: absolute path to the certificate file
        :param str key_path: absolute path to the private key file
        :param str chain_path: absolute path to the certificate chain file
        :param str fullchain_path: absolute path to the certificate fullchain file (cert plus chain)

        :raises .PluginError: when cert cannot be deployed
        """

        self.hvac_client.renew_token()

        data = {
            'cert': open(cert_path).read(),
            'key': open(key_path).read(),
            'chain': open(fullchain_path).read()
        }

        self.hvac_client.write(
            os.path.join(self.conf('vault-path'), 'data', domain),
            data=data
        )

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
