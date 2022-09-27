from pathlib import Path
import tokenize_uk
import udpipe

def gen_out_file(filename, suffix='_acc'):
  p = Path(filename)
  return "{0}{1}{2}".format(Path.joinpath(p.parent, p.stem), suffix, p.suffix)

def process(file):
    # udpipeProcessor = udpipe.UDPipe()
    udpipeProcessor = udpipe.UkBert()
    text = ''
    with open(file, "r") as infile:
        text = infile.read()
    parList = tokenize_uk.text2sent(text)
    
    with open(gen_out_file(inFile), 'w') as outFile:
        for par in parList:
            outFile.write("\n")
            for sent in par:
                outFile.write(udpipeProcessor.setAccent(sent))
                outFile.write("\n")


inFile = 'test.txt'
process(inFile)