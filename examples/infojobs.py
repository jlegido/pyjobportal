#!/usr/bin/python

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

from pyjobportal import Infojobs
from settings import api_url, client_id, client_secret, payload, days_back,\
                     report_title, report_footer, days_offset, date_format,\
                     api_date_format
from base64 import b64decode

i = Infojobs(client_id = b64decode(client_id), client_secret =
             b64decode(client_secret), api_url = api_url, payload = payload,
             report_title = report_title, days_back = days_back, days_offset =
             days_offset, report_footer = report_footer, date_format =
             date_format, api_date_format = api_date_format)

i.job_offer_list_to_file('infojobs.html')
