import ckanaggregatorpy.datagov.package_cache
import ckanaggregatorpy.datahubio.package_cache
import ckanaggregatorpy.pdeu.package_cache


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
            results.append({'rdfpackages': rdfpackages, 'prefix': prefix, 'ckanApiUrl': ckanApiUrl})
        return results

if __name__ == "__main__":
    ckanQuery = CkanQuery()
    ckanQuery.getRdfPackagesRdfResourcesOnly()
    import ipdb; ipdb.set_trace()
    print "hi"
