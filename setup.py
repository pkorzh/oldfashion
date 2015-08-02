#!/usr/bin/env python
try:
    from setuptools import setup
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install

# Allow trove classifiers in previous python versions
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None


class CustomInstallCommand(install):
    def run(self):
        install.run(self)


def requireModules(moduleNames=None):
    import re
    if moduleNames is None:
        moduleNames = []
    else:
        moduleNames = moduleNames

    commentPattern = re.compile(r'^\w*?#')
    moduleNames.extend(
        filter(lambda line: not commentPattern.match(line),
            open('requirements.txt').readlines()))

    return moduleNames

scripts = [
    'oldfashion=oldfashion_host.command_line:main'
]

setup(
    cmdclass={
        'install': CustomInstallCommand,
    },

    name='oldfashion',
    packages=['oldfashion_host'],
    version='1.0.0',

    author='Platon Korzh',
    author_email='platon@korzh.io',

    description='oldfashion host',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers'
    ],

    install_requires=requireModules([

    ]),

    include_package_data = True,

    entry_points=dict(console_scripts=scripts)
)
