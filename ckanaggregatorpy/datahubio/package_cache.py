import os.path

import ckanaggregatorpy.datahubio as datahubio
import ckanaggregatorpy.interfaces

class PackageCache(ckanaggregatorpy.interfaces.PackageCacheInterface):
    cacheFolder = datahubio.cacheFolder
    ckanClient = datahubio.ckanClient
    prefix = "datahubio"
    ckanApiUrl = datahubio.ckanApiUrl

    def __init__(self):
        super(self.__class__, self).__init__()

if __name__ == "__main__":
    packageCache = PackageCache()
    #pkgList = packageCache.getPackageList()
    #packageCache.updatePackages()
    rdfPackages = packageCache.getRdfPackagesRdfResourcesOnly()
    import ipdb; ipdb.set_trace()
