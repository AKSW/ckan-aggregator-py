import os

import ckanaggregatorpy.datagov.package_cache
import ckanaggregatorpy.datahubio.package_cache
import ckanaggregatorpy.pdeu.package_cache
import ckanaggregatorpy.opencanada.package_cache

from ckanaggregatorpy.interfaces.loadsaveinterface import LoadSaveInterface

class CkanQuery(LoadSaveInterface):
    formatsFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../data/formats.set"))
    ckanCaches = [
            ckanaggregatorpy.datagov.package_cache.PackageCache(),
            ckanaggregatorpy.datahubio.package_cache.PackageCache(),
            ckanaggregatorpy.pdeu.package_cache.PackageCache(),
            ckanaggregatorpy.opencanada.package_cache.PackageCache()
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

    def getCsvPackages(self):
        results = []
        for ckanCache in self.ckanCaches:
            csvpackages = ckanCache.getCsvPackages()
            prefix = ckanCache.prefix
            ckanApiUrl = ckanCache.ckanApiUrl
            #Prefixes are mapped to name in ckan_catalog table in LODStats_WWW
            results.append({'csvpackages': csvpackages, 'prefix': prefix, 'ckanApiUrl': ckanApiUrl})
        return results

    def getRdfPackagesRdfResourcesOnlyNormalized(self):
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

    def encode(self, string):
        if(string is None):
            return ""
        elif(type(string) is int):
            return string
        elif(string is ""):
            return "N/A"
        else:
            return string.encode('utf-8')

    def getFormats(self):
        if(not os.path.isfile(self.formatsFile)):
            self.updateFormats()
            return self.loadFile(self.formatsFile)
        else:
            return self.loadFile(self.formatsFile)

    def updateFormats(self):
        formats = set()
        for ckanCache in self.ckanCaches:
            packages = ckanCache.getPackagesStream()
            for package in packages:
                for resource in package['resources']:
                    formats.add(resource['format'])
        self.saveFile(self.formatsFile, formats)

    def getLicensesCount(self):
        for ckanCache in self.ckanCaches:
            licenses = {}
            packages = ckanCache.getPackagesStream() # generator
            prefix = ckanCache.prefix
            ckanApiUrl = ckanCache.ckanApiUrl
            for package in packages:
                isopen = package.get('isopen', '')
                license = package.get('license', '')
                license_id = package.get('license_id', '')
                license_title = package.get('license_title', '')
                license_url = package.get('license_url', '')
                if(licenses.get(license_id, 0) != 0):
                    count = licenses.get(license_id)['count'] + 1
                else:
                    count = 1
                licenses[license_id] = {
                    'license': license,
                    'license_id': license_id,
                    'license_title': license_title,
                    'license_url': license_url,
                    'count': count
                }
            f = open('license'+prefix+'.csv', 'wb+')
            for license in licenses:
                csvStringLicense = ", ".join([str(self.encode(license)),
                                              str(self.encode(licenses[license]['count'])),
                                              str(self.encode(licenses[license]['license_title'])),
                                              str(self.encode(licenses[license]['license_url'])),
                                              str(self.encode(licenses[license]['license']))])
                f.write(csvStringLicense + "\n")
            f.close()

if __name__ == "__main__":
    ckanQuery = CkanQuery()
    #rdfPackages = ckanQuery.getRdfPackagesRdfResourcesOnly()
    #ckanQuery.dumpRdfPackagesRdfResourcesOnly()
    #ckanQuery.getLicensesCount()
    csvPackages = ckanQuery.getCsvPackages()
    import ipdb; ipdb.set_trace()
