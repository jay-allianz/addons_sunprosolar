# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Allianz Technology, A subsidiary of SAT Group, Inc.
#    Copyright (C) 2012 OpenERP SA (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name" : "SPS - CRM",
    "version" : "6.3",
    "author" : "Allianz Technology",
    "category" : "Tools",
    "website" : "'http://www.allianztechnology.com",
    "description": """This module provides the functionality to generate Leads of customer. 
    """,
    'depends': ['base','product','crm','city','document','account','analytic','project', 'sale'],
    'demo': [
        'crm_lead_demo.xml',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'lead_view.xml',
        'crm_data.xml',
        'crm_report_view.xml',
        'station_view.xml',
        'wizard/crm_lead_to_opportunity_view.xml',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
