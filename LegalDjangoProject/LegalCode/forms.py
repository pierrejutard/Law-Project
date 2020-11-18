from django import forms
from django.forms import ModelForm
from django.forms import formset_factory
from LegalCode.models import Associe, SocieteBeneficiaire, ApportNatureFichiers, SocieteSource,CaractApport,CommissaireComptes

class DateInput(forms.DateInput):
    input_type = 'date'

class CaractApport_Form(ModelForm):
    class Meta:
        model = CaractApport
        fields='__all__'

class Associe_Form(ModelForm):
    class Meta:
        model = Associe
        fields='__all__'
        widgets = {'DateNaissance_Associe': DateInput(),}
    def __init__(self, *args, **kwargs):
        super(Associe_Form, self).__init__(*args, **kwargs)
        self.fields['Nom_Associe'].widget.attrs['placeholder'] = 'Dupont'
        #self.fields['Prenom_Associe'].widget.attrs['placeholder'] = 'Martin'
        #self.fields['VilleNaissance_Associe'].widget.attrs['placeholder'] = 'Paris (75008)'
        
class CommissaireComptes_Form(ModelForm):
    class Meta:
        model = CommissaireComptes
        fields='__all__'

class SocieteBeneficiaire_Form(ModelForm):
    class Meta:
        model = SocieteBeneficiaire
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super(SocieteBeneficiaire_Form, self).__init__(*args, **kwargs)
        #self.fields['Form_SocieteBeneficiaire_MontantCapital'].widget.attrs['placeholder'] = '100.000'

class SocieteSource_Form(ModelForm):
    class Meta:
        model = SocieteSource
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super(SocieteSource_Form, self).__init__(*args, **kwargs)
        #self.fields['Form_SocieteSource_Adresse'].widget.attrs['placeholder'] = '1 rue Buot, 75013 Paris'
        #self.fields['Form_SocieteSource_MontantCapital'].widget.attrs['placeholder'] = '100.000'

class ApportNatureFichiers_Form(ModelForm):
    class Meta:
        model = ApportNatureFichiers
        fields='__all__'