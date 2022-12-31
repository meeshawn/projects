# -*- coding: utf-8 -*-
"""
Collocations Detection

@author: Meeshawn Marathe
"""
#%%
import re
import numpy as np
import sys

class CollocationsDetection:
    def __init__(self, corpus, measure):
        self.corpus = corpus
        self.measure = measure
        self.dict_unigram = {}
        self.dict_bigram = {}
        self.N_unigrams = 0
        self.N_bigrams = 0
        self.bigrams_chi_square_score = {}
        self.bigrams_pmi_score = {}
        
    def extractUnigramsBigrams(self):
        file = open(self.corpus,"r")
        
        punc_list = [',', '.', ';', ':', '\'', '\"' , '-', ')', '(', '[', ']', '!', '?']
        
        print("Extracting unigrams and bigrams from {} ...".format(self.corpus))
        # Unigram and Bigram Frequency count
        for line in file:
            sentence = line.strip()
            
            # Split sentences into words based on whitespaces
            sentence = re.split('\s+', sentence)
            prev_word = ""
            for word in sentence:
                # Convert all words to lower case
                word = word.lower()
                        
                # Split hyphenated words (For ex: top-rated, high-ranked etc)
                if len(word) > 1 and word.find("-") != -1:
                    idx = word.find("-")
                    left = word[0:idx]
                    right = word[idx+1:]
                    
                    self.dict_unigram[left] = self.dict_unigram.get(left, 0) + 1
                    
                    if prev_word != "":
                        pair_of_words = prev_word + " " + left
                        self.dict_bigram[pair_of_words] = self.dict_bigram.get(pair_of_words, 0) + 1
                    
                    # Considering at max 2 hyphens in a 3 word phrase (For ex: five-year-old)
                    idx = right.find("-")
                    if idx!= -1:
                        R_left = right[0:idx]
                        R_right = right[idx+1:]
                        self.dict_unigram[R_left] = self.dict_unigram.get(R_left, 0) + 1
                        self.dict_unigram[R_right] = self.dict_unigram.get(R_right, 0) + 1
                        
                        pair_of_words = left + " " + R_left
                        self.dict_bigram[pair_of_words] = self.dict_bigram.get(pair_of_words, 0) + 1
        
                        pair_of_words = R_left + " " + R_right
                        self.dict_bigram[pair_of_words] = self.dict_bigram.get(pair_of_words, 0) + 1
                        prev_word = R_right
                    else:
                        self.dict_unigram[right] = self.dict_unigram.get(right, 0) + 1
                        
                        pair_of_words = left + " " + right
                        self.dict_bigram[pair_of_words] = self.dict_bigram.get(pair_of_words, 0) + 1
                        prev_word = right                
                    continue
                
                if word not in punc_list:
                    self.dict_unigram[word] = self.dict_unigram.get(word, 0) + 1
                
                    if prev_word != "":
                        pair_of_words = prev_word + " " + word
                        self.dict_bigram[pair_of_words] = self.dict_bigram.get(pair_of_words, 0) + 1
                        
                    prev_word = word
        file.close()

    def countNgrams(self):
        # Calculating number of unigrams and bigrams
        print("Calculating the number of unigrams and bigrams from {} ...".format(self.corpus))

        for pair in self.dict_unigram:
            self.N_unigrams = self.N_unigrams + self.dict_unigram[pair]
        
        for pair in self.dict_bigram:
            self.N_bigrams = self.N_bigrams + self.dict_bigram[pair]
        
        print("Num of unigrams: {}".format(self.N_unigrams))
        print("Num of bigrams: {}".format(self.N_bigrams))
    
    def computeMeasures(self):
        if self.measure == 'chi-square':
            self.computeChiSquare()
        elif self.measure == 'PMI':
            self.computePMI()
        else:
            print("Wrong input. Pass either of these arguments: \'chi-square\' or \'PMI\'")
        
    def computeChiSquare(self):
        # Computing chi-square
        '''
          ________________
          |  O_11  | O_12
          |  O_21  | O_22
          '''
        print("Computing the chi-square measure on the bigrams ...")
        for string in self.dict_bigram:
            pair = re.split("\s+", string)
            first_word = pair[0]
            second_word = pair[1]
            
            # Observed quantities
            O_11 = self.dict_bigram[string]
            O_12 = self.dict_unigram[second_word] - O_11
            O_21 = self.dict_unigram[first_word] - O_11
            O_22 = self.N_bigrams - O_11 - O_12 - O_21
            
            # Expected quantities    
            E_11 = self.dict_unigram[first_word]*self.dict_unigram[second_word]/self.N_bigrams   
            E_12 = (O_12 + O_22)*self.dict_unigram[second_word]/self.N_bigrams
            E_21 = self.dict_unigram[first_word]*(O_21 + O_22)/self.N_bigrams
            E_22 = (O_12 + O_22)*(O_21 + O_22)/self.N_bigrams
            
            A = ((O_11 - E_11)**2)/E_11
            B = ((O_12 - E_12)**2)/E_12
            C = ((O_21 - E_21)**2)/E_21
            D = ((O_22 - E_22)**2)/E_22
            
            chi_square = A + B + C + D
            self.bigrams_chi_square_score[string] = chi_square
                
    def computePMI(self):
        print("Computing the PMI measure on the bigrams ...")
        for string in self.dict_bigram:
            pair = re.split("\s+", string)
            first_word = pair[0]
            second_word = pair[1]
            
            # ratio = N_unigrams*dict_bigram[string]/(dict_unigram[first_word]*dict_unigram[second_word])
            pmi = np.log(self.N_unigrams) + np.log(self.dict_bigram[string]) - np.log(self.dict_unigram[first_word]) - np.log(self.dict_unigram[second_word])
            self.bigrams_pmi_score[string] = pmi   
            
    def displayTop20(self):
        print("\nPrinting top 20 bi-grams as per {}:\n".format(self.measure)) 
        if self.measure == 'chi-square':
            score_list = self.bigrams_chi_square_score
        elif self.measure == 'PMI':
            score_list = self.bigrams_pmi_score
        count = 0
        for x in sorted(score_list, key = score_list.get, reverse=True):
            if count != 20:
                print("[{}] {}" .format(x, score_list[x]))
                count +=1
            else:
                break
    

def main(args):
    corpus = args[1]
    measure = args[2]
    
    # Step 0: Create an instance of the CollocationsDetection class
    CD = CollocationsDetection(corpus, measure)
    
    # Step 1: Filter punctuations and extract unigrams and bigrams
    CD.extractUnigramsBigrams()
    
    # Step 2: Count and display the number of unigram and bigrams extracted
    CD.countNgrams()
    
    # Step 3: Compute the required measure: chi-square or PMI
    CD.computeMeasures()
    
    # Step 4: Display the top 20 bigrams based on the measure
    CD.displayTop20()
    

if __name__ == "__main__":
    main(sys.argv)
