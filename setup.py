from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = [req.strip() for req in f if not req.strip().startswith('#')]

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
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'rentme = rentme:management_command',
        ],
    }
)
