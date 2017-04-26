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
    install_requires=[
        'aiodns',
        'aiohttp',
        'bitarray',
        'cchardet',
        'celery',
        'django_celery_beat',
        'django_celery_results',
        'django',
        'ImageHash',
        'psycopg2',
    ],
    entry_points={
        'console_scripts': [
            'rentme = rentme:management_command',
        ],
    }
)
