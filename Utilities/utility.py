import json
import datetime
import os, re
import puremagic
from py_essentials import hashing as hs
import uuid


def stix_to_json(stixObject):
    return json.loads(stixObject.serialize())


def convertCtimeToISOFormat(ctime):
    dt = datetime.datetime.strptime(ctime, "%a %b %d %H:%M:%S %Y").isoformat()
    return str(dt)


def md5Hash(file):
    md5 = hs.fileChecksum(file, "md5")
    return md5


def sha256Hash(file):
    return hs.fileChecksum(file, "sha256")


def getsizeoffile(file):
    return os.path.getsize(file)


def getmimetype(file):
    # it is based on the magic number and not on file extension
    return puremagic.magic_file(file)


def getuuid():
    return str(uuid.uuid4())


def currenttime():
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def datetimeconvertforpulsedive(datetime):
    splitted=re.split(" ", datetime)
    return (splitted[0] + "T" + splitted[1] + "Z")

#take the ports of malware's activity
def portspulsedive(object):
    #regex for taking the numbers of the collection
    allnum=re.findall('(\d+)', str(object))
    ports=[]
    #taking only the ports,not the aid and indicators,loop by step=3
    r=range(0,len(allnum),3)
    for x in r:
        ports.append(allnum[x])
    return ports

#same for other values
def manyvaluespulsedive(object):
    object=json.dumps(object,indent=4)
    allstr=re.findall('(".+")', str(object))
    values=[]
    r=range(0,len(allstr),3)
    for x in r:
        values.append(allstr[x].replace('"',""))
    return values




