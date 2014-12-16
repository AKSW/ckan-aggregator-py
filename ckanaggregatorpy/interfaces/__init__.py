import os.path
import time
import ckanaggregatorpy.assets.formats

try:
    import cPickle as pickle
except:
    import pickle

class PackageCacheInterface(object):
    packageListFile = None
    packagesFolder = None
    ckanClient = None

    def __init__(self):
        self.packageListFile = os.path.join(self.cacheFolder, "packageList.dump")
        self.packagesFolder = os.path.join(self.cacheFolder, "packages")
        self.rdfPackagesFile = os.path.join(self.cacheFolder, "rdfPackages.dump")
        self.rdfPackagesRdfResourcesOnlyFile = os.path.join(self.cacheFolder, "rdfPackagesRdfResourcesOnly.dump")

    def getRdfPackagesRdfResourcesOnly(self):
        if(not os.path.isfile(self.rdfPackagesRdfResourcesOnlyFile)):
            self.updateRdfPackagesRdfResourcesOnly()
            return self.loadFile(self.rdfPackagesRdfResourcesOnlyFile)
        else:
            return self.loadFile(self.rdfPackagesRdfResourcesOnlyFile)

    def updateRdfPackagesRdfResourcesOnly(self):
        rdfPackages = self.getRdfPackages()
        rdfFormats = ckanaggregatorpy.assets.formats.RDF
        for rdfPackage in rdfPackages:
            for num, resource in enumerate(rdfPackage['resources']):
                if(not resource['format'] in rdfFormats):
                    rdfPackage['resources'][num] = None
        self.saveFile(self.rdfPackagesRdfResourcesOnlyFile, rdfPackages)

    def getRdfPackages(self):
        if(not os.path.isfile(self.rdfPackagesFile)):
            self.updateRdfPackages()
            return self.loadFile(self.rdfPackagesFile)
        else:
            return self.loadFile(self.rdfPackagesFile)

    def updateRdfPackages(self):
        rdfFormats = ckanaggregatorpy.assets.formats.RDF
        packageList = self.getPackageList()
        numberOfPackages = len(packageList)
        rdfPackages = []
        for num, packageId in enumerate(packageList):
            print("Querying package %d out of %d" % (num + 1, numberOfPackages))
            packageFile = os.path.join(self.packagesFolder, packageId)
            if(not os.path.exists(packageFile)):
                print("Package %s does not exist in the cache! Try updatePackages()" % packageId)
                continue
            else:
                package = self.loadFile(packageFile)
                for resource in package['resources']:
                    if(resource['format'] in rdfFormats):
                        print("Adding package %s to RDF cache" % (packageId))
                        rdfPackages.append(package)
                        break
        self.saveFile(self.rdfPackagesFile, rdfPackages)

    def updatePackages(self):
        packageList = self.getPackageList()
        numberOfPackages = len(packageList)
        for num, packageId in enumerate(packageList):
            print("Fetching package %d out of %d" % (num + 1, numberOfPackages))
            packageFile = os.path.join(self.packagesFolder, packageId)
            if(os.path.exists(packageFile)):
                print("Package %s already exists in the cache" % packageId)
                continue
            try:
                package = self.ckanClient.package_entity_get(packageId)
                self.saveFile(packageFile, package)
            except BaseException as e:
                print("Could not fetch %s because of %s" % (packageId, str(e)))

    def getPackageList(self):
        if(self.isPackageListOutdated()):
            self.updatePackageList()
            return self.loadFile(self.packageListFile)
        else:
            return self.loadFile(self.packageListFile)

    def saveFile(self, filepath, obj):
        #provide full path to the file as filepath and obj to save
        try:
            file = open(filepath, 'wb')
            pickle.dump(obj, file, protocol=pickle.HIGHEST_PROTOCOL)
            file.close()
        except BaseException as e:
            print("Could not save the file %s because %s" % (filepath, str(e)))

    def loadFile(self, filepath):
        #provide full path to the file as filepath
        file = open(filepath, 'rb')
        obj = pickle.load(file)
        file.close()
        return obj

    def updatePackageList(self):
        packageList = self.ckanClient.package_list()
        self.saveFile(self.packageListFile, packageList)

    def isPackageListOutdated(self):
        #Does not exist
        if(not os.path.isfile(self.packageListFile)):
            print("%s does not exists!" % self.packageListFile)
            return True

        #Is older than 1 week (all functions are in seconds)
        packageListAge = time.time() - os.path.getmtime(self.packageListFile)
        week = 604800 #seconds
        month = 2419200 #seconds
        if(packageListAge > month):
            print("%s is older than a month!" % self.packageListFile)
            return True

        #File empty (corrupted?)
        if(os.stat(self.packageListFile).st_size == 0):
            print("%s is empty!" % self.packageListFile)
            return True

        return False
