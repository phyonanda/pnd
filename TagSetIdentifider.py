def searchTagSetInLine(file,search_word):
    temp = ',' + search_word + ','
    r_Lines =[]
    found_Lines = []
    f = open(file, encoding="utf16")
    r_Lines = f.readlines()
    new_line = list(map(lambda line : line.strip(), r_Lines))
    for i in range(len(new_line)):
        if (temp in new_line[i]) :
           
            found_Lines.append(new_line[i])
    f.close()
    return (found_Lines)


