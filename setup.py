#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='lh-platform-integration-service',
    version='0.0.1',
    description='Leadhub Platform Integration Service',
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(exclude=['doc', 'tests*']),
    install_requires=[
        # 'msgpack-python',
        # 'pymongo',
        # 'pyyaml',
        # 'lh-logging-helpers',
        # 'lh-mongo-queue',
        # 'lh-process-dispatcher',
        # 'lhrpc',
        # 'requests',
        # 'simplejson',
    ],
    entry_points={
        'console_scripts': [
            'lh-platform-integration-service=lh_platform_integration_service:platform_integration_service_main',
        ],
    })
