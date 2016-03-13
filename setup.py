# Plie Setup file
from setuptools import setup

setup(
    name='plie',
    packages=['plie'],
    version='0.2.0',
    desciption='A TUI interface library built upon Blessed',
    long_description=open('README.rst').read(),
    author='Jessie Wincek',
    url='https://github.com/jbwincek/Plie',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 1 - Planning',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Natural Language :: English',
    ],
    keywords='TUI Library terminal',
    install_requires=[
        'blessed',
    ],
)