import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='mini-backend',
    version='1.0.0',
    description='Long Project',
    url='https://github.com/digvijay18/dehaat.git',
    author='Digvijay Sisodia',
    install_requires=[
        'amqp==1.4.9',
        'anyjson==0.3.3',
        'billiard==3.3.0.23',
        'celery==3.1.26.post2',
        'configparser==4.0.2',
        'contextlib2==0.6.0.post1',
        'Django==1.11.29',
        'django-celery==3.3.1',
        'django-redis-cache==2.1.1',
        'djangorestframework==3.9.4',
        'future==0.18.2',
        'importlib-metadata==1.7.0',
        'kombu==3.0.37',
        'pathlib2==2.3.5',
        'psycopg2==2.8.5',
        'python-dateutil==2.8.1',
        'pytz==2020.1',
        'redis==3.5.3',
        'scandir==1.10.0',
        'six==1.15.0',
        'vine==1.3.0',
        'zipp==1.2.0'
    ]
)