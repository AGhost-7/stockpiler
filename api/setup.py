from setuptools import setup, find_packages

setup(
    name='api',
    packages=find_packages(),
    version='0.0',
    install_requires=[
        'sqlalchemy==1.1.14',
        'flask==0.12.2',
        'bcrypt==3.1.0',
        'Flask-Mail==0.9.1',
        'flask-sqlalchemy==2.2',
        'pymysql==0.7.11',
        'Faker==0.8.3'
    ],
    extras_require={
        'dev': [
            'pytest==3.2.2',
            'requests==2.18.4'
        ]
    },
    scripts=['bin/api', 'bin/api_create_tables']
)
