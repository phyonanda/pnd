def creating_pos_grammer_sentance_file():
    count = 0
    f = open("learned_sentence.txt", 'w+',encoding="utf8")
    g = open("pos_sentance.txt", 'w+',encoding="utf8")
    inputString = ""
    inputFile = open("tagged_corpus.txt", 'r',encoding="utf8")

    if inputFile.mode == 'r':
        inputString = inputFile.readlines()
   
    for line in inputString:
        output = line.split('#')
        count = 0
        for temp in output:
            jput = temp.split()

            for tem in jput:
                count += 1
                if (count % 2 == 1):
                    if (count == 1):
                        f.write(tem)
                    else:
                        f.write('$' + tem)
                else:
                    if (count == 2):
                        g.write(tem)
                    else:
                        g.write('#' + tem)
        f.write('\n')
        g.write('\n')


def countingTrainedWords():
    file = open("tagged_corpus.txt","rt",encoding="utf8")
    data = file.read()
    words = data.split()
    print('Number of trained words: ', len(words))

def countingTrainedSentance():
    num_lines = 0
    with open('tagged_corpus.txt', 'r',encoding="utf8") as f:
        for line in f:
            num_lines += 1
    print("Number of trained lines:",num_lines)

def addlinetofile(file,x):
    with open(file, "a" ,encoding = 'utf-8') as myfile:
        myfile.write('\n'+ x)


creating_pos_grammer_sentance_file()
print('Successfully loaded')
countingTrainedWords()
countingTrainedSentance()
