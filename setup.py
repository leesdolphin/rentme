from setuptools import find_packages, setup

setup(
    name='rentme',
    version='',
    packages=find_packages(),
    url='',
    license='',
    author='lee',
    author_email='',
    description='',
    include_package_data=True,
    install_requires=['django', 'celery', 'django_celery_results',
                      'django_celery_beat', 'aiohttp', 'cchardet', 'aiodns', 'psycopg2']
)
