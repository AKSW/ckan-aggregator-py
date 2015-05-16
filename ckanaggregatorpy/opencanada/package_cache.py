import os.path

import ckanaggregatorpy.interfaces
import ckanaggregatorpy.opencanada as opencanada

class PackageCache(ckanaggregatorpy.interfaces.PackageCacheInterface):
    cacheFolder = opencanada.cacheFolder
    ckanClient = opencanada.ckanClient
    prefix = "opencanadaca"
    ckanApiUrl = opencanada.ckanApiUrl
    ckanBaseUrl = opencanada.ckanBaseUrl

    def __init__(self):
        super(self.__class__, self).__init__()

if __name__ == "__main__":
    packageCache = PackageCache()
    #pkgList = packageCache.getPackageList()
    packageCache.updatePackages()
    #rdfPackages = packageCache.getRdfPackages()
    #packageCache.updateRdfCache()
    print "Done!"
