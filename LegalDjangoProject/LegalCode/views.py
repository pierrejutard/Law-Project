from django.http import HttpResponse
from django.shortcuts import render
from Doclegaleauto.forms import Associe_Form, SocieteBeneficiaire_Form, ApportNatureFichiers_Form, CommissaireComptes_Form, SocieteSource_Form,CaractApport_Form
from django.forms import formset_factory
from zipfile import ZipFile
from django.shortcuts import redirect
from Doclegaleauto.DocDico import Get_dico_ApportNature_modele
from Doclegaleauto.String_operations import Text_Replacement
from Doclegaleauto.Write_Word_Contract import Create_Word_Contract_File
from Doclegaleauto.models import ApportNatureFichiers 
import io

#Main Page view
def MainPage_view(request):
    return render(request, 'Doclegaleauto/MainPage.html',)

#Apport Nature Parameters view
def ApportNatureParameters_view(request):
    ApportNatureFichiersForm = ApportNatureFichiers_Form()
    if request.method == 'POST': 
        ApportNatureFichiersForm=ApportNatureFichiers_Form(request.POST)
        if ApportNatureFichiersForm.is_valid():
            ANF = ApportNatureFichiersForm.save()
            ANF_id = ANF.id
        return redirect('Parametres/Formulaires/' + str(ANF_id))
    else:
        ApportNatureFichiersForm = ApportNatureFichiers_Form()
    return render(request, 'Doclegaleauto/ApportNatureParameters.html',{'ApportNatureFichiers_Form':ApportNatureFichiersForm})

#Apport en nature forms view
def ApportNatureFormulaires_view(request,ANF_id):
    if request.method == 'POST': 
        ANF_obj = ApportNatureFichiers.objects.get(pk=ANF_id) 
        ANF_Attr_List = []
        for attr, value in vars(ANF_obj).items():
            if value == True:
                ANF_Attr_List.append(attr)
        if len(ANF_Attr_List) == 1:
            File_name = ANF_Attr_List[0]
            Result_dico = {}
            Result_dico = Get_Result_dico(request,File_name)
            Contrat_word = Create_Word_Contract_File(Result_dico)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename='+ File_name +'.docx'
            Contrat_word.save(response)
            return response
        else:
            f = io.BytesIO()
            zipObj = ZipFile(f, 'a')
            for File_name in ANF_Attr_List:
                Result_dico = {}
                Result_dico = Get_Result_dico(request,File_name)
                Contrat_word = Create_Word_Contract_File(Result_dico)
                Contrat_word.save(File_name + '.docx')
                zipObj.write(File_name + '.docx')
            zipObj.close()
            response = HttpResponse(f.getvalue(),content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=ContratApportNatureDossier.zip'
            return response
    else:
        ANF_obj = ApportNatureFichiers.objects.get(pk=ANF_id) 
        SocieteBeneficiaireForm = SocieteBeneficiaire_Form()
        CommissaireComptesForm = CommissaireComptes_Form()
        associe_formset = formset_factory(Associe_Form,extra=2)
        SocieteSourceForm = SocieteSource_Form()
        CaractApportForm = CaractApport_Form()
        context = {
                    'ANF_obj': ANF_obj,
                    'SocieteBeneficiaireForm':SocieteBeneficiaireForm,
                    'associe_formset':associe_formset,
                    'CommissaireComptesForm':CommissaireComptesForm,
                    'SocieteSourceForm':SocieteSourceForm,
                    'CaractApportForm':CaractApportForm
                  }
    return render(request, 'Doclegaleauto/ApportNatureFormulaires.html',context)

def Get_Result_dico(request,File_name):
    Result_dico = {}
    Document_dico = {}
    Document_dico = Get_dico_ApportNature_modele(File_name)
    Parties_form_types_dico = {}
    Parties_form_types_dico = Get_ContratApportNature_Parties_form_types_dico(File_name)
    # filling the forms dico corresponding to the post request
    forms_dico = {}
    forms_dico = Get_PostRequest_dico(request,Parties_form_types_dico)
    # filling the result form dico
    for i_partie in Document_dico:
        i_partie_doc = ""
        i_partie_doc = Document_dico[i_partie]
        if 'Autre' in i_partie:
            Result_dico[i_partie] = i_partie_doc
        else:
            I_Partie_forms_dico = {}
            I_Partie_forms_dico = Parties_form_types_dico[i_partie]
            cpt = 0
            Partie_ref = ""
            # split the forms dico in two arrays :one with repeted forms and the other one with unique forms
            Unique_form_names_str = ""
            Repeted_form_names_str = ""
            for i_form,i_form_dico in forms_dico.items():
                form_name = ""
                form_name = Get_Form_Name(i_form)
                if form_name in I_Partie_forms_dico.keys():
                    if I_Partie_forms_dico[form_name] == '!':
                        Unique_form_names_str = Unique_form_names_str + i_form + '|'
                    else:
                        Repeted_form_names_str = Repeted_form_names_str + i_form + '|'
            # filling the i-part of the document following the forms involved in
            # Case 'unique' forms in  a part o the document
            i_unique_partie_doc = ""
            if Unique_form_names_str != "":
                Unique_form_names_arr = Get_form_names_arr(Unique_form_names_str)
                for i_form in Unique_form_names_arr:
                    i_unique_partie_doc = Text_Replacement(i_partie_doc, forms_dico[i_form])
                    i_partie_doc = i_unique_partie_doc
            else:
                i_unique_partie_doc = i_partie_doc
            # Case 'repeted' forms in a part of the document
            i_rep_uniq_partie_doc = ""
            if Repeted_form_names_str != "":
                Repeted_form_names_arr = Get_form_names_arr(Repeted_form_names_str)
                for i_form in Repeted_form_names_arr:
                    i_rep_uniq_partie_doc = Text_Replacement(i_unique_partie_doc, forms_dico[i_form])
                    cpt = cpt + 1
                    Partie_ref = i_partie + '.' + str(cpt)
                    Result_dico[Partie_ref] = i_rep_uniq_partie_doc
            else:
                if Unique_form_names_str != "":
                    cpt = cpt + 1
                    Partie_ref = i_partie + '.' + str(cpt)
                    Result_dico[Partie_ref] = i_unique_partie_doc
    return Result_dico

# function returning a dico with the forms involved in each partie for a specific document
def Get_ContratApportNature_Parties_form_types_dico(File_name):
    Parties_form_types_dico = {}
    if File_name == 'ContratApportNature':
        Parties_form_types_dico ['Partie1'] = {'Associe': 'repete'}
        Parties_form_types_dico ['Partie2'] = {'SocieteBeneficiaire': '!'}
        Parties_form_types_dico ['Partie3'] = {'SocieteSource': '!'}
        Parties_form_types_dico ['Partie4'] = {'Associe': 'repete'}
        Parties_form_types_dico ['Partie5'] = {'SocieteSource': '!','Associe': 'repete'}
        Parties_form_types_dico ['Partie6'] = {'CaractApport': '!','SocieteBeneficiaire': '!'}
    elif File_name == 'DecisionAssocieDesignationCommissaire':
        Parties_form_types_dico ['Partie1'] = {'SocieteBeneficiaire':'!'}
        Parties_form_types_dico ['Partie2'] = {'Associe':'repete'}
        Parties_form_types_dico ['Partie3'] = {'CommissaireComptes':'!'}
        Parties_form_types_dico ['Partie4'] = {'Associe':'!','SocieteSource': '!'}
        Parties_form_types_dico ['Partie5'] = {'CommissaireComptes':'!'}
    elif File_name == 'DecisionAssocieApport':
        Parties_form_types_dico ['Partie1'] = {'SocieteBeneficiaire': '!'}
        Parties_form_types_dico ['Partie2'] = {'Associe': 'repete'}
        Parties_form_types_dico ['Partie3'] = {'Associe': 'repete','SocieteSource': '!','CommissaireComptes':'!'}
    elif File_name == 'RapportduPresident':
        Parties_form_types_dico ['Partie1'] = {'SocieteBeneficiaire': '!','SocieteSource':'!','CaractApport':'!'}
        Parties_form_types_dico ['Partie2'] = {'Associe': 'repete'}
        Parties_form_types_dico ['Partie3'] = {'CommissaireComptes':'!'}
    return Parties_form_types_dico

# function returning the name of the form (example: form_associe_0 => associe)
def Get_Form_Name(i_form):
    Form_names_str = ""
    if i_form.count("_") < 2:
        Form_names_str = i_form.split("_")[-1]
    else:
        Form_names_str = i_form.split("_")[-2]
    return Form_names_str

# function returning an array of form names
def Get_form_names_arr(Form_names_str):
    Form_names_arr = []
    Form_names_str = Form_names_str[:-1]
    if '|' in Form_names_str:
        Form_names_arr = Form_names_str.split('|')
    else:
        Form_names_arr.append(Form_names_str)
    return Form_names_arr

# function filling the data forms dico w.r.t to the post request
def Get_PostRequest_dico(request, Parties_form_types_dico):
    Post_request_dico = {}
    Post_request_dico = request._post
    forms_dico = {}
    for k,v in Post_request_dico.items():
        if '_' in k or '-' in k:
            # key (name), subkey dico preparation 
            if not '-' in k:
                subkey = k.split('_')[-1] + k.split('_')[-2] 
                key = '_'.join(k.split('_')[:2])
            else:
                Ksplit = k.split('-')[-1]
                subkey = Ksplit.replace('_','')
                key = k.split('-')[0] +'_'+ k.split('_')[-1] +'_'+ k.split('-')[1]
            forms_dico.setdefault(key, {}).update({subkey:v})
    return forms_dico