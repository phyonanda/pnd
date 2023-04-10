def fetchingavaliablePOS():
    Pos_tag_list = []
    r_Lines =[]
                
                
    f = open('POS.txt', encoding="utf-16")
    r_Lines = f.readlines()
    new_line = list(map(lambda line : line.strip(), r_Lines))
    for i in range(len(new_line)):
        
        li = new_line[i].split(',')[1]
        Pos_tag_list.append(li)

    return Pos_tag_list
                    

    f.close()

