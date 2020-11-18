def Get_dico_ApportNature_modele(File_name):
    PartDoc_dico = {}
    Part_Cpt = 0
    Oth_Part_Cpt = 0
    InPart=False
    with open("C:/Users/user/Desktop/Template_" + File_name + '.txt', encoding='utf-8') as TextFile:
        for line in TextFile:
            if '[\n' in line or InPart == True:
                Part_Cpt = Part_Cpt + 1
                Str_Part = ""
                while "]\n" not in line:
                    Str_Part = Str_Part + line
                    line = TextFile.readline()
                InPart=False
                key_Partdoc_dico = "Partie" + str(Part_Cpt)
                PartDoc_dico[key_Partdoc_dico] = Str_Part
            else:
                Oth_Part_Cpt = Oth_Part_Cpt + 1
                Str_Part = ""
                while "[\n" not in line and line != '':
                    Str_Part = Str_Part + line
                    line = TextFile.readline()
                InPart=True
                key_Partdoc_dico = "AutrePartie" + str(Oth_Part_Cpt)
                PartDoc_dico[key_Partdoc_dico]= Str_Part
    return PartDoc_dico