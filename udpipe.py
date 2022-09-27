#from lib2to3.pgen2.tokenize import tokenize
from transformers import TokenClassificationPipeline, AutoTokenizer, AutoModelForTokenClassification
import requests
import accent_db
import get_predictions

# MOVA_URL = "https://api.mova.institute/udpipe/process?tokenizer&tagger&parser&model=uk&data={0}"
MOVA_URL = "http://lindat.mff.cuni.cz/services/udpipe/api/process?tokenizer&tagger&parser&model=uk&data={0}"

verbTenseMap = {'Pres':'P', 'Past':'O', 'Fut':'F', '-':'-'}

def featureToUkTag(posTag, featureMap):
    ret = ''
    if len(featureMap) > 1:
        features = featureMap.split('|')
        fMap = dict()
        fMap['Gender'] = '-'
        fMap['Number'] = '-'
        fMap['Case'] = '-'
        fMap['Person'] = '-'
        fMap['Tense'] = '-'
        for f in features:
            v = f.split('=')
            fMap[v[0]] = v[1]
        if posTag == 'NOUN':
            ret = 'N'+fMap['Gender'][0]+fMap['Number'][0]+fMap['Case'][0]
        elif posTag == 'VERB':
            # TODO extend
            ret = 'V'+fMap['Gender'][0]+fMap['Number'][0]+fMap['Person'][0]+verbTenseMap[fMap['Tense']]
            #+fMap['Aspect'][0]+fMap['VerbForm'][0]+fMap['Mood'][0]
        elif posTag == 'ADJ':
            ret = 'A'+fMap['Gender'][0]+fMap['Number'][0]+fMap['Case'][0]
        elif posTag == 'ADV':
            ret = 'D'
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
        self.accentDb = accent_db.AccentDb(useAmbiguous=True)

    def tokenize(self, sent):
        ret = []
        response = requests.get(self.url.format(sent))
        json_dict = response.json()

        lines = json_dict["result"].split('\n')
        print(json_dict["result"])

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

class UkBert:
    # use pretrained BERT-Model from
    # https://huggingface.co/ukr-models/uk-morph
    # stored locally
    def __init__(self):
        self.accentDb = accent_db.AccentDb(useAmbiguous=True)
        self.tokenizer = AutoTokenizer.from_pretrained('../rnn_pos_tagging/uk-morph')
        self.model = AutoModelForTokenClassification.from_pretrained('../rnn_pos_tagging/uk-morph')

    def tokenize(self, sent):
        ret = []
        res = get_predictions.get_word_predictions(self.model, self.tokenizer, [sent])

        wfs = res[0][0]
        features = res[1][0]
        for idx,wf in enumerate(wfs):
            if '__' in features[idx]:
                data = features[idx].split('__')
                posTag = data[0]
                ukrFeatures = data[1]
            else:
                posTag = features[idx]
                ukrFeatures = ''
            taggedToken = TaggedToken(wf, wf, posTag, ukrFeatures)
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

data = "співачки зізналися, що іноді можуть показати характер."
data = "Немов снігом за шкуру сипнуло."
data = "Ми тримали гострі ножі."
data = "що ти робиш, брате."
data = "Дівчина співає пісню."
data = "Я співаю пісню."
data = "Хлопець співав пісню."
data = "Дівча співало пісню."
data = "Ми співаєм пісню."
data = "Ти співаєш пісню."
data = "Вони співають пісню."
data = "Співати завжди весело."
data = "Ми любимо співати."
data = "Співай, мій соловейку."
data = "Тому й ми співаймо, Христа прославляймо."
data = "Я співайтиму для нього."
data = "Дівчина співала пісню."
data = "сидить, як чорт у болоті."
data = "Вона весь день пекла хліб."
data = "Я отримав подарунок з пекла."
data = "тепло може передаватися між тілами за допомогою теплопровідності."
data = "В квартирі було тепло."
data = "Коли вже стане тепло?"
data = "Сьогодні дуже тепло."
data = "Я отримав подарунок з пекла."

# udpipe = UDPipe()
udpipe = UkBert()
[print(x) for x in udpipe.tokenize(data)]
print(udpipe.setAccent(data))
