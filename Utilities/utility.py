import json
import datetime
import os
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
