__author__ = 'teng.gao'


class Word(object):
    def __init__(self, wordObject):
        self.wordsId = wordObject[0]
        self.wordsContent = wordObject[1]
        self.parentsID = wordObject[2]
        self.publishTime = wordObject[3]
        self.raiseflag = wordObject[4]

    def getDic(self):
        return {'wordsId': self.wordsId, 'wordsContent': self.wordsContent, 'parentsID': self.parentsID,
                'publishTime': self.publishTime, 'raiseflag': self.raiseflag}

