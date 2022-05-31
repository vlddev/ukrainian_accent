from lib2to3.pgen2.tokenize import tokenize
import requests
import accent_db

MOVA_URL = "https://api.mova.institute/udpipe/process?tokenizer&tagger&parser&model=uk&data={0}"

def featureToUkTag(posTag, featureMap):
    ret = ''
    if len(featureMap) > 1:
        features = featureMap.split('|')
        fMap = dict()
        fMap['Gender'] = '-'
        fMap['Number'] = '-'
        fMap['Case'] = '-'
        for f in features:
            v = f.split('=')
            fMap[v[0]] = v[1]
        if posTag == 'NOUN':
            ret = 'N'+fMap['Gender'][0]+fMap['Number'][0]+fMap['Case'][0]
        elif posTag == 'VERB':
            # TODO extend
            ret = fMap['Aspect'][0]+fMap['VerbForm'][0]
        elif posTag == 'ADJ':
            ret = 'A'+fMap['Gender'][0]+fMap['Number'][0]+fMap['Case'][0]
    return ret

class TaggedToken:
    def __init__(self, wf, inf, posTag, featureMap):
        self.wf = wf
        self.accent = wf
        self.inf = inf
        self.posTag = posTag
        self.ukTag = featureToUkTag(posTag, featureMap).lower()

    def __repr__(self):
        return f'TaggedToken(wf={self.wf}, accent={self.accent}, inf={self.inf}, posTag={self.posTag}, ukTag={self.ukTag})'

    def setAccent(self, accent):
        self.accent = accent

class UDPipe:
    def __init__(self, url=MOVA_URL):
        self.url = url
        self.accentDb = accent_db.AccentDb()

    def tokenize(self, sent):
        ret = []
        response = requests.get(self.url.format(sent))
        json_dict = response.json()

        lines = json_dict["result"].split('\n')

        for line in lines:
            if line.startswith("#") or len(line) < 2: continue
            # print(line)
            vals = line.split('\t')
            taggedToken = TaggedToken(vals[1], vals[2], vals[3], vals[5])
            # TODO optimize 
            wfAccent = self.accentDb.getAccent(taggedToken.wf, taggedToken.ukTag)
            taggedToken.setAccent(wfAccent) 
            ret.append(taggedToken)
        return ret

    def setAccent(self, sent):
        ret = []
        tokens = self.tokenize(sent)
        tokCount = len(tokens) - 1
        for idx,item in enumerate(tokens):
            if idx > 0 and idx < tokCount and item.posTag != 'PUNCT':
                ret.append(" ")
            ret.append(item.accent)
        return "".join(ret)


# udpipe_url = "http://lindat.mff.cuni.cz/services/udpipe/api/process?tokenizer&tagger&parser&model=uk&data={0}"

"""
data = "співачки зізналися, що іноді можуть показати характер."
data = "що ти робиш, брате."
data = "сидить, як чорт у болоті."
data = "Немов снігом за шкуру сипнуло."
data = "Ми тримали гострі ножі."

udpipe = UDPipe()
[print(x) for x in udpipe.tokenize(data)]
print(udpipe.setAccent(data))
"""