from setuptools import setup
import sys

if sys.version_info < (3, 6):
    sys.exit('ERROR: Portkey only supports Python 3.6 or above.')

setup(
    name='Portkey',
    version='0.1.0',
    packages=['portkey'],
    url='https://github.com/red8012/portkey',
    license='Apache License 2.0',
    author='Yu-Ann Chen',
    author_email='red8012@gmail.com',
    description='A Python framework for interacting with in-browser DOM via websockets',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6'
    ],
    requires=['websockets', 'werkzeug']
)
