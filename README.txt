General approach used for genome assembly problem.

The problem was divided into the following sub-problems.

1. readDataFromFile(filename): This function reads the file. The file is laid out in fasta format where the ">" identifier segregates each sequence. This function reads the file and creates two dictionaries, one associated with the sequence and the other associated with the names. 

2. getOverlap(left, right): This function finds the overlap between two sequences. It starts from the longest overlap possible, which is the length of the left sequence and iteratively checks for smaller segements. It returns once it finds an overlap.

3. getAllOverlaps(reads): This function takes in the sequences from 1. and uses the function in 2. to find pairwise length of overlaps between all the reads.

4. findFirstRead(overlaps): This function uses the overlaps information and creates a transpose of the dictionary. From this transpose it tries to find the sequence which only fits well when it is on the left.

5. findKeyForLargestOverlap(d): This function takes in a dictionary and returns the key associated with the largest value.

6. findOrder(overlaps): Starting from the first read, this function recursively finds the order in which the reads must be joined by finding the largest overlap across each pair with that read..

7. assembleGenome(order, reads, overlaps): This function takes in the information from 1. , 6.  and 3. and returns the assembled genome.

---------------------------------------------------------------------------------

Using the tool:

On the command line run:

    python main.py --filename /path/to/file

This should return the genome on the output screen.
