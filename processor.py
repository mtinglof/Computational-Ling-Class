import nltk
from nltk import bigrams 
from nltk import collocations
from nltk import FreqDist 
from nltk import word_tokenize
class processor:
    def __init__(self): 
        self.key_words = []
        self.key_phrases = []
        self.words_count = len(self.key_words)
        self.call_count = 0
        self.seek_count = 0
        self.personal_count = 0
        self.paths = [r'C:\Users\mting\Documents\Baye Ling\Baye-Ling\Callout.txt',   
         r'C:\Users\mting\Documents\Baye Ling\Baye-Ling\seeking.txt', r'C:\Users\mting\Documents\Baye Ling\Baye-Ling\personals.txt']
        self.tokens = {}
        self.call_dic = {}
        self.seek_dic = {}
        self.personal_dic = {}
        self.titles = ("callout", "seeking", "personals")
        self.totalword_count = {}

    def token(self): 
        for index, path in enumerate(self.paths):
            tokens = word_tokenize(open(path).read())
            self.totalword_count[self.titles[index]] = len(tokens)
            tester = FreqDist(list(bigrams(tokens)))
            f = open("results.txt", "a")
            f.write(str(tester.most_common(20)))
            self.tokens[self.titles[index]] = FreqDist([tokens.lower() for tokens in tokens])

    def freq(self): 
        self.token()
        call_dist = self.tokens['callout']
        seeking_dist = self.tokens['seeking']
        personal_dist = self.tokens['personals']
        for word in self.key_words: 
            self.call_dic[word] = call_dist[word]
            self.seek_dic[word] = seeking_dist[word]
            self.personal_dic[word] = personal_dist[word]
            # self.call_count = call_dist[word] + self.call_count
            # self.seek_count = seeking_dist[word] + self.seek_count
            # self.personal_count = personal_dist[word] + self.personal_count
        
    def prob(self, submit): 
        for word in submit:
            subtoken = word_tokenize(submit)
        same_words = []
        # seek_word_total = self.seek_count + self.words_count
        # call_word_total = self.call_count + self.words_count
        # personal_word_total = self.personal_count + self.words_count
        for word in subtoken: 
            for keyword in self.key_words: 
                if word.lower() == keyword: 
                    same_words.append(word.lower())
        prob_seek = 1
        prob_call = 1
        prob_personal = 1
        for word in same_words: 
            prob_seek = ((self.seek_dic[word]+1)/self.totalword_count['seeking'])*prob_seek
            prob_call = ((self.call_dic[word]+1)/self.totalword_count['callout'])*prob_call
        per_call = prob_call/(prob_call+prob_seek)
        per_seek = prob_seek/(prob_call+prob_seek)
        per_personal = prob_personal/(prob_call+prob_seek+prob_personal)
        # f = open("results.txt", "a")
        # if .75 > per_call and .75 > per_seek: 
        #     f.write("Personal " + str(per_seek) + " " + str(per_call) + "\n")
        # if per_call > per_seek: 
        #     f.write("Callout " + str(per_seek) + " " + str(per_call) + "\n")
        # else: 
        #     f.write("Seeking " + str(per_seek) + " " + str(per_call) + "\n")


           
test = processor()
items = test.freq()
tfile = open(r'C:\Users\mting\Documents\Baye Ling\Baye-Ling\personals.txt', "r")
for line in tfile:
    test.prob(line)
tfile.close()