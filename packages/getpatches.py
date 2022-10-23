# Author: Kevin Eberson
#
#
# A script which creates a package list by webscraping the Linux from Scratch patches website
# link: https://www.linuxfromscratch.org/lfs/view/development/chapter03/patches.html

from bs4 import BeautifulSoup

def GetDefinitionList(url):
    if(url == ""):
        print("Error, empty link.")
        exit(1)

    from urllib.request import urlopen
        
    page = urlopen(url)
    html = page.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    definitionList = soup.find_all("div", {"class": "materials"})

    return definitionList

##################################################################################################

def GetNames(names):
    if(names is None):
        print("Error, names are None.")
        exit(1)

    soup = BeautifulSoup(str(names), 'html.parser')
    namesList = []

    for name in soup.find_all("span", {"class": "term"}):
        result = name.get_text()
        
        foundName = result.partition(" -")[0].lower()
        namesList.append(foundName)

    return namesList

##################################################################################################
def ExtractPatchLinks(links):
    if(links is None):
        print('Error, links is None.')
        exit(1)

    soup = BeautifulSoup(str(links), 'html.parser')
    urlList = []

    for link in soup.find_all('a', href=True):
        result = link.get_text()

        if('.patch' in result):
            urlList.append(result.strip())

    return urlList

##################################################################################################

def ExtractMD5Sums(sums):
    if(sums is None):
        print('Error, sums is None.')
        exit(1)

    soup = BeautifulSoup(str(sums), 'html.parser')
    md5sumList = []

    for results in soup.find_all("code"): 
        sum = results.get_text()

        if (len(sum) == 32):
            md5sumList.append(sum)

    return md5sumList

##################################################################################################

def ExtractPackageData(csvPath, definitionList):
    soup = BeautifulSoup(str(definitionList), 'html.parser')

    # package name + version
    names = soup.find_all('span', {'class' : 'term'})
    # all links
    links = soup.find_all('a', {'class' : 'ulink'})
    # all md5 + SHA256 sums
    sums = soup.find_all('code', {'class' : 'literal'})

    nameList = GetNames(names)
    urlList = ExtractPatchLinks(links)
    md5sumList = ExtractMD5Sums(sums)

    with open(csvPath, 'a+') as csvFile:
        for i in range(len(md5sumList)):
            csvLine = nameList[i] + ';' + urlList[i] + ';' + md5sumList[i]
            csvFile.write(csvLine + '\n')
            print(csvLine)
        
##################################################################################################

def main():
        from os import path, getcwd, remove
        url = "https://www.linuxfromscratch.org/lfs/view/development/chapter03/patches.html"

    #get the html data from the lfs website
        print("Getting patchlist from %s" % url)
        definitionList = GetDefinitionList(url)

        csvFileName = "patchlist.csv"
        csvPath = getcwd() + "/" + csvFileName

        if(path.exists(csvFileName)):
            remove(csvFileName)

        print("Appending patchlist to %s." % csvFileName)
        ExtractPackageData(csvPath, definitionList)
        print("Finished generating patchlist.")
        exit(0)      

##################################################################################################

if __name__ == "__main__":
    main()