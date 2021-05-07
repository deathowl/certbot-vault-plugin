from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='certbot-vault',  # Required
    version='0.3.1',  # Required
    description='Certbot plugin to store certificates in Hashicorp Vault',
    url='https://github.com/emartech/certbot-vault-plugin',  # Optional

    author='Balint Csergo',  # Optional

    author_email='<bcsergo@emarsys.com>',  # Optional

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='certbot vault',  # Optional

    packages=find_packages(),  # Required

    install_requires=[
        'acme==1.9.0',
        'certbot==1.9.0',
        'PyOpenSSL==19.1.0',
        'setuptools',
        'zope.component==4.6.2',
        'zope.event==4.5.0',
        'zope.interface==5.2.0',
        'hvac==0.10.5'
    ],
    include_package_data=True,
    entry_points={
        'letsencrypt.plugins': [
            'vault = certbot_vault.plugin:VaultInstaller',
        ],
    },

)
