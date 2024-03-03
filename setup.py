from setuptools import setup, find_packages
setup(
name='pytest-in-robotframework',
version='0.0.13',
author='Petr Kus',
author_email='petrkus@email.cz',
description="The extension enables easy execution of pytest tests within the Robot Framework environment.",
long_description=open('README.md').read(),
long_description_content_type='text/markdown', # Robot Framework use text/x-rst - there is obviously support for RF Examples.
install_requires=[
        'pytest',
        'robotframework>=6.1',
        'decorator',
        'pytest-is-running'
    ], # are not shown at PyPi?
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
"Framework :: Pytest",
"Framework :: Robot Framework",
"Framework :: Robot Framework :: Library",
"Framework :: Robot Framework :: Tool",
"Topic :: Software Development :: Testing",
"Topic :: Software Development :: Quality Assurance"
],
python_requires='>=3.8',
)