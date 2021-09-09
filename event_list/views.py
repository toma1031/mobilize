from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404
import requests
import json
from datetime import datetime
from urllib.parse import urlparse


def index_view(request):
    # Define URL
    url = 'https://api.mobilize.us/v1/events'

    # query parameter
    parameter = request.GET.get("cursor")

    # If you can get the query parameters, set the query parameters to the default URL (https://api.mobilize.us/v1/events)
    if parameter:
        url = url + '?' + "cursor" + "=" + parameter + "&" + "timeslot_start=gte_now"
        # Get URL
        return_json = json.loads(requests.get(url).text)
        response = return_json['data']
    # No query parameter
    else:
        # Let leave the url
        url = 'https://api.mobilize.us/v1/events?timeslot_start=gte_now'
        return_json = json.loads(requests.get(url).text)
        response = return_json['data']


    # if 'error' in return_json:
    #     raise Http404('does not exist')

    dic_for_templates_for_html = []
    dic_for_templates_for_js = []
    for summary in response:
        # Sometimes the Location key of the summary may not contain anything
        if summary['location'] is None :
            # reference
            # https://note.nkmk.me/python-pass-usage/
            # If it is none, it will proceed to the next step without performing any further processing,
            continue
        else:
            dic_title = summary['title']
            try:
                dic_latitude = summary['location']['location']['latitude']
                dic_longitude = summary['location']['location']['longitude']
            except KeyError:
                dic_latitude = None
                dic_longitude = None

        # reference
        # https://pg-chain.com/python-in#:~:text=Python%E3%81%A7%E3%81%AF%E3%80%8Cin%E3%80%8D%E3%82%92%E4%BD%BF%E3%81%A3,%E8%BF%94%E3%81%99%E3%81%93%E3%81%A8%E3%81%8C%E3%81%A7%E3%81%8D%E3%81%BE%E3%81%99%E3%80%82
        # https://www.javadrive.jp/python/string/index1.html#section2
        # If the dic_title (event title) contains a single quota
        if "'" in dic_title:
            # Use an escape sequence
            # https://www.javadrive.jp/python/string/index2.html
            # Replace single quotation with empty
            dic_title = dic_title.replace("'", "")
        # If the dic_title (event title) contains a double orientation
        elif '"' in dic_title:
            # Replace double quotation with empty
            dic_title = dic_title.replace('"', '')

        start_date_list = []
        for i in range(len(summary['timeslots'])):
            start_date = summary['timeslots'][i]['start_date']
            start_date_list.append(datetime.fromtimestamp(start_date))

            new_d_for_html = {
                'new_id': summary['id'],
                'new_title': dic_title,
                'new_description': summary['description'],
                'new_timezone': summary['timezone'],
                'new_latitude': dic_latitude,
                'new_longitude': dic_longitude,
                'new_start_dates': start_date_list,
            }

            new_d_for_js = {
                'new_title': dic_title,
                'new_latitude': dic_latitude,
                'new_longitude': dic_longitude,
            }

        dic_for_templates_for_html.append(new_d_for_html)
        dic_for_templates_for_js.append(new_d_for_js)

    # Extract only the query parameter part from the url
    # reference
    # https://www.headboost.jp/python-delete-strings/
    url_next_querry_parameter = '?' + urlparse(return_json['next']).query if return_json['next'] else None 
    url_previous_querry_parameter = '?' + urlparse(return_json['previous']).query if return_json['previous'] else None 
    context = {
        # For HTML
        'list_data_for_html': dic_for_templates_for_html,

        # For Javascript
        # For using on the Script(HTML) side, it is once converted to JSON format on the Views side.
        # reference
        # https://python.softmoco.com/basics/python-json-dump.php
        'list_data_for_js': json.dumps(dic_for_templates_for_js),

        # For Pagination
        'url_next_querry_parameter': url_next_querry_parameter,
        'url_previous_querry_parameter': url_previous_querry_parameter,
    }

    return render(request, 'index.html', context)