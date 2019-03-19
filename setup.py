"""Setup script for package."""
import re
from setuptools import setup, find_packages

VERSION = re.search(r'^VERSION\s*=\s*"(.*)"', open("lemmy/version.py").read(), re.M).group(1)
with open("README.md", "rb") as f:
    LONG_DESCRIPTION = f.read().decode("utf-8")

setup(
    name="lemmy",
    version=VERSION,
    description="Lemmatizer for Danish",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Soren Lind Kristiansen",
    author_email="sorenlind@mac.com",
    url="https://github.com/sorenlind/lemmy/",
    keywords="nlp lemma lemmatizer lemmatiser danish spacy",
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'notebooks': ['pandas', 'jupyter', 'unicodecsv', 'bs4', 'tqdm', 'regex', 'spacy'],
        'dev': [
            'pandas', 'jupyter', 'unicodecsv', 'bs4', 'tqdm', 'regex', 'spacy', 'pylint', 'pycodestyle', 'pydocstyle',
            'yapf', 'pytest', 'tox'
        ],
        'test': ['pytest', 'tox'],
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Danish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic'
    ])
