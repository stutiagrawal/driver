import genomeAssembly as g
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='main.py', description="Genome Assembly")
    parser.add_argument('--filename', required=True)

    args = parser.parse_args()

    reads, names = g.readDataFromFile(args.filename)
    overlaps = g.getAllOverlaps(reads)
    first = g.findFirstRead(overlaps)
    order = g.findOrder(first, overlaps, list())
    genome = g.assembleGenome(order, reads, overlaps)
    print(genome)
