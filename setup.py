from io import open

from setuptools import find_packages, setup

with open('tsu/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

readme_file="README.md"

with open(readme_file) as f:
    readme = f.read()

REQUIRES = ['docopt', 'wrapt']

setup(
    name='tsu',
    version=version,
    description='A su wrapper for Termux',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Cswl coldwind',
    author_email='cswl@gmail.com',
    maintainer='Cswl coldwind',
    maintainer_email='cswl@gmail.com',
    url='https://github.com/_/tsu',
    license='MIT',

    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    install_requires=REQUIRES,
    tests_require=['coverage', 'pytest'],

    entry_points={ 'console_scripts'
 : [ 'tsu=tsu.main:cli' ]},


    packages=find_packages()
)
