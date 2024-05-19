# setup.py
from setuptools import setup, find_packages

setup(
    name='battery_characterisation_tool',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'pandas',
        'seaborn',
        # Add any other dependencies your package requires
    ],
    author='Zoe Wright',
    author_email='zoe.wright@exeter.ox.ac.uk',
    description='A package for plotting battery characterisation data',
    url='https://github.com/zoehwright/batterycharacterisationtool',  # Replace with your actual URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
