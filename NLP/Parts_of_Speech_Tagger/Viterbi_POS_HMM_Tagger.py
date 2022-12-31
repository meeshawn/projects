# -*- coding: utf-8 -*-
"""

@author: Meeshawn Marathe
"""
import numpy as np
import re
import sys

class Viterbi:
    def __init__(self, train, test):
        self.train = train
        self.test = test
        self.dict_word = {}
        self.dict_word_tag = {}
        self.dict_uni_tags = {}
        self.dict_bi_tags = {}
        self.correct = 0
        self.total = 0
        # self.vSize = 0

        
    def extractTokensAndPOS(self, word):
        # Extract tokens and POS tags from the corpus
        pos = 0
        tag_pos = -1
        word_temp = word
        
        while True:
            pos = word_temp.find('/')
            if pos == -1:
                break
            tag_pos = tag_pos + pos + 1
            word_temp = word_temp[pos+1:]
                        
        token = word[:tag_pos]
        tag = word[tag_pos+1:]
        
        # Convert all words to lower case to obtain true counts
        token = token.lower()
        
        # Check for multiple tags 
        pos = 0
        tags = []
        while True:
            pos = tag.find('|')
            if pos == -1:
                break   
            tags.append(tag[:pos])
            tag = tag[pos+1:]
            
        tags.append(tag)
        return token, tags
    
    def computeRawCounts(self):
        file = open(self.train, 'r')
        
        print('Computing all the raw counts from {} ...\n' .format(self.train))
        
        for line in file:
            sentence = line.strip()
            sentence = re.split('\s+', sentence)
            
            # Let 'BOS' signify the beginning of a sentence
            self.dict_uni_tags['BOS'] = self.dict_uni_tags.get('BOS', 0) + 1
            
            prev_tags = []
            prev_tags.append('BOS')

            for word in sentence:
                # Extract tokens and POS tags from the training corpus
                token, tags = self.extractTokensAndPOS(word)

                # Computing all the raw counts:
 
                self.dict_word[token] = self.dict_word.get(token, 0) + 1
                
                # NOTE:- For multiple tags, the respective counts have been 
                # increased by one for each one of them.   
                for tag in tags:
                    word_and_tag = token + ' ' + tag
                    self.dict_word_tag[word_and_tag] = self.dict_word_tag.get(word_and_tag, 0) + 1
                    self.dict_uni_tags[tag] = self.dict_uni_tags.get(tag, 0) + 1
                    for prev_tag in prev_tags:
                        string_of_tags = prev_tag + ' ' + tag
                        self.dict_bi_tags[string_of_tags] = self.dict_bi_tags.get(string_of_tags, 0) + 1
                        
                prev_tags = tags
        
        # self.vSize = len(self.dict_word)        
        file.close()
        
    def computeViterbiAndWriteData(self):
        
        file_read = open(self.test, 'r')
        file_write = open('POS.test.out', 'w')

        print('Computing the most probable tag sequences in {} using the Viterbi algorithm and writing the predictions to POS.test.out ...\n' .format(self.test))
        
        tag_list = []
        for tag in self.dict_uni_tags:
            tag_list.append(tag)
        
        for line in file_read:
            sentence = line.strip()
            sentence = re.split('\s+', sentence)
            
            word_seq = []
            tag_seq_gold = []
            tag_seq_predict = []
            
            for word in sentence:
                token, tags = self.extractTokensAndPOS(word)
                word_seq.append(token)
                tag_seq_gold.append(tags[0]) # Considering only the first tag in case of multiple tags
            
            scores = np.zeros(shape = (len(self.dict_uni_tags), len(word_seq)))
            back_ptr = np.zeros(shape = (len(self.dict_uni_tags), len(word_seq)), dtype=int)
            
            # Initialization 
            for tag, idx_tag in zip(tag_list, range(len(tag_list))):
                if tag == 'BOS':
                    continue
                
                # score(tag,1) = P(W1/tag)*P(tag/'BOS')
                word_and_tag = word_seq[0] + ' ' + tag
                if self.dict_word_tag.get(word_and_tag) == None:
                    if self.dict_word.get(word_seq[0]) == None:
                        # New unseen word. Apply smoothing techniques:
                        # Method 1: Laplace Smoothing:
                        # emission = (1 + self.dict_word_tag.get(word_and_tag, 0))/(1 + self.dict_uni_tags[tag])
                        # Method 2: Tag all new unseen words as nouns.
                        emission = 1/(1+self.dict_uni_tags['NP'])
                    else:
                        emission = 0 # The word doesn't have the given tag in the corpus
                else:
                    emission = self.dict_word_tag[word_and_tag]/self.dict_uni_tags[tag]
                    
                string_of_tags = 'BOS' + ' ' + tag
                if self.dict_bi_tags.get(string_of_tags) == None:
                    transmission = 0 # 'BOS' doesn't appear before the current tag
                else:
                    transmission = self.dict_bi_tags[string_of_tags]/self.dict_uni_tags['BOS']
                scores[idx_tag][0] = emission*transmission
                back_ptr[idx_tag][0] = 0

                
            # Iteration
            idx_wrd = 1
            for word in word_seq[1:]:
                for tag, idx_tag in zip(tag_list, range(len(tag_list))):
                    if tag == 'BOS':
                        continue
                    
                    # score(tag,n) = P(Wn/tag)*MAXOverJ(score(j_tag,n-1)P(tag/j_tag))
                    word_and_tag = word + ' ' + tag
                    if self.dict_word_tag.get(word_and_tag) == None:
                        if self.dict_word.get(word) == None: 
                            # New unseen word. Apply smoothing techniques:
                            # Method 1: Laplace Smoothing:
                            # emission = (1 + self.dict_word_tag.get(word_and_tag, 0))/(1 + self.dict_uni_tags[tag])
                            # Method 2: Tag all new unseen words as nouns.
                            emission = 1/(1+self.dict_uni_tags['NP'])
                        else:
                            emission = 0 # The word doesn't have the given tag in the corpus
                    else:
                        emission = self.dict_word_tag[word_and_tag]/self.dict_uni_tags[tag]
                    
                    products = np.zeros(shape=(len(tag_list),1))
                    for j_tag, j in zip(tag_list, range(len(tag_list))):
                        if j_tag == 'BOS':
                            continue
                        string_of_tags = j_tag + ' ' + tag
                        if self.dict_bi_tags.get(string_of_tags) == None:
                            transmission = 0 # Prev tag doesn't appear before the current tag
                        else:
                            transmission = self.dict_bi_tags[string_of_tags]/self.dict_uni_tags[j_tag]
                        products[j] = scores[j][idx_wrd-1]*transmission
                    
                    max_product = np.max(products)  
                    scores[idx_tag][idx_wrd] = emission*max_product
                    back_ptr[idx_tag][idx_wrd] = np.argmax(products)
                idx_wrd = idx_wrd + 1
                                
            # Sequence Identification
            J = np.argmax(scores[:,idx_wrd-1]) # Tag of the last word in the seqeunce
            tag_seq_predict.append(tag_list[J])
            
            back_idx = -2
            for word in reversed(word_seq[:-1]):
                J = np.argmax(scores[:,back_idx + 1])
                J = back_ptr[J][back_idx + 1]
                tag_seq_predict.insert(0, tag_list[J])
                back_idx = back_idx - 1          
                
            # Writing each sentence along with the predicted POS tags in POS.test.out
            for word, tag in zip(word_seq, tag_seq_predict):
                file_write.write(word + '/' + tag + ' ')
            
            file_write.write('\n')
            
            # Calculate the number of correct tag predictions in each sentence
            for y, y_hat in zip(tag_seq_gold, tag_seq_predict):
                if y == y_hat:
                    self.correct = self.correct + 1
            
            self.total = self.total + len(tag_seq_gold)
                
                    
        file_write.close()
        file_read.close()
        print("Sucessfully exported data to POS.test.out\n")
        
    def computeAccuracy(self):
        accuracy = self.correct/self.total*100
        print("The Accuracy of the Viterbi-based POS Tagging model with", self.test, ": {:.2f}%" .format(accuracy))
        


def main(args):
    
    train_dataset = args[1]
    test_dataset = args[2]
        
    # Step 0: Create an instance of the Viterbi class:
    pos_tagger = Viterbi(train_dataset, test_dataset)
    
    # Step 1: Compute all the required raw counts from the training corpus 
    # for the Viterbi algorithm:
    pos_tagger.computeRawCounts()
    
    # Step 2: Compute the most probable tag sequence for each sentence in the
    # training corpus using the Viterbi algorithm and write the prediction
    # data to a .out file:
    pos_tagger.computeViterbiAndWriteData()
    
    # Step 3: Compute and display the accuracy of the Viterbi-based POS tagger:
    pos_tagger.computeAccuracy()


if __name__ == "__main__":
    main(sys.argv)

