from django import forms
from .models import all_stock_names
from dal import autocomplete

class searchStockForm(forms.ModelForm):
    class Meta:
        model=all_stock_names
        autocomplete_fields=("name")
        fields=["name"]
        #widgets={"name":autocomplete.ModelSelect2(url="search")}
        widgets={"name":autocomplete.ListSelect2(url="search")}  #for some reason this one works
