# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2013 Serpent Consulting Services (<http://serpentcs.com>).
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
    "name" : "SunPro Financial Reports",
    "version" : "0.3",
    "author" : "Serpent Consulting Services Pvt. Ltd.",
    "website" : "http://www.serpentcs.com",
    "depends" : ["base", "account"],
    "category" : "Localisation/Accounting",
    "description": """This modules allows you to create your own Financial Statements by creating templates for Balance Sheets and Income Statements, including Analytic Ledgers within the "Report Templates" menu (Accounting > Reporting > Legal Reports > Accounting Reports > Report Templates).\n"""\
    "\n"\
    """You will be able to generate Year-To-Date (End. Balance), monthly (12 Months + YTD), or quarterly (4QRT's + YTD) reports. In addition, you can generate periodic reports based on date or period intervals. Comparison Balance Sheets are also available.\n"""\
    "\n"\
    """Please remember to go to the Account Signage tab, which is found within your company's profile (Settings > Companies > Companies) in order to prevent accounts with credit balances from being displayed with negative signs.""",
                    
    "demo" : [],
    "data" : [
        "security/security.xml",
        "view/report.xml", 
        "view/wizard.xml",
        "view/account_view.xml",
        "view/company_view.xml",
        "view/account_financial_report_view.xml",
        "view/periodic_financial_reports_view.xml",
        "security/ir.model.access.csv",
    ],
    "auto_install": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: