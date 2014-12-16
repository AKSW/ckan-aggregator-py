import os.path

import ckanaggregatorpy.interfaces
import ckanaggregatorpy.pdeu as pdeu

class PackageCache(ckanaggregatorpy.interfaces.PackageCacheInterface):
    cacheFolder = pdeu.cacheFolder
    ckanClient = pdeu.ckanClient
    prefix = "pdeu"
    ckanApiUrl = pdeu.ckanApiUrl

    def __init__(self):
        super(self.__class__, self).__init__()

if __name__ == "__main__":
    packageCache = PackageCache()
    #pkgList = packageCache.getPackageList()
    #packageCache.updatePackages()
    rdfPackages = packageCache.getRdfPackages()
    import ipdb; ipdb.set_trace()
