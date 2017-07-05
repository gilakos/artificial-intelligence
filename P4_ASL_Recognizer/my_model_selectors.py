import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)

class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # TODO implement model selection using CV
        
        # create a temporary neg infinity best score
        best_score = float('-Inf')
        # create an empty best number of states
        best_num_components = None
        # define the number of splits for splitting method
        n_splits = 3
        # set the split method to kfold
        split_method = KFold(n_splits=n_splits)
        # loop through the options for number of components aka hidden states
        for num_components in range(self.min_n_components, self.max_n_components+1):
            # store the scores for this number of components
            n_scores = []
            # test if the length of the sequences is smaller than the number of splits
            if len(self.sequences) < n_splits:
                #print('sequences {} less than splits {} -> skipping...'.format(len(self.sequences), n_splits))
                # skip this test of folds
                continue
            # loop through the training and testing folds of the sequences
            for train_idx, test_idx in split_method.split(self.sequences):
                # get the training data with combine sequence utility function
                x_train, lengths_train = combine_sequences(train_idx, self.sequences)
                # get the testing data with combine sequence utility function
                x_test, lengths_test = combine_sequences(test_idx, self.sequences)
                # create the model
                model = GaussianHMM(n_components=num_components, n_iter=1000, random_state=self.random_state)
                # fit the model
                model.fit(x_train, lengths_train)
                # add try/except to eliminate non-viable models
                try:
                    # calculate the score of the model aka Log Likelihood
                    score = model.score(x_test, lengths_test)
                    # add score to list
                    n_scores.append(score)
                except:
                    pass
            # calculate the mean score
            n_mean = np.mean(n_scores)
            # test if this mean is better than current best score
            if n_mean > best_score:
                # update the best number of components
                best_num_components = num_components
                # update the best score
                best_score = n_mean
        # test if a best model was found
        if best_num_components is not None:
            #print('best number of components found -> {}'.format(best_num_components))
            return self.base_model(best_num_components)
        else:
            #print('best number of components not found -> returning constant {}'.format(self.min_n_components))
            return self.base_model(self.min_n_components)

class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score
    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components
        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # TODO implement model selection based on BIC scores

        # create a temporary pos infinity best score
        best_score = float('Inf')
        # create an empty best number of states
        best_num_components = None
        # set the n value for the BIC formula - constant for this model
        n_val = len(self.X)
        # loop through the options for number of components aka hidden states
        for num_components in range(self.min_n_components, self.max_n_components + 1):
            # set the p value for the BIC formula - constant for this loop
            p_val = num_components^2 + 2*num_components*len(self.X[0]) - 1
            # create the model
            model = GaussianHMM(n_components=num_components, n_iter=1000, random_state=self.random_state)
            # fit the model
            model.fit(self.X, self.lengths)
            # add try/except to eliminate non-viable models
            try:
                # calculate the score of the model aka Log Likelihood
                score = model.score(self.X, self.lengths)
                # calculate the BIC score
                bic = -2*score+p_val*math.log(n_val)
                # compare to best score
                if bic < best_score:
                    # update the best number of components
                    best_num_components = num_components
                    # update the best score
                    best_score = bic
            except:
                pass
        # test if a best model was found
        if best_num_components is not None:
            #print('best number of components found -> {}'.format(best_num_components))
            return self.base_model(best_num_components)
        else:
            #print('best number of components not found -> returning constant {}'.format(self.min_n_components))
            return self.base_model(self.min_n_components)


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion
    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components
        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # TODO implement model selection based on DIC scores

        # create a temporary pos infinity best score
        best_score = float('-Inf')
        # create an empty best number of states
        best_num_components = None

        # loop through the options for number of components aka hidden states
        for num_components in range(self.min_n_components, self.max_n_components + 1):
            # create a zero variable for the anti score (normalized score for all other worlds)
            anti_score = 0.0
            # create a counter for the other words
            word_count = 0
            # create the model
            model = GaussianHMM(n_components=num_components, n_iter=1000, random_state=self.random_state)
            # fit the model
            model.fit(self.X, self.lengths)
            # add try/except to eliminate non-viable models
            try:
                # calculate the score of the model aka Log Likelihood
                score = model.score(self.X, self.lengths)

                # loop through all the other words
                for word in self.hwords:
                    # check if other word is same as tested word
                    if word == self.this_word:
                        continue
                    # get testing data for other word
                    x_other, lengths_other = self.hwords[word]
                    try:
                        # calculate and update the antiscore
                        anti_score += model.score(x_other, lengths_other)
                        # update the word count
                        word_count += 1
                    except:
                        pass
                # normalize the antiscore
                anti_score /= float(word_count)

                # calculate the DIC score
                dic = score-anti_score
                # compare to best score
                if dic > best_score:
                    # update the best number of components
                    best_num_components = num_components
                    # update the best score
                    best_score = dic
            except:
                    pass
        # test if a best model was found
        if best_num_components is not None:
            #print('best number of components found -> {}'.format(best_num_components))
            return self.base_model(best_num_components)
        else:
            #print('best number of components not found -> returning constant {}'.format(self.min_n_components))
            return self.base_model(self.min_n_components)