# -*- coding: utf-8 -*-
"""
Word Sense Disambiguation using Naive Bayes  Classifier

@author: Meeshawn Marathe
"""
import math
import sys

class WSD:
    def __init__(self, dataset):
        self.dataset = dataset
        self.corpus = []
        self.train = []
        self.test = []
        self.dict_sense = {}
        self.dict_word = {}
        self.dict_word_and_sense = {}
        self.y_sense = []
        self.y_sense_hat = []
        self.totalCorrect = 0
        self.mode = 0
        self.punc_list = [',', '.', ';', ':', '\'', '\"' , '-', ')', '(', '[', ']', '!', '?']
        self.stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',\
                          "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',\
                          'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',\
                          'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', \
                          'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', \
                          'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', \
                          'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',\
                          'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', \
                           'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', \
                          'with', 'about', 'against', 'between', 'into', 'through', 'during', \
                          'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', \
                          'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',\
                          'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',\
                          'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',\
                          'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', \
                          't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now',\
                          'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn',\
                          "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", \
                          'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', \
                          "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", \
                          'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', \
                          "won't", 'wouldn', "wouldn't"]
        
    def dataParse(self):        
        file = open(self.dataset,'r')

        read_target_sentence = False
        
        for line in file:
            sentence = line.strip()
            sentence = sentence.split()
            
            # Extract the sense & instance IDs and their corresponding target 
            # sentences:
            for word in sentence:
                if 'instance=' in word:
                    instance_id = word.split('=')[1][1:-1]
                    
                if 'senseid' in word:
                    sense = word.split('=')[1][1:-3]
                    
                elif '<context>' in word:  
                    read_target_sentence = True
                    target_sentence = []
                    
                elif '</context>' in word:
                    read_target_sentence = False
                    self.corpus.append([target_sentence, sense, instance_id])
                    target_sentence = []
                
                elif read_target_sentence:
                    target_sentence.append(word)
                    
        file.close()
    
    def fiveFoldValidation(self, mode):
        self.mode = mode
        size = int(math.ceil(len(self.corpus)/5))
        
        if mode == 1:
            self.test = self.corpus[:size]
        elif mode == 2:
            self.test = self.corpus[size:2*size]
        elif mode == 3:
            self.test = self.corpus[2*size:3*size]
        elif mode == 4:
            self.test = self.corpus[3*size:4*size]
        elif mode == 5:
            self.test = self.corpus[4*size:]
        else:
            print('Select the correct mode. Returning...')
            
        self.train = [row for row in self.corpus if row not in self.test]
            
        self.dict_sense = {}
        self.dict_word = {}
        self.dict_word_and_sense = {}
        self.y_sense = []
        self.y_sense_hat = []
    
    def dataClean(self, word):
        # Convert to lower case
        word = word.lower()
        
        # Remove punctuations at the begining and end of a word
        if word[-1] in self.punc_list:
            word = word[:-1]
        if word[0] in self.punc_list:
            word = word[1:]
            
        return word
        
    def computeRawCounts(self):
        
        for sentence, sense, instance_id in self.train:
            # Compute the raw counts
            self.dict_sense[sense] = self.dict_sense.get(sense, 0) + 1

            for word in sentence:     
                if '<head>' not in word:
                    # Remove punctuation instances
                    if len(word) == 1 and word in self.punc_list:
                        continue
                    
                    word = self.dataClean(word)
                                               
                    # Remove stopwords
                    if word in self.stop_words:
                        continue
                    
                    # # Split hyphenated words (For ex: top-rated, high-ranked etc)
                    # if len(word) > 1 and word.find("-") != -1:
                    #     words = word.split('-')
                    # else:
                    #     words.append(word)
                    # words.append(word)
                    # for wrd in words: 
                    self.dict_word[word] = self.dict_word.get(word, 0) + 1
                    word_and_sense = word + ' ' + sense
                    self.dict_word_and_sense[word_and_sense] = self.dict_word_and_sense.get(word_and_sense, 0) + 1
                    
    def naiveBayesClassifier(self):
        
        sum_sense = 0
        
        for counts in self.dict_sense.values():
            sum_sense = sum_sense + counts
            
        for sentence, sense, instance_id in self.test:
            self.y_sense.append(sense)
            
            scores = {}           
            for sense in self.dict_sense:
                score = 0
                for word in sentence:
                    if '<head>' not in word:
                        # Remove punctuation instances
                        if len(word) == 1 and word in self.punc_list:
                            continue
                        
                        word = self.dataClean(word)
                                                   
                        # Remove stopwords
                        if word in self.stop_words:
                            continue                        
                        
                        word_and_sense = word + ' ' + sense
                        # Laplace-Smoothing
                        if self.dict_word_and_sense.get(word_and_sense) == None:
                            likelihood = 1/(self.dict_sense[sense] + len(self.dict_word)) # count(sense) + Vocab(sense1) + Vocab(sense2)
                        else:
                            likelihood = (self.dict_word_and_sense[word_and_sense])/self.dict_sense[sense]
                        score = score + math.log(likelihood)
                
                score = score + math.log((self.dict_sense[sense])/sum_sense)
                scores[sense] = score
                
            max_score_sense = max(scores, key = scores.get)
            self.y_sense_hat.append(max_score_sense)
        
    def computeFoldAccuracy(self):
        correct = 0
        total = len(self.test)
        
        for prediction, label in zip(self.y_sense_hat, self.y_sense):
            if prediction ==  label:
                correct = correct + 1
                
        accuracy = correct/total*100
        print('<{}> Accuracy of the fold-{} validation: {:.2f} %' .format(self.dataset, self.mode, accuracy))
        
        self.totalCorrect = self.totalCorrect + correct
        
    def computeOverallAccuracy(self):
        accuracy = self.totalCorrect/len(self.corpus)*100
        print('<{}> Overall Accuracy of the WSD Classifier: {:.2f} %' .format(self.dataset, accuracy))
        
        
    def writeToFile(self):
        out_file = self.dataset + '.out'
        print('Writing data to {} ...' .format(out_file))
        
        if self.mode == 1:
            file = open(out_file, 'w')
        else:
            file = open(out_file, 'a')
            
        file.write('Fold {} \n' .format(self.mode))
        
        idx = 0
        for sentence, sense, instance_id in self.test:
            file.write(instance_id + ' ' + self.y_sense_hat[idx]+ "\n")
            idx = idx + 1
        
        file.write('\n')
        file.close()
        print('Done')
            
         
def main(args):
    
    dataset = args[1]

# Step 0: Create an instance of th WSD class
    wsdClassifier = WSD(dataset)
    
# Step 1: Parse the dataset to extract sentences along with their senses
    wsdClassifier.dataParse()
    
# Step 2: Prepare the dataset to perform the 1st 5-fold validation       
    wsdClassifier.fiveFoldValidation(1)
    
# Step 3: Compute the raw counts required for predicting the sense
    wsdClassifier.computeRawCounts()
    
# Step 4: Predict sense for a given test sequence using Naive Bayes Classifier
    wsdClassifier.naiveBayesClassifier()
    
# Step 5: Compute the accuracy of the fold
    wsdClassifier.computeFoldAccuracy()
    
# Step 6: Write prediction data to a file
    wsdClassifier.writeToFile()

# Step 7: Repeat the steps for all the remaining 5 folds    
    
    # 5-fold Validation 2
    wsdClassifier.fiveFoldValidation(2)
    wsdClassifier.computeRawCounts()
    wsdClassifier.naiveBayesClassifier()
    wsdClassifier.computeFoldAccuracy()
    wsdClassifier.writeToFile()
         
    # 5-fold Validation 3
    wsdClassifier.fiveFoldValidation(3)
    wsdClassifier.computeRawCounts()
    wsdClassifier.naiveBayesClassifier()
    wsdClassifier.computeFoldAccuracy()
    wsdClassifier.writeToFile()
    
    # 5-fold Validation 4
    wsdClassifier.fiveFoldValidation(4)
    wsdClassifier.computeRawCounts()
    wsdClassifier.naiveBayesClassifier()
    wsdClassifier.computeFoldAccuracy()
    wsdClassifier.writeToFile()
    
    # 5-fold Validation 5
    wsdClassifier.fiveFoldValidation(5)
    wsdClassifier.computeRawCounts()
    wsdClassifier.naiveBayesClassifier()
    wsdClassifier.computeFoldAccuracy()
    wsdClassifier.writeToFile()
    
# Step 8: Combine the correct predictions across all the folds and compute
# the overall accuracy:
    wsdClassifier.computeOverallAccuracy()
    
if __name__ == "__main__":
    main(sys.argv)
