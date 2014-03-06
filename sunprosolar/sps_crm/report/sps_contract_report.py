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

import time
from openerp.report import report_sxw

class contract(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(contract, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time, 
            'get_utility_company': self.get_utility_company,
            'get_meter_no': self.get_meter_no,
            'get_account_no': self.get_account_no,
            'get_roof_type': self.get_roof_type,
            'get_roof_type_age': self.get_roof_type_age,
            'get_install_date': self.get_install_date,
            'get_total_contract_price': self.get_total_contract_price,
            'get_sales_person':self.get_sales_person,
            'get_reg_no':self._get_reg_no,
            'get_lead_city_id':self._lead_city_id,
            'get_address':self.get_address,
            'get_lead_name':self._lead_name,
            'get_annul_usage':self._annul_usage,
            'get_stc_dc_rating':self._stc_dc_rating,
            'get_products':self.get_products,
            
        })
        
    def _lead_name(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_name = False
        if lead_id:
            lead_name = lead_obj.browse(self.cr, self.uid, lead_id)[0].name
        return lead_name
    
    def get_products(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_name = False
        sting = ''
        if lead_id:
            for data in solar_ids:
                module = data.module_product_id.name
                inverter = data.invertor_product_id.name
                product = str(module) + ',' + str(inverter)
                string = string + product
        return string
    
    def _annul_usage(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_name = False
        if lead_id:
            annual_ele_usage = lead_obj.browse(self.cr, self.uid, lead_id)[0].annual_ele_usage
        return annual_ele_usage
    
    def _stc_dc_rating(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_name = False
        if lead_id:
            stc_dc_rating = lead_obj.browse(self.cr, self.uid, lead_id)[0].stc_dc_rating
        return stc_dc_rating
    
    def _lead_city_id(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_name = False
        if lead_id:
            name = lead_obj.browse(self.cr, self.uid, lead_id)[0].city_id.name or ''
            zip = lead_obj.browse(self.cr, self.uid, lead_id)[0].city_id.zip or ''
            state =  lead_obj.browse(self.cr, self.uid, lead_id)[0].state_id.name or ''
            country =  lead_obj.browse(self.cr, self.uid, lead_id)[0].country_id.name or ''
            
            city_id = str(name) + ' ' + str(zip) + ' ' + str(state) + ' ' + str(country)
        return city_id
    
    def get_address(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_data = False
        if lead_id:
            street = lead_obj.browse(self.cr, self.uid, lead_id)[0].street or ''
            street2 = lead_obj.browse(self.cr, self.uid, lead_id)[0].street2 or ''
            lead_data = str(street) + ' ' + str(street2)
        return lead_data
        
    def get_sales_person(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_data = False
        if lead_id:
            lead_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].user_id.name
        return lead_data
    
    def get_total_contract_price(self, customer):
        analytic_obj = self.pool.get("account.analytic.account")
        analytic_id = analytic_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        analytic_data = False
        if analytic_id:
            analytic_data = analytic_obj.browse(self.cr, self.uid, analytic_id)[0].amount
        return analytic_data

    def get_install_date(self, customer):
        analytic_obj = self.pool.get("account.analytic.account")
        analytic_id = analytic_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        analytic_data = False
        if analytic_id:
            analytic_data = analytic_obj.browse(self.cr, self.uid, analytic_id)[0].date_start
        return analytic_data

    def get_utility_company(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_data = False
        if lead_id:
            lead_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].utility_company_id.name
        return lead_data
    
    def _get_reg_no(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_data = False
        if lead_id:
            lead_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].reg_no
        return lead_data

    def get_meter_no(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_data = False
        if lead_id:
            lead_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].meter_no
        return lead_data

    def get_account_no(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_data = False
        if lead_id:
            lead_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].acc_no
        return lead_data

    def get_roof_type(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_data = False
        if lead_id:
            lead_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].roof_type.name
        return lead_data

    def get_roof_type_age(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_data = False
        if lead_id:
            lead_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].age_house_year
        return lead_data

report_sxw.report_sxw('report.crm.contract', 'sale.order', 'addons/sps_crm/report/sps_contract_report.rml', parser=contract, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: