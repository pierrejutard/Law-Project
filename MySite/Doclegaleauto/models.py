from django.db import models
from django import forms

SEX_CHOICES= [
    ('Mr','Mr'),
    ('Mme','Mme')
    ]

Nationality_CHOICES= [
    ('belge','belge'),
    ('française','française')
    ]

FormJuridiqueSociete_CHOICES= [
    ('entreprise unipersonnelle à responsabilité limitée','entreprise unipersonnelle à responsabilité limitée'),
    ('société anonyme','société anonyme'),
    ('société par actions simplifiée','société par actions simplifiée'),
    ('société à responsabilité limitée','société à responsabilité limitée'),
    ]

class ApportNatureFichiers(models.Model):
    ContratApportNature = models.BooleanField(verbose_name = "Contrat d'apport en nature")
    DecisionAssocieApport = models.BooleanField(verbose_name = "Décision associé(Apport)")
    DecisionAssocieDesignationCommissaire = models.BooleanField(verbose_name = "Décision associé(Désignation commissaire)")
    RapportduPresident = models.BooleanField(verbose_name = "Rapport du Président")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

class Associe(models.Model):
    Sexe_Associe = models.CharField(max_length=4,choices=SEX_CHOICES,default = 'Mr',verbose_name="Sexe")
    Nom_Associe = models.CharField(max_length=40, verbose_name = "Nom")
    #Prenom_Associe = models.CharField(max_length=40, verbose_name = "Prénom")
    #Nationalite_Associe = models.CharField(max_length=100,choices=Nationality_CHOICES, default = 'française', verbose_name = "Nationalité")
    #DateNaissance_Associe = models.DateField(verbose_name = "Date de Naissance")
    #VilleNaissance_Associe = models.CharField(max_length=100, verbose_name = "Ville de naissance")
    #Adresse_Associe = models.CharField(max_length=100, verbose_name = "Adresse")
    #NombreActionSocieteSource_Associe = models.IntegerField( verbose_name = "Nombre actions dans société source")
    #NombreActionApporte_Associe = models.IntegerField(verbose_name = "Nombre actions apportées")
    #MontantGlobalApporte_Associe = models.IntegerField(verbose_name = "Montant global apporté")

class SocieteBeneficiaire(models.Model):
    Form_SocieteBeneficiaire_Nom = models.CharField(max_length=30, verbose_name = "Nom")
    Form_SocieteBeneficiaire_Adresse = models.CharField(max_length=100,verbose_name = "Adresse")
    #Form_SocieteBeneficiaire_FormeJuridique = models.CharField(max_length=100,choices=FormJuridiqueSociete_CHOICES, verbose_name = "Forme Juridique")
    #Form_SocieteBeneficiaire_MontantCapital = models.FloatField(verbose_name = "Montant Capital")
    #Form_SocieteBeneficiaire_NombreAction = models.CharField(max_length=100,verbose_name = "Nombre action")
    #Form_SocieteBeneficiaire_ValeurAction = models.FloatField(verbose_name = "Valeur action")
    #Form_SocieteBeneficiaire_NumRCS = models.CharField(max_length=30, verbose_name = "Numéro RCS")
    #Form_SocieteBeneficiaire_SexePresident = models.CharField(max_length=30, verbose_name = "Sexe (président)")
    #Form_SocieteBeneficiaire_NomPresident = models.CharField(max_length=30, verbose_name = "Nom (président)")
    #Form_SocieteBeneficiaire_PrenomPresident = models.CharField(max_length=30, verbose_name = "Prénom (président)")

class SocieteSource(models.Model):
    Form_SocieteSource_Nom = models.CharField(max_length=50, verbose_name = "Nom")
    Form_SocieteSource_FormeJuridique = models.CharField(max_length=100,choices=FormJuridiqueSociete_CHOICES, verbose_name = "Forme Juridique")
   #Form_SocieteSource_Adresse = models.CharField(max_length=100,verbose_name = "Adresse")
   #Form_SocieteSource_MontantCapital = models.FloatField(verbose_name = "Montant Capital")
   # Form_SocieteSource_NombreAction = models.FloatField(verbose_name = "Nombre action")
   # Form_SocieteSource_ValeurAction = models.FloatField(verbose_name = "Valeur action ")
   # Form_SocieteSource_NumRCS = models.CharField(max_length=30, verbose_name = "Numéro RCS")

class CaractApport(models.Model):
    Form_CaractApport_NbreActionApport = models.FloatField(verbose_name = "Nombre actions attribuées")
    #Form_CaractApport_NbreTotalActionAssocieSocieteSource = models.FloatField(verbose_name = "Nombre d'actions des associés dans société source")
   # Form_CaractApport_MontantApport = models.FloatField(verbose_name = "Montant apport")
   # Form_CaractApport_MontantCapitalFinalSocieteBeneficiaire = models.FloatField(verbose_name = "Capital Final Societe Beneficiaire")

class CommissaireComptes(models.Model):
    Form_CommissaireComptes_Sexe = models.CharField(max_length=4, verbose_name = "Sexe")
    #Form_CommissaireComptes_Nom = models.CharField(max_length=40, verbose_name = "Nom")
    #Form_CommissaireComptes_Prenom = models.CharField(max_length=40, verbose_name = "Prénom")