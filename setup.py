"""A setuptools based setup module.
"""
import subprocess
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
version = subprocess.run('git describe'.split(' '), capture_output=True, encoding='utf-8').stdout

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as reqs:
    requirements = reqs.read().splitlines()

setup(

    name='git-sentry',  # Required
    version=version,  # Required
    description='GitHub User Access Sentry',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)

    url='https://github.com/dragosdumitrache/git-sentry',  # Optional
    author='Dragos Dumitrache',  # Optional
    author_email='dragos@afterburner.dev',  # Optional

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='git user access management',  # Optional
    packages=find_packages(),  # Required
    python_requires='>=3.7',
    install_requires=requirements,  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'sentry=git_sentry.main.sentry:run_cli',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/dragosdumitrache/git-sentry/issues',
        'Source': 'https://github.com/dragosdumitrache/git-sentry/',
    },
)
