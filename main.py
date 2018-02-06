import os

from data.scripts import json_to_text, cleaner, createDatasets
import learning.Classifiers as clf

# Origin datafile downloaded from jmcauley.ucsd.edu/data/amazon/ in ORIGIN_FOLDER_1
ORIGIN_FOLDER_1 = "../data/data_books"
ORIGIN_FOLDER_2 = "../data/data_video" # eg (we will learn video data from books)

# In this folder are files such that : 
# - every line is of the form "[original ratings]\t[original review]"
STRIPPED_METADATA_FOLDER_1 = "data/data_books_stripped"
STRIPPED_METADATA_FOLDER_2 = "data/data_videos_stripped"

# In this folder are files such that : 
# - every line is of the form "[new ratings]\t[list of relevant words]" with [new ratings] in {"Negative", "Neutral", "Positive"}
CLEANED_DATA_FOLDER_1 = "../data/data_books_cleaned"
CLEANED_DATA_FOLDER_2 = "../data/data_videos_cleaned"

TRAINING_SET_FOLDER_1 = "../data/data_books_training_set"
TESTING_SET_FOLDER_1 = "../data/data_books_testing_set"
TRAINING_SET_FOLDER_2 = "../data/data_videos_training_set"
TESTING_SET_FOLDER_2 = "../data/data_videos_testing_set"

DICT_WORDS = "../data/dict_words/20k.txt"

def stripMetadata(source_folder, target_folder):
    """
    Get files from the folder [source_folder], 
    Perfom the stripping
    Put the results in file (or files) in target_folder
    """
    json_to_text.JsonHandler(source_folder, target_folder).convert()

def simplifyRatingAndKeepRelevantWords(source_folder, target_folder):
    """
    Get files from the folder [source_folder], 
    Simplify the rating and keep relevant words only
    Put the results in file (or files) in target_folder
    """
    cleaner.TextCleaner(source_folder, target_folder).clean()
    
    
def createTrainingSetAndTestSet(source_folder, target_training_set_folder, target_testing_set_folder):
    nb_train, nb_test = createDatasets.createDataset(source_folder, target_training_set_folder, target_testing_set_folder)
    print("{} files written in {}".format(nb_train, target_training_set_folder))
    print("{} files written in {}".format(nb_test, target_testing_set_folder))



def learn(training_set_folder):
    print("========================")
    print("|        TRAIN         |")
    print("========================")

    return clf.learn(training_set_folder, False)



def transferLearn(old_model, training_set_folder):
    return old_model



def showResults(model, testing_set_folder):
    print("========================")
    print("|        TEST          |")
    print("========================")
    clf.showResults(model, testing_set_folder)



if __name__ == "__main__":
    ## Pre-processing for the two datasets.
    print("\n--- PREPROCESSING ---")
    #stripMetadata(ORIGIN_FOLDER_1, STRIPPED_METADATA_FOLDER_1)
    #simplifyRatingAndKeepRelevantWords(STRIPPED_METADATA_FOLDER_1, CLEANED_DATA_FOLDER_1)

    #stripMetadata(ORIGIN_FOLDER_2, STRIPPED_METADATA_FOLDER_2)
    #simplifyRatingAndKeepRelevantWords(STRIPPED_METADATA_FOLDER_2, CLEANED_DATA_FOLDER_2)

    # Learning
    print("\n--- LEARNING FROM DATASET 1 ---")
    #createTrainingSetAndTestSet(CLEANED_DATA_FOLDER_1, TRAINING_SET_FOLDER_1, TESTING_SET_FOLDER_1)
    
    model1 = learn(TRAINING_SET_FOLDER_1)
    showResults(model1, TESTING_SET_FOLDER_1)

    # TransferLearning
    print("\n--- TRANSFER LEARNING FROM DATASET 1 APPLIED TO DATASET 2---")
    #createTrainingSetAndTestSet(CLEANED_DATA_FOLDER_2, TRAINING_SET_FOLDER_2, TESTING_SET_FOLDER_2)
    model2 = transferLearn(model1, TRAINING_SET_FOLDER_2) # <---- Difference here!!
    showResults(model2, TESTING_SET_FOLDER_2)


