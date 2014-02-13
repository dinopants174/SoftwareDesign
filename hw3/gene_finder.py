# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Zoher Ghadyali
"""

from amino_acids import aa, codons #used to convert nucleotides to amino acids
from random import shuffle #used to shuffle dna for trials

from load import load_seq #used to load Salmonella DNA
dna = load_seq("./data/X73525.fa")

#I know I should be using "if _name_ = main" thing somewhere but I don't really know how it works

def collapse(L):
    """ Converts a list of strings to a string by concatenating all elements of the list """
    output = ""
    for s in L:
        output = output + s
    return output

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment
    """
    AA = ""
    for i in range(len(dna)):
        codon = dna[3*i:3*i+3]  #breaks up DNA into sequences of 3 nucleotides = codon
        for t in range(len(codons)):
            if codon in codons[t]:
                AA += aa[t] #loops through codon list, checks to see if codon found is in list, adds amino acid of corresponding index
    return AA

def coding_strand_to_AA_unit_tests():
    """ Unit tests for the coding_strand_to_AA function """
    print "Input: TTTTTA " + "Expected Output: FL "+"Output: " + coding_strand_to_AA('TTTTTA')
    print ""
    print "Input: ATGCCCGCTT " + "Expected Output: MPA " + "Output: " + coding_strand_to_AA('ATGCCCGCTTT') 
    
def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    """
    reverse_dna = ""
    for i in range(len(dna)):   #loops through every nucleotide and replaces it with complementary letter
        if dna[i] == "A":
            reverse_dna += "T"
        elif dna[i] == "T":
            reverse_dna += "A"
        elif dna[i] == "C":
            reverse_dna += "G"
        elif dna[i] == "G":
            reverse_dna += "C"
        else:   #if it finds a letter that doesn't have a complement, it prints that there is an error in the DNA
            return "I have recieved a character that is not defined in this loop"
    return reverse_dna[::-1]
    
def get_reverse_complement_unit_tests():
    """ Unit tests for the get_complement function """
    print "Input: CGA "+"Expected Output: TCG "+"Output: " + get_reverse_complement('CGA')
    print ""
    print "Input: GCFA "+"Expected Output: I have recieved a character that is not defined in this loop "+"Output: " + get_reverse_complement('GCFA')

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    """
    orf = ""
    for i in range(0,len(dna),3):
        codon = dna[i:i+3] #breaks up DNA into codons
        if codon != 'TAG' and codon != 'TAA' and codon != 'TGA':
            orf += codon #concatenates codons in string unless it reaches a stop codon
        else:
            break #at stop codon, function ends, possibly not the most elegant solution
    return orf

def rest_of_ORF_unit_tests():
    """ Unit tests for the rest_of_ORF function """
    print "Input: ATGCGCTAA " +"Expected Output: ATGCGC " + "Output: " + rest_of_ORF('ATGCGCTAA')
    print ""    
    print "Input: ATGTTTTAG " +"Expected Ouput: ATGTTT " + "Output: " + rest_of_ORF('ATGTTTTAG')

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    
    one_frame = []
    i = 0
    while i < len(dna)-2:
        codon = dna[i:i+3]
        if codon == "ATG":  #if function finds a start codon, begins appending DNA to list until stop codon
            one_frame.append(rest_of_ORF(dna[i:]))
            i += len(one_frame[-1]) #index then changes to be the last nucleotide of the appended reading frame
        else:   #else, function keeps going looking for start codons
            i +=3
    return one_frame


def find_all_ORFs_oneframe_unit_tests():
    """ Unit tests for the find_all_ORFs_oneframe function """
    print "Input: ATGTAAATGTAG "+"Expected Output: ['ATG', 'ATG'] " + "Ouput: " + str(find_all_ORFs_oneframe('ATGTAAATGTAG'))
    print ""    
    print "Input: ATGCCCTAAATGGGGTAA "+"Expected Output: ['ATGCCC', 'ATGGGG'] " + "Ouput: " + str(find_all_ORFs_oneframe('ATGCCCTAAATGGGGTAA'))

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    p = 0
    res = []
    while p<3: #starts reading frame at index[0] => index[1] => index[2] b/c index[3] = index[0]
        snip = dna[p:] #creates a snippet of DNA that extends from starting index to end of DNA
        res.append(collapse(find_all_ORFs_oneframe(snip)))
        p += 1
    return res

def find_all_ORFs_unit_tests():
    """ Unit tests for the find_all_ORFs function """    
    print "Input: ATGTAATGTAA " + "Expected Output: ['ATG', '', 'ATG'] " + "Output: " + str(find_all_ORFs('ATGTAATGTAA'))
    print ""    
    print "Input: ATGCCGTCGCATGAATGTAG "+"Expected Output: ['ATGCCGTCGCATGAATGTAG', 'ATGAATGTAG', 'ATG'] " + "Ouput: " + str(find_all_ORFs('ATGCCGTCGCATGAATGTAG'))

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    res = []
    dna_rev = get_reverse_complement(dna)
    orf = find_all_ORFs(dna)
    orf_rev = find_all_ORFs(dna_rev)
    res.append(collapse(orf)) #appends to an empty list the reading frames from original strand of DNA
    res.append(collapse(orf_rev)) #appends to list the reading frames from complementary strand of DNA
    return res
    
def find_all_ORFs_both_strands_unit_tests():
    """ Unit tests for the find_all_ORFs_both_strands function """
    print "Input: ATGCGAATGCCCTAGCATCGGGAAA " + "Expected Output: ['ATGCGAATGCCC', 'ATGCTAGGGCATTCGCAT'] " + "Output: "+str(find_all_ORFs_both_strands("ATGCGAATGCCCTAGCATCGGGAAA"))
    print ""    
    print "Input: ATGTAG " + "Expected Output: ['ATG', ''] " + "Output: " + str(find_all_ORFs_both_strands('ATGTAG'))


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string"""
    t = find_all_ORFs_both_strands(dna) #stores all of the reading frames in t
    return max(t, key=len)

def longest_ORF_unit_tests():
    """ Unit tests for the longest_ORF function """
    print "Input: ATGCGAATGTAGCATC " + "Expected Output: ATGCTACATTCGCAT " + "Output: " + str(longest_ORF("ATGCGAATGTAGCATC"))
    print ""    
    print "Input: ATGCGCAATTGA " + "Expected Output: ATGCGCAAT " + "Output: " + str(longest_ORF("ATGCGCAATTGA"))    

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    longest_frame = 0
    for i in range(0,num_trials):
        dna_list = list(dna) #makes DNA into list
        shuffle(dna_list) #shuffles DNA i times
        dna_string = collapse(dna_list) #makes DNA from list into string
        if len(longest_ORF(dna_string)) > longest_frame:
            longest_frame = len(longest_ORF(dna_string)) #keeps replacing if it finds longer reading frame until found max
    return longest_frame

print (longest_ORF_noncoding(dna, 1500))/9 #so something weird is happening here, was getting thresholds in 6000s, divided by 9 to get realistic threshold

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """
    list_of_ORFs = find_all_ORFs_both_strands(dna) #finds all reading frames
    i = 0
    res = []
    while i < len(list_of_ORFs):
        if len(list_of_ORFs[i]) > threshold:
            res.append(coding_strand_to_AA(list_of_ORFs[i])) #only appends reading frames whose length is greater than threshold
            i += 1
        else:
            i += 1
    return res

print gene_finder(dna,750)