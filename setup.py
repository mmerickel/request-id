from setuptools import setup, find_packages

def readfile(name):
    with open(name) as f:
        return f.read()

readme = readfile('README.rst')
changes = readfile('CHANGES.rst')

install_requires = [
    'WebOb',
]

tests_require = [
    'pytest',
    'pytest-catchlog',
    'pytest-cov',
    'WebTest',
]

setup(
    name='request-id',
    version='0.3.1',
    description='Attach a unique identifier to every WSGI request.',
    long_description=readme + '\n\n' + changes,
    url='https://github.com/mmerickel/request_id',
    author='Michael Merickel',
    author_email='pylons-discuss@googlegroups.com',
    keywords='wsgi unique identifier tracing correlation',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
    ],
    packages=find_packages('src', exclude=['tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    install_requires=install_requires,
    extras_require={
        'testing': tests_require,
    },
    test_suite='tests',
    entry_points={
        'paste.filter_app_factory': [
            'main = request_id:make_filter',
        ],
    },
)
