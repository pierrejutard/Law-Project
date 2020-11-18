def Tokenization_Sentence(Sentence):
    Tok_Sentence = "|"
    Punctuations = '''\xa0!()-}[\n]\t{;:'",<>./?@#$%^&*_~'''
    Space = " "
    for char in Sentence:
        if char in Punctuations or char in Space:
            Tok_Sentence = Tok_Sentence + "|" + char + "|"
        else:
            Tok_Sentence = Tok_Sentence + char
    return Tok_Sentence

def List_To_String(Temp_List):  
    str1 = ""  
    for ele in Temp_List:  
        str1 += ele    
    return str1  

def Text_Replacement(Text_to_replace, words_to_replace_dico):
    Replaced_Text = ""
    Token_i_partie = ""
    Split_Token_i_partie = ""
    Token_i_partie = Tokenization_Sentence(Text_to_replace)
    Split_Token_i_partie = Token_i_partie.split("|")
    for i_word in range(len(Split_Token_i_partie)):
        if Split_Token_i_partie[i_word] in words_to_replace_dico:
            Split_Token_i_partie[i_word] = words_to_replace_dico[Split_Token_i_partie[i_word]]
    Replaced_Text = List_To_String(Split_Token_i_partie)
    return Replaced_Text