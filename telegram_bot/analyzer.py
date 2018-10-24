import nltk
import re
import pymorphy2

nltk.download("punkt")


class Analyzer:

    def __init__(self, content):
        self.content = content

    def get_stats(self):

        # tokenize paragraphs into words and sentences
        text = ' '.join(self.content)
        words = nltk.tokenize.word_tokenize(re.sub("[^\w\s]", " ", text), language='english')
        sentences = nltk.tokenize.sent_tokenize(text, language='english')

        # get rid of empty tokens
        while '' in words:
            words.remove('')
        while ' ' in words:
            words.remove(' ')
        while '' in sentences:
            sentences.remove('')
        while ' ' in words:
            sentences.remove(' ')

        # count words, sentences and characters
        W = len(words)
        S = len(sentences)
        C = len(''.join(words))

        # yields error-message for pages with no text in <p>
        if (W == 0) or (S == 0) or (C == 0):
            return 'Error. Blank Web-page. Word/Sentence count in <p> is 0'

        # Automated Readability Index: longer words and longer sentences
        # make sentences harder to understand
        ARI = 4.71 * C / W + 0.5 * W / S - 21.43
        grade = 'N/A'
        if ARI <= 4:
            grade = 'elementary'
        elif ARI <=10:
            grade = 'middle'
        elif ARI <=12:
            grade = 'high'
        elif ARI <= 13:
            grade = 'college'
        elif ARI > 13:
            grade = 'graduate'

        # find 10 most frequent words on the page
        m = pymorphy2.MorphAnalyzer()
        lemmas = [m.parse(token)[0].normal_form for token in words]
        top_10 = nltk.FreqDist(lemmas).most_common(10)

        # prepare report
        stats = {'word count': W,
                 'sentence count': S,
                 'characters count': C,
                 'ARI-readability': ARI,
                 'text complexity': grade,
                 'top-10': top_10}

        return stats
