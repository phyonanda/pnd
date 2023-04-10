
def countPOSInLine(file,search_word):
    r_Lines =[]
    found_Lines = []
    count = 0
  
    f = open(file, encoding="utf8")
    r_Lines = f.readlines()
    new_line = list(map(lambda line : line.strip(), r_Lines))
    for i in range(len(new_line)):
        segline = new_line[i].split('#')
        for j in range (len(segline)):
            if (search_word == segline[j]) :
                count = count + 1
        
                
    f.close()
    return (count)

def countPOSInLine2(file,search_word):

    r_Lines =[]
    found_Lines = []
    count = 0
   
    f = open(file, encoding="utf8")
    r_Lines = f.readlines()
    new_line = list(map(lambda line : line.strip(), r_Lines))
    for i in range(len(new_line)):
        segline = new_line[i].split('#')
        secondseglines = iter(segline)
        next(secondseglines)
        out = ['#'.join((first,second))
               for first,second in zip(segline,secondseglines)]
        for j in range (len(out)):
            if (search_word == out[j]) :
                count = count + 1
          
    f.close()
    return (count)

def searchPOSInLine3(file,search_word):
   
    r_Lines =[]
    found_Lines = []
    
  
    f = open(file, encoding="utf8")
    r_Lines = f.readlines()
    new_line = list(map(lambda line : line.strip(), r_Lines))
    
    for i in range(len(new_line)):
        segline = new_line[i].split('#')
        for j in range (len(segline)):
            if (search_word == segline[j]) :
            
        
                found_Lines.append(new_line[i])
    f.close()
    return (found_Lines)

def counting_one_line(pos_searchline,tok):
    k = 0
    for i in range(len(pos_searchline)):

        q = str(pos_searchline[i])
        k = k + q.count(tok)
    return(k)

def total_counting(func,pos):
    if func == 'current':
        s = countPOSInLine("pos_sentance.txt",pos)
    else:
        s = countPOSInLine2("pos_sentance.txt",pos)
        
    counter = 0
    counter = counter + counting_one_line(s, pos)
    return(counter)

def respective_counter(func,tokenlist):
    respective_count = []
    for k in range(len(tokenlist)):
        respective_count.append(total_counting(func,str(tokenlist[k])))
    return(respective_count)



