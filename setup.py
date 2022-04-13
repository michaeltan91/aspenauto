from setuptools import setup

setup(name='aspenauto',
      version='1.0',
      description='TU Delft ESS E&I, Aspen Plus Python Interface',
      author='Michael Tan',
      license='Apache Licence 2.0',
      packages=['aspenauto'],
      install_requires = [
          'xlrd',
          'pyexcel',
          'pandas',
          'epynet',
          'openpyxl'
      ],
      zip_safe=False)