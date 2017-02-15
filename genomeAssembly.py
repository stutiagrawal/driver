import os

def readDataFromFile(filename):
    """ Reads the fastq file and returns a dictionary of sequences """

    if not isinstance(filename, str):
        raise Exception("Filename must be a string containing the path to file.")
    if not len(filename) > 0:
        raise Exception("Filename cannot be empty. Please provide a valid filename.")
    if not os.path.isfile(filename):
        raise Exception("Could not find path to file, please ensure the path is correct")

    sequences = dict()
    names = dict()
    count = 0

    f = open(filename, "r")
    for line in f:
        if line.startswith(">"):
            if(count > 0):
                sequences[count] = seq
                names[count] = seqName
            seq = str()
            seqName = line.replace(">","").rstrip()
            count += 1
        else:
            seq += line.rstrip()
    sequences[count] = seq
    names[count] = seqName
    f.close()

    return (sequences, names)

def getOverlap(left, right):
    """ Get overlaps between two strings"""

    if not isinstance(left, str) or not isinstance(right, str):
        raise Exception("Inputs must be strings")
    if left == "" or right == "":
        return ""

    for i in xrange(len(left)):
        partLeft = left[i:]
        partRight = right[:len(left)-i]
        if partLeft == partRight:
            if partLeft != None:
                return partLeft
    return ""

    #d = difflib.SequenceMatcher(None, left, right)
    """
    leftstart, rightstart, size = d.find_longest_match(0, len(left), 0, len(right))

    assert(leftstart >= 0 and leftstart <= len(left))
    assert(rightstart >= 0 and rightstart <= len(right) and rightstart <= len(left))
    assert(size <= min(len(left), len(right)))
    assert(left[leftstart:leftstart + size] == right[rightstart: rightstart + size])
    """
    #return d
    #return left[leftstart:leftstart + size]

def getAllOverlaps(reads):
    """ Gets overlaps between all pairs of reads. """

    assert(isinstance(reads, dict))

    pairwise = dict()
    readnames = reads.keys()

    for i in readnames:
        for j in readnames:
            if not i == j:
                if i not in pairwise:
                    pairwise[i] = dict()
                if j not in pairwise[i]:
                    pairwise[i][j] = 0
                pairwise[i][j] = len(getOverlap(reads[i], reads[j]))

    assert(len(pairwise) == len(reads))
    for x in pairwise:
        assert(len(pairwise[x]) == len(reads)-1)

    return pairwise


def trans(p):
    "Creates a matrix transpose of the pairwise overlaps"

    transform = dict()
    for key, value in p.items():
        if isinstance(value, dict):
            for k, v in value.items():
                if k not in transform:
                    transform[k] = list()
                transform[k].append(v)
    return transform

def findFirstRead(pairwise):
    """ Gets the read which should be the first in the assembly. """

    if pairwise == dict():
        raise Exception("Cannot find first read in an empty dictionary")

    t = trans(pairwise)
    firstOverlap = 0
    firstkey = 0
    for key in t:
        if firstOverlap == 0:
            firstOverlap = max(t[key])
        if max(t[key]) <= firstOverlap:
            firstkey = key
            firstOverlap = max(t[key])

    assert(firstkey != None)

    return firstkey

def findKeyForLargestOverlap(d):
    """ Returns the key associated with the largest overlap """

    assert(isinstance(d, dict))

    if d == dict():
        raise Exception("Cannot find largest key in empty dictionary")

    maxOverlap = 0
    nextRecord = None

    for key, value in d.items():
        if value > maxOverlap:
            maxOverlap = value
            nextRecord = key

    return nextRecord

def findOrder(name, overlaps, order=list()):
    """ Returns the order in which the sequences must be joined """

    #print overlaps.keys()

    nextName = findKeyForLargestOverlap(overlaps[name])
    #print nextName
    #print len(order), len(overlaps)
    if len(order) == 0:
        order.append(name)
    if len(order) == len(overlaps):
        return order
    else:
        order.append(nextName)
        return findOrder(nextName, overlaps, order)

def assembleGenome(readOrder, reads, overlaps):
    """ Returns the assembled genome """

    assembledGenome = ""
    prevRead = 0

    for currRead in xrange(len(readOrder)):
        currName = readOrder[currRead]
        if currRead == 0:
            assembledGenome = reads[currName]

        else:
            assert(prevName in overlaps)
	    assert(currName in overlaps[prevName])
	    overlap = overlaps[prevName][currName]
            assembledGenome += reads[currName][overlap:]

        prevName = currName

    return assembledGenome

