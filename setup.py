from distutils.core import setup

name = 'troia-api-client'
version = '0.1'


setup(
      name=name,
      version=version,
      description='Troia API client',
      install_requires = [
          'requests',
      ],
      packages=["client"],
      )
