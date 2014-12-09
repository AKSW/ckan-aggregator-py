import os.path
import time
import requests

try:
    import cPickle as pickle
except:
    import pickle

import ckanaggregatorpy.datagov as datagov

class PackageCache(object):
    packageListFile = os.path.join(datagov.cacheFolder, "packageList.dump")
    packagesFolder = os.path.join(datagov.cacheFolder, "packages")
    pagesFolder = os.path.join(datagov.cacheFolder, "pages")
    datagovPageUrl = "http://catalog.data.gov/dataset?page="
    datagovNumberOfPages = 6705 # this number has to be updated manually

    def __init__(self):
        self.ckanClient = datagov.ckanClient

    def getPackages(self):
        pass

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
        """
            ckanclient.package_list() does not work for data.gov portal
            we have to fetch all the pages from the web portal 
            and then scrape package ids from them
        """
        self.updateDataGovPages()
        self.extractDataGovDatasetIds()

    def extractDataGovDatasetIds(self):
        """
            Extract Dataset Ids from the scraped pages
            Should be run after updateDataGovPages
        """
        datasetIds = []
        for i in range(1, self.datagovNumberOfPages + 1):
            pageFile = os.path.join(self.pagesFolder, "page" + str(i))
            pageUrl = self.datagovPageUrl+str(i)
            if(not os.path.isfile(pageFile)):
                print("Page %s does not exist! Did you run updateDataGovPages?" % pageUrl)
                break
            f = open(pageFile, "rU")
            page = f.read()
            f.close()
            soup = BeautifulSoup(page)
            for dataset in soup.find_all(href=re.compile("dataset/")):
                datasetIds.append(dataset["href"].split("/")[-1])
         
        self.saveFile(packageListFile, datasetIds)
            
    def updateDataGovPages(self):
        """
            Saves all the pages from the data.gov portal to data/datagov/pages folder
        """
        for i in range(1, self.datagovNumberOfPages + 1):
            print("Getting page %s out of %s" % (i, self.datagovNumberOfPages))
            pageFile = os.path.join(self.pagesFolder, "page" + str(i))
            pageUrl = self.datagovPageUrl+str(i)
            if(os.path.isfile(pageFile)):
                print("Page %s is already fetched, skipping." % pageUrl)
            r = requests.get(pageUrl)
            assert r.status_code == requests.status_codes.codes.OK
            f = open(pageFile, "w")
            f.write(r.content)
            f.close()
            time.sleep(0.5)

    def isPackageListOutdated(self):
        #Does not exist
        if(not os.path.isfile(self.packageListFile)):
            print("%s does not exists!" % self.packageListFile)
            return True

        #Is older than 1 week (all functions are in seconds)
        packageListAge = time.time() - os.path.getmtime(self.packageListFile)
        week = 604800 #seconds
        if(packageListAge > week):
            print("%s is older than a week!" % self.packageListFile)
            return True

        #File empty (corrupted?)
        if(os.stat(self.packageListFile).st_size == 0):
            print("%s is empty!" % self.packageListFile)
            return True

        return False

if __name__ == "__main__":
    packageCache = PackageCache()
    pkgList = packageCache.getPackageList()
    #packageCache.updatePackages()
    import ipdb; ipdb.set_trace()
    print "hi"
