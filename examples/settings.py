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

from datetime import datetime

host = 'https://api.infojobs.net'
api_url = host + '/api/1/offer'
username = 'yourClientID'
password = 'yourClientsecret'
payload = {
	   'province': 'barcelona',
           'category': 'informatica-telecomunicaciones',
           'maxResults': 1000,
	}
report_title = 'Infojobs job offers'
report_footer = '<br>Report generated using pyjobportal<br>'
# Job offer format
# 2013-11-02T20:50:55.000+0000
# Job offer publishedMin and publishedMax format
# 2013-11-01T00:00:00Z
date_format = '%d/%m/%Y'
api_date_format = '%Y-%m-%dT%H:%M:%S.%f'
weekday = datetime.today().weekday()
if weekday == 0:
    days_back = 3 
else:
    days_back = 1
days_offset = 1
