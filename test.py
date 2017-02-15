import unittest
from genomeAssembly import *

class TestGenomeAssembly(unittest.TestCase):

    def testReadDataFromFile(self):

        with self.assertRaises(Exception):
            readDataFromFile("NonExistantFile.txt")

        with self.assertRaises(Exception):
            readDataFromFile("")

        with self.assertRaises(Exception):
            readDataFromFile(42)

    def testGetOverlap(self):

        assert(getOverlap("AAAT", "AAATCCC") == "AAAT")

        assert(getOverlap("TAAATCCC", "AAATCCC") == "AAATCCC")

        assert(getOverlap("", "AAAA") == "")

        with self.assertRaises(Exception):
            getOverlap(1, "AAA")

        with self.assertRaises(Exception):
            getOverlap("AAA", 1)

        assert(getOverlap("GGCTCCCCACGGGGTACCCATAACTTGACAGTAGATCTCGTCCAGACCCCTAGC",
                          "CGATTCCAGGCTCCCCACGGGGTACCCATAACTTGACAGTAGATCTC") == "C")

        assert(getOverlap("CGATTCCAGGCTCCCCACGGGGTACCCATAACTTGACAGTAGATCTC",
                          "GGCTCCCCACGGGGTACCCATAACTTGACAGTAGATCTCGTCCAGACCCCTAGC") == "GGCTCCCCACGGGGTACCCATAACTTGACAGTAGATCTC")

    def testFindFirstRead(self):

        p = {1: {2: 4, 3: 7, 4: 1},
            2: {1: 1, 3: 1, 4: 7},
            3: {1: 0, 2: 7, 4: 4},
            4: {1: 0, 2: 1, 3: 0}}

        assert(findFirstRead(p) == 1)

        p = dict()

        with self.assertRaises(Exception):
            findFirstRead(p)


    def testFindKeyForLargestOverlap(self):

        p = {2: 4, 3: 7, 4: 1}

        assert(findKeyForLargestOverlap(p) == 3)

        p = dict()

        with self.assertRaises(Exception):
            findKeyForLargestOverlap(p)


    def testFindOrder(self):

        p = {1: {2: 4, 3: 7, 4: 1},
            2: {1: 1, 3: 1, 4: 7},
            3: {1: 0, 2: 7, 4: 4},
            4: {1: 0, 2: 1, 3: 0}}

        assert(findOrder(1, p) == [1,3,2,4])

suite = unittest.TestLoader().loadTestsFromTestCase(TestGenomeAssembly)
unittest.TextTestRunner(verbosity=3).run(suite)
