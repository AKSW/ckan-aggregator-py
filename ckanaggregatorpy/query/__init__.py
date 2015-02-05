import ckanaggregatorpy.datagov.package_cache
import ckanaggregatorpy.datahubio.package_cache
import ckanaggregatorpy.pdeu.package_cache

try:
    import cPickle as pickle
except:
    import pickle

class CkanQuery(object):
    ckanCaches = [
            ckanaggregatorpy.datagov.package_cache.PackageCache(),
            ckanaggregatorpy.datahubio.package_cache.PackageCache(),
            ckanaggregatorpy.pdeu.package_cache.PackageCache()
            ]
    def __init__(self):
        pass

    def getRdfPackagesRdfResourcesOnly(self):
        results = []
        for ckanCache in self.ckanCaches:
            rdfpackages = ckanCache.getRdfPackagesRdfResourcesOnly()
            prefix = ckanCache.prefix
            ckanApiUrl = ckanCache.ckanApiUrl
            #Prefixes are mapped to name in ckan_catalog table in LODStats_WWW
            results.append({'rdfpackages': rdfpackages, 'prefix': prefix, 'ckanApiUrl': ckanApiUrl})
        return results

    def dumpRdfPackagesRdfResourcesOnly(self, path='/tmp/ckan_catalogs.pickled'):
        rdfPackages = ckanQuery.getRdfPackagesRdfResourcesOnly()
        file = open(path, 'wb')
        pickle.dump(rdfPackages, file, protocol=pickle.HIGHEST_PROTOCOL)
        file.close()

if __name__ == "__main__":
    ckanQuery = CkanQuery()
    #rdfPackages = ckanQuery.getRdfPackagesRdfResourcesOnly()
    ckanQuery.dumpRdfPackagesRdfResourcesOnly()
    print "done"
