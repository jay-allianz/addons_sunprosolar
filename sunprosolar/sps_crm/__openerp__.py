# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
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
    'depends': ['base','sps_product','sale_crm','city','document','account','analytic','project'],
    'demo': [
        'crm_lead_demo.xml',
    ],
    'data': [
#        'security/security.xml',
#        'security/ir.model.access.csv',
        'lead_view.xml',
        'crm_data.xml',
        'crm_report_view.xml',
        'station_view.xml',
        'sequence.xml',
        'email_template_data.xml',
#        'lead_email_template.xml',
        'wizard/crm_lead_to_opportunity_view.xml',
        'wizard/import_utility_company_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
