"""Vault Let's Encrypt installer plugin."""

from __future__ import print_function

import os
import logging
import hvac

import zope.interface
import OpenSSL.crypto

from datetime import datetime
from certbot import interfaces
from certbot import errors
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
        add("vault-role-id",
            default=os.getenv('VAULT_ROLE_ID'),
            help='AppRole ID'
        )
        add("vault-secret-id",
            default=os.getenv('VAULT_SECRET_ID'),
            help='AppRole Secret ID'
        )
        add("vault-addr",
            default=os.getenv('VAULT_ADDR'),
            help="Vault URL"
        )
        add("vault-mount",
            default=os.getenv('VAULT_MOUNT'),
            help="Vault Mount Point"
        )
        add("vault-path",
            default=os.getenv('VAULT_PATH'),
            help="Vault Mount Point"
        )

    def __init__(self, *args, **kwargs):
        super(VaultInstaller, self).__init__(*args, **kwargs)
        self.hvac_client = hvac.Client(self.conf('vault-addr'))

        if self.conf('vault-token'):
            self.hvac_client.token = self.conf('vault-token')


        if self.conf('vault-role-id') and self.conf('vault-secret-id'):
            self.hvac_client.auth_approle(self.conf('vault-role-id'), self.conf('vault-secret-id'))

    def prepare(self):  # pylint: disable=missing-docstring,no-self-use
        """
        Prepare the plugin
        """

        if not self.hvac_client.is_authenticated():
            raise errors.PluginError('Not authenticated')

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        """
        Human-readable string to help understand the module
        """
        return (
            "Hashicorp Vault Plugin",
            "Vault: %s" % (
                self.conf('vault-addr'),
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

        cert = open(cert_path).read()

        date_format = "%Y%m%d%H%M%SZ"

        openssl_cert = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM,
            cert
        )

        data = {
            'type': 'urn:scheme:type:certificate',
            'cert': cert,
            'key': open(key_path).read(),
            'chain': open(fullchain_path).read(),
            'serial': openssl_cert.get_serial_number(),
            'life': {
                'issued': int(datetime.strptime(openssl_cert.get_notBefore().decode(), date_format).timestamp()),
                'expires': int(datetime.strptime(openssl_cert.get_notAfter().decode(), date_format).timestamp()),
            }
        }

        domains = []
        ext_count = openssl_cert.get_extension_count()
        for i in range(0, ext_count):
            ext = openssl_cert.get_extension(i)
            if 'subjectAltName' in str(ext.get_short_name()):
                sub = ext._subjectAltNameString()
                for row in [x.strip() for x in sub.split(',')]:
                    if row.startswith('DNS:'):
                        domains.append(row[len('DNS:'):])

        if domains:
            data['domains'] = domains

        self.hvac_client.secrets.kv.v2.create_or_update_secret(
            mount_point=self.conf('vault-mount'),
            path=os.path.join(self.conf('vault-path'), domain),
            secret=data
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
