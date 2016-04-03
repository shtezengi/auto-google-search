import logging

from django.views.generic import FormView
from django.core.urlresolvers import reverse

from auto_google_search.apps.website import forms as website_forms
from auto_google_search.apps.website import models as website_models

logger = logging.getLogger(__name__)


class IndexView(FormView):
    """
    This view is responsible for validating user's search term, and crawling google and extracting the first 20
    results based on the given search term, and storing them into the database.

    @note: for this view POST request is being used because as opposed to other common search mechanisms this search
    functionality will store the searched and extracted data into our database, so it makes data changes, and it should
    be done through a POST request as opposed to a GET request

    """
    template_name = "index.html"
    form_class = website_forms.SearchForm

    def get(self, request, search_record_id=None, *args, **kwargs):
        if search_record_id:
            self.request.session['search_record_id'] = search_record_id
        return super(IndexView, self).get(request, *args, **kwargs)

    def form_invalid(self, form):
        return super(IndexView, self).form_invalid(form)

    def form_valid(self, form):
        """
        Extracts and saves results if the search form is validated successfully

        :param form: (website_forms.SearchForm object)
        :return: (HttpResponseRedirect object)

        """
        self.request.session['search_record_id'] = form.extract_and_save_results()
        return super(IndexView, self).form_valid(form)

    def get_success_url(self):
        return reverse('index')

    def get_context_data(self, **kwargs):
        """
        Specifies context data

        :param kwargs:
        :return: (dict) context data

        """
        context = super(IndexView, self).get_context_data(**kwargs)
        search_record_id = self.request.session.get('search_record_id', None)

        context['formatted_search_history'] = website_models.SearchRecord.objects.get_formatted_search_history(
            selected_search_record_id=search_record_id
        )

        if search_record_id:
            search_record = website_models.SearchRecord.objects.get(pk=search_record_id)
            context['formatted_search_record_data'] = search_record.get_formatted_extracted_data()

        return context