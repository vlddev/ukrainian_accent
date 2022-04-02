import requests

def featureToUkTag(posTag, featureMap):
    ret = ''
    if len(featureMap) > 1:
        features = featureMap.split('|')
        fMap = dict()
        for f in features:
            v = f.split('=')
            fMap[v[0]] = v[1]
        if posTag == 'NOUN':
            ret = 'N'+fMap['Gender'][0]+fMap['Number'][0]+fMap['Case'][0]
        elif posTag == 'VERB':
            # TODO extend
            ret = fMap['Aspect'][0]+fMap['VerbForm'][0]
        elif posTag == 'ADJ':
            ret = fMap['Gender'][0]+fMap['Number'][0]+fMap['Case'][0]
    return ret

class TaggedToken:
    def __init__(self, wf, inf, posTag, featureMap):
        self.wf = wf
        self.inf = inf
        self.posTag = posTag
        self.ukTag = featureToUkTag(posTag, featureMap)

    def __repr__(self):
        return f'TaggedToken(wf={self.wf}, inf={self.inf}, posTag={self.posTag}, ukTag={self.ukTag})'

class UDPipe:
    def __init__(self, url):
        self.url = url

    def tokenize(self, sent):
        ret = []
        response = requests.get(udpipe_url.format(data))
        json_dict = response.json()

        lines = json_dict["result"].split('\n')

        for line in lines:
            if line.startswith("#") or len(line) < 2: continue
            print(line)
            vals = line.split('\t')
            ret.append(TaggedToken(vals[1], vals[2], vals[3], vals[5]))
        return ret


# udpipe_url = "http://lindat.mff.cuni.cz/services/udpipe/api/process?tokenizer&tagger&parser&model=uk&data={0}"
udpipe_url = "https://api.mova.institute/udpipe/process?tokenizer&tagger&parser&model=uk&data={0}"

data = "співачки зізналися, що іноді можуть показати характер."
data = "що ти робиш, брате."
data = "сидить, як чорт у болоті."
data = "Немов снігом за шкуру сипнуло."

udpipe = UDPipe(udpipe_url)
print(udpipe.tokenize(data))