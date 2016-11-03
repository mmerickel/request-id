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
    name='request-id',
    version='0.2.1',
    description='Attach a unique identifier to every WSGI request.',
    long_description=README + '\n\n' + CHANGES,
    url='https://github.com/mmerickel/request_id',
    author='Michael Merickel',
    author_email='michael@merickel.org',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
    ],
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'paste.filter_app_factory': [
            'main = request_id:make_filter',
        ],
    },
)
