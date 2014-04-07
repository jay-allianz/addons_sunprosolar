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
import datetime
from openerp.report import report_sxw
from pychart import *
import tempfile
class proposal_report(report_sxw.rml_parse):
    bar_out_filename = tempfile.mktemp(suffix=".png", prefix="bar1")
    pie_out_filename = tempfile.mktemp(suffix=".png", prefix="pie")
    old_bill_total = 0
    new_bill_total = 0
    bill_saving_total = 0
    pv_energy_total = 0
    srec_total = 0
    incentive_total = 0
    lead_cost_rebate_lines = []
    file_name = "/tmp/bar1.png"
    file_name_pie = "/tmp/pie.png"    
    customer_id = 0
    estimated_shading = 0
    number_of_years = 0
    cars_off_roads = 0.0
    tree_planting_equi = 0.0
    first_year_saving = 0.0
    co2_emission = 0
    total_saving = 0
    def __init__(self, cr, uid, name, context=None):
        super(proposal_report, self).__init__(cr, uid, name, context=context)
        self.count = 0.0
        self.localcontext.update({
            'time': time,
            'lead_STC_rating_get': self._lead_STC_rating_get ,
            'lead_CEC_rating_get': self._lead_CEC_rating_get,
            'lead_site_average_sun_get': self._lead_site_average_sun_get,
            'lead_annual_solar_prod_get': self._lead_annual_solar_prod_get,
            'lead_annual_usage_get': self._lead_annual_usage_get,
            'lead_annual_offset_get': self._lead_annual_offset_get,
            'lead_roof_type_get': self._lead_roof_type_get,
            'get_solar_info' : self._lead_solar_info,
            'calculate_cost_rebate' : self._calculate_cost_rebate,
            'lead_get_cost_rebate' : self._get_cost_rebate,
            'lead_get_old_bill_total' : self._get_old_bill_total,
            'lead_get_new_bill_total' : self._get_new_bill_total,
            'lead_get_bill_saving_total' : self._get_bill_saving_total,
            'lead_make_bar_chart' : self._make_bar_chart,
            'lead_make_pie_chart' : self._make_pie_chart,
            'get_estimate_shade' : self._get_estimated_shade,
            'get_number_of_years' : self._get_number_of_years,
            'get_cars_off_roads' : self._get_cars_off_roads,
            'get_tree_planting_equi' : self._get_tree_planting_equi,
            'get_first_year_saving' : self._get_first_year_saving,
            'get_estimated_offset' : self._get_estimated_offset,
            'get_co2_emission' : self._get_co2_emission,
            'get_gasoline_equi' : self._get_gasoline_equi,
            'get_avg_home_powered' : self._get_avg_home_powered,
            'get_avg_light_bulb_powered' : self._get_avg_light_bulb_powered,
            'get_miles_driven' : self._get_miles_driven,
            'get_gross_system_price' : self._get_gross_system_price,
            'get_net_system_cost' : self._get_net_system_cost,
            'get_total_savings' : self._get_total_savings,
            'get_rebate_amt' : self._get_rebate_amt,
            'get_lead_name':self._lead_name,
            'get_lead_street1':self._lead_street1,
            'get_lead_street2':self._lead_street2,
            'get_lead_city_id':self._lead_city_id,
            'get_count' : self.get_count,
            'set_count' : self.set_count
        })
        
    def get_count(self):
        if not self.count:
            self.count += 1
            return False
        return True
    
    def set_count(self):
        self.count = 0.0
        return '' 
        
    def _lead_name(self, id):
        lead_obj = self.pool.get("crm.lead")
        reference = 'sale.order,' + str(id)
        lead_id = lead_obj.search(self.cr, self.uid, [('ref', '=', reference)])
        lead_name = False
        if lead_id:
            lead_name = lead_obj.browse(self.cr, self.uid, lead_id)[0].name
        return lead_name
    
    def _lead_street1(self, id):
        lead_obj = self.pool.get("crm.lead")
        reference = 'sale.order,' + str(id)
        lead_id = lead_obj.search(self.cr, self.uid, [('ref', '=', reference)])
        lead_name = False
        street1=''
        if lead_id:
            street1 = lead_obj.browse(self.cr, self.uid, lead_id)[0].street
        return street1
    
    def _lead_city_id(self, id):
        lead_obj = self.pool.get("crm.lead")
        reference = 'sale.order,' + str(id)
        lead_id = lead_obj.search(self.cr, self.uid, [('ref', '=', reference)])
        lead_name = False
        city_id = ''
        if lead_id:
            name = lead_obj.browse(self.cr, self.uid, lead_id)[0].city_id.name or ''
            zip = lead_obj.browse(self.cr, self.uid, lead_id)[0].city_id.zip or ''
            state =  lead_obj.browse(self.cr, self.uid, lead_id)[0].state_id.name or ''
            country =  lead_obj.browse(self.cr, self.uid, lead_id)[0].country_id.name or ''
            
            city_id = str(name) + ' ' + str(zip) + ' ' + str(state) + ' ' + str(country)
        return city_id
    
    def _lead_street2(self, id):
        lead_obj = self.pool.get("crm.lead")
        reference = 'sale.order,' + str(id)
        lead_id = lead_obj.search(self.cr, self.uid, [('ref', '=', reference)])
        lead_name = False
        street2 = ''
        if lead_id:
            street2 = lead_obj.browse(self.cr, self.uid, lead_id)[0].street2
        return street2
    
    def _get_first_year_saving(self):
        return self.first_year_saving
    
    def _get_tree_planting_equi(self):
        return self.tree_planting_equi
    
    def _get_cars_off_roads(self):
        return self.cars_off_roads

    def _get_estimated_shade(self):
        return self.estimated_shading
    
    def _get_number_of_years(self):
        return self.number_of_years

    def _make_bar_chart(self, id):
        lead_obj = self.pool.get("crm.lead")
        tilt_azimuth_obj = self.pool.get('tilt.azimuth')
        reference = 'sale.order,' + str(id)
        lead_id = lead_obj.search(self.cr, self.uid, [('ref', '=', reference)])
        pro_data = []
        usage_data = False
        if lead_id:
            usage_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].anual_electricity_usage_ids
        else:
            return
        use_data = None
        for usage in usage_data:
            if usage.name == datetime.datetime.now().year and usage.type == "monthly":
                use_data = usage
        
        if not use_data:
            return
        theme.use_color = True
        theme.default_font_size = 14
        theme.reinitialize()
        
        fd = file(self.file_name, "w")
        can = canvas.init(fd, "png")
        data = [("Jan", use_data.jan), ("Feb", use_data.feb),
            ("Mar", use_data.mar), ("Apr", use_data.apr),
            ("May", use_data.may), ("Jun", use_data.jun),
            ("Jul", use_data.jul), ("Aug", use_data.aug),
            ("Sep", use_data.sep), ("Oct", use_data.oct),
            ("Nov", use_data.nov), ("Dec", use_data.dec)]
        
        if lead_id:
            production_data = lead_obj.browse(self.cr, self.uid, lead_id)[0]
        
        if production_data:
            pro_data = [("Jan", production_data.jan_production), ("Feb", production_data.feb_production),
                        ("Mar", production_data.mar_production), ("Apr", production_data.apr_production),
                        ("May", production_data.may_production), ("Jun", production_data.jun_production),
                        ("Jul", production_data.jul_production), ("Aug", production_data.aug_production),
                        ("Sep", production_data.sep_production), ("Oct", production_data.oct_production),
                        ("Nov", production_data.nov_production), ("Dec", production_data.dec_production)]
        ar = area.T(size=(600, 300),
                    y_grid_interval=200, 
                    x_coord = category_coord.T(data, 0),
                    x_axis=axis.X(label="", label_offset=(0, -7)),
                    y_axis=axis.Y(label="KWHs"),
                    legend=legend.T(loc=(250,-80)),
                    y_range=(0, None))
        ar.add_plot(bar_plot.T(label="Usage", data=data,width=30,fill_style = fill_style.aquamarine1), 
                    line_plot.T(label="Production", data=pro_data, ycol=1))
        ar.draw(can)
        can.close()
        return True
        
    def _make_pie_chart(self):
        theme.use_color = True
        theme.default_font_size = 20
        theme.reinitialize()
        fd = file(self.file_name_pie, "w")
        can = canvas.init(fd, "png")
        tot = self.old_bill_total + self.new_bill_total
        old_per = new_per = 0
        if tot:
            old_per = int(round((self.old_bill_total*100)/tot,0))
            new_per = int(round((self.new_bill_total*100)/tot,0))
            data = [("Old Bill " + str(old_per)+" %", old_per),("New Bill " + str(new_per)+" %", new_per)]
            ar = area.T(size=(600,600), legend=legend.T(loc=(200,0)),
                        x_grid_style = None, y_grid_style = None)
            plot = pie_plot.T(data=data, arc_offsets=[0,0,0,0],
                      fill_styles=[fill_style.aquamarine1,fill_style.yellow],
                              label_offset = 0,
                              arrow_style = arrow.fat1, radius=150)
            ar.add_plot(plot)
            ar.draw(can)
            can.close()
            return True
        
    def _get_old_bill_total(self):
        return self.old_bill_total
    
    def _get_new_bill_total(self):
        return self.new_bill_total
    
    def _get_bill_saving_total(self):
        return self.bill_saving_total
    
    def _get_cost_rebate(self):
        return self.lead_cost_rebate_lines
    
    def _get_estimated_offset(self):
        return format(int(round(self.pv_energy_total*(self.estimated_shading or 1)/100,0)),',d')
    
    def _get_co2_emission(self):
        return format(int(round(self.co2_emission,0)),',d')
    
    def _get_gasoline_equi(self):
        return format(int(round(self.gas_equi,0)),',d')
    
    def _get_avg_home_powered(self):
        return format(int(round(self.avg_home_powered,0)),',d')
    
    def _get_avg_light_bulb_powered(self):
        return format(int(round(self.avg_light_bulb_powered,0)),',d')
    
    def _get_miles_driven(self):
        return format(int(round(self.miles_driven,0)),',d')
    
    def _get_gross_system_price(self):
        return self.grand_total
    
    def _get_net_system_cost(self):
        return self.net_system_cost or 0.1
    
    def _get_total_savings(self):
        return self.total_saving
    
    def _get_rebate_amt(self):
        return self.rebate_amt
    
    def _calculate_cost_rebate(self, id):
        lead_obj = self.pool.get("crm.lead")
        user_obj = self.pool.get('res.users')
        reference = 'sale.order,' + str(id)
        lead_id = lead_obj.search(self.cr, self.uid, [('ref', '=', reference)])
        cur_user = user_obj.browse(self.cr, self.uid, self.uid)
        sale_order_data = self.pool.get('sale.order').browse(self.cr, self.uid, id)
        lead_data = []
        crm_lead = False
        self.number_of_years = self.cars_off_roads = self.tree_planting_equi = self.co2_emission = self.gas_equi = self.avg_home_powered = self.avg_light_bulb_powered = self.miles_driven = self.rebate_amt = 0
        if lead_id:
            crm_lead = lead_obj.browse(self.cr, self.uid, lead_id)[0]
            lead_data = crm_lead.cost_rebate_ids
            self.estimated_shading = crm_lead.estimate_shade
            self.number_of_years = crm_lead.number_of_years
            self.cars_off_roads = crm_lead.cars_off_roads * crm_lead.number_of_years
            self.tree_planting_equi = crm_lead.tree_planting_equi * crm_lead.number_of_years
            self.co2_emission = crm_lead.co2_offset_pounds * crm_lead.number_of_years
            self.gas_equi = crm_lead.gasoline_equi * crm_lead.number_of_years
            self.avg_home_powered = crm_lead.ave_home_powered * crm_lead.number_of_years
            self.avg_light_bulb_powered = crm_lead.ave_light_bulb_powered * crm_lead.number_of_years
            self.miles_driven = cur_user.company_id.avg_yearly_miles * crm_lead.number_of_years
            self.rebate_amt = crm_lead.rebate_amt
        self.old_bill_total = 0
        self.new_bill_total = 0
        self.bill_saving_total = 0
        flag = True
        self.grand_total = sale_order_data.amount_total
        self.srec_total = 0
        self.incentive_total = 0
        self.total_saving = 0
        if lead_data:
            for cost_rebate in lead_data:
                if flag:
                    self.first_year_saving = cost_rebate.elec_bill_savings
                    flag = False
                self.old_bill_total += cost_rebate.old_bill
                self.new_bill_total += cost_rebate.new_bill
                self.bill_saving_total += cost_rebate.elec_bill_savings
                self.pv_energy_total += cost_rebate.pv_energy
                self.total_saving += cost_rebate.srecs + cost_rebate.incentives + cost_rebate.depriciation_savings
                self.srec_total += cost_rebate.srecs
                self.incentive_total += cost_rebate.incentives
        self.net_system_cost = self.grand_total - self.srec_total - self.incentive_total
        self.lead_cost_rebate_lines = lead_data
            
    def _lead_STC_rating_get(self, id):
        lead_obj = self.pool.get("crm.lead")
        reference = 'sale.order,' + str(id)
        lead_id = lead_obj.search(self.cr, self.uid, [('ref', '=', reference)])
        lead_data = False
        if lead_id:
            lead_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].stc_dc_rating
        return lead_data
    
    def _lead_CEC_rating_get(self, id):
        lead_obj = self.pool.get("crm.lead")
        reference = 'sale.order,' + str(id)
        lead_id = lead_obj.search(self.cr, self.uid, [('ref', '=', reference)])
        lead_cec_data = False
        if lead_id:
            lead_cec_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].cec_ac_rating
        return lead_cec_data
    
    def _lead_site_average_sun_get(self, id):
        lead_obj = self.pool.get("crm.lead")
        reference = 'sale.order,' + str(id)
        lead_id = lead_obj.search(self.cr, self.uid, [('ref', '=', reference)])
        lead_avg_sun_data = False
        if lead_id:
            lead_avg_sun_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].site_avg_sun_hour
        return lead_avg_sun_data  
    
    def _lead_annual_solar_prod_get(self, id):
        lead_obj = self.pool.get("crm.lead")
        reference = 'sale.order,' + str(id)
        lead_id = lead_obj.search(self.cr, self.uid, [('ref', '=', reference)])
        lead_annual_solar_pro_data = False
        if lead_id:
            lead_annual_solar_pro_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].annual_solar_prod
        return lead_annual_solar_pro_data
    
    def _lead_annual_usage_get(self, id):
        lead_obj = self.pool.get("crm.lead")
        reference = 'sale.order,' + str(id)
        lead_id = lead_obj.search(self.cr, self.uid, [('ref', '=', reference)])
        lead_annual_usage_get = False
        if lead_id:
            lead_annual_usage_get = lead_obj.browse(self.cr, self.uid, lead_id)[0].annual_ele_usage
        return lead_annual_usage_get
    
    def _lead_annual_offset_get(self, customer):
        lead_obj = self.pool.get("crm.lead")
        lead_id = lead_obj.search(self.cr, self.uid, [('partner_id.id', '=', customer)])
        lead_annual_offset_get = False
        if lead_id:
            lead_annual_offset_get = lead_obj.browse(self.cr, self.uid, lead_id)[0].co2_offset_tons
        return lead_annual_offset_get
    
    def _lead_roof_type_get(self, id):
        lead_obj = self.pool.get("crm.lead")
        reference = 'sale.order,' + str(id)
        lead_id = lead_obj.search(self.cr, self.uid, [('ref', '=', reference)])
        lead_roof_type_get = False
        if lead_id:
            lead_roof_type_get = lead_obj.browse(self.cr, self.uid, lead_id)[0].roof_type.name
        return lead_roof_type_get
    
    def _lead_solar_info(self, id):
        lead_obj = self.pool.get("crm.lead")
        reference = 'sale.order,' + str(id)
        lead_id = lead_obj.search(self.cr, self.uid, [('ref', '=', reference)])
        solar_data = False
        solar_info = []
        if lead_id:
            solar_data = lead_obj.browse(self.cr, self.uid, lead_id)[0].solar_ids
        if not solar_data:
            return solar_info
        tilt_degree_dict = {'n':'North',
                        'ne':'North-East',
                        'e':'East',
                        'se':'South-East',
                        's':'South',
                        'sw':'South-West',
                        'w':'West',
                        'nw':'North-West'}
        i = 1
        for solar in solar_data:
            info_dict = {}
            info_dict['arr_name'] = "Array "+str(i)+" :"
            info_dict['module_info'] = str(solar.num_of_module)+" "+solar.module_product_id.name+" Modules"
            info_dict['inverter_info'] = str(solar.num_of_invertor)+" "+solar.inverter_product_id.name+" Modules"
            info_dict['orientation_info'] = solar.faceing.tilt+" degrees "+ tilt_degree_dict.get(solar.tilt_degree,"") + " Orientation"
            solar_info.append(info_dict)
            i += 1
        return solar_info
    
    
    
report_sxw.report_sxw('report.proposal.report', 'sale.order', 'addons/sps_crm/report/sps_proposal.rml', parser=proposal_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
