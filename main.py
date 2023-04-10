import tkinter as tk
from tkinter import messagebox, Tk
import ctypes
from tokenSearcher import searchInLine
from tokenSearcher import tokenSegmentation
from tokenSearcher import tokenmatching
from tokenSearcher import token_matcher
from  tokenSearcher import POStokenmatching
from tokenSearcher import PostokenSegmentation
from scipy.stats import entropy
from file_loading import creating_pos_grammer_sentance_file , addlinetofile
from posCounter import respective_counter
from posCounter import searchPOSInLine3
from  DeterminingPOSTag import compareTwoambigousTag
from  DeterminingPOSTag import calculatingEntropy
from TagSetIdentifider import searchTagSetInLine
from avaliable_pos_fetcher import fetchingavaliablePOS
import copy
import sys
import os



def alert(title, message, kind='info',hidemain=True ):
    if kind not in ('error', 'warning', 'info'):
        raise ValueError('Unsupported alert kind.')

    show_method = getattr(messagebox, 'show{}'.format(kind))
    show_method(title, message)




def backToMain():
    newWindow.destroy()
    root.deiconify()

def createAddframe():
    global AddWindow
    AddWindow = tk.Toplevel(newWindow)
    AddWindow.after(500,newWindow.withdraw )

    

    b8 = Button(AddWindow,text='Back',command = backToResultWindow)
    b8.pack()

    var31 = StringVar()
    label31 = Label( AddWindow, textvariable=var31, relief='flat',fg='red')
    var31.set("Note: This is Developer developer options\n If You are not the developer Please do not use it.")
    label31.pack()

    var32 = StringVar()
    label32 = Label(AddWindow, textvariable=var32, relief='flat')
    var32.set("When you add the sentance, \n 1. Each word in sentance must has its coresponding Tag with # between \n 2. Each word must be delimt by only one space \n Eg Sentance.. မမ#NPR က#VAC နေသည်#POVP")
    label32.pack()

    

    
    scrollbar2 = Scrollbar(AddWindow,orient=HORIZONTAL)
    global ez
    ez = Entry(AddWindow, width = 100,xscrollcommand=scrollbar2.set)
    ez.pack(fill = X)
    ez.focus_set()

    scrollbar2.config( command = e.xview )
    scrollbar2.pack(fill = X)
    
    AddWindow.bind('<Return>',AddSentanceToCorpus)
    b4 = Button(AddWindow,text='Enter',command=AddSentanceToCorpus)
    b4.pack()
    AddWindow.mainloop()


def backToResultWindow():
    AddWindow.destroy()
    newWindow.deiconify()
    
    
def AddSentanceToCorpus(event=None):
    iline = ez.get()
    words = list(iline.split(' '))

    if (iline==''):
        alert('Null Sentence Error','PLease Enter A Sentence!!!',kind='error')

    elif( ' ' not in  iline or '#' not in iline):
        alert('Delimiter Error','Please Enter A sentence with space and #',kind='error')

    elif(iline[0] == '#' or iline[-1] == '#'):
        print('Delimiter Error',' Do not enter # at the end or start of sentence',kind='error')
        

    elif('  ' in iline):
        print('Input Sentence Error',' Please use the delimiter space only once',kind='error')

    elif(' # ' in iline):
        print('Input Sentence Error',' Tag set or word is missing in the sentance please check the sentance',kind='error')
        
        

    elif(words[-1] == '' or words[0] == ''):
        print('Delimiter Error',' Do not enter space at the end or start of sentence!!!',kind='error')

    elif(iline.count('#') != len(words)):
        print('Tag set Error',' There are some word without Tag set',kind='error')


    else:
        avaliable_pos = fetchingavaliablePOS()
        print(avaliable_pos)
        cond = True
        print('good')
        #print(words)
        pos_word_arr = []
        myanmar_word_arr = []
        for word in range (len(words)):
            if (words[word].split('#')[1] not in avaliable_pos):
                cond = False
                pos_word_arr.clear()
                myanmar_word_arr.clear()
                
                print('Data Integrity Constraint','Some Pos Tag Set in sentance is not avaliable',kind='error')
                break

            else:
                pos_word_arr.append(words[word].split('#')[1])
                myanmar_word_arr.append(words[word].split('#')[0])


        learned_sentance_seperater = '$'
        pos_sentance_seperater = '#'
        
        
        if cond == True:
            ez.delete(0, "end")
            learned_sentance = learned_sentance_seperater.join(myanmar_word_arr)
            #print(learned_sentance)
            pos_sentance = pos_sentance_seperater.join(pos_word_arr)
            #print(pos_sentance)
                
                
            addlinetofile('tagged_corpus.txt',iline)
            addlinetofile('learned_sentence.txt',learned_sentance)
            addlinetofile('pos_sentance.txt',pos_sentance)

            topS = Toplevel()
            topS.title('Yeah!!!')
            
            Message(topS, text =  'Sucessfully Added',pady = 40).pack(expand = 1,fill=X)
            topS.after(3000, topS.destroy)
            topS.mainloop()


def searchforpos(event=None):
    global xy
    string = xy.get()
    
    if(string == ''):
        alert('Input Error','Do not leave the input Blank',kind='warning')
        
    elif(string.isalpha() == False):
        alert('Input Error','This format is not supported',kind='warning')
    else:
        xy.delete(0, "end")
        global output2
        output2 = ['']
        Tagresult = searchTagSetInLine('POS.txt', string.upper())
        if Tagresult == []:
            alert('Sorry','There is no tag set you want to serach',kind='info')
        else:
            Tag = Tagresult[0].split(',')
            
            showout = 'Tag Set :::   ' + Tag[1] + '\n' + 'Part Of Speech :::   ' + Tag[0] + '\n' + u'ဝါစင်္ဂ :::   ' + Tag[2] + '\n' + 'Examples :::   ' + Tag[3]

            
            top = Toplevel()
            top.title('Result')
            
            
            Message(top, text = showout ,pady = 30).pack(expand = 1,fill=X)
            top.after(15000, top.destroy)
            top.mainloop()
            

def importtext(event=None):
    
    global e
    string = e.get()
    
    
    
    words = list(string.split('$'))
    if (string==''):
        alert('Null Sentence Error','PLease Enter A Sentence!!!',kind='error')
    elif('$' not in string):
        alert('Delimiter Error','Please Enter A sentence with $ and at least two words!!!',kind='error')
    elif(words[-1] == '' or words[0] == ''):
        alert('Delimiter Error','Do not enter $ at the first or end of sentence!!!',kind='error')        
    else:
        e.delete(0, "end")
        
        FirstATag = {'entropy': 0.0, 'CombinedPos': []}
        SecondATag = {}
        proArr = []
        resultset = {}
        possibleTagset1 = []
        resultTagset1 = []
      
            
        cond = 'True'
        for q in range (len(words) - 1):
            firstword_filtered_token = searchInLine("tagged_corpus.txt",str(words[q]))
            secondword_filtered_token = searchInLine("tagged_corpus.txt",str(words[q+1]))
             
            if (firstword_filtered_token == [] and secondword_filtered_token ==[]):
                
                cannot_line = 'there is no Pos for the word ( ' + words[q] +' ) and ( '+ words[q+1] + ' )'
                possibleTagset1.append(cannot_line)
                resultTagset1.append(cannot_line)
                
            elif(firstword_filtered_token == [] and secondword_filtered_token !=[]):
                if string.count('$') == 1:
                   alert('Input Sentance Error','Enter a valid sentance',kind='error')
                   cond = 'False'
                elif (q+2 < len(words) and searchInLine("tagged_corpus.txt",str(words[q+2])) == []):
                    alert('Model Error','N-gram does not support this',kind = 'warning')
                    
                else:
                    cannot_line  = 'there is no Pos for the word ( ' + words[q] + ' )'
                    possibleTagset1.append(cannot_line)
                    resultTagset1.append(cannot_line)
            elif(secondword_filtered_token ==[] and firstword_filtered_token !=[] ):
                if string.count('$') == 1:
                   alert('Input Sentance Error','Enter a valid sentance',kind='error')
                   
                   cond = 'False'
                elif string.count('$') == 2:
                    alert('Model Error','N-gram does not support this',kind = 'warning')
                else:
                                    
                    FirstCPOS = FirstATag['CombinedPos']
                    filtered_first_Fresult = []
                    for po in range(len(FirstCPOS)):
                        if FirstCPOS[po].split('#')[1] not in filtered_first_Fresult:
                            filtered_first_Fresult.append(FirstCPOS[po].split('#')[1])

                        
        

                    for pos in range(len(filtered_first_Fresult)):
                        filtered_first_Fresult_tagset_line = words[q] + ' is ( ' + str(filtered_first_Fresult[pos]) + ' )'
                        resultTagset1.append(filtered_first_Fresult_tagset_line)
                                    
                    First_Pos_Found_line = []
                    for var in range (len(firstword_filtered_token)):
                        first_possible_tagset_line = words[q] + ' can be ( '+str(firstword_filtered_token[var]) + ' )'
                        possibleTagset1.append(first_possible_tagset_line)

                    
                    cannot_line  = 'there is no Pos for the word ( ' + words[q+1] + ' )'
                    possibleTagset1.append(cannot_line)
                    resultTagset1.append(cannot_line)
            else:
                
                                
                #for 1st word
                First_Pos_Found_line = []
               
                firstword_filtered_pos_token_withnext = []

               
                firstword_pos_token_withnext_copy = []
                for var in range (len(firstword_filtered_token)):
                    first_possible_tagset_line = words[q] + ' can be ( '+str(firstword_filtered_token[var]) + ' )'
                    possibleTagset1.append(first_possible_tagset_line)
                    

                    First_Pos_Found_line =  searchPOSInLine3("pos_sentance.txt", firstword_filtered_token[var])
                   
                        
                
                
              
                    for d in range(len(First_Pos_Found_line)):
                        Firstword_Pos_seg_token = PostokenSegmentation(str(First_Pos_Found_line[d]))
                    
                        
                        firstword_pos_token_withnext = POStokenmatching('withnext', Firstword_Pos_seg_token, firstword_filtered_token[var])
                
                            
                        
                #for 1st word next pos
                        if (len(firstword_pos_token_withnext) == 1):
                            
                            if (firstword_pos_token_withnext[0] not in firstword_filtered_pos_token_withnext):
                                firstword_filtered_pos_token_withnext.append(firstword_pos_token_withnext[0])
                        else:
                            for f in range(len(firstword_pos_token_withnext)):
                              
                                if (firstword_pos_token_withnext[f] not in firstword_filtered_pos_token_withnext):
                                    firstword_filtered_pos_token_withnext.append(firstword_pos_token_withnext[f])
                
                #firstword_filtered_pos_token_withnext = list(set(firstword_pos_token_withnext_copy))
                
                

              
                            
                

                #for 2nd word
                
                Second_Pos_Found_line = []
                
                secondword_filtered_pos_token_withprevious = []

               
                secondword_pos_token_withprevious_copy = []
                for var in range (len(secondword_filtered_token)):
                    if(q == len(words) - 2):
                        second_possible_tagset_line = words[q+1] + ' can be ( '+str(secondword_filtered_token[var]) + ' )'
                        possibleTagset1.append(second_possible_tagset_line)
                        
                    Second_Pos_Found_line = searchPOSInLine3("pos_sentance.txt", secondword_filtered_token[var])

                
               
                for pos in range(len(secondword_filtered_token)):
                    for line in range(len(Second_Pos_Found_line)):
                        Secondword_Pos_seg_token = PostokenSegmentation(Second_Pos_Found_line[line])

                        
                        secondword_pos_token_withprevious = POStokenmatching('withprevious', Secondword_Pos_seg_token, secondword_filtered_token[pos])
                       
                              
                #for 2nd word preious pos
                        if (len(secondword_pos_token_withprevious) == 1):
                            

                            if (secondword_pos_token_withprevious[0] not in secondword_filtered_pos_token_withprevious):
                                secondword_filtered_pos_token_withprevious.append(secondword_pos_token_withprevious[0])
                        else:
                            for f in range(len(secondword_pos_token_withprevious)):
                                
                                if (secondword_pos_token_withprevious[f] not in secondword_filtered_pos_token_withprevious):
                                  secondword_filtered_pos_token_withprevious.append(secondword_pos_token_withprevious[f])
                
                #secondword_filtered_pos_token_withprevious = list(set(secondword_pos_token_withprevious_copy))         
               

                
                result = token_matcher(firstword_filtered_pos_token_withnext,secondword_filtered_pos_token_withprevious)
                
                #word probility

                SecondATag.clear()
                SecondATag= calculatingEntropy(result)
                
                Fresult = compareTwoambigousTag(FirstATag, SecondATag)
                
                filered_Fresult = []
                for item in range(len(Fresult)):
                    if Fresult[item] not in filered_Fresult:
                        filered_Fresult.append(Fresult[item])

                for pos in range(len(filered_Fresult)):
                    filered_Fresult_tagset_line = words[q] + ' is ( ' + str(filered_Fresult[pos]) + ' )'
                    resultTagset1.append(filered_Fresult_tagset_line)

                

                if(q == len(words) - 2):
                    
                    filered_last_Fresult = []
                    
                    LastCPOS = SecondATag['CombinedPos']
                    for po in range(len(LastCPOS)):
                        if LastCPOS[po].split('#')[1] not in filered_last_Fresult:
                            filered_last_Fresult.append(LastCPOS[po].split('#')[1])

                    for pos in range(len(filered_last_Fresult)):
                        filered_last_Fresult_tagset_line = words[q+1] + ' is ( ' + str(filered_last_Fresult[pos]) + ' )'
                        resultTagset1.append(filered_last_Fresult_tagset_line)

            if SecondATag != {}:
                FirstATag.clear()
                FirstATag = copy.deepcopy(SecondATag)
                proArr.clear()

            
        if cond == 'True':
            global newWindow
            newWindow = tk.Toplevel(root)
                
                
            newWindow.after(500,root.withdraw )
                
                
                
            geoString = str(ctypes.windll.user32.GetSystemMetrics(0))+"x"+str(ctypes.windll.user32.GetSystemMetrics(1))
            screenWidth = ctypes.windll.user32.GetSystemMetrics(0)
            screenHeight = ctypes.windll.user32.GetSystemMetrics(1)
                 
                
            newWindow.geometry(geoString)
            var2 = StringVar()
            label2 = Label( newWindow, textvariable=var2, relief=RAISED )
            var2.set("Possible Tag Set")
            label2.place(x = 0, y = 30, width = screenWidth, height = 30)

                

            scrollbar = Scrollbar(newWindow)
                
            scrollbar.place(x = 0,y = 60, width = 20, height = screenHeight/2 - 30)
            mylist1 = Listbox(newWindow, yscrollcommand = scrollbar.set , width = 40)

            for line in range(len(possibleTagset1)):
                mylist1.insert(END, str(possibleTagset1[line]))
                if 'there is no Pos for the word' in possibleTagset1[line]:
                    mylist1.itemconfig(line, foreground="red")
                        
                
                
                
            mylist1.place(x = 20, y = 60, width = screenWidth, height = screenHeight/2 - 30)
            scrollbar.config( command = mylist1.yview )
            var3 = StringVar()
            label3 = Label( newWindow, textvariable=var3, relief=RAISED )
            var3.set("Result Tag Set")
            label3.place(x = 0, y = screenHeight/2 + 30 , width = screenWidth, height = 30)

            scrollbar2 = Scrollbar(newWindow)
            scrollbar2.place(x = 0,y = (screenHeight/2) + 60, width = 20, height = screenHeight/2 - 130)
            mylist2 = Listbox(newWindow, yscrollcommand = scrollbar2.set , width = 40)
            for line in range(len(resultTagset1)):
               mylist2.insert(END, str(resultTagset1[line]))
               if 'there is no Pos for the word' in resultTagset1[line]:
                   mylist2.itemconfig(line, foreground="red")

                
            mylist2.place(x = 20, y = (screenHeight/2) + 60, width = screenWidth, height = screenHeight/2 - 130)
            scrollbar2.config( command = mylist2.yview )

            var5 = StringVar()
            label5 = Label( newWindow, textvariable=var5, relief='flat')
            var5.set("Enter the tag set you want to search")
            label5.place(x = screenWidth/2 , y = 0, width = screenWidth/6, height = 30)
            var6 = StringVar()
            label6 = Label( newWindow, textvariable=var6, relief='flat')
            var6.set("Add New Sentance To Corpus")
            label6.place(x = screenWidth/40 + 5 , y = 0, width = screenWidth/6, height = 30)

            b3 = Button(newWindow,text='Add sentance',command=createAddframe)
            b3.place(x  =  23*screenWidth/120 +10, y = 0, height = 30, width = screenWidth/15)
            global xy
            xy = Entry(newWindow, width = 40)
            xy.place(x = 2 * screenWidth/3 , y = 0, width = screenWidth/9 , height = 30)
            xy.focus_set()
                
            newWindow.bind('<Return>',searchforpos)
            b1 = Button(newWindow,text='Enter',command=searchforpos)
            b1.place(x  =  7 * screenWidth/9 + 50, y = 0, height = 30, width = screenWidth/15)
                

            b2 = Button(newWindow,text='Back',command = backToMain)
            b2.place(x  =  0, y = 0, height = 30, width = screenWidth/40)
                
                
                

            var111 = StringVar()
            label111 = Label( newWindow, textvariable=var111, relief='flat' )
            var111.set("Copyright (c) 2020 MIIT org \n All Rights Reserved.")
            label111.pack(side='bottom')
            newWindow.mainloop()


            
            


        
from tkinter import *
creating_pos_grammer_sentance_file()
root = tk.Tk()
root.geometry('450x150')
root.title('Project')


var1a = StringVar()
label1 = Label( root, textvariable=var1a, relief=RAISED )
var1a.set("Enter a sentence with the words seperated by a character $ only between the words")
label1.pack()

var = StringVar()
label = Label( root, textvariable=var, relief=RAISED )

var.set("Note: The input have at least two words")
label.pack()

scrollbar1 = Scrollbar(root,orient=HORIZONTAL)
e = Entry(root, xscrollcommand=scrollbar1.set)
e.pack(fill = X)
e.focus_set()
scrollbar1.config( command = e.xview )
scrollbar1.pack(fill = X)



root.bind('<Return>',importtext)
b = Button(root,text='Enter',command=importtext)

b.pack()





var11 = StringVar()
label11 = Label( root, textvariable=var11, relief='flat' )
var11.set("Copyright (c) 2020 MIIT org \n All Rights Reserved.")
label11.pack(side='bottom')



root.mainloop()
