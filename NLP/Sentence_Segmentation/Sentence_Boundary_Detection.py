# -*- coding: utf-8 -*-
"""
Sentence Boundary Detection

@author: Meeshawn Marathe
"""
#%%
import sys
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier

class SentenceBoundaryDetection:
    def __init__(self, train, test):
        self.train = train
        self.test = test
        self.classifier = DecisionTreeClassifier(random_state=0)
        
    def featureExtract(self, dataset):   
        # From the Pandas documentation, quoting = 3 implies ignoring all quotes
        # Had to add this argument to eliminate grouping of words under quotes
        # and resolve the parsing error

        # Troubleshooting reference:
        # https://stackoverflow.com/questions/18016037/pandas-parsererror-eof-character-when-reading-multiple-csv-files-to-hdf5

        df = pd.read_csv(dataset, sep = " ", quoting = 3, header = None)
        # Let us define a feature matrix "X" conatining the following features:
        #    X[n][0] = (L) Word to the left of "."  
        #    X[n][1] = (R) Word to the right of "." 
        #    X[n][2] = Length of L < 3 ??? (0 or 1)
        #    X[n][3] = is L capitalized??? (0 or 1)
        #    X[n][4] = is R capitalized??? (0 or 1)
        
        # Additional 3 features:
        #    X[n][5] = is L less than 3 AND capitalized???
        #    X[n][6] = is the word a period ???
        #    X[n][7] = Count of the number of periods in L
        
        #    where n is the 'nth' datapoint. A sum total of 8 features:

        X = np.empty((0,8))
        Y = np.empty((0,1))

        # Extracting words from the series data (df[1]) and building the feature
        # vector:
        idx = 0
        print("Extracting features and labels from {} ..." .format(dataset))
        for word in df[1]:
            if  word[-1] == ".":
                left = word[:-1]
                right = df[1][idx+1] if idx != len(df[1]) - 1 else ""
                L_less_than_3 = 1 if len(left) < 3 else 0
                L_capitalized = 1 if left!= "" and left[0].isupper() else 0
                R_capitalized = 1 if right!= "" and right[0].isupper() else 0 
        
                L_less_than_3_and_capitalized = L_less_than_3 and L_capitalized
                is_period = 1 if word == "." else 0
                
                L_num_of_periods = 0
                for ch in left:
                    if ch == ".":
                        L_num_of_periods = L_num_of_periods + 1
                
                # log_L_num_of_periods = np.log(L_num_of_periods) if L_num_of_periods!=0 else 0
                
                # L_num_of_NO_periods = len(left) - L_num_of_periods                
                # log_L_num_of_NO_periods = np.log(L_num_of_NO_periods) if L_num_of_NO_periods!=0 else 0
                
                # Converting text to numeric data
                left = len(left)
                right = len(right)
                
                features = np.array([[left, right, L_less_than_3 ,L_capitalized, R_capitalized, L_less_than_3_and_capitalized, is_period, L_num_of_periods]])
                # features = np.array([[left, right, L_less_than_3 ,L_capitalized, R_capitalized]])
                # features = np.array([[L_less_than_3_and_capitalized, is_period, L_num_of_periods]])
                
                X = np.append(X, features, axis=0)
                
                # Extracting the assigned labels Y associated with the dataset
                label = df[2][idx]
                Y = np.append(Y, np.array([[label]]), axis=0)
            idx = idx+1
        return X, Y
    
        # # Another method for mapping text data to numeric data (Gives ~93% accuracy)
        # print("Converting text data to numeric data within the feature matrix ...")
        # left_words = X[:,0]
        # right_words = X[:,1]
        # if dataset == self.train:
        #     words = np.append(left_words, right_words, axis = 0)
        #     self.word_map = dict([(n,m) for m,n in enumerate(sorted(set(words)))])
        
        # left_words_numeric = np.empty((0,1))
        # right_words_numeric = np.empty((0,1))
        
        # for left_word, right_word in zip(left_words, right_words):
        #     if self.word_map.get(left_word) == None:
        #         left_append = len(left_word)
        #     else:
        #         left_append = self.word_map.get(left_word)
        #     left_words_numeric = np.append(left_words_numeric, np.array([[left_append]]), axis = 0)
            
        #     if self.word_map.get(right_word) == None:
        #         right_append = len(right_word)
        #     else:
        #         right_append = self.word_map.get(right_word)
        #     right_words_numeric = np.append(right_words_numeric, np.array([[right_append]]), axis = 0)
        
        # idx = 0
        # for left_word, right_word in zip(left_words_numeric, right_words_numeric):
        #     X[idx,0] = left_word[0]
        #     X[idx,1] = right_word[0]
        #     idx = idx + 1
        # return X, Y
    
    def trainClassifier(self, X, Y):
        # For this assignment, we will be building a Decision Tree Classifier:  
        print("Building a decision tree classifier from the training set (X,Y) ...")
        self.classifier.fit(X,Y)
        
    def testClassifier(self, X_test):        
          
        print("Testing the trained Decision Tree Classifier on the feature matrix from {} ..." .format(self.test))
        Y_hat = self.classifier.predict(X_test)
        return Y_hat
            
    def computeAccuracy(self, Y_hat, Y_gold):        
        positives = 0
        for prediction, truth in zip(Y_hat, Y_gold):
            if truth[0] == prediction:
                positives = positives + 1

        accuracy = 100*positives/len(Y_hat)
        print("Accuracy of the SBD classifier: {:.3f} % ({}/{} words)" .format(accuracy, positives, len(Y_hat)))
        
    def writePredictionData(self, Y_hat):
        df = pd.read_csv(self.test, sep = " ", quoting = 3, header = None)
        
        idx = 0
        idx_predict = 0
        file = open("SBD.test.out", "w")
        print("\nWriting data to SBD.test.out ...")
        
        for word in df[1]:
            if  word[-1] == ".":
                label = Y_hat[idx_predict]    
                idx_predict = idx_predict + 1
            else:
                label = " "
            file.write(str(df[0][idx]) + " " + str(df[1][idx])  + " " + label + "\n")
            idx = idx + 1
        
        print("Sucessfully exported data to SBD.test.out")
        file.close()

   
def main(args):
    
    trainDataset = args[1]
    testDataset = args[2]
    
    # Step 0: Creating an object of the class SentenceBoundaryClassifier
    SBD = SentenceBoundaryDetection(trainDataset, testDataset)
    
    # Step 1: FEATURE EXTRACTION FROM TRAINING DATASET    
    X, Y = SBD.featureExtract(trainDataset)
    
    # Step 2: TRAINING A DECISION TREE CLASSIFIER
    SBD.trainClassifier(X, Y)
    
    # Step 3: FEATURE EXTRACTION FROM TEST DATASET
    X_test, Y_gold = SBD.featureExtract(testDataset)
    
    # Step 4: PREDICTING LABELS FOR TEST DATASET
    Y_hat = SBD.testClassifier(X_test)
    
    # Step 5: ACCURACY COMPUTATIONS
    SBD.computeAccuracy(Y_hat, Y_gold)
    
    # Step 6: WRITE PREDICTION DATA TO FILE
    SBD.writePredictionData(Y_hat)

if __name__ == "__main__":
    main(sys.argv)

