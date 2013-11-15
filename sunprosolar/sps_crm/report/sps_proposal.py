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
import pygal                                                       # First import pygal


class proposal_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(proposal_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'lead_STC_rating_get': self._lead_STC_rating_get ,
            'lead_CEC_rating_get': self._lead_CEC_rating_get,
            'lead_site_average_sun_get': self._lead_site_average_sun_get,
            'lead_annual_solar_prod_get': self._lead_annual_solar_prod_get,
            'lead_annual_usage_get': self._lead_annual_usage_get,
            'lead_annual_offset_get': self._lead_annual_offset_get,
            'lead_roof_type_get': self._lead_roof_type_get,
            'lead_module_info_get': self._lead_module_info_get,
            'lead_invertor_info_get': self._lead_invertor_info_get,
#            'bar_chart':self._bar_chart,
        })
        
#    def _bar_chart(self):
#        bar_chart = pygal.Bar()                                            # Then create a bar graph object
#        bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
#        bar_chart.render_to_file('bar_chart.svg')
#        
        
    def _lead_STC_rating_get(self, customer):
        lead_obj=self.pool.get("crm.lead")
        lead_id= lead_obj.search(self.cr, self.uid, [('partner_id.id','=',customer)])
        lead_data=False
        if lead_id:
            lead_data = lead_obj.browse(self.cr,self.uid,lead_id)[0].stc_dc_rating
        return lead_data
    
    def _lead_CEC_rating_get(self, customer):
        lead_obj=self.pool.get("crm.lead")
        lead_id= lead_obj.search(self.cr, self.uid, [('partner_id.id','=',customer)])
        lead_cec_data=False
        if lead_id:
            lead_cec_data = lead_obj.browse(self.cr,self.uid,lead_id)[0].cec_ac_rating
        return lead_cec_data
    
    def _lead_site_average_sun_get(self, customer):
        lead_obj=self.pool.get("crm.lead")
        lead_id= lead_obj.search(self.cr, self.uid, [('partner_id.id','=',customer)])
        lead_avg_sun_data=False
        if lead_id:
            lead_avg_sun_data = lead_obj.browse(self.cr,self.uid,lead_id)[0].site_avg_sun_hour
        return lead_avg_sun_data  
    
    def _lead_annual_solar_prod_get(self, customer):
        lead_obj=self.pool.get("crm.lead")
        lead_id= lead_obj.search(self.cr, self.uid, [('partner_id.id','=',customer)])
        lead_annual_solar_pro_data=False
        if lead_id:
            lead_annual_solar_pro_data = lead_obj.browse(self.cr,self.uid,lead_id)[0].annual_solar_prod
        return lead_annual_solar_pro_data
    
    def _lead_annual_usage_get(self, customer):
        lead_obj=self.pool.get("crm.lead")
        lead_id= lead_obj.search(self.cr, self.uid, [('partner_id.id','=',customer)])
        lead_annual_usage_get=False
        if lead_id:
            lead_annual_usage_get = lead_obj.browse(self.cr,self.uid,lead_id)[0].annual_ele_usage
        return lead_annual_usage_get
    
    def _lead_annual_offset_get(self, customer):
        lead_obj=self.pool.get("crm.lead")
        lead_id= lead_obj.search(self.cr, self.uid, [('partner_id.id','=',customer)])
        lead_annual_offset_get=False
        if lead_id:
            lead_annual_offset_get = lead_obj.browse(self.cr,self.uid,lead_id)[0].co2_offset_tons
        return lead_annual_offset_get
    
    def _lead_roof_type_get(self, customer):
        lead_obj=self.pool.get("crm.lead")
        lead_id= lead_obj.search(self.cr, self.uid, [('partner_id.id','=',customer)])
        lead_roof_type_get=False
        if lead_id:
            lead_roof_type_get = lead_obj.browse(self.cr,self.uid,lead_id)[0].roof_type.name
        return lead_roof_type_get
    
    def _lead_module_info_get(self, customer):
        lead_obj=self.pool.get("crm.lead")
        lead_id= lead_obj.search(self.cr, self.uid, [('partner_id.id','=',customer)])
        lead_module_info_get=""
        if lead_id:
            no_module = lead_obj.browse(self.cr,self.uid,lead_id)[0].num_of_module
            lead_module_name = lead_obj.browse(self.cr,self.uid,lead_id)[0].module_product_id.name
            lead_module_info_get = str(no_module) +" " + str(lead_module_name)  + " Modules"
        return lead_module_info_get
    
    def _lead_invertor_info_get(self, customer):
        lead_obj=self.pool.get("crm.lead")
        lead_id= lead_obj.search(self.cr, self.uid, [('partner_id.id','=',customer)])
        lead_invertor_info_get=""
        if lead_id:
            no_invertor = lead_obj.browse(self.cr,self.uid,lead_id)[0].num_of_invertor
            lead_invertor_name = lead_obj.browse(self.cr,self.uid,lead_id)[0].inverter_product_id.name
            lead_invertor_info_get = str(no_invertor) +" " + str(lead_invertor_name)  + " Invertor"
        return lead_invertor_info_get
    
report_sxw.report_sxw('report.proposal.report', 'sale.order', 'addons/sps_crm/report/sps_proposal.rml', parser=proposal_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: