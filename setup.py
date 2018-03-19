from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))



setup(
    name='certbot-vault',  # Required
    version='0.1.1',  # Required
    description='Certbot plugin to store certificates in Hashicorp Vault',
    url='https://github.com/deathowl/certbot-vault-plugin',  # Optional

    author='Balint Csergo',  # Optional

    author_email='<bcsergo@emarsys.com>',  # Optional

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='certbot vault',  # Optional

    packages=find_packages(),  # Required

    install_requires=[
        'acme==0.22.0',
        'certbot>=0.22.0',
        'PyOpenSSL',
        'setuptools',
        'zope.component==4.4.1',
        'zope.event==4.1.0',
        'zope.interface==4.4.3',
        'hvac'
    ],
    include_package_data=True,
    entry_points={
        'letsencrypt.plugins': [
            'vault = certbot_vault.plugin:Installer',
        ],
    },



)
