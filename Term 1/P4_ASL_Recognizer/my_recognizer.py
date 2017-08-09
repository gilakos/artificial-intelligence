import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    
    # get the word set
    hwords = test_set.get_all_Xlengths()
    
    # loop through all of the words
    for word_id in range(0, len(test_set.get_all_Xlengths())):
        # create dictionary for this word's probabilities
        word_prob = {}
        # set the best score to neg infinity
        best_score = float('-Inf')
        # create an empty guess
        guess_word = None
        # get the training values for this word
        X, lengths = hwords[word_id]

        # loop through the word-model pairs in models input
        for word, model in models.items():
            try:
                # get the score
                score = model.score(X, lengths)
                # add the score to the word probabilities
                word_prob[word] = score
                # check if the score is better than best
                if score > best_score:
                    # update guess
                    guess_word = word
                    # update best score
                    best_score = score
            except:
                pass
        probabilities.append(word_prob)
        guesses.append(guess_word)
    return probabilities, guesses
