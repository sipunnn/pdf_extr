import re

def data_extractor_numbers(text,spliter,index_splitter, dic_to_write,stopper,key,list_1,regex,occurence):
    bd = "" 
    if spliter == ' ':
        bd = text
    else:        
        try:     
            value = text.split(spliter)
            if stopper != ' ':
                y = value[index_splitter].index(stopper)
                for x in value[index_splitter][0:y]:
                    if x == stopper:
                        pass
                    else:
                        if x.isnumeric():
                            bd += x
                        elif x in list_1:
                            bd += x
                        elif x == ' ':
                            bd += x
                        else:
                            pass
            else:
                for x in value[index_splitter][0:]:
                   bd += x
        except:
            bd = 'Keyword Not Found'
    if regex == '':
        pass
    else:
        value = re.findall(regex, bd)
        try:
            bd = value[occurence]
        except:
            bd = 0
    dic_to_write[key] = bd
    return bd



def data_extractor_string(text,spliter,index_splitter,dic_to_write,stopper,key,list_1,regex,occurence):
    bd = ""
    try:     
        value = text.split(spliter)
        if stopper != ' ':
            y = value[index_splitter].index(stopper)
            for x in value[index_splitter][0:y]:
                if x == stopper:
                    pass
                else:
                    if x.isalpha():
                        bd += x
                    elif x in list_1:
                        bd += x
                    elif x == ' ':
                        bd += x
                    else:
                        pass
        else:
            for x in value[index_splitter][0:]:
               bd += x
    except:
        bd = 'Keyword Not Found'
    if regex == '':
        pass
    else:
        value = re.findall(regex, bd)
        try:
            bd = value[occurence]
        except:
            bd = 0
    dic_to_write[key] = bd
    return bd


def data_extractor_alphanumeric(text,spliter,index_splitter,dic_to_write,stopper,key,list_1,regex,occurence):
    bd = ""
    try:     
        value = text.split(spliter)
        if stopper != ' ':
            y = value[index_splitter].index(stopper)
            for x in value[index_splitter][0:y]:
                if x == stopper:
                    pass
                else:
                    if x.isalnum():
                        bd += x
                    elif x in list_1:
                        bd += x
                    elif x == ' ':
                        bd += x
                    else:
                        pass
        else:
            for x in value[index_splitter][0:]:
               bd += x
    except:
        bd = 'Keyword Not Found'
    if regex == '':
        pass
    else:
        value = re.findall(regex, bd)
        try:
            bd = value[occurence]
        except:
            bd = 0
    dic_to_write[key] = bd
    return bd


