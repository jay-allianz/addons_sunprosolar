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
            'get_roof_vents_moved':self._roof_vents_moved,
            'get_dormers_moved':self._dormers_moved,
            'get_service_needed':self._service_needed,
            'get_trenching':self._trenching,
            'get_tilt_azimuth':self._tilt_azimuth,
            'get_mount':self._mount,
            'get_rebate_amt':self.get_rebate_amt,
            'get_total_due':self.get_total_due,
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
        products_str = ' '
        if lead_id:
            for data in lead_obj.browse(self.cr, self.uid, lead_id)[0].solar_ids:
                module = data.module_product_id.name
                inverter = data.inverter_product_id.name
                product = str(module) + ', ' + str(inverter) + ', '
                products_str = products_str + product
        return products_str
    
    def _tilt_azimuth(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        if lead_id:
            tilt = lead_obj.browse(self.cr, self.uid, lead_id)[0].faceing.tilt
            azimuth = lead_obj.browse(self.cr, self.uid, lead_id)[0].tilt_degree
            tilt_azimuth = str(tilt) + '/' + str(azimuth)
        return tilt_azimuth
    
    def _annul_usage(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
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
        if lead_id:
            street = lead_obj.browse(self.cr, self.uid, lead_id)[0].street or ''
            street2 = lead_obj.browse(self.cr, self.uid, lead_id)[0].street2 or ''
            lead_data = str(street) + ' ' + str(street2)
        return lead_data
    
    def get_rebate_amt(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        rebate_amt = 0.0
        if lead_obj:
            rebate = lead_obj.browse(self.cr, self.uid, lead_obj)[0].rebate
        return rebate
        
    def get_sales_person(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        if lead_id:
            lead_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].user_id.name
        return lead_data
    
    def _roof_vents_moved(self, customer):
        analytic_obj = self.pool.get("account.analytic.account")
        analytic_id = analytic_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        if analytic_id:
            roof_vents_moved = analytic_obj.browse(self.cr, self.uid, analytic_id)[0].roof_vents_moved
        return roof_vents_moved
    
    def _dormers_moved(self, customer):
        analytic_obj = self.pool.get("account.analytic.account")
        analytic_id = analytic_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        if analytic_id:
            dormers_moved = analytic_obj.browse(self.cr, self.uid, analytic_id)[0].dormers_moved
        return dormers_moved
    
    def _trenching(self, customer):
        analytic_obj = self.pool.get("account.analytic.account")
        analytic_id = analytic_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        if analytic_id:
            trenching = analytic_obj.browse(self.cr, self.uid, analytic_id)[0].trenching
        return trenching
    
    def _service_needed(self, customer):
        analytic_obj = self.pool.get("account.analytic.account")
        analytic_id = analytic_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        if analytic_id:
            service_needed = analytic_obj.browse(self.cr, self.uid, analytic_id)[0].service_needed
        return service_needed
    
    def _mount(self, customer):
        analytic_obj = self.pool.get("account.analytic.account")
        analytic_id = analytic_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        if analytic_id:
            mount = analytic_obj.browse(self.cr, self.uid, analytic_id)[0].mount
        return mount
    
    def get_total_contract_price(self, customer):
        analytic_obj = self.pool.get("account.analytic.account")
        analytic_id = analytic_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        analytic_data = False
        if analytic_id:
            analytic_data = analytic_obj.browse(self.cr, self.uid, analytic_id)[0].amount
        return analytic_data
    
    def get_total_due(self, customer):
        analytic_obj = self.pool.get("account.analytic.account")
        analytic_id = analytic_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        due = 0.0
        if analytic_id:
            total_amt = analytic_data = analytic_obj.browse(self.cr, self.uid, analytic_id)[0].amount
            deposit = analytic_data = analytic_obj.browse(self.cr, self.uid, analytic_id)[0].deposit
            due = total_amt-deposit
        return due
    
    def get_install_date(self, customer):
        analytic_obj = self.pool.get("account.analytic.account")
        analytic_id = analytic_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        analytic_data = ' '
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