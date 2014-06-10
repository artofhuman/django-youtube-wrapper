#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


with open('README.md') as f:
    readme = f.read()

setup(
    name='django-youtube-wrapper',
    version='0.0.1',
    description='Wrapper for youtube',
    long_description=readme,
    author='Pupkov Semen',
    author_email='semen.pupkov@gmail.com',
    url='https://github.com/artofhuman/django-youtube-wrapper',
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    packages=find_packages(),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python 2.7',
        'Programming Language :: Python 3.0',
    )
)
