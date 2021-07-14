import setuptools
from pos_etf.main import __algoetf_version__

long_description = open("README.md").read()

setuptools.setup(
    name='AlgoETF',
    version=__algoetf_version__,
    url="https://github.com/danmurphy1217/pos-etf",
    entry_points={
        "console_scripts": ['algoetf=pos_etf.main:main']
    },
    description="Enter Description Here",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dan Murphy",
    author_email="danielmurph8@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        "aiohttp==3.7.4.post0",
        "async-timeout==3.0.1",
        "attrs==20.3.0",
        "autopep8==1.5.5",
        "certifi==2020.12.5",
        "cffi==1.14.5",
        "chardet==4.0.0",
        "idna==2.10",
        "msgpack==1.0.2",
        "multidict==5.1.0",
        "prompt-toolkit==1.0.14",
        "py-algorand-sdk==1.4.1",
        "pycodestyle==2.6.0",
        "pycparser==2.20",
        "pycryptodome==3.10.1",
        "pycryptodomex==3.10.1",
        "Pygments==2.9.0",
        "PyInquirer==1.0.3",
        "PyNaCl==1.4.0",
        "regex==2021.7.6",
        "requests==2.25.1",
        "six==1.15.0",
        "toml==0.10.2",
        "typing-extensions==3.7.4.3",
        "urllib3==1.26.3",
        "wcwidth==0.2.5",
        "yarl==1.6.3"
    ],
    python_requires=">= 3.7"
)