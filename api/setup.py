from setuptools import setup, find_packages

setup(
    name='api',
    packages=find_packages(),
    version='0.0',
    install_requires=[
    ],
    extras_require={
    },
    scripts=['bin/api', 'bin/api_create_tables', 'bin/api_test_mail']
)
