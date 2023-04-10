def searchInLine(file,search_word):
    temp = search_word + '#'
    r_Lines =[]
    found_Lines = []
   
    f = open(file, encoding="utf8")
    r_Lines = f.readlines()
    new_line = list(map(lambda line : line.strip(), r_Lines))
    for i in range(len(new_line)):
        if temp in new_line[i]:
            
            segline = new_line[i].split()
            for j in range (len(segline)):
               
                if (search_word == segline[j].split('#')[0]):
                   
                    if segline[j].split('#')[1] not in found_Lines:
                        found_Lines.append(segline[j].split('#')[1])
    f.close()
    return (found_Lines)



def PostokenSegmentation(str):
    tokens = list(str.split('#'))
    return tokens

def tokenSegmentation(str):
    tokens = list(str.split(' '))
    return tokens

def tokenmatching(segTokens,search_token):
    q = []
    temp = search_token + '#'
    for i in range (len(segTokens)):
        
        if temp in segTokens[i]:
           

            s = segTokens[i].split('#')[1]


            q.append(s)
    return q

def POStokenmatching(func,segTokens,search_token):
    q = []

    for i in range (len(segTokens)):
        
        if search_token == segTokens[i]:
          
            if (func == 'withnext'):
                if (i == len(segTokens) - 1):
                    s = None
                else:
                   
                    s = segTokens[i] + '#' + segTokens[i+1]
            elif(func == 'withprevious'):
                if (i == 0):
                    s = None

                else:
                    s = segTokens[i-1] + '#' + segTokens[i]
            elif(func == 'current'):
                s = segTokens[i]


            q.append(s)
    return q

def token_matcher(list1,list2):
    matchlist = []
    for i in range (len(list1)):
        if list1[i] in list2:
            matchlist.append(list1[i])
    if None in matchlist:
        matchlist.remove(None)
    return matchlist

def token_Equalizer(searching,Searchinglist):
    temp = False
    for item in range (len(Searchinglist)):
        if searching == Searchinglist[item]:
            temp = True
    return (temp)



