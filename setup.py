from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(name='duckgoose',
      version='0.1',
      description='Utility functions for the fast ai mooc',
      url='http://github.com/svenski/duckgoose',
      author='Sergiusz Bleja',
      author_email='duckgoose@bleja.org',
      license='MIT',
      long_description=long_description,
      packages=['duckgoose'],
      install_requires=['google-images-download'],
      zip_safe=False)
