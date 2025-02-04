#!/usr/bin/env python

import configparser
import os
import setuptools

with open("README.md", "r") as rf:
    long_description = rf.read()

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), "chord_metadata_service", "package.cfg"))

setuptools.setup(
    name=config["package"]["name"],
    version=config["package"]["version"],

    python_requires=">=3.6",
    install_requires=[
        "bento_lib[django]==2.3.0",
        "Django>=2.2.20,<3.0",
        "django-autocomplete-light==3.8.2",
        "django-cors-headers>=3.7,<3.8",
        "django-filter>=2.4,<3.0",
        "djangorestframework>=3.11.2,<3.12",
        "djangorestframework-camel-case>=1.2.0,<2.0",
        "django-rest-swagger==2.2.0",
        "elasticsearch==7.8.0",
        "fhirclient>=3.2,<4.0",
        "isodate==0.6.0",
        "jsonschema>=3.2,<4.0",
        "psycopg2-binary>=2.8,<2.9",
        "PyJWT[crypto]==2.4.0",
        "python-dateutil>=2.8,<3.0",
        "python-dotenv==0.14.0",
        "rdflib==6.0.1",
        "requests>=2.25.1,<3.0",
        "requests-unixsocket>=0.2.0,<0.3.0",
        "rfc3987==1.3.8",
        "strict-rfc3339==0.7",
        "tabulate>=0.8.9,<0.9",
        "uritemplate>=3.0,<4.0",
    ],

    author=config["package"]["authors"],

    description="An implementation of a clin/pheno metadata store for the Bento platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=setuptools.find_packages(),
    include_package_data=True,

    url="https://github.com/bento-platform/katsu",
    license="LGPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent"
    ]
)
