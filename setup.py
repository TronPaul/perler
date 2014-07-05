import os
import sys
from setuptools import setup
from setuptools import find_packages

version = '0.0.1-SNAPSHOT'

install_requires = ['Pillow']

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='perler',
    version=version,
    description="image to perler bead conversion",
    long_description=read('README.rst'),
    classifiers=[
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='perler',
    author='Mark McGuire',
    author_email='mark.b.mcg@gmail.com',
    url='https://github.com/TronPaul/perler/',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)
