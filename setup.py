import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as fp:
    README = fp.read()
with open(os.path.join(here, 'CHANGES.rst')) as fp:
    CHANGES = fp.read()

install_requires = [
    'WebOb',
]

setup(
    name='request_id',
    version='0.1.0',
    description='Attach a unique identifier to every request.',
    long_description=README + '\n\n' + CHANGES,
    url='https://github.com/mmerickel/request_id',
    license='MIT',
    author='Michael Merickel',
    author_email='michael@merickel.org',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Pyramid',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
    ],
    packages=find_packages(),
    install_requires=install_requires,
)
