import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from urllib2 import HTTPError, URLError
from bs4 import BeautifulSoup

from auto_google_search.libs import google


logger = logging.getLogger(__name__)


class SearchRecordManager(models.Manager):
    """
    Manager for model 'SearchRecord'

    """
    def search_and_extract(self, search_term):
        """
        Uses google.search function to get the first 20 search results based on the given term, and then creates a
        search record object and calls extract_and_save_search_results in order to extract results, and at the end
        saves the new search record object.

        :param search_term: (string) the entered search term
        :return: (int) the id of the newly created search record object

        """
        search_response_urls = google.search(query=search_term,
                                             num=settings.NUMBER_OF_RESULTS_PER_PAGE_IN_GOOGLE,
                                             stop=settings.NUMBER_OF_RESULTS,
                                             only_standard=True)

        search_record = SearchRecord(search_term=search_term)

        search_record.save()
        is_successful = SearchResult.objects.extract_and_save_search_results(
            search_record=search_record,
            search_response_urls=search_response_urls)

        search_record.is_successful = is_successful
        search_record.save()
        return search_record.pk

    def get_formatted_search_history(self, selected_search_record_id=None):
        """
        Creates an array of formatted successful search records in the following format and returns it.
        {
            'search_term': '',
            'search_timestamp': '',
            'url': '',
            'is_selected': True/False
        }

        :param selected_search_record_id: (int) the id of the search record object which is currently selected
        :return: (array) array of formatted successful search results

        """
        return [{
            'search_term': search_record.search_term,
            'search_timestamp': search_record.search_timestamp.strftime("%B %d, %Y  %I:%M %P"),
            'url': reverse('history', args=(search_record.pk,)),
            'is_selected': (search_record.pk == int(selected_search_record_id)) if selected_search_record_id is not None else False
        } for search_record in self.all() if search_record.is_successful]


class SearchRecord(models.Model):
    """
    Search Record model which handles ORMs for the table 'ags_search_record'

    """
    search_term = models.CharField(max_length=500)
    search_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_successful = models.BooleanField(default=False)

    objects = SearchRecordManager()

    class Meta:
        """
        Specifies database table name and sorting order while retrieving data from this model

        """
        db_table = 'ags_search_record'
        ordering = ["-search_timestamp"]

    def __str__(self):
        return self.search_term

    def get_formatted_extracted_data(self):
        """
        Formats current the current search record, also goes through each result, and ultimately each extracted info
        of each result and creates a dictionary from them in the following format.
        {
            'search_term': '',
            'formatted_results':[
                {
                    'result_number': 1,
                    'url': '',
                    'title': '',
                    'formatted_extracted_info': [
                        {
                            'extracted_info_key': 'Meta',
                            'extracted_info_value': 'Value'
                        },
                        {
                            'extracted_info_key': 'Title',
                            'extracted_info_value': 'Value'
                        }
                    ]
                }
            ]
        }

        :return: (dict) a dictionary containing 'formatted_results' and 'search_term'

        """
        formatted_results = []

        result_number = 1

        # Using related-names django backward foreign key feature, we can access results from our current record object.
        for result in self.results.all():
            formatted_result = {
                'result_number': result_number,
                'url': result.url,
                'title': result.title
            }
            formatted_extracted_info = []
            result_number += 1

            # Using related-names django backward foreign key feature,
            # we can access extracted_info from each search result object.
            for extracted_info in result.extracted_info.all():
                formatted_extracted_info.append({
                    'extracted_info_key': extracted_info.extracted_info_key,
                    'extracted_info_value': extracted_info.extracted_info_value
                })

            formatted_result['formatted_extracted_info'] = formatted_extracted_info
            formatted_results.append(formatted_result)

        return {
            'formatted_results': formatted_results,
            'search_term': self.search_term
        }


class SearchResultManager(models.Manager):
    """
    Manager for model 'SearchRecord'

    """
    def extract_and_save_search_results(self, search_record, search_response_urls):
        """
        Extracts and saves the results for the given search record based on the given search urls

        :param search_record: (SearchRecord object) the current search record object
        :param search_response_urls: (Generator) the list of yielded urls resulted from the google search
        :return: (Boolean) whether or not we retrieved results from the given search term

        """
        # Search results are considered successful if we get any links back from our google search
        is_successful = False
        order = 1

        # Goes through each link and gets the html page of the link and creates a search result object for it, and
        # starts extracting the info inside the website using extract_and_save_website_info function.
        for url in search_response_urls:
            is_successful = True
            try:
                html_page = google.get_page(url=url)
            except (HTTPError, URLError) as e:
                logger.warning(e)
                continue

            soup_html_page = BeautifulSoup(html_page)
            title = unicode(self._extract_title(soup_html_page=soup_html_page))
            search_result = SearchResult(search_record=search_record, url=url, order=order, title=title)
            search_result.save()

            SearchExtractedInfo.objects.extract_and_save_website_info(
                search_result=search_result,
                soup_html_page=soup_html_page)

            order += 1

        return is_successful

    def _extract_title(self, soup_html_page):
        """
        Goes through the given page and retrieves the title of the page and returns it.

        :param soup_html_page: (BeautifulSoup object)
        :return: (string) title of the given page

        """
        title = soup_html_page.find('title')

        if title and len(title.contents) > 0:
            return title.contents[0]
        else:
            return ""


class SearchResult(models.Model):
    """
    Search Result model which handles ORMs for the table 'ags_search_result'

    """
    search_record = models.ForeignKey(SearchRecord, related_name='results')
    url = models.URLField()
    title = models.CharField(max_length=500)
    order = models.SmallIntegerField(default=0)

    objects = SearchResultManager()

    class Meta:
        """
        Specifies database table name and sorting order while retrieving data from this model

        """
        db_table = 'ags_search_result'
        ordering = ['order']

    def __str__(self):
        return self.title


class SearchExtractedInfoManager(models.Manager):
    """
    Manager for modal 'SearchExtractedInfo'

    """
    def extract_and_save_website_info(self, search_result, soup_html_page):
        """
        Extracts specified elements from the given html page and creates SearchExtractedInfo objects for them which
        will be associated with the given search_result object

        :param search_result: (SearchResult object)
        :param soup_html_page: (BeautifulSoup object)
        :return: None

        """
        # Goes through each criteria in settings and extract the specified element from the page if possible
        for criteria in settings.DATA_EXTRACTION_CRITERIA_AND_CONTENT_DESTINATIONS:

            if criteria['attribute'] is None:
                extracted_tag = soup_html_page.find(criteria['tag'])
            else:
                extracted_tag = soup_html_page.find(
                    criteria['tag'], attrs={criteria['attribute']: criteria['attribute_value']})

            if not extracted_tag:
                continue

            extracted_info_value = ""
            if criteria['attribute_to_extract'] is None:
                if len(extracted_tag.contents) > 0:
                    extracted_info_value = unicode(''.join(extracted_tag.contents))
            else:
                extracted_info_value = unicode(extracted_tag.attrs[criteria['attribute_to_extract']])

            if len(extracted_info_value.strip()) == 0:
                continue

            search_extracted_info = SearchExtractedInfo(search_result=search_result)
            search_extracted_info.extracted_info_key = criteria['criteria_name']
            search_extracted_info.extracted_info_value = extracted_info_value
            search_extracted_info.save()


class SearchExtractedInfo(models.Model):
    """
    Search Extracted Info model which handles ORMs for the table 'ags_search_extracted_info'

    """
    search_result = models.ForeignKey(SearchResult, related_name='extracted_info')
    extracted_info_key = models.CharField(max_length=100)
    extracted_info_value = models.TextField(max_length=50000, null=True, blank=True, default=None)

    objects = SearchExtractedInfoManager()

    class Meta:
        """
        Specifies database table name

        """
        db_table = 'ags_search_extracted_info'

    def __str__(self):
        return self.extracted_info_key + ' - (' + self.search_result.title + ')'