import nltk
import re
import pymorphy2


class Analyzer:

    def __init__(self, content):
        self.content = content

    def get_stats(self):
        text = ' '.join(self.content)
        words = nltk.tokenize.word_tokenize(re.sub("[^\w\s]", " ", text), language='english')
        sentences = nltk.tokenize.sent_tokenize(text, language='english')

        while '' in words:
            words.remove('')
        while ' ' in words:
            words.remove(' ')
        while '' in sentences:
            sentences.remove('')
        while ' ' in words:
            sentences.remove(' ')

        W = len(words)
        S = len(sentences)
        C = len(''.join(words))

        ARI = 4.71 * C / W + 0.5 * W / S - 21.43
        grade = 'N/A'
        if ARI <= 4:
            grade = 'elementary'
        elif ARI <=10:
            grade = 'middle'
        elif ARI <=12:
            grade = 'high'
        elif ARI == 13:
            grade = 'college'
        elif ARI >= 13:
            grade = 'graduate'

        m = pymorphy2.MorphAnalyzer()
        lemmas = [m.parse(token)[0].normal_form for token in words]
        top_10 = nltk.FreqDist(lemmas).most_common(10)

        stats = {'word count': W,
                 'sentence count': S,
                 'characters count': C,
                 'ARI-readability': ARI,
                 'text complexity': grade,
                 'top-10': top_10}

        return stats
