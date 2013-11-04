#!/usr/bin/python2

# pyjobportal is a python library to deal wiht job portal APIs
# Copyright (C) 2013 Jamgo S.C.C.L. info@jamgo.es
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from requests.auth import HTTPBasicAuth
from requests import get, Session
import inspect
import json
from pprint import pprint
from datetime import datetime, timedelta

from sys import exit
import inspect

class JobPortalWebSpider(object):
    ''' General purpose bstract class to play with job portals API '''

    def __init__(self, **kwargs):
        ''' Common settings to all APIs '''
        self.username = kwargs['username']
        self.api_url = kwargs['api_url']
        self.days_back = kwargs['days_back']
        self.days_offset = kwargs['days_offset']
        self.report_footer =  kwargs['report_footer']
        self.api_date_format =  kwargs['api_date_format']
        self.date_format = kwargs['date_format']
        self.html_report = '<html><head><meta http-equiv="Content-Type"'+\
                           ' content="text/html; charset=utf-8" /></head>'
        self.starting_date = self._get_date_days_back(self.days_back)
        self.end_date = self._get_date_days_back(self.days_offset)
        self.payload = self._format_payload(kwargs['payload'])
        self.session = Session()
        self.response = self._http_request_job_offer()
        self.session.headers = {'content-type': 'application/json'}
        self.job_offer = self._get_job_offer_list()
        self.report_title = self._get_report_title(kwargs['report_title'])

    def _http_request_job_offer(self):
        ''' Makes HTTP request to job portal API with payload params '''
        raise NotImplementedError( "Should have implemented this" )

    def _format_payload(self, payload):
        ''' Adapts payload used to make HTTP request to job portal API '''
        raise NotImplementedError( "Should have implemented this" )

    def _get_job_offer_list(self):
        ''' Build a list of JobOffer objects '''
        raise NotImplementedError( "Should have implemented this" )

    def __repr__(self):
        ''' Method should return a string, and not print out ''' 
        output = ''
        for job_offer in self.job_offer:
            output += str(job_offer)
        return output

    def job_offer_list_to_file(self, file_name):
        ''' Loops self.job_offer and prints each of them '''
        self._compose_html_report()
        self._write_report_to_file(file_name)

    def _compose_html_report(self):
        ''' Loops over self.job_offer and returns html file '''
        self.html_report += '%s%s%s' %('<b>', self.report_title, '</b><br><br>')
        for job_offer in [job_offer.to_html() for job_offer in self.job_offer]:
            self.html_report += job_offer+'<br>'
        self.html_report += '%s%s' %(self.report_footer, '</html>')
        self.html_report = self.html_report.encode('utf-8')

    def _get_report_title(self, title):
        ''' Returns a string with title and current date '''
        return '%s (%s 00:00:00 - %s 23:59:59 )' %(title, self.starting_date,
                                                   self.end_date)

    def _get_date_days_back(self, days_back):
        ''' Returns a string with starting date of report '''
        return (datetime.now() + timedelta(-days_back)).\
                     strftime(self.date_format)

    def _write_report_to_file(self, file_name):
        ''' Writes self.html_report content to specified file '''
        f = open(file_name, 'w')
        f.write(self.html_report)
        f.close()

class JobOffer(object):

    def __init__(self, job_portal = None, title = None, city = None, url =
                 None, published = None, salary = None):
        ''' Common attributes to all job offers '''
        self.job_portal = job_portal
        self.title = title
        self.url = url
        self.city = city
        self.published = published
        self.salary = salary

    def __repr__(self):
        ''' Method should return a string, and not print out ''' 
        #return "{}({})".format(self.__class__.__name__, vars(self))
        #return "%s(%r)" % (self.__class__, self.__dict__)
        return str(pprint (vars(self))).replace('None','').strip()

    def to_html(self):
        ''' Returns one single string with HTML formatted object '''
        return '%s %s %s <a href="%s">%s</a> %s' \
               %(self.job_portal, self.published, self.city, self.url,
                 self.title, self.salary)

class InfojobsJobOffer(JobOffer):

    def __init__(self, job_offer, date_format, api_date_format):
        ''' Translates Infojobs properties to JobOffer ones '''
        JobOffer.__init__(self, 'Infojobs', job_offer['title'],
                          job_offer['city'], job_offer['link'],
                          self._from_rfc_3339_to_datetime(
                                                    job_offer['published'],
                                                    api_date_format,
                                                    date_format),
                          job_offer['salaryMax']['value'])

    def _from_rfc_3339_to_datetime(self, rfc_3389_string, in_format,
                                   out_format):
        ''' Returns formatted datetime from RFC 3339 date string '''
        # TODO: use a 3rd party library
        # 2013-11-02T20:50:55.000+0000
        date_string = rfc_3389_string.split('+')[0][:-1]
        return datetime.strptime(date_string, in_format).strftime(out_format)

class Infojobs(JobPortalWebSpider):

    def __init__(self, **kwargs):
        ''' Infojobs API requires a password too '''
        self.password = kwargs['password']
        JobPortalWebSpider.__init__(self, **kwargs)

    def _format_payload(self, payload):
        ''' Infojobs API requires RFC 3389 date for instance '''
        # http://developer.infojobs.net/documentation/operation/offer-list-1.xhtml
        payload['publishedMin'] = self._from_datetime_to_rfc_3339(
                                  self.starting_date, self.date_format,
                                  self.api_date_format)
        payload['publishedMax'] = self._from_datetime_to_rfc_3339(
                                  self.end_date, self.date_format,
                                  self.api_date_format, True)
        return payload

    def _http_request_job_offer(self):
        return self.session.get(self.api_url, auth=(self.username,
                                                             self.password),
                                         params = self.payload)

    def _get_job_offer_list(self):
        return [InfojobsJobOffer(offer, self.date_format, self.api_date_format)
               for offer in self.response.json()['offers']]

    def _from_datetime_to_rfc_3339(self, date_in, in_format, out_format,
                                   format_to_last_minute = False):
        ''' Returns RFC 3339 string deom formatted datetime '''
        # TODO: improve 23:59:59 mechanism
        # TODO: use a 3rd party library
        # 2013-11-02T20:50:55.000+0000
        if format_to_last_minute:
            return str(datetime.strptime(date_in, in_format).strftime(
                       out_format))[:-15] + '23:59:59Z'
        else:
            return str(datetime.strptime(date_in, in_format).strftime(
                      out_format))[:-7] + 'Z'
