"""
import useful libraries to project
"""
try:
    import re
    import string
    from app.data_base import DataBase

except ImportError:
    print("Need to fix the installation")
    raise

"""
return to user the sentences that maybe he want to complete
"""
class AutoCompleteData:

    database = DataBase()

    def __init__(self, input):
        self.completed_sentence = input
        self.current_completed_sentence = input
        self.sentences = []
        # for calculate score in 'add_char' and 'delete_char'
        self.point_add_del = {0:10, 1:8, 2:6, 3:4}
        self.all_sentences = []

    """
    check if current sentence match to return to user -
    the words that user enter need to be orderly in sentence like user enter and all words need to be in sentence if it is -return true else return false
    """
    def check_all_sentence(self, sentence):
        # loop over on all words that user enter
        for i in range(len(self.current_completed_sentence)):
            # this variable hold the first word that user enter without reference to special chars
            tmp_sentences = re.sub('[!@#$%^&*().,;:/?><"\']', "", sentence[0].lower())
            # this variable hold the current word that user enter without reference to special chars
            new_name = re.sub('[!@#$%^&*().,;:/?><"\']', "", self.current_completed_sentence[i])
            # check if all words that user enter exist in same sentence
            if new_name not in tmp_sentences:
                return False
            if i != len(self.current_completed_sentence) - 1:
                # if words that user enter in sentence but exist another word between the words that user exist
                # then return false
                if tmp_sentences.find(
                        re.sub('[!@#$%^&*().,;:/?><"\']', "", self.current_completed_sentence[i + 1])) != (
                tmp_sentences).find(new_name) + len(new_name) + 1:
                    return False
        return True

    """
    get from database all sentence that contain the first word that user enter and call to 'check_all_sentence'
    that check if this sentence can return to user and call to 'add_char', 'delete_char' and 'change_char'
    in order to try to return user sentences with fix word to word that user enter  
    """
    def find_string(self):
        # if word that user enter in database then check if sentences in database is match to return to user
        try:
            # get value of the first word that user enter the value is array of sentences that the first word that user enter in these sentences
            # over on these sentences in 'for' loop
            for i in AutoCompleteData.database.get(
                    re.sub('[!@#$%^&*().,;:/?><"\']', "", self.current_completed_sentence[0])):
                # check if return the current sentence to user
                if self.check_all_sentence(i):
                    self.sentences.append((i[0], 0))

        except:
            pass
        # in order to improve the auto complete data the system also look for word that same to word that user enter
        # like delete one char from word that user enter or add a char to the word or change a char in word
        # to another char
        self.add_char()
        self.delete_char()
        self.change_char()
        # user get only 5 sentences, so sort the sentences according the score from low to high
        # and return the first five with low score
        self.sentences.sort(key=lambda tup: tup[1])
        # the user get only 5 sentences to complete
        for i in range(len(self.sentences[:5])):
            # print to user the score of sentence and sentence
            print(str(i+1)+": " + "score: " + str(self.sentences[i][1]) + " " + str(self.sentences[i][0]))

    """
    function that try to delete char to word that user enter 
    """
    def delete_char(self):
        fixed_words_and_scores = []
        # over all words that user enter
        for index_word in range(len(self.current_completed_sentence)):
            arr = []
            # over on length of word that user enter
            for i in range(len(self.completed_sentence[index_word])):
                # calculate score for each word that fix, the score is according to location the char that deleted in word
                # if location in begin of word the score is 10 else the score being small
                try:
                    score_to_decrease = self.point_add_del[i]
                # if location of deleted char in word in after 5 chars the score is 1
                except:
                    score_to_decrease = 1
                # append tuple of the fix word and its score to array
                arr.append((self.current_completed_sentence[index_word][:i]+self.current_completed_sentence[index_word][i+1:], score_to_decrease))
            # append to array the basic word that user enter, without fix the word
            arr.append((self.current_completed_sentence[index_word], 0))
            # 'fixed_words_and_scores' is array of arrays of tuple of fix word and its score len of 'fixed_words_and_scores' is number of word that user
            # enter, each array in 'fixed_words_and_scores' contain tuples for another word that user enter
            fixed_words_and_scores.append(arr)
        # send the 'fixed_words_and_scores' to 'check_sentences_for_fix_word' function that check which sentences with fix word can return to user
        self.check_sentences_for_fix_word(fixed_words_and_scores)

    """
    function that try to add char from word that user enter
    """
    def add_char(self):
        fixed_words_and_scores = []
        # over all words that user enter
        for index_word in range(len(self.current_completed_sentence)):
            arr = []
            # over on length of word that user enter
            for i in range(len(self.current_completed_sentence[index_word])+1):
                # calculate score for each word that fix, the score is according to location the char that added to word
                # if location in begin of word the score is 10 else the score being small
                try:
                    score_to_decrease = self.point_add_del[i]
                # if location of added char in word in after 5 chars the score is 1
                except:
                    score_to_decrease = 1
                # over all the alphabet and try to add each char to word
                for char in string.ascii_lowercase:
                    # append tuple of the fix word and its score to array
                    arr.append((self.current_completed_sentence[index_word][:i]+char+self.current_completed_sentence[index_word][i:], score_to_decrease))
            # append to array the basic word that user enter, without fix the word
            arr.append((self.current_completed_sentence[index_word], 0))
            # 'fixed_words_and_scores' is array of arrays of tuple of fix word and its score len of 'fixed_words_and_scores' is number of word that user
            # enter, each array in 'fixed_words_and_scores' contain tuples for another word that user enter
            fixed_words_and_scores.append(arr)
        # send the 'fixed_words_and_scores' to 'check_sentences_for_fix_word' function that check which sentences with fix word can return to user
        self.check_sentences_for_fix_word(fixed_words_and_scores)

    """
    function that try to change a char from word that user enter
    """
    def change_char(self):
        # for calculate score
        point = {0:5, 1:4, 2:3, 3:2, 4:1}
        fixed_words_and_scores = []
        # over all words that user enter
        for index_word in range(len(self.current_completed_sentence)):
            arr = []
            # over on length of word that user enter
            for i in range(len(self.current_completed_sentence[index_word])):
                # over all the alphabet and try to add each char to word
                for char in string.ascii_lowercase:
                    # calculate score for each word that fix, the score is according to location the new char in word
                    # if location in begin of word the score is 5 else the score being small
                    try:
                        score_to_decrease = point[i]
                    # if location of new char that change to word in after 5 chars the score is 1
                    except:
                        score_to_decrease = 1
                    # append tuple of the fix word and its score to array
                    arr.append((self.current_completed_sentence[index_word][:i]+char+self.current_completed_sentence[index_word][i+1:], score_to_decrease))
            # append to array the basic word that user enter, without fix the word
            arr.append((self.current_completed_sentence[index_word], 0))
            # 'fixed_words_and_scores' is array of arrays of tuple of fix word and its score len of 'fixed_words_and_scores' is number of word that user
            # enter, each array in 'fixed_words_and_scores' contain tuples for another word that user enter
            fixed_words_and_scores.append(arr)
            # send the 'fixed_words_and_scores' to 'check_sentences_for_fix_word' function that check which sentences with fix word can return to user
            self.check_sentences_for_fix_word(fixed_words_and_scores)

    """
    function that get array of arrays that each array contain tuples with fix word and its score
    and check the append to 'sentences' the sentences that contain every words that user enter but
    try it on fix words
    """
    def check_sentences_for_fix_word(self, fixed_words_and_scores):
        # over on array of arrays of fix words
        for l in range(len(fixed_words_and_scores)):
            # over on each array in array of arrays
            for j in range(len(fixed_words_and_scores[l])):
                # assignment to 'self.current_completed_sentence' each fix word.
                # ([0] it is to get only the fix word and not its score)
                self.current_completed_sentence[l] = fixed_words_and_scores[l][j][0]
                try:
                    # get sentences from database that contain the current fix word
                    for i in AutoCompleteData.database.get(
                            re.sub('[!@#$%^&*().,;:/?><"\']', "", self.current_completed_sentence[0])):
                        # call function 'check_all_sentence' and send each sentence to check if this sentence can return
                        # to user. and check that this sentence not already exist in 'self.sentences' who hold all sentence
                        # that return to user
                        if self.check_all_sentence(i) and i[0] not in [j[0] for j in self.sentences]:
                            # append the sentence and score
                            self.sentences.append((i[0], fixed_words_and_scores[l][j][1]))
                except:
                    pass
