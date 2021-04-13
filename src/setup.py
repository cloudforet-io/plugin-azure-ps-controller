from setuptools import setup, find_packages
 
with open('VERSION', 'r') as f:
    VERSION = f.read().strip()
    f.close()
 
setup(
    name='plugin-azure-power-scheduler-controller',
    version=VERSION,
    description='Azure plugin for power scheduler',
    long_description='Azure plugin for power scheduler which turn on/off given google cloud compute vm',
    url='https://www.spaceone.dev/',
    author='MEGAZONE SpaceONE Team',
    author_email='admin@spaceone.dev',
    license='Apache License 2.0',
    packages=find_packages(),
    install_requires=[
        'spaceone-core',
        'spaceone-api',
        'spaceone-tester',
        'google-auth',
        'google-api-python-client',
        'schematics'
    ],
    zip_safe=False,
)
