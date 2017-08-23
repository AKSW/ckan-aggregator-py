"""
    First import the necessary PackageCache class (opendataleipzig in this case).
    To see all available PackageCache class simple use find tool:
    find . -name package_cache.py
"""
from ckanaggregatorpy.opendataleipzig.package_cache import PackageCache

"""
    We initialize the class and request package list to see if API requests
    are allowed.
"""
packageCache = PackageCache()
pkgList = packageCache.getPackageList()
print("Leipzig Open Data portal contains {} number of packages.".format(len(pkgList)))

"""
    The next step is to "update" packages. This will scrape all the packages from CKAN
    and save them to the data folder.
"""
print("Updating the local package cache...")
packageCache.updatePackages()

"""
    Now we have the local cache in place we can filter the RDF packages only.
"""
rdfPackages = packageCache.getRdfPackagesRdfResourcesOnly()
print("Leipzig Open Data portal contains {} packages, which contain RDF data".format(len(rdfPackages)))

"""
    Each of the rdf package in rdfPackages list contains the metadata from CKAN
"""
import pprint
pprinter = pprint.PrettyPrinter()
print("Showing metadata from CKAN for the first RDF package")
pprinter.pprint(rdfPackages[0])
