from setuptools import setup, find_packages

with open('README.md') as fhandle:
    long_description = fhandle.read()


setup(
    name='pyansible',
    version='1.0.0',
    description='A module for interfacing with Ansible Runner and Inventory.',
    long_description=long_description,
    url="https://github.com/bdastur/spam",
    author="Behzad Dastur",
    author_email="bdastur@gmail.com",
    license='Apache Software License',
    classifier=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],

    keywords='ansible',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['rexutil',
                      'MarkupSafe',
                      'jinja2',
                      'PyYAML',
                      'ansible==1.9.4']
)

