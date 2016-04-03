import logging

from django import forms

from auto_google_search.apps.website import models


logger = logging.getLogger(__name__)


class SearchForm(forms.Form):
    search_term = forms.CharField(required=True)

    def extract_and_save_results(self):
        """
        Extracts and saves search term results by calling the 'search_and_extract' function of class 'SearchRecord'

        :return: (SearchRecord object)

        """
        search_term = self.cleaned_data['search_term']
        return models.SearchRecord.objects.search_and_extract(search_term=search_term)
