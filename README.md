ckan-aggregator-py
==================

ckan-aggregator-py scrapes CKAN metadata stores and can specifically filter RDF datasets.
Implemented scrapers are (can be extended, read further):
* [data.gov](http://catalog.data.gov)
* [datahub.io](http://datahub.io)
* [opencanada](http://open.canada.ca/data/en/)
* [publicdata.eu](http://publicdata.eu/)

This repository should be viewed as a toolbox, which needs to be extended to be able to serve a particular use case.
The author used the application to scrape RDF datasets and load it into [LODStats](http://lodstats.aksw.org/) for further processing.

Installation
==================

Given that you have [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/) installed, execute the following commands:
```bash
mkvirtualenv aggregator-py
cdvirtualenv
mkdir src && cd src
git clone git@github.com:dice-group/ckan-aggregator-py.git && cd ckan-aggregator-py
```

This will create Python virtual environment called *aggregator-py* and clone [ckan-aggregator-py](https://github.com/dice-group/ckan-aggregator-py) into src/ckan-aggregator-py in the created virtual env.

Configuration
==================

To create the necessary folders you will need to run init.sh script:
```
./init.sh
```

This will create the data folder with necessary subfolders. The scraped data will be stored there.

```
data
├── csvresources
│   └── propertymatchingdata
├── datagov
│   ├── packages
│   ├── pages
│   └── rdfPackages
├── datahubio
│   ├── packages
│   └── rdfPackages
├── opendataleipzig
│   ├── packages
│   └── rdfPackages
└── pdeu
    ├── packages
    └── rdfPackages
```

Then install the necessary dependencies:
```
pip install -r requirements.txt
```

By default *ckan-aggregator-py* access CKAN without API key.
If you want to have more requests to CKAN endpoint than an average user, it is a good idea to register on a CKAN instance and use API key.
To configure, for example, API key for datahub.io, simply override \_\_init\_\_.py with example-key file as follows:
```
cp ckanaggregatorpy/datahubio/__init__.py-example-key ckanaggregatorpy/datahubio/__init__.py
```
Then edit new init file in your favorite editor.

Usage
==================

Here we demonstrate usage of *ckan-aggregator-py* for scraping Open Leipzig data portal.
For this example, we provide [open-leipzig.py](./open-leipzig.py) script.
Please read inline comments for further pointers.
