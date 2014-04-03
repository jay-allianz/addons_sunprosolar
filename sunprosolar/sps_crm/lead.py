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
from openerp.osv import fields, osv
import datetime
from tools.translate import _
import math
import time
import tools
from openerp import SUPERUSER_ID

class type_of_sale(osv.Model):

    _name = "type.of.sale"
    _columns = {
            'name': fields.char('Type Of Sale', size=30),
            'number_of_days': fields.integer('Number Of Days'),
        }
    
class crm_lead(osv.Model):
    """ Model for CRM Lead. """
    _inherit = "crm.lead"
    
    def _lead_create_contact(self, cr, uid, lead, name, is_company, parent_id=False, context=None):
        partner = self.pool.get('res.partner')
        vals = {'name': name,
            'user_id': lead.user_id.id,
            'comment': lead.description,
            'section_id': lead.section_id.id or False,
            'parent_id': lead.utility_company_id.id or False,
            'phone': lead.phone,
            'mobile': lead.mobile,
            'email': tools.email_split(lead.email_from) and tools.email_split(lead.email_from)[0] or False,
            'fax': lead.fax,
            'title': lead.title and lead.title.id or False,
            'function': lead.function,
            'street': lead.street,
            'street2': lead.street2,
            'zip': lead.zip,
            'city': lead.city,
            'country_id': lead.country_id and lead.country_id.id or False,
            'state_id': lead.state_id and lead.state_id.id or False,
            'is_company': is_company,
            'type': 'contact'
        }
        partner = partner.create(cr, uid, vals, context=context)
        return partner
    
    def on_change_station_and_utility(self, cr, uid, ids, city_id, context=None):
        values ={'utility_company_id': False, 'loc_station_id': False}
        if city_id:
            station_obj = self.pool.get('insolation.incident.yearly')
            utility_company_obj = self.pool.get('res.partner')
            city = self.pool.get('city.city').browse(cr, uid, city_id, context=context)
            utility_ids = utility_company_obj.search(cr, uid, [('is_utility_company','=',1),('from_zip','<=',int(city.zip)),('to_zip','>=',int(city.zip))], context=context)
            station_ids = station_obj.search(cr, uid, [], context=context)
            if not station_ids:
                raise osv.except_osv(_('Warning'), _('Station is not defined!'))
            station_data = station_obj.browse(cr, uid, station_ids, context=context)
            if utility_ids:
                u_company = utility_ids[0]
                utility_company_data = utility_company_obj.browse(cr, uid, utility_ids, context=context)
                for u_data in utility_company_data:
                    for data in station_data:
                        values = {'utility_company_id' : u_data.id or False,
                                   'loc_station_id' : data.id or False}
        return {'value' : values}

    def on_change_partner(self, cr, uid, ids, partner_id, context=None):
        res = super(crm_lead, self).on_change_partner(cr, uid, ids, partner_id, context=context)
        values = {}
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            res['value'].update({'partner_is_company':partner.is_company,
                                 'spouse' : partner.spouse and partner.spouse.id or False,
                                 'contact_name': partner.name or '',
                                 'last_name': partner.last_name or '',
                                 'city_id' : partner.city_id and partner.city_id.id or False,
                                 })
        return res

    def _get_deadline(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context=context):
            date_today = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
            deadline = date_today + datetime.timedelta(days=data and data.type_of_sale_id and data.type_of_sale_id.number_of_days or 0)
            res[data.id] = str(deadline.date())
        return res
        
    def _reponsible_user(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for u in self.browse(cr, uid, ids, context=context):
            partner = self.pool.get('res.users').browse(cr, uid, uid, context=context)
            user = partner.name
            res[u.id] = user
        return res

    def _get_require_doc(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context=context):
            for doc in data.doc_req_ids:
                if doc.document_id:
                    if doc.document_id.datas == False:
                        res[data.id] = False
                    else:
                        res[data.id] = True
                else:
                    res[data.id] = False
        return res
    
    def _get_stc_dc_rating(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            rating = 0.0
            for line in data.solar_ids:
                rating += line.stc_dc_rating
            res[data.id] = rating
        return res
    
    def _get_ptc_dc_rating(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            rating = 0.0
            for line in data.solar_ids:
                rating += line.ptc_dc_rating
            res[data.id] = rating
        return res
    
    def _get_cec_ac_rating(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            rating = 0.0
            for line in data.solar_ids:
                rating += line.cec_ac_rating
            res[data.id] = rating
        return res
    
    def _get_ptc_stc_ratio(self, cr, uid, ids, name, args, context=None):
        res={}
        rating=0.0
        line_number=0
        for data in self.browse(cr, uid, ids, context):
            for line in data.solar_ids:
                rating += line.ptc_stc_ratio
                line_number += 1
            if line_number:
                res[data.id] = rating/line_number
            else:
                res[data.id] = rating
        return res
     
    def _get_output(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            output = 0.0
            line_number = 0
            for line in data.solar_ids:
                output += line.array_output
                line_number += 1
            if line_number:
                res[data.id] = output / line_number
            else:
                res[data.id] = output
        return res
    
    def _get_annual_solar_prod(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            annual_prod = 0
            for line in data.solar_ids:
                annual_prod += line.annual_solar_prod or 0
            res[data.id] = annual_prod
        return res
    
    def _get_annual_solar_prod_display(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            annual_solar_prod_display = 0
            for line in data.solar_ids:
                annual_solar_prod_display += line.annual_solar_prod_display or 0
            res[data.id] = annual_solar_prod_display
        return res
    
    def _get_annual_ele_usage(self, cr, uid, ids, name, args, context=None):
        res = {}
        line_number=0
        for data in self.browse(cr, uid, ids, context):
            annual_ele_usage = 0.0
            for line in data.solar_ids:
                line_number += 1
                annual_ele_usage += line.annual_ele_usage
            if line_number:
                res[data.id] = annual_ele_usage/line_number
            else:
                res[data.id] = annual_ele_usage
        return res
    
    def _get_site_avg_sun_hour(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            site_avg_hour = 0.0
            no_of_arr = 0
            if data.solar_ids:
                no_of_arr = len(data.solar_ids)
            for line in data.solar_ids:
                site_avg_hour += line.site_avg_sun_hour
            if no_of_arr != 0:
                res[data.id] = site_avg_hour / no_of_arr
            else:
                res[data.id] = site_avg_hour
        return res

    def _get_co2_offset_tons(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            co2_offset_tons = 0.0
            for line in data.solar_ids:
                co2_offset_tons += line.co2_offset_tons
            co2_offset_tons_r = round(co2_offset_tons, 0)
            res[data.id] = co2_offset_tons_r
        return res 

    def _get_co2_offset_pounds(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            co2_offset_pounds = 0.0
            for line in data.solar_ids:
                co2_offset_pounds += line.co2_offset_pounds
            co2_offset_pounds_r = round(co2_offset_pounds, 0)
            res[data.id] = co2_offset_pounds_r
        return res
    
    def _get_cars_off_roads(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            cars_off_roads = 0.0
            for line in data.solar_ids:
                cars_off_roads += line.cars_off_roads
            cars_off_roads_r = round(cars_off_roads,0)
            res[data.id] = cars_off_roads_r
        return res
    
    def _get_gasoline_equi(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            gasoline_equi = 0.0
            for line in data.solar_ids:
                gasoline_equi += line.gasoline_equi
            gasoline_equi_r = round(gasoline_equi, 0)
            res[data.id] = gasoline_equi_r
        return res
    
    def _get_tree_equi(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            tree_equi = 0.0
            for line in data.solar_ids:
                tree_equi += line.tree_equi
            tree_equi_r = round(tree_equi, 0)
            res[data.id] = tree_equi_r
        return res
    
    def _get_tree_planting_equi(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            tree_planting_equi = 0.0
            for line in data.solar_ids:
                tree_planting_equi += line.tree_planting_equi
            tree_planting_equi_r = round(tree_planting_equi, 0)
            res[data.id] = tree_planting_equi_r
        return res
    
    def _get_ave_home_powered(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            ave_home_powered = 0.0
            for line in data.solar_ids:
                ave_home_powered += line.ave_home_powered
            ave_home_powered_r = round(ave_home_powered ,0)
            res[data.id] = ave_home_powered_r
        return res
    
    def _get_ave_light_bulb_powered(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            ave_light_bulb_powered = 0.0
            for line in data.solar_ids:
                ave_light_bulb_powered += line.ave_light_bulb_powered
            ave_light_bulb_powered_r = round(ave_light_bulb_powered, 0)
            res[data.id] = ave_light_bulb_powered_r
        return res
    
    def _get_years_40_offset_tree(self, cr, uid, ids, name, args, context=None):
        res = {}
        years_40_offset_tree = 0.0
        for data in self.browse(cr, uid, ids, context):
            years_40_offset_tree = data.annual_equvi_tree * 40
            res[data.id] = years_40_offset_tree
        return res
    
    def _get_annnual_co2_car(self, cr, uid, ids, name, args, context=None):
        res = {}
        annnual_co2_car = 0.0
        for data in self.browse(cr, uid, ids, context):
            annnual_co2_car = data.medium_pollusion * data.avg_yearly_miles
            res[data.id] = annnual_co2_car
        return res
    
    def _get_old_bill(self, cr, uid, ids, context=None):
        res = {}
        pricelist_obj = self.pool.get('product.pricelist')
        product_obj = self.pool.get('product.product')
        product_ids = product_obj.search(cr, uid, [], context=context)
        pro_id = product_ids and product_ids[0]
        for data in self.browse(cr, uid, ids, context):
            price = 0.0
            total_old_bill = 0.0
            old_bill =  0.0
            usage = 0.0
            count = 1
            if data.utility_company_id and data.utility_company_id.property_product_pricelist:
                context.update({'get_field':'summer_qty'})
                summer_qty = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, data.annual_ele_usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                if data.anual_electricity_usage_ids :
                    year = data.anual_electricity_usage_ids[0].name
                    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                        month_list = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    else:
                        month_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    if data.anual_electricity_usage_ids[0].type == 'yearly':
                        usage = data.anual_electricity_usage_ids[0].usage_kwh / 12
                    for days in month_list:
                        if data.anual_electricity_usage_ids[0].type == 'monthly':
                            if count == 1:
                                usage = data.anual_electricity_usage_ids[0].jan
                            elif count == 2:
                                usage = data.anual_electricity_usage_ids[0].feb
                            elif count == 3:
                                usage = data.anual_electricity_usage_ids[0].mar
                            elif count == 4:
                                usage = data.anual_electricity_usage_ids[0].apr
                            elif count == 5:
                                usage = data.anual_electricity_usage_ids[0].may
                            elif count == 6:
                                usage = data.anual_electricity_usage_ids[0].jun
                            elif count == 7:
                                usage = data.anual_electricity_usage_ids[0].jul
                            elif count == 8:
                                usage = data.anual_electricity_usage_ids[0].aug
                            elif count == 9:
                                usage = data.anual_electricity_usage_ids[0].sep
                            elif count == 10:
                                usage = data.anual_electricity_usage_ids[0].oct
                            elif count == 11:
                                usage = data.anual_electricity_usage_ids[0].nov
                            elif count == 12:
                                usage = data.anual_electricity_usage_ids[0].dec
                        count += 1
                        year += 1
                        if not summer_qty:
                            summer_qty = 0
                        basline = summer_qty * days
                        over_basline1 = basline * 0.3
                        over_basline2 = basline * 0.7
                        context.update({'get_field':'daily_meter_charges'})
                        
                        daily_meter_charge = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, data.annual_ele_usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not daily_meter_charge:
                            daily_meter_charge = 0
                        basic_charge = daily_meter_charge * days
                        
                        context.update({'get_field':'tier1'})
                        tier1 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, data.annual_ele_usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not tier1:
                            tier1 = 0
                        base_line_summer = days * 13.5 * tier1
                        
                        context.update({'get_field':'off_peak_tier2'})
                        peak_tier2 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, data.annual_ele_usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not peak_tier2:
                            peak_tier2 = 0
                        over_base_line1_1 = over_basline1 * peak_tier2
                        
                        context.update({'get_field':'part_peak_tier3'})
                        peak_tier3 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, data.annual_ele_usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not peak_tier3:
                            peak_tier3 = 0
                        over_base_line1_2 = over_basline2 * peak_tier3
                        
                        context.update({'get_field':'surcharge_3'})
                        surcharge3 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, data.annual_ele_usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not surcharge3:
                            surcharge3 = 0
                        
                        context.update({'get_field':'surcharge_4'})
                        surcharge4 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, data.annual_ele_usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not surcharge4:
                            surcharge4 = 0
                        
                        context.update({'get_field':'surcharge_5'})
                        surcharge5 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, data.annual_ele_usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not surcharge5:
                            surcharge5 = 0
                        
                        context.update({'get_field':'surcharge_6'})
                        surcharge6 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, data.annual_ele_usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not surcharge6:
                            surcharge6 = 0
                        
                        context.update({'get_field':'rate_stablization'})
                        rate_stablization = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, data.annual_ele_usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not rate_stablization:
                            rate_stablization = 0
                        delivery_subtotal = basic_charge + round(base_line_summer,2) + round(over_base_line1_1,2) + round(over_base_line1_2,2) + surcharge3 + surcharge4 + surcharge5 + surcharge6 + rate_stablization
                        
                        context.update({'get_field':'stage_changes'})
                        stage_change = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, data.annual_ele_usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not stage_change:
                            stage_change = 0
                        stage_changes = stage_change * usage
                        
                        total_old_bill = delivery_subtotal + stage_changes
                        old_bill = old_bill + total_old_bill
        return old_bill
    
    def _get_new_bill(self, cr, uid, ids, context=None):
        res = {}
        pricelist_obj = self.pool.get('product.pricelist')
        product_obj = self.pool.get('product.product')
        tilt_azimuth_obj = self.pool.get('tilt.azimuth')
        product_ids = product_obj.search(cr, uid, [], context=context)
        pro_id = product_ids and product_ids[0]
        for data in self.browse(cr, uid, ids, context):
            final_new_bill = 0.0
            bill_new = 0.0
            new_bill =  0.0
            new_bill_list = []
            flag = 0
            
            for solar_line_data in data.solar_ids:
                price = 0.0
                new_bill =  0.0
                count = 1
                production = 0.0
                usage = 0.0
                total_new_bill = 0.0
                tilt_azimuth_id = tilt_azimuth_obj.search(cr, uid, [('tilt_azimuth_id','=',solar_line_data.loc_station_id.id),('tilt','=', solar_line_data.faceing.id),('azimuth','=',solar_line_data.tilt_degree)], context=context)
                if tilt_azimuth_id:
                    jan_production = data.jan_production
                    feb_production = data.feb_production
                    mar_production = data.mar_production
                    apr_production = data.apr_production
                    may_production = data.may_production
                    jun_production = data.jun_production
                    jul_production = data.jul_production
                    aug_production = data.aug_production
                    sep_production = data.sep_production
                    oct_production = data.oct_production
                    nov_production = data.nov_production
                    dec_production = data.dec_production
                            
                    cur_year = datetime.datetime.now().year
                    if cur_year % 4 == 0 and cur_year % 100 != 0 or cur_year % 400 == 0:
                        month_list = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    else:
                        month_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    for days in month_list:
                        if count == 1:
                            usage = jan_production
                        elif count == 2:
                            usage = feb_production
                        elif count == 3:
                            usage = mar_production
                        elif count == 4:
                            usage = apr_production
                        elif count == 5:
                            usage = may_production
                        elif count == 6:
                            usage = jun_production
                        elif count == 7:
                            usage = jul_production
                        elif count == 8:
                            usage = aug_production
                        elif count == 9:
                            usage = sep_production
                        elif count == 10:
                            usage = oct_production
                        elif count == 11:
                            usage = nov_production
                        elif count == 12:
                            usage = dec_production
                        count += 1
                        
                        context.update({'get_field':'summer_qty'})
                        summer_qty = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not summer_qty:
                            summer_qty = 0
                        basline = summer_qty * days
                        over_basline1 = basline * 0.3
                        over_basline2 = basline * 0.7
                        context.update({'get_field':'daily_meter_charges'})
                                
                        daily_meter_charge = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not daily_meter_charge:
                            daily_meter_charge = 0
                        basic_charge = daily_meter_charge * days
                                
                        context.update({'get_field':'tier1'})
                        tier1 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not tier1:
                            tier1 = 0
                        base_line_summer = days * 13.5 * tier1
                                
                        context.update({'get_field':'off_peak_tier2'})
                        peak_tier2 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not peak_tier2:
                            peak_tier2 = 0
                        over_base_line1_1 = over_basline1 * peak_tier2
                                
                        context.update({'get_field':'part_peak_tier3'})
                        peak_tier3 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not peak_tier3:
                            peak_tier3 = 0
                        over_base_line1_2 = over_basline2 * peak_tier3
                                
                        context.update({'get_field':'surcharge_3'})
                        surcharge3 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not surcharge3:
                            surcharge3 = 0
                                
                        context.update({'get_field':'surcharge_4'})
                        surcharge4 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not surcharge4:
                            surcharge4 = 0
                                
                        context.update({'get_field':'surcharge_5'})
                        surcharge5 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not surcharge5:
                            surcharge5 = 0
                                
                        context.update({'get_field':'surcharge_6'})
                        surcharge6 = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not surcharge6:
                            surcharge6 = 0
                                
                        context.update({'get_field':'rate_stablization'})
                        rate_stablization = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not rate_stablization:
                            rate_stablization = 0
                        delivery_subtotal = basic_charge + round(base_line_summer,2) + round(over_base_line1_1,2) + round(over_base_line1_2,2) + surcharge3 + surcharge4 + surcharge5 + surcharge6 + rate_stablization
                                
                        context.update({'get_field':'stage_changes'})
                        stage_change = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, usage, context=context)[data.utility_company_id.property_product_pricelist.id]
                        if not stage_change:
                            stage_change = 0
                        stage_changes = stage_change * usage
                        
                        total_new_bill = delivery_subtotal + stage_changes
                        new_bill = new_bill + total_new_bill
            new_bill_list.append(new_bill)
            for bill in new_bill_list:
                bill_new += bill
                flag += 1
            final_new_bill = bill_new / flag
        return final_new_bill

    def _get_company_tier_amount(self, cr, uid, ids, name, args, context=None):
        res = {}
        pricelist_obj = self.pool.get('product.pricelist')
        product_obj = self.pool.get('product.product')
        product_ids = product_obj.search(cr, uid, [], context=context)
        pro_id = product_ids and product_ids[0]
        for data in self.browse(cr, uid, ids, context):
            price = 0.0
            if data.utility_company_id and data.utility_company_id.property_product_pricelist:
                price = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, data.annual_ele_usage, data.partner_id.id, context=context)[data.utility_company_id.property_product_pricelist.id]
            res[data.id] = price
        return res

    def _get_cost_rebate(self, cr, uid, ids, name, args, context=None):
        result = {}
        
        cost = 0.0
        for data in self.browse(cr, SUPERUSER_ID, ids, context=context):
            result[data.id] = {
                'cost' : 0.0,
                'down_payment_amt' : 0.0, 
                'loan_amt' : 0.0,
                'rebate_amt' : 0.0,
                'cost_peack_kw' : 0.0,
                'inverter_cost' : 0.0,
            }
            cost = 0 
            cost_per_array= 0.0
            down_payment_amt = 0
            rebate_amt = 0
            cost_peack_kw = 0.0
            inverter_cost = 0.0
            
            if data.solar_ids:
                for array_id in data.solar_ids:
#                    cost_per_array = (array_id.num_of_module * (((array_id.module_product_id.pv_module_power_stc * array_id.module_product_id.cost_per_stc_watt)+(array_id.module_product_id.pv_module_power_stc * array_id.module_product_id.labor_per_stc_watt)+(array_id.module_product_id.pv_module_power_stc * array_id.module_product_id.materials_per_stc)) * (1 + array_id.module_product_id.markup / 100)))  + (array_id.num_of_invertor * ((array_id.inverter_product_id.power_rating * array_id.inverter_product_id.cost_per_ac_capacity_watt)+(array_id.inverter_product_id.power_rating * array_id.inverter_product_id.labor_per_ac_watt)+(array_id.inverter_product_id.power_rating * array_id.inverter_product_id.materials_per_ac_watt)))
#                    cost_per_array = (array_id.module_product_id.standard_price * array_id.num_of_module) + (array_id.inverter_product_id.standard_price * array_id.num_of_invertor)
                    cost_per_array = (((array_id.stc_dc_rating * 1000 * array_id.module_product_id.cost_per_stc_watt)+(array_id.stc_dc_rating * 1000 * array_id.module_product_id.labor_per_stc_watt)+(array_id.stc_dc_rating * 1000 * array_id.module_product_id.materials_per_stc)) * (1 + (array_id.module_product_id.markup / 100)))  + ((array_id.inverter_product_id.power_rating * array_id.inverter_product_id.cost_per_ac_capacity_watt)+(array_id.inverter_product_id.power_rating * array_id.inverter_product_id.labor_per_ac_watt)+(array_id.inverter_product_id.power_rating * array_id.inverter_product_id.materials_per_ac_watt))
                    cost += cost_per_array
                    cost_peack_kw += (((array_id.stc_dc_rating * 1000 * array_id.module_product_id.cost_per_stc_watt)+(array_id.stc_dc_rating * 1000 * array_id.module_product_id.labor_per_stc_watt)+(array_id.stc_dc_rating * 1000 * array_id.module_product_id.materials_per_stc)) * (1 + (array_id.module_product_id.markup / 100)))
                    inverter_cost += ((array_id.inverter_product_id.power_rating * array_id.inverter_product_id.cost_per_ac_capacity_watt)+(array_id.inverter_product_id.power_rating * array_id.inverter_product_id.labor_per_ac_watt)+(array_id.inverter_product_id.power_rating * array_id.inverter_product_id.materials_per_ac_watt))
            if cost and data.down_payment:
                down_payment_amt = cost * data.down_payment
            if cost and data.rebate:
                rebate_amt = cost * data.rebate
            loan_amt = cost - down_payment_amt - rebate_amt
            result[data.id] = {
                'cost' : cost,
                'down_payment_amt' : down_payment_amt,
                'rebate_amt' : rebate_amt, 
                'loan_amt' : loan_amt,
                'cost_peack_kw' : cost_peack_kw,
                'inverter_cost' : inverter_cost,
            }
        return result
    
    def _get_pbi_epbb_incentive(self, cr, uid, ids, name, args, context=None):
        result = {}
        epbb_resi = {1:0.0,2:2.50,3:2.20,4:1.90,5:1.55,6:1.10,7:0.65,8:0.35,9:0.25,10:0.20}
        epbb_comm = {1:0.0,2:2.50,3:2.20,4:1.90,5:1.55,6:1.10,7:0.65,8:0.35,9:0.25,10:0.20}
        epbb_non_pro = {1:0.0,2:3.25,3:2.95,4:2.65,5:2.30,6:1.85,7:1.40,8:1.10,9:0.90,10:0.70}
        epbb = {'residential':epbb_resi,'commercial':epbb_comm,'non_profit':epbb_non_pro}
        pbi_resi = {1:0.0,2:0.39,3:0.34,4:0.26,5:0.22,6:0.15,7:0.09,8:0.05,9:0.03,10:0.03}
        pbi_comm = {1:0.0,2:0.39,3:0.34,4:0.26,5:0.22,6:0.15,7:0.09,8:0.05,9:0.03,10:0.03}
        pbi_non_pro = {1:0.0,2:0.50,3:0.46,4:0.37,5:0.32,6:0.26,7:0.19,8:0.15,9:0.12,10:0.09}
        pbi = {'residential':pbi_resi,'commercial':pbi_comm,'non_profit':pbi_non_pro}
        insentive_data = {'epbb':epbb,'pbi':pbi}
        pbi_epbb_incentive = 0.0
        for data in self.browse(cr, uid, ids, context):
            if data.insentive_type:
                epbb_or_pbi = insentive_data.get(data.insentive_type,{})
                if data.property:
                    res_com_pro = epbb_or_pbi.get(data.property,{})
                    if data.sci_step:
                        pbi_epbb_incentive = res_com_pro.get(data.sci_step,0.0)
            result[data.id] = pbi_epbb_incentive
        return result
    
    def run_lead_days(self, cr, uid, automatic=False, use_new_cursor=False, context=None):
        lead_ids = self.search(cr, uid, [('type','=','lead')], context=context)
        if lead_ids:
            for lead_brw in self.browse(cr, uid, lead_ids, context=context):
                flag = True
                for doc in lead_brw.doc_req_ids:
                    if doc.collected == False:
                        flag = False
                if lead_brw and lead_brw.lead_date:
                    date_today = datetime.datetime.strptime(str(lead_brw.lead_date), "%Y-%m-%d")
                    deadline = date_today + datetime.timedelta(days=lead_brw and lead_brw.lead_days or 0)
                    if datetime.datetime.today() > deadline and flag == False:
                        obj_mail_server = self.pool.get('ir.mail_server')
                        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
                        if not mail_server_ids:
                            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
                        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
                        email_from = mail_server_record.smtp_user
                        if not email_from:
                            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
                        if not lead_brw.email_from:
                            raise osv.except_osv(_('Warning'), _('%s User have no email defined !'))
                        else:
                            subject_line = 'Notification For Upload documents.'
                            message_body = 'Hello,' + tools.ustr(lead_brw.contact_name) + ' ' + tools.ustr(lead_brw.last_name) + '<br/><br/>Please upload your required documents ! <br/><br/><br/> Thank You.'
                            message_user = obj_mail_server.build_email(
                                email_from=email_from,
                                email_to=[lead_brw.email_from],
                                subject=subject_line,
                                body=message_body,
                                body_alternative=message_body,
                                email_cc=None,
                                email_bcc=None,
                                attachments=None,
                                references=None,
                                object_id=None,
                                subtype='html',
                                subtype_alternative=None,
                                headers=None)
                            self.send_email(cr, uid, message_user, mail_server_id=mail_server_ids[0], context=context)
        return True
    
    def _get_monthly_production(self, cr, uid, ids, name, args, context=None):
        res = {}
        jan_production = 0.0
        feb_production = 0.0
        mar_production = 0.0
        apr_production = 0.0
        may_production = 0.0
        jun_production = 0.0
        jul_production = 0.0
        aug_production = 0.0
        sep_production = 0.0
        oct_production = 0.0
        nov_production = 0.0
        dec_production = 0.0
        line_no = 0
        
        for data in self.browse(cr, uid, ids, context):
            
            res[data.id] = {
                'jan_production': 0.0,
                'feb_production': 0.0,
                'mar_production': 0.0,
                'apr_production': 0.0,
                'may_production': 0.0,
                'jun_production': 0.0,
                'jul_production': 0.0,
                'aug_production': 0.0,
                'sep_production': 0.0,
                'oct_production': 0.0,
                'nov_production': 0.0,
                'dec_production': 0.0,
            }
            if data.solar_ids:
                for line in data.solar_ids:
                    jan_production += line.jan_production
                    feb_production += line.feb_production
                    mar_production += line.mar_production
                    apr_production += line.apr_production
                    may_production += line.may_production
                    jun_production += line.jun_production
                    jul_production += line.jul_production
                    aug_production += line.aug_production
                    sep_production += line.sep_production
                    oct_production += line.oct_production
                    nov_production += line.nov_production
                    dec_production += line.dec_production
                    line_no += 1
            else:
                line_no = 1
                
            if line_no:
                res[data.id]['jan_production'] = jan_production/line_no
                res[data.id]['feb_production'] = feb_production/line_no
                res[data.id]['mar_production'] = mar_production/line_no
                res[data.id]['apr_production'] = apr_production/line_no
                res[data.id]['may_production'] = may_production/line_no
                res[data.id]['jun_production'] = jun_production/line_no
                res[data.id]['jul_production'] = jul_production/line_no
                res[data.id]['aug_production'] = aug_production/line_no
                res[data.id]['sep_production'] = sep_production/line_no
                res[data.id]['oct_production'] = oct_production/line_no
                res[data.id]['nov_production'] = nov_production/line_no
                res[data.id]['dec_production'] = dec_production/line_no
                        
        return res
        
    _columns = {
         'last_name': fields.char('Last Name', size=32),
         'middle_name':fields.char("Middle Name", size=32),
         'lead_date': fields.date('Date', required=True),
         'lead_days': fields.integer('Lead Days'),
         'property': fields.selection([('commercial', 'Commercial'), ('residential', 'Residential'), ('non_profit', 'None Profit')], 'Property', help="Which type of Property?"),
         'insentive_type' : fields.selection([('epbb','EPBB'),('pbi','PBI')],'Insentive Type'),
         'sci_step' : fields.selection([
                        (1,'Step 1'),
                        (2,'Step 2'),
                        (3,'Step 3'),
                        (4,'Step 4'),
                        (5,'Step 5'),
                        (6,'Step 6'),
                        (7,'Step 7'),
                        (8,'Step 8'),
                        (9,'Step 9'),
                        (10,'Step 10')
                    ],'Current SCI Step'),
         'spouse': fields.many2one('res.partner', string='Secondary Customer', help="Secondary Customer (spouse) in case he/she exist."),
         'utility_company_id': fields.many2one('res.partner', 'Utility Company', domain=[('is_utility_company','=',True)]),
         'doc_req_ids' : fields.one2many('document.required', 'crm_lead_id', 'Required Documents'),
         'required_document':fields.function(_get_require_doc, method=True, type='boolean', string="Required Document Collected?", help="Checked if Yes."),
         'acc_no':fields.char('Account Number', size=32),
         'meter_no': fields.char('Meter Number', size=32),
         'bill_average': fields.float(' Electric Bill Amount Average'),
         'bill_month': fields.char('Months for Bill Average', size=128,),
         'bill_month1': fields.char('Months for Bill Total', size=128,),
         'bill_total': fields.float('Electric Bills Total Amount', help="Electric Bills Total 12-24-months depending on utility company"),
         'rate_plan': fields.char('Rate Plan', size=32),
         'bill_summer': fields.float('Summer Monthly Bill Amount', help="Monthly electrical bill cost in Summer"),
         'bill_winter': fields.float('Winter Monthly Bill Amount', help="Monthly electrical bill cost in Winter"),
         'home_note': fields.text('Note'),
         'electricity_note': fields.text('Note'),
         'marketing_note': fields.text('Note'),
         'accounting_note': fields.text('Note'),
         'home': fields.selection([ ('own', 'Own Home'),
                                    ('rent', 'Renting')],
                                    string='Home'),
         'quote': fields.boolean('Had a Solar Quote?', help='Checked if customer have Solar Quotation of any other Company.'),
         'quote_info': fields.many2one('company.quotation', 'Quotation Information'),
         'heat_home': fields.selection([('natural_gas', 'Natural Gas'), ('propane', 'Propane'), ('all_electric', 'All Electric')], 'Heat Home Technique'),
         'home_sq_foot': fields.float('Home Sq-Footage'),
         'age_house_year': fields.integer('Age of House'),
         'age_house_month': fields.integer('Age of House month'),
         'roof_type': fields.many2one('roof.type', 'Type Of Roof'),
         'time_own_year': fields.integer('Owned Home Time', help="How long have you owned your home?"),
         'partner_is_company' : fields.boolean('Partner is Company'),
         'time_own_month': fields.integer('Owned home Time month'),
         'spent_money': fields.float('Money spent to Heat Home', help='How much spent to heat home?'),
         'equity': fields.boolean('Equity', help="Do you have equity in your home? Checked if Yes."),
         'loc_station_id' : fields.many2one('insolation.incident.yearly', 'Closest NERL Locations'),
         'tilt_degree' : fields.selection(
                    [
                        ('n', '[N]North'),
                        ('ne', '[NE]North-East'),
                        ('e', '[E]East'),
                        ('se', '[SE]South-East'),
                        ('s', '[S]South'),
                        ('sw', '[SW]South-West'),
                        ('w', '[W]West'),
                        ('nw', '[NW]North-West')
                    ], 'Facing / Azimuth'),
        'faceing' : fields.many2one('tilt.tilt', 'Degree Tilt'),
        'estimate_shade': fields.integer('Estimated Shading'),
        'utility_bill' : fields.boolean('Utility Bill', help="Checked Utility bill to sign customer contract."),
        'lead_source': fields.many2one('crm.case.channel','Lead Source'),
        'level_of_lead': fields.many2one('level.lead', 'Level Of Lead'),
        'qualified': fields.boolean('Qualification Data?'),
        'annual_income': fields.float('Annual Income'),
        'tax_liability': fields.float('Tax Liability'),
        'credit_source': fields.float('Credit Score'),
        'property_tax': fields.float('Property Tax'),
        'appointment_ids': fields.one2many('crm.meeting', 'crm_id', 'Appointments'),
        'type_of_sale_id': fields.many2one('type.of.sale', 'Type Of Sale'),
        'deadline': fields.function(_get_deadline, method=True, type='date', string="Deadline",),
        'deposit': fields.float('Deposit'),
        'federal_tax': fields.selection([('yes', 'Yes'), ('no', 'No')], 'Federal Tax Advantage?'),
        'property_tax': fields.selection([('yes', 'Yes'), ('no', 'No')], 'Property Tax Paid?', help="Have your property tax paid on time for the last 3 years?"),
        'mortgage': fields.selection([('yes', 'Yes'), ('no', 'No')], 'Mortgage been paid?', help="Has your mortgage been paid on time for the last 12 months?"),
        'bankruptcy': fields.selection([('yes', 'Yes'), ('no', 'No')], 'Filed for a bankruptcy?', help="Have you filed for a bankruptcy in the past 7 years?"),
        'rate_credit': fields.selection([('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')], 'Rate Credit', help="How would you rate your credit?"),
        'attachment_ids': fields.many2many('ir.attachment', 'email_template_attachment_sps_rel', 'mail_template_id', 'attach_id', 'Attachments'),
        'see_lead_home_note': fields.boolean('See Lead Home Note'),
        'crm_lead_home_note_ids': fields.one2many('crm.lead.home.description', 'home_id', 'Notes'),
        'anual_electricity_usage_ids' : fields.one2many('electricity.usage', 'lead_id', 'Anual Electricity Usage'),
        'see_lead_electricity_note': fields.boolean('See Lead Electricity Note'),
        'crm_lead_electricity_note_ids': fields.one2many('crm.lead.electricity.description', 'electricity_id', 'Notes'),
        'see_lead_marketing_note': fields.boolean('See Lead Marketing Note'),
        'crm_lead_marketing_note_ids': fields.one2many('crm.lead.marketing.description', 'marketing_id', 'Notes'),
        'see_lead_accounting_note': fields.boolean('See Lead Accounting Note'),
        'crm_lead_accounting_note_ids': fields.one2many('crm.lead.accounting.description', 'accounting_id', 'Notes'),
        'see_lead_system_note': fields.boolean('See Lead System Note'),
        'crm_lead_system_note_ids': fields.one2many('crm.lead.system.description', 'system_id', 'Notes'),
        'see_lead_all_note': fields.boolean('See Lead All Note'),
        'crm_lead_all_tabs_note_ids': fields.one2many('crm.lead.all.tabs.description', 'all_tab_id', 'Notes'),
        'responsible_user': fields.function(_reponsible_user, type='char', method=True, string="Responsible User for Appointment", help="Responsible User for Appointment setup"),
        'solar_ids' : fields.one2many("solar.solar", "crm_lead_id", "Solar Information"),
        'loan_period' :fields.float("Loan Period(Years)"),
        'down_payment' :fields.float("Down Payment (%)"),
        'loan_interest_rate' :fields.float("Loan Interest Rate (%)"),
        'cost_peack_kw' : fields.function(_get_cost_rebate, string="Cost / Peack KW",type="float",multi="cost_all"),
        'pv_kw_decline':fields.float('PV KW Decline (%)'),
        'grid_energy_rate':fields.function(_get_company_tier_amount, type='float', method=True, string="Electricity Grid energy intial Rate Per KWh/$"),
        'grid_rate_increase_by':fields.float('Grid Rate Increase By'),
        'rebate':fields.float("Rebate"),
        'srec':fields.float('SREC/kwh'),
        'number_of_years':fields.integer('Number Of Years'),
        'replace_inverter_every':fields.float('Replace Inverter Every(Years)'),
        'replace_inverter_over_loan_period' : fields.integer("Replace Inverter Over Loan Period"),
        'inverter_cost' : fields.function(_get_cost_rebate, string="Inverter Cost",type="float",multi="cost_all"),
        'array_output' : fields.function(_get_output, string='Solar Array Output', type='float'),
        'peak_kw_stc' : fields.function(_get_stc_dc_rating, string='Yearly output per KW', type='float'),
        'sun_hour_per_day' : fields.function(_get_site_avg_sun_hour, string='Sun Hours Per Day', type='float',digits=(12,3)),
        'pbi_epbb_incentive' : fields.function(_get_pbi_epbb_incentive, string="PBI-EPBBB Incentive", type="float"),
        'cost' : fields.function(_get_cost_rebate, string="Cost",type="float",multi="cost_all"),
        'down_payment_amt' : fields.function(_get_cost_rebate, string="Down Payment (Amount)",store=True,type="float",multi="cost_all"),
        'loan_amt' : fields.function(_get_cost_rebate, string='Loan Amount',type="float",multi="cost_all"),
        'rebate_amt' : fields.function(_get_cost_rebate, string="Rebate Amount",type="float",store=True,multi="cost_all"),
        'cost_rebate_ids' : fields.one2many( 'cost.rebate','crm_lead_id',string = 'Cost & Rebate'),
        'auto_zip' : fields.char(string="Auto-Zipcode"),
        'co2_offset_tons' : fields.function(_get_co2_offset_tons, string='CO2 Offset (Tons)', type='integer', help="Tons of Carbon Annually"),
        'co2_offset_pounds' : fields.function(_get_co2_offset_pounds, string='CO2 Offset (Pounds)', type="integer", help="Pounds of Carbon annually Eliminated"),
        'cars_off_roads' : fields.function(_get_cars_off_roads, string='Cars off the Road', type="integer", help="Cars taken off the road for one year"),
        'gasoline_equi' : fields.function(_get_gasoline_equi, string='Gasoline Equivalent (Gallons of Gas)', type='integer'),
        'tree_equi' : fields.function(_get_tree_equi, string='Tree Equivalent', type='integer', help="Trees cleaning the Air for one year"),
        'tree_planting_equi' : fields.function(_get_tree_planting_equi, string='Tree Planting Equivalent', type='integer', help="Trees planted for life of tree"),
        'ave_home_powered' : fields.function(_get_ave_home_powered, string='Average Homes Powered', type='integer', help="Homes Powered for One Year"),
        'ave_light_bulb_powered' : fields.function(_get_ave_light_bulb_powered, string='Average Light-bulbs Powered', type='integer', help="Light-bulbs Powered for One Year"),
        'stc_dc_rating': fields.function(_get_stc_dc_rating, string='STC-DC Rating', type='float',digits=(12,3)),
        'ptc_dc_rating': fields.function(_get_ptc_dc_rating, string='PTC-DC Rating', type='float',digits=(12,3)),
        'cec_ac_rating': fields.function(_get_cec_ac_rating, string='CEC-AC Rating', type='float',digits=(12,3)),
        'ptc_stc_ratio': fields.function(_get_ptc_stc_ratio, string='PTC STC Ratio', type='float',digits=(12,3)),
        'annual_solar_prod_display': fields.function(_get_annual_solar_prod_display, string='Annual Solar Production (KWh)', type='integer', digits=(12,3)),
        'annual_solar_prod': fields.function(_get_annual_solar_prod, string='Annual Solar Production (KWh)', type='float', digits=(12,3)),
        'annual_ele_usage': fields.function(_get_annual_ele_usage, string='Annual Electricity Usage (KWh)', type='float', digits=(12,3)),
        'site_avg_sun_hour': fields.function(_get_site_avg_sun_hour, string='Site Average Sun Hours', type='float'),
        'project_photo_ids' : fields.one2many('project.photos', 'crm_lead_id', "Project Photos"),
        'project_review_ids' : fields.one2many('project.reviews', 'crm_lead_id', "Project Reviews"),
        'friend_refer_ids' : fields.one2many('friend.reference', 'crm_lead_id', "Friend References"),
        'submit_que_ids' : fields.one2many('submit.question', 'crm_lead_id', "Submit Question"),
        'reg_no' : fields.char('Registration Number.'),
        'intial_photo': fields.binary('Initial Photo'),
        'final_photo':fields.binary('Final Photo'),
        
        'jan_production': fields.function(_get_monthly_production, method=True, type='float', multi='monthly_production', string="January Production", store=True),
        'feb_production': fields.function(_get_monthly_production, method=True, type='float', multi='monthly_production', string="February Production", store=True),
        'mar_production': fields.function(_get_monthly_production, method=True, type='float', multi='monthly_production', string="March Production", store=True),
        'apr_production': fields.function(_get_monthly_production, method=True, type='float', multi='monthly_production', string="April Production", store=True),
        'may_production': fields.function(_get_monthly_production, method=True, type='float', multi='monthly_production', string="May Production", store=True),
        'jun_production': fields.function(_get_monthly_production, method=True, type='float', multi='monthly_production', string="June Production", store=True),
        'jul_production': fields.function(_get_monthly_production, method=True, type='float', multi='monthly_production', string="July Production", store=True),
        'aug_production': fields.function(_get_monthly_production, method=True, type='float', multi='monthly_production', string="Aug Production", store=True),
        'sep_production': fields.function(_get_monthly_production, method=True, type='float', multi='monthly_production', string="Sep Production", store=True),
        'oct_production': fields.function(_get_monthly_production, method=True, type='float', multi='monthly_production', string="October Production", store=True),
        'nov_production': fields.function(_get_monthly_production, method=True, type='float', multi='monthly_production', string="November Production", store=True),
        'dec_production': fields.function(_get_monthly_production, method=True, type='float', multi='monthly_production', string="December Production", store=True),
        }

    _defaults = {
            'name': '/',
            'home':'own',
            'property': 'residential',
            'number_of_years':25,
            'lead_date': fields.date.context_today,
            'reg_no': lambda obj, cr, uid, context:obj.pool.get('ir.sequence').get(cr, uid, 'crm.lead'),
    }
    
    
    def calculate_table(self, cr, uid, ids, context=None):
        result = {}
        cost_rebate_obj = self.pool.get('cost.rebate')
        user_obj = self.pool.get('res.users')
        pricelist_obj = self.pool.get('product.pricelist')
        product_obj = self.pool.get('product.product')
        cur_user = user_obj.browse(cr, uid, uid, context=context)
        elec_bill_savings = 0
        prev_old_bill = 0
        depriciation_savings = 0
        prev_new_bill = 0
        
        old_rec_len = len(self.browse(cr, uid, ids[0],context=context).cost_rebate_ids)
        if old_rec_len:
            cost_rebate_ids = cost_rebate_obj.search(cr, uid, [('crm_lead_id','=',ids[0])],context=context)
            cost_rebate_obj.unlink(cr, uid, cost_rebate_ids)
        
        for data in self.browse(cr, uid, ids, context=context):
            if not data.utility_company_id:
                raise osv.except_osv(_('Warning'), _('You must select Utility Company for count Cost and Rebate!'))
            annual_ele_usage = 0.0
            for line in data.anual_electricity_usage_ids:
                if line.name == datetime.datetime.now().year:
                    if line.usage_kwh:
                        annual_ele_usage = line.usage_kwh
            res = []
            prev_old_bill = self._get_old_bill(cr, uid, ids, context=context)
            prev_new_bill = self._get_new_bill(cr, uid, ids, context=context)
            prev_pv_energy = data.annual_solar_prod or 0
            context.update({'get_field':'tier1'})
            grid_energy_rate = 0
            product_ids = product_obj.search(cr, uid, [], context=context)
            pro_id = product_ids and product_ids[0]
            if data.utility_company_id:
                grid_energy_rate = pricelist_obj.price_get(cr, uid, [data.utility_company_id.property_product_pricelist.id], pro_id, data.annual_ele_usage, context=context)[data.utility_company_id.property_product_pricelist.id]
#            elec_bill_savings = prev_pv_energy * grid_energy_rate
            elec_bill_savings = self._get_new_bill(cr, uid, ids, context=context)
            i = data.loan_interest_rate
            n = data.loan_period
            PV = data.loan_amt
            loan_installment = 0
            if i != 0:
                loan_installment = PV / ((1- (1 / pow((1 + i),n) )) / i) 
            
            if data.loan_period != 0.0:
                depriciation = data.cost/data.loan_period
            else:
                depriciation = data.cost
            depriciation_savings = depriciation * ((cur_user.company_id.fedral_tax + cur_user.company_id.sales_tax)/100)
            
            if not data.annual_ele_usage:
                annual_ele_usage_temp = 1
            else:
                annual_ele_usage_temp = data.annual_ele_usage
            for yr in range(data.number_of_years):
                year = yr + 1
                if year >= 15:
                    yearly_payout = data.down_payment_amt + 7428 + (prev_old_bill - elec_bill_savings) - (prev_pv_energy * data.srec) - (prev_pv_energy * data.pbi_epbb_incentive) - depriciation_savings
                else:
                    yearly_payout = data.down_payment_amt + 7428 + (prev_old_bill - elec_bill_savings) - (prev_pv_energy * data.srec) - (prev_pv_energy * data.pbi_epbb_incentive) - depriciation_savings + 5000
                
                vals = {
                    'year':year,
                    'old_bill':prev_old_bill,
                    'pv_energy' : prev_pv_energy * 1000,
                    'elec_bill_savings' : prev_new_bill, #(prev_old_bill - ((prev_pv_energy * 1000 * prev_old_bill) / annual_ele_usage_temp)),
#                    'new_bill' : ((prev_pv_energy * 1000 * prev_old_bill) / annual_ele_usage_temp),
                    'new_bill' : prev_old_bill - prev_new_bill,
                    'srecs' : prev_pv_energy * data.srec,
                    'incentives' : prev_pv_energy * data.pbi_epbb_incentive,
                    'depriciation' : 0,
                    'depriciation_savings' : 0,
                    'yearly_payout' : yearly_payout,
                    'loan_installment' : 0,
                    'crm_lead_id': data.id
                }
                if year <= data.loan_period:
                    vals.update({'depriciation' : depriciation, 'depriciation_savings' : depriciation_savings, 'loan_installment':loan_installment})
                res.append(cost_rebate_obj.create(cr, uid, vals,context=context))
                prev_old_bill = prev_old_bill * ( 1 + data.grid_rate_increase_by)
                prev_pv_energy = prev_pv_energy * (( 100 - data.pv_kw_decline)/100)
                prev_new_bill = prev_new_bill - (prev_new_bill*data.pv_kw_decline)
                elec_bill_savings = prev_pv_energy * grid_energy_rate * math.pow(( 1 + data.grid_rate_increase_by ),year)  
            result[data.id] = res#
        return True
    
    def on_change_notifiy_customer(self, cr, uid, ids, notify_customer, context=None):
        if notify_customer == True:
            for data in self.browse(cr, uid, ids, context=context):
                for doc in data.document_ids:
                    if doc.doc == False:
                        return False
                    else:
                        obj_mail_server = self.pool.get('ir.mail_server')
                        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
                        if not mail_server_ids:
                            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
                        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
                        email_from = mail_server_record.smtp_user
                        if not email_from:
                            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
                        if not data.email_from:
                            raise osv.except_osv(_('Warning'), _('%s User have no email defined !' % data.contact_name))
                        else:
                            subject_line = 'Notification For uploded Document.'
                            message_body = 'Hello,' + tools.ustr(data.contact_name) + ' ' + tools.ustr(data.last_name) + '<br/><br/>The Documents: <br/>' + tools.ustr(doc.name) + '<br/>is successfully Uploded.<br/><br/> Thank You.'
                            message_user = obj_mail_server.build_email(
                                email_from=email_from,
                                email_to=[data.email_from],
                                subject=subject_line,
                                body=message_body,
                                body_alternative=message_body,
                                email_cc=None,
                                email_bcc=None,
                                attachments=None,
                                references=None,
                                object_id=None,
                                subtype='html',
                                subtype_alternative=None,
                                headers=None)
                            self.send_email(cr, uid, message_user, mail_server_id=mail_server_ids[0], context=context)
        return True
    
    def on_change_notifiy_user(self, cr, uid, ids, notify_user, context=None):
        if notify_user == True:
            for data in self.browse(cr, uid, ids, context=context):
                for doc in data.document_ids:
                    if doc.doc == False:
                        return False
                    else:
                        obj_mail_server = self.pool.get('ir.mail_server')
                        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
                        if not mail_server_ids:
                            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
                        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
                        email_from = mail_server_record.smtp_user
                        if not email_from:
                            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
                        email_to = []
                        for user in data.user_notification_id:
                            if not user.email:
                                raise osv.except_osv(_('Warning'), _('%s User have no email defined !' % user.name))
                            else:
                                email_to.append(user.email)
                                subject_line = 'Notification For uploded Document.'
                                message_body = 'Hello,' + tools.ustr(user.name) + '<br/><br/>The Document <br/>' + tools.ustr(doc.name) + '<br/>is successfully Uploded.<br/><br/> Thank You.'
                                message_user = obj_mail_server.build_email(
                                    email_from=email_from,
                                    email_to=email_to,
                                    subject=subject_line,
                                    body=message_body,
                                    body_alternative=message_body,
                                    email_cc=None,
                                    email_bcc=None,
                                    attachments=None,
                                    references=None,
                                    object_id=None,
                                    subtype='html',
                                    subtype_alternative=None,
                                    headers=None)
                                self.send_email(cr, uid, message_user, mail_server_id=mail_server_ids[0], context=context)
        return True

    def on_change_utility_company(self, cr, uid, ids, utility_company_id, context=None):
        values = {}
        document_list = []
        if utility_company_id:
            utility_company = self.pool.get('res.partner').browse(cr, uid, utility_company_id, context=context)
            for document in utility_company.document_ids:
                    document_list.append({'doc_id':document.id})
            values = {'doc_req_ids' : document_list or False}
        return {'value' : values}
    
    def redirect_lead_view(self, cr, uid, lead_id, context=None):
        models_data = self.pool.get('ir.model.data')

        # Get opportunity views
        dummy, form_view = models_data.get_object_reference(cr, uid, 'crm', 'crm_case_form_view_leads')
        dummy, tree_view = models_data.get_object_reference(cr, uid, 'crm', 'crm_case_tree_view_leads')
        return {
            'name': _('Lead'),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'crm.lead',
            'domain': [('type', '=', 'lead')],
            'res_id': int(lead_id),
            'view_id': False,
            'views': [(form_view or False, 'form'),
                      (tree_view or False, 'tree'),
                      (False, 'calendar'), (False, 'graph')],
            'type': 'ir.actions.act_window',
        }
        
    def _convert_opportunity_data(self, cr, uid, lead, customer, section_id=False, context=None):
        res = super(crm_lead, self)._convert_opportunity_data(cr, uid, lead, customer, section_id=section_id, context=context)
        res.update({ 'street' : lead.street, 'street2' : lead.street2, 'city' : lead.city_id.id})
        return res
        
    def openMap(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        cur_rec = self.browse(cr, uid, ids, context=context)[0]
        url = "http://maps.google.com/maps?oi=map&q="
        if cur_rec.street:
            url += cur_rec.street.replace(' ', '+')
        if cur_rec.street2:
            url += '+' + cur_rec.street2.replace(' ', '+')
        if cur_rec.city_id:
            url += '+' + cur_rec.city_id.name.replace(' ', '+')
        if cur_rec.city_id.state_id:
            url += '+' + cur_rec.city_id.state_id.name.replace(' ', '+')
        if cur_rec.city_id.country_id:
            url += '+' + cur_rec.city_id.country_id.name.replace(' ', '+')
        if cur_rec.city_id.zip:
            url += '+' + cur_rec.city_id.zip.replace(' ', '+')
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new'
        }
    
    def type_change(self, cr, uid, ids, context=None):
        """
        Convert opportunity to lead.
        """
        if context is None:
            context = {}
        context.update({
            'active_model': 'crm.lead',
            'active_ids': ids,
             
        })
        opportunity = self.pool.get('crm.lead')
        opportunity_ids = context.get('active_ids', [])
        self.write(cr, uid, opportunity_ids, {"type":"lead"})
        return opportunity.redirect_lead_view(cr, uid, opportunity_ids[0], context=context)
        
    def send_email(self, cr, uid, message, mail_server_id, context):
        '''
           This method sends mail using information given in message 
        '''
        obj_mail_server = self.pool.get('ir.mail_server')
        obj_mail_server.send_email(cr, uid, message=message, mail_server_id=mail_server_id, context=context)
    
    def create(self, cr, uid, vals, context=None):
        if not context:
            context = {}
        type_context = context.get('default_type')
        if type_context == 'opportunity':
            crm_case_stage_obj = self.pool.get('crm.case.stage')
            stage_id = crm_case_stage_obj.search(cr, uid, [('name', '=', 'Initial Contact')])
            vals.update({'stage_id': stage_id[0]})
            return super(crm_lead, self).create(cr, uid, vals, context=context)
        res = super(crm_lead, self).create(cr, uid, vals, context=context)
        if res and vals and vals.get('home_note'):
            self.pool.get('crm.lead.home.description').create(cr, uid, {
                                                                'home_id': res,
                                                                'home_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['home_note']
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'all_tab_id': res,
                                                                'all_tab_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['home_note']
                                                            })
        if res and vals and vals.get('electricity_note'):
            self.pool.get('crm.lead.electricity.description').create(cr, uid, {
                                                                'electricity_id': res,
                                                                'electricity_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['electricity_note']
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'all_tab_id': res,
                                                                'all_tab_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['electricity_note']
                                                            })
        if res and vals and vals.get('marketing_note'):
            self.pool.get('crm.lead.marketing.description').create(cr, uid, {
                                                                'marketing_id': res,
                                                                'marketing_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['marketing_note']
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'all_tab_id': res,
                                                                'all_tab_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['marketing_note']
                                                            })
        if res and vals and vals.get('accounting_note'):
            self.pool.get('crm.lead.accounting.description').create(cr, uid, {
                                                                'accounting_id': res,
                                                                'accounting_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['accounting_note']
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'all_tab_id': res,
                                                                'all_tab_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['accounting_note']
                                                            })
        if res and vals and vals.get('system_note'):
            self.pool.get('crm.lead.system.description').create(cr, uid, {
                                                                'system_id': res,
                                                                'system_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['system_note']
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'all_tab_id': res,
                                                                'all_tab_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['system_note']
                                                            })
        return res

    def write(self, cr, uid, ids, vals, context=None):
        if vals and vals.get('home_note'):
            self.pool.get('crm.lead.home.description').create(cr, uid, {
                                                                'home_id': ids[0],
                                                                'home_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('home_note')
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'all_tab_id': ids[0],
                                                                'all_tab_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('home_note')
                                                            })
        if vals and vals.get('electricity_note'):
            self.pool.get('crm.lead.electricity.description').create(cr, uid, {
                                                                'electricity_id': ids[0],
                                                                'electricity_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('electricity_note')
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'all_tab_id': ids[0],
                                                                'all_tab_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('electricity_note')
                                                            })
        if vals and vals.get('marketing_note'):
            self.pool.get('crm.lead.marketing.description').create(cr, uid, {
                                                                'marketing_id': ids[0],
                                                                'marketing_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('marketing_note')
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'all_tab_id': ids[0],
                                                                'all_tab_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('marketing_note')
                                                            })
        if vals and vals.get('accounting_note'):
            self.pool.get('crm.lead.accounting.description').create(cr, uid, {
                                                                'accounting_id': ids[0],
                                                                'accounting_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('accounting_note')
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'all_tab_id': ids[0],
                                                                'all_tab_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('accounting_note')
                                                            })
        if vals and vals.get('system_note'):
            self.pool.get('crm.lead.system.description').create(cr, uid, {
                                                                'system_id': ids[0],
                                                                'system_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('system_note')
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'all_tab_id': ids[0],
                                                                'all_tab_user_id': uid,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('system_note')
                                                            })
        return super(crm_lead, self).write(cr, uid, ids, vals, context=context)

    def view_lead_home_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': True, 'see_lead_electricity_note': False, 'see_lead_marketing_note': False, 'see_lead_accounting_note': False, 'see_lead_system_note': False, 'see_lead_all_note': False})
        return True

    def view_lead_electricity_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': False, 'see_lead_electricity_note': True, 'see_lead_marketing_note': False, 'see_lead_accounting_note': False, 'see_lead_system_note': False, 'see_lead_all_note': False})
        return True

    def view_lead_marketing_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': False, 'see_lead_electricity_note': False, 'see_lead_marketing_note': True, 'see_lead_accounting_note': False, 'see_lead_system_note': False, 'see_lead_all_note': False})
        return True
    
    def view_lead_accounting_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': False, 'see_lead_electricity_note': False, 'see_lead_marketing_note': False, 'see_lead_accounting_note': True, 'see_lead_system_note': False, 'see_lead_all_note': False})
        return True
    
    def view_lead_system_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': False, 'see_lead_electricity_note': False, 'see_lead_marketing_note': False, 'see_lead_accounting_note': False, 'see_lead_system_note': True, 'see_lead_all_note': False})
        return True

    def view_lead_all_tab_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': False, 'see_lead_electricity_note': False, 'see_lead_marketing_note': False, 'see_lead_accounting_note': False, 'see_lead_system_note': False, 'see_lead_all_note': True})
        return True

    def exit_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': False, 'see_lead_electricity_note': False, 'see_lead_marketing_note': False, 'see_lead_accounting_note': False, 'see_lead_system_note': False, 'see_lead_all_note': False})
        return True

class solar_solar(osv.Model):
    """Model for Solar Information"""
    
    _name = 'solar.solar'

    def _get_system_rating_data(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            res[data.id] = {
                'stc_dc_rating': 0.0,
                'ptc_dc_rating': 0.0,
                'cec_ac_rating': 0.0,
                'ptc_stc_ratio': 0.0,
                'co2_offset_tons' : 0,
                'co2_offset_pounds' : 0,
                'cars_off_roads' : 0,
                'gasoline_equi' : 0,
                'tree_equi' : 0,
                'tree_planting_equi' : 0,
                'ave_home_powered' : 0,
                'ave_light_bulb_powered' : 0,
                'annual_solar_prod_display':0,
                'annual_solar_prod' : 0,
                'annual_ele_usage' : 0,
                'site_avg_sun_hour' : 0,
                'array_size' : 0,
                'array_output' : 0,
            }
            stc_dc_rating_amount = ptc_dc_rating_amount = cec_ac_rating_amount = ptc_stc_ratio_amount = 0.00
            if data.module_product_id.pv_module_power_stc:
                stc_dc_rating_amount = data.num_of_module * (data.module_product_id.pv_module_power_stc / 1000)
            if data.module_product_id.module_ptc_rating:
                ptc_dc_rating_amount = data.num_of_module * (data.module_product_id.module_ptc_rating / 1000)
                cec_ac_rating_amount = (ptc_dc_rating_amount * data.inverter_product_id.cec_efficiency) / 100
            if stc_dc_rating_amount and ptc_dc_rating_amount:
                ptc_stc_ratio_amount = (ptc_dc_rating_amount / stc_dc_rating_amount)
            res[data.id]['stc_dc_rating'] = stc_dc_rating_amount or 0.0
            res[data.id]['ptc_dc_rating'] = ptc_dc_rating_amount or 0.0
            res[data.id]['cec_ac_rating'] = cec_ac_rating_amount or 0.0
            res[data.id]['ptc_stc_ratio'] = ptc_stc_ratio_amount or 0.0
            if data and data.crm_lead_id and data.crm_lead_id.anual_electricity_usage_ids:
                for line in data.crm_lead_id.anual_electricity_usage_ids:
                    if line and line.usage_kwh:
                        res[data.id]['annual_ele_usage'] = line.usage_kwh
                    else:
                        res[data.id]['annual_ele_usage'] = 0.0
            production = None
            avg_sun_hour = 0
            
            if data and data.loc_station_id:
                if data.loc_station_id and data.loc_station_id.tilt_azimuth_ids:
                    for t_a_data in data.loc_station_id.tilt_azimuth_ids:
                        if t_a_data.azimuth == data.tilt_degree and t_a_data.tilt.id == data.faceing.id:
                            production = t_a_data.production
                            avg_sun_hour = t_a_data.annual_avg
                        if avg_sun_hour:
                            res[data.id]['site_avg_sun_hour'] = avg_sun_hour
                            annual_solar_prod = None
                            if ptc_stc_ratio_amount:
                                tot_perfomance_ratio = (data.inverter_product_id.cec_efficiency / 100) * 0.84 * (ptc_stc_ratio_amount / 100)
                                if data.estimate_shade == 0:
                                    data.estimate_shade = 100
                                annual_solar_prod = (stc_dc_rating_amount * production  * (data.estimate_shade/100)) / 1000
                                annual_solar_prod_display = annual_solar_prod * 1000
#                                annual_solar_prod = ptc_dc_rating_amount * avg_sun_hour * 365 * tot_perfomance_ratio
                            if annual_solar_prod:
                                annual_s_prod = annual_solar_prod
                                res[data.id]['annual_solar_prod'] = annual_s_prod
                                res[data.id]['annual_solar_prod_display'] = annual_solar_prod_display
                    if production:
                        user_obj = self.pool.get('res.users')
                        cur_user = user_obj.browse(cr, uid, uid, context=context)
                        avg_co2_ele = cur_user.company_id.avg_co2_ele
                        annnual_co2_car = cur_user.company_id.annnual_co2_car
                        emmision_gas = cur_user.company_id.emmision_gas
                        annual_equvi_tree = cur_user.company_id.annual_equvi_tree
                        years_40_offset_tree = cur_user.company_id.years_40_offset_tree
                        annual_home_ele = cur_user.company_id.annual_home_ele
                        avg_light_bulb = cur_user.company_id.avg_light_bulb
                        if data and data.crm_lead_id and data.crm_lead_id.solar_ids:
                            num_of_arrays = len(data.crm_lead_id.solar_ids)
                        else:
                            num_of_arrays = data.num_of_arrays
                        res[data.id]['array_size'] = num_of_arrays
                        res[data.id]['array_output'] = production
                        output = production * stc_dc_rating_amount
                        res[data.id]['array_output'] = output
                        co2_offset_tons = output * avg_co2_ele / 2000
                        res[data.id]['co2_offset_tons'] = co2_offset_tons
                        co2_offset_pounds = co2_offset_tons * 2000
                        res[data.id]['co2_offset_pounds'] = co2_offset_pounds
                        cars_off_roads = co2_offset_pounds / annnual_co2_car
                        res[data.id]['cars_off_roads'] = cars_off_roads
                        gasoline_equi = co2_offset_pounds / emmision_gas
                        res[data.id]['gasoline_equi'] = gasoline_equi
                        tree_equi = output / annual_equvi_tree
                        res[data.id]['tree_equi'] = tree_equi
                        tree_planting_equi = output / years_40_offset_tree
                        res[data.id]['tree_planting_equi'] = tree_planting_equi
                        ave_home_powered = output / 8900
                        res[data.id]['ave_home_powered'] = ave_home_powered
                        ave_light_bulb_powered = output / avg_light_bulb
                        res[data.id]['ave_light_bulb_powered'] = ave_light_bulb_powered
                        
        return res
    
    def _get_monthly_production_solar(self, cr, uid, ids, name, args, context=None):
        res = {}
        tilt_azimuth_obj = self.pool.get('tilt.azimuth')
        for data in self.browse(cr, uid, ids, context):
            sum = 0.0
            res[data.id] = {
                'jan_production': 0.0,
                'feb_production': 0.0,
                'mar_production': 0.0,
                'apr_production': 0.0,
                'may_production': 0.0,
                'jun_production': 0.0,
                'jul_production': 0.0,
                'aug_production': 0.0,
                'sep_production': 0.0,
                'oct_production': 0.0,
                'nov_production': 0.0,
                'dec_production': 0.0,
            }
            
            jan_production = 0.0
            feb_production = 0.0
            mar_production = 0.0
            apr_production = 0.0
            may_production = 0.0
            jun_production = 0.0
            jul_production = 0.0
            aug_production = 0.0
            sep_production = 0.0
            oct_production = 0.0
            nov_production = 0.0
            dec_production = 0.0
                
            if data and data.loc_station_id:
                tilt_azimuth_id = tilt_azimuth_obj.search(cr, uid, [('tilt_azimuth_id','=',data.loc_station_id.id),('tilt','=', data.faceing.id),('azimuth','=',data.tilt_degree)],context=context)
                if tilt_azimuth_id:
                    tilt_azimuth_data = tilt_azimuth_obj.browse(cr, uid, tilt_azimuth_id, context=context)[0]
                    sum = tilt_azimuth_data.jan + tilt_azimuth_data.feb + tilt_azimuth_data.mar + tilt_azimuth_data.apr + tilt_azimuth_data.may + tilt_azimuth_data.jun + tilt_azimuth_data.jul + tilt_azimuth_data.aug + tilt_azimuth_data.sep + tilt_azimuth_data.oct + tilt_azimuth_data.nov + tilt_azimuth_data.dec
                    jan_production = (tilt_azimuth_data.jan * data.annual_solar_prod * 1000)/sum
                    feb_production = (tilt_azimuth_data.feb * data.annual_solar_prod * 1000)/sum
                    mar_production = (tilt_azimuth_data.mar * data.annual_solar_prod * 1000)/sum
                    apr_production = (tilt_azimuth_data.apr * data.annual_solar_prod * 1000)/sum
                    may_production = (tilt_azimuth_data.may * data.annual_solar_prod * 1000)/sum
                    jun_production = (tilt_azimuth_data.jun * data.annual_solar_prod * 1000)/sum
                    jul_production = (tilt_azimuth_data.jul * data.annual_solar_prod * 1000)/sum
                    aug_production = (tilt_azimuth_data.aug * data.annual_solar_prod * 1000)/sum
                    sep_production = (tilt_azimuth_data.sep * data.annual_solar_prod * 1000)/sum
                    oct_production = (tilt_azimuth_data.oct * data.annual_solar_prod * 1000)/sum
                    nov_production = (tilt_azimuth_data.nov * data.annual_solar_prod * 1000)/sum
                    dec_production = (tilt_azimuth_data.dec * data.annual_solar_prod * 1000)/sum
                            
            res[data.id]['jan_production'] = jan_production
            res[data.id]['feb_production'] = feb_production
            res[data.id]['mar_production'] = mar_production
            res[data.id]['apr_production'] = apr_production
            res[data.id]['may_production'] = may_production
            res[data.id]['jun_production'] = jun_production
            res[data.id]['jul_production'] = jul_production
            res[data.id]['aug_production'] = aug_production
            res[data.id]['sep_production'] = sep_production
            res[data.id]['oct_production'] = oct_production
            res[data.id]['nov_production'] = nov_production
            res[data.id]['dec_production'] = dec_production
                        
        return res
    
    _columns = {
                'loc_station_id' : fields.many2one('insolation.incident.yearly', 'Closest NERL Locations'),
                'tilt_degree' : fields.selection(
                            [
                                ('n', '[N]North'),
                                ('ne', '[NE]North-East'),
                                ('e', '[E]East'),
                                ('se', '[SE]South-East'),
                                ('s', '[S]South'),
                                ('sw', '[SW]South-West'),
                                ('w', '[W]West'),
                                ('nw', '[NW]North-West')
                            ], 'Facing / Azimuth'),
                'faceing' : fields.many2one('tilt.tilt', 'Degree Tilt'),
                'crm_lead_id': fields.many2one('crm.lead', "Lead"),
                'module_product_id': fields.many2one('product.product', 'Module Name', domain=[('product_group', '=', 'module')], type='module'),
                'num_of_module': fields.integer('Number of modules'),
                'inverter_product_id':fields.many2one('product.product', 'Inverters Name', domain=[('product_group', '=', 'inverter')], type='inverter'),
                'num_of_invertor':fields.integer('Number of Inverters'),
                'num_of_arrays':fields.char('Array Number',size = 32, readonly=True,
                                            help="This Number of Arrays is automatically created by OpenERP."),
                'stc_dc_rating': fields.function(_get_system_rating_data, string='STC-DC Rating', type='float', multi='rating_all',digits=(12,3)),
                'ptc_dc_rating': fields.function(_get_system_rating_data, string='PTC-DC Rating', type='float', multi='rating_all',digits=(12,3)),
                'cec_ac_rating': fields.function(_get_system_rating_data, string='CEC-AC Rating', type='float', multi='rating_all',digits=(12,3)),
                'ptc_stc_ratio': fields.function(_get_system_rating_data, string='PTC STC Ratio', type='float', multi='rating_all',digits=(12,3)),
                
                'array_size' : fields.function(_get_system_rating_data, string='Solar Array Size', type='integer', multi='green_all', help="Solar Array Size"),
                'production' : fields.function(_get_system_rating_data, string='Yearly output per KW', type='integer', multi='green_all', help="Yearly output per KW"),
                'array_output' : fields.function(_get_system_rating_data, string='Solar Array Output', type='integer', multi='green_all', help="Solar Array Output"),
                'co2_offset_tons' : fields.function(_get_system_rating_data, string='CO2 Offset', type='integer', multi='green_all', help="Tons of Carbon Annually"),
                'co2_offset_pounds' : fields.function(_get_system_rating_data, string='CO2 Offset', type="integer", multi='green_all', help="Pounds of Carbon annually Eliminated"),
                'cars_off_roads' : fields.function(_get_system_rating_data, string='Cars off the Road', type="integer", multi='green_all', help="Cars taken off the road for one year"),
                'gasoline_equi' : fields.function(_get_system_rating_data, string='Gasoline Equivalent (Gallons of Gas)', type='integer', multi="green_all"),
                'tree_equi' : fields.function(_get_system_rating_data, string='Tree Equivalent', type='integer', multi="green_all", help="Trees cleaning the Air for one year"),
                'tree_planting_equi' : fields.function(_get_system_rating_data, string='Tree Planting Equivalent', type='integer', multi="green_all", help="Trees planted for life of tree"),
                'ave_home_powered' : fields.function(_get_system_rating_data, string='Average Homes Powered', type='integer', multi="green_all", help="Homes Powered for One Year"),
                'ave_light_bulb_powered' : fields.function(_get_system_rating_data, string='Average Light-bulbs Powered', type='integer', multi="green_all", help="Light-bulbs Powered for One Year"),
                
                'annual_solar_prod_display': fields.function(_get_system_rating_data, string='Annual Solar Production(KWh)', type='integer', multi='rating_all', digits=(12,3)),
                'annual_solar_prod': fields.function(_get_system_rating_data, string='Annual Solar Production(KWh)', type='float', multi='rating_all', digits=(12,3)),
                'annual_ele_usage': fields.function(_get_system_rating_data, string='Annual Electricity Usage(KWh)', type='float', multi='rating_all',digits=(12,3)),
                'site_avg_sun_hour': fields.function(_get_system_rating_data, string='Site Avarage Sun Hours', type='float', multi='rating_all'),
                'estimate_shade': fields.float('Estimated Shading'),
                
                'jan_production': fields.function(_get_monthly_production_solar, method=True, type='float', multi='monthly_production', string="January Production", store=True),
                'feb_production': fields.function(_get_monthly_production_solar, method=True, type='float', multi='monthly_production', string="February Production", store=True),
                'mar_production': fields.function(_get_monthly_production_solar, method=True, type='float', multi='monthly_production', string="March Production", store=True),
                'apr_production': fields.function(_get_monthly_production_solar, method=True, type='float', multi='monthly_production', string="April Production", store=True),
                'may_production': fields.function(_get_monthly_production_solar, method=True, type='float', multi='monthly_production', string="May Production", store=True),
                'jun_production': fields.function(_get_monthly_production_solar, method=True, type='float', multi='monthly_production', string="June Production", store=True),
                'jul_production': fields.function(_get_monthly_production_solar, method=True, type='float', multi='monthly_production', string="July Production", store=True),
                'aug_production': fields.function(_get_monthly_production_solar, method=True, type='float', multi='monthly_production', string="Aug Production", store=True),
                'sep_production': fields.function(_get_monthly_production_solar, method=True, type='float', multi='monthly_production', string="Sep Production", store=True),
                'oct_production': fields.function(_get_monthly_production_solar, method=True, type='float', multi='monthly_production', string="October Production", store=True),
                'nov_production': fields.function(_get_monthly_production_solar, method=True, type='float', multi='monthly_production', string="November Production", store=True),
                'dec_production': fields.function(_get_monthly_production_solar, method=True, type='float', multi='monthly_production', string="December Production", store=True),
                }
    

    def create(self, cr, uid, vals, context=None):
        crm_obj = self.pool.get('crm.lead')
        if vals.get('crm_lead_id', False):
            crm_rec = crm_obj.browse(cr, uid, vals['crm_lead_id'], context=context)
            LenArray = len([x.id for x in crm_rec.solar_ids])
            vals.update({'num_of_arrays' : LenArray + 1})
        return super(solar_solar, self).create(cr, uid, vals, context=context)
    
    def unlink(self, cr, uid, ids, context=None):
        line_no=0
        crm_obj = self.pool.get('crm.lead')
        solar_data = self.browse(cr, uid, ids, context=context)
        for record in solar_data:
            lead_id = record.crm_lead_id.id
            crm_data = crm_obj.browse(cr, uid, lead_id, context=context)
            for solar_line in crm_data.solar_ids:
                if solar_line.id != ids[0]:
                    line_no += 1
                    self.write(cr, uid, solar_line.id,{'num_of_arrays':line_no})
        return super(solar_solar, self).unlink(cr, uid, ids, context=context)

class crm_lead_home_description(osv.Model):

    """ Model for CRM Lead Home Information Notes. """

    _name = 'crm.lead.home.description'

    _rec_name = 'home_id'

    _columns = {
            'home_id': fields.many2one('crm.lead', 'Name'),
            'home_user_id': fields.many2one('res.users', 'User'),
            'date': fields.datetime('Date Time'),
            'notes': fields.text('Note')
    }

class crm_lead_electricity_description(osv.Model):

    """ Model for CRM Lead Electricity Information Notes. """

    _name = 'crm.lead.electricity.description'

    _rec_name = 'electricity_id'

    _columns = {
            'electricity_id': fields.many2one('crm.lead', 'Name'),
            'electricity_user_id': fields.many2one('res.users', 'User'),
            'date': fields.datetime('Date Time'),
            'notes': fields.text('Note')
    }

class crm_lead_marketing_description(osv.Model):

    """ Model for CRM Lead Marketing Information Notes. """

    _name = 'crm.lead.marketing.description'

    _rec_name = 'marketing_id'

    _columns = {
            'marketing_id': fields.many2one('crm.lead', 'Name'),
            'marketing_user_id': fields.many2one('res.users', 'User'),
            'date': fields.datetime('Date Time'),
            'notes': fields.text('Note')
    }

class crm_lead_accounting_description(osv.Model):

    """ Model for CRM Lead Accounting Information Notes. """

    _name = 'crm.lead.accounting.description'

    _rec_name = 'accounting_id'

    _columns = {
            'accounting_id': fields.many2one('crm.lead', 'Name'),
            'accounting_user_id': fields.many2one('res.users', 'User'),
            'date': fields.datetime('Date Time'),
            'notes': fields.text('Note')
    }

class crm_lead_system_description(osv.Model):

    """ Model for CRM Lead System Information Notes. """

    _name = 'crm.lead.system.description'

    _rec_name = 'system_id'

    _columns = {
            'system_id': fields.many2one('crm.lead', 'Name'),
            'system_user_id': fields.many2one('res.users', 'User'),
            'date': fields.datetime('Date Time'),
            'notes': fields.text('Note')
    }

class crm_lead_all_tabs_description(osv.Model):

    """ Model for CRM Lead All Tab Information Notes. """

    _name = 'crm.lead.all.tabs.description'

    _rec_name = 'all_tab_id'

    _columns = {
            'all_tab_id': fields.many2one('crm.lead', 'Name'),
            'all_tab_user_id': fields.many2one('res.users', 'User'),
            'date': fields.datetime('Date Time'),
            'notes': fields.text('Note')
    }

class company_quotation(osv.Model):
    """ Model for Product. """
    _name = "company.quotation"
    _description = "Other Company Quotation Information."
    _rec_name = "company_name"
    
    _columns = {
        'company_name': fields.many2one('res.company', 'Company Name'),
        'product_ids' : fields.many2many('product.product', 'product_lead_rel', 'pro_id', 'lead_id', 'Equipments', help="Select or create equipments offered by the Company."),
        'quote_amount' : fields.float('Quoted Amount'),
        'quote_desc': fields.text("Quotation Infomation"),
        }
    
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        rec_name = 'company_name'
        res = []
        for r in self.read(cr, uid, ids, [rec_name], context):
            res.append((r['id'], r[rec_name][1]))
        return res
    
class level_lead(osv.osv):
    """ Model for Lead Level. """
    _name = "level.lead"
    _description = "Level of lead Information."
    
    _columns = {
        'name': fields.char('Technique Name'),
        'description': fields.text('Description'),
        'parent_id': fields.many2one('level.lead', 'Parent Level'),
        }
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the Lead Level must be unique !')
    ]
    
    _constraints = [
        (osv.osv._check_recursion, 'Error ! You cannot create recursive Sales team.', ['parent_id'])
    ]
    
    def name_get(self, cr, uid, ids, context=None):
        """Overrides orm name_get method"""
        if not isinstance(ids, list) :
            ids = [ids]
        res = []
        if not ids:
            return res
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context)

        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res
    
class roof_type(osv.Model):
    """ Model for Heat home. """
    _name = "roof.type"
    _description = "Type of Roof Information."
    
    _columns = {
        'name': fields.char('Technique Name'),
        'description': fields.text('Description'),
        }

class crm_opportunity2phonecall(osv.TransientModel):
    """Converts Opportunity to Phonecall"""
    _inherit = 'crm.opportunity2phonecall'

    def action_schedule(self, cr, uid, ids, context=None):
        action_res = super(crm_opportunity2phonecall, self).action_schedule(cr, uid, ids, context=context)
        stage_id = self.pool.get('crm.case.stage').search(cr, uid, [('name', '=', 'Initial Contact')])
        self.pool.get('crm.lead').write(cr, uid, context.get('active_ids'), {'stage_id': stage_id[0]})
        return action_res

class project_project(osv.Model):
    
    _inherit = 'project.project'
    
    def create(self, cr, uid, vals, context=None):
        if context is None: context = {}
        project_id = super(project_project, self).create(cr, uid, vals, context=context)
        if vals and vals.get('analytic_account_id'):
            for account in self.pool.get('account.analytic.account').browse(cr, uid, [vals['analytic_account_id']]):
                member_list = []
                for member in account.members:
                    member_list.append((4, member.id))
                    self.write(cr, uid, [project_id], {'members': member_list})
        return project_id

class ir_attachment(osv.Model):
    _inherit = "ir.attachment"
    
    def onchange_datas_fname(self, cr, uid, ids, datas_fname, context=None):
        values = {}
        values = {"name": datas_fname}
        return {'value' : values}
    
class document_required(osv.Model):
    
    _name = "document.required"
    
    _columns = {
        'doc_id': fields.many2one('documents.all', 'Document Name'),
        'document_id': fields.many2one('ir.attachment',"Document" ),
        'collected' : fields.boolean("Collected"),
        'crm_lead_id' : fields.many2one('crm.lead', 'Lead'),
        'partner_id' : fields.many2one('res.partner', 'Customer'),
    }
    
    def write(self, cr, uid, ids, vals, context=None):
        if not vals.get('document_id', None):
            return super(document_required, self).write(cr, uid, ids, vals, context=context)
        vals.update({'collected' : True})
        res = super(document_required, self).write(cr, uid, ids, vals, context=context)
        cur_rec = self.browse(cr, uid, ids, context=context)[0]
        
        user_obj = self.pool.get('res.users')
        user_rec = user_obj.browse(cr, uid, uid, context=context)
        
        send_mail_obj = self.pool.get('send.send.mail')
        NO_REC_MSG = ''
        SUB_LINE = 'Notification for Document Upload.'
        MSG_BODY = 'Hello Admin,<br/>' + user_rec.name + ' uploaded a Document named ' + cur_rec.doc_id.name + '.<br/><br/>The Document is successfully Uploaded.<br/><br/> Thank You.'
        send_mail_obj.send(cr, uid, NO_REC_MSG, SUB_LINE, MSG_BODY, 'admin@sunpro-solar.com', context=context)
        
        if cur_rec.doc_id.inform_customer:
            for user in cur_rec.doc_id.inform_users:
                if user.email:
                    MSG_BODY = 'Hello ' + user.name + ',<br/>' + user_rec.name + ' uploaded a Document named ' + cur_rec.doc_id.name + '.<br/><br/>The Document is successfully Uploaded.<br/><br/> Thank You.'
                    send_mail_obj.send(cr, uid, NO_REC_MSG, SUB_LINE, MSG_BODY, user.email, context=context)
        
        if cur_rec.crm_lead_id.user_id:
            MSG_BODY = 'Hello ' + cur_rec.crm_lead_id.user_id.name + ',<br/>' + user_rec.name + ' uploaded a Document named ' + cur_rec.doc_id.name + '.<br/><br/>The Document is successfully Uploaded.<br/><br/> Thank You.'
            send_mail_obj.send(cr, uid, NO_REC_MSG, SUB_LINE, MSG_BODY, cur_rec.crm_lead_id.user_id.email, context=context)
            
        return res

class documents_all(osv.Model):
    """ Model for document information """
    _name = "documents.all"
    _description = "Documents Information."
    
    _columns = {
         'name': fields.char('Document Name'),
         'code': fields.char('Code'),
         'inform_customer' : fields.boolean("Inform Customer"),
         'inform_users' : fields.many2many("res.users", "partner_doc_rel", "partner_id", 'doc_id', 'Users'),
         'prevent': fields.boolean('Prevent'),
     }
    
    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'The code of the Document must be unique !')
    ]
    
class res_partner(osv.Model):
    """ Model for Partner. """
    _inherit = "res.partner"
    
    def _get_total_bonus(self, cr, uid, ids, name, args, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            total_bonus = 0.0
            for line in data.cash_bonus_ids:
                total_bonus += line.cash
            res[data.id] = total_bonus
        return res
    
    _columns = {
        'is_utility_company' : fields.boolean("Is a Utility Company?"),
        'spouse': fields.many2one('res.partner', string='Secondary Customer', help="Secondary Customer (spouse) in case he/she exist."),
        'last_name': fields.char('Last Name'),
        'middle_name' : fields.char('Middle Name'),
        'document_ids': fields.many2many('documents.all', 'company_document_rel', 'partner_id', 'document_id', 'Required Documents'),
        'from_zip': fields.char('Zip (From)'),
        'to_zip' : fields.char('Zip (To)'),
        'cash_bonus_ids' : fields.one2many('cash.bonus','res_partner_id','Cash Bonus'),
        'total_bonus' : fields.function(_get_total_bonus,string="Toatal Bonus", type = "float", method= True),
        'zip_ids' : fields.many2many('city.city','city_res_part_rel',"city_id","res_part_id","Zip"),
    }
    
    def openMap(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        cur_rec = self.browse(cr, uid, ids, context=context)[0]
        url = "http://maps.google.com/maps?oi=map&q="
        if cur_rec.street:
            url += cur_rec.street.replace(' ', '+')
        if cur_rec.street2:
            url += '+' + cur_rec.street2.replace(' ', '+')
        if cur_rec.city_id:
            url += '+' + cur_rec.city_id.name.replace(' ', '+')
        if cur_rec.city_id.state_id:
            url += '+' + cur_rec.city_id.state_id.name.replace(' ', '+')
        if cur_rec.city_id.country_id:
            url += '+' + cur_rec.city_id.country_id.name.replace(' ', '+')
        if cur_rec.city_id.zip:
            url += '+' + cur_rec.city_id.zip.replace(' ', '+')
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new'
        }
    
res_partner()

class crm_meeting(osv.Model):
    """ Model for CRM meetings """
    _inherit = 'crm.meeting'
    
    _columns = {
            'meeting_type': fields.selection([('appointment', 'Appointment'), ('assistance', 'Assistance'), ('general_meeting', 'General Meeting')], 'Meeting Type'),
            'schedule_appointment': fields.datetime('Schedule Date'),
            'appointment_outcome': fields.text('Outcome of the Appointment'),
            'crm_id':fields.many2one('crm.lead', 'CRM'),
            'reason': fields.text('Reason'),
    }
    
    _defaults = {
            'name': '/',
            'meeting_type': 'appointment',
    }
    
    def onchange_dates(self, cr, uid, ids, start_date, duration=False, end_date=False, allday=False, context=None):
        res = super(crm_meeting, self).onchange_dates(cr, uid, ids, start_date, duration=duration, end_date=end_date, allday=allday, context=context)
        if not ids:
            res['value'].update({'schedule_appointment': start_date})
        return res    
    
    def create(self, cr, uid, ids, context=None):
        res = super(crm_meeting, self).create(cr, uid, ids, context=context)
        if context.get('default_opportunity_id'):
            crm_case_stage_obj = self.pool.get('crm.case.stage')
            opo_obj = self.pool.get('crm.lead')
            stage_id = crm_case_stage_obj.search(cr, uid, [('name', '=', 'Appointment Setup')])
            opo_obj.write(cr, uid, [context.get('default_opportunity_id')], {'stage_id': stage_id[0],'appointment_ids': [(6,0,[res])]})
        return res
    
    def send_email(self, cr, uid, message, mail_server_id, context):
        '''
           This method sends mail using information given in message 
        '''
        obj_mail_server = self.pool.get('ir.mail_server')
        obj_mail_server.send_email(cr, uid, message=message, mail_server_id=mail_server_id, context=context)
    
    def salesteam_send_email(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        crm_meeting_data = self.browse(cr, uid, ids[0], context=context)
        crm_obj = self.pool.get('crm.lead')
        crm_data = crm_obj.browse(cr, uid, crm_meeting_data.crm_id, context= context)
        if crm_meeting_data.crm_id:
            crm_obj = self.pool.get('crm.lead')
            crm_id = crm_obj.search(cr, uid, [('id','=',crm_meeting_data.crm_id.id)])
            crm_data = crm_obj.browse(cr, uid, crm_id, context=context)
            obj_mail_server = self.pool.get('ir.mail_server')
            crm_case_stage_obj = self.pool.get('crm.case.stage')
            mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
            if not mail_server_ids:
                raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
            mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
            email_from = mail_server_record.smtp_user
            if not email_from:
                raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
            email_to = []
            for data in self.browse(cr, uid, ids, context):
                if not data.user_id:
                    raise osv.except_osv(_('Warning'), _('There is no Responsible Person define for meeting  !'))
                else:
                    if not data.user_id.email:
                        raise osv.except_osv(_('Warning'), _('%s Responsible user have no email defined !' % data.user_id.name))
                    else:
                        email_to.append(data.user_id.email)
                for crm_data1 in crm_data:
                    subject_line = 'New Customer ' + tools.ustr(crm_data1.partner_id and crm_data1.partner_id.name or '') + ' ' + tools.ustr(crm_data1.last_name) + ' Comes.'
                    message_body = 'Hello,<br/><br/>There is a new customer comes.<br/><br/>Customer Information<br/><br/>First Name : ' + tools.ustr(crm_data1.contact_name) + '<br/><br/>Last Name : ' + tools.ustr(crm_data1.last_name) + '<br/><br/>Address : ' + tools.ustr(crm_data1.street) + ', ' + tools.ustr(crm_data1.street2) + ', ' + tools.ustr(crm_data1.city_id and crm_data1.city_id.name or '') + ', ' + tools.ustr(crm_data1.city_id and crm_data1.city_id.state_id and crm_data1.city_id.state_id.name or '') + ', ' + tools.ustr(crm_data1.city_id and crm_data1.city_id.country_id and crm_data1.city_id.country_id.name or '') + ', ' + tools.ustr(crm_data1.city_id and crm_data1.city_id.zip or '') + '<br/><br/>Email : ' + tools.ustr(crm_data1.email_from) + '<br/><br/>Phone : ' + tools.ustr(crm_data1.phone) + '<br/><br/> Thank You.'
                    message_hrmanager = obj_mail_server.build_email(
                    email_from=email_from,
                    email_to=email_to,
                    subject=subject_line,
                    body=message_body,
                    body_alternative=message_body,
                    email_cc=None,
                    email_bcc=None,
                    attachments=None,
                    references=None,
                    object_id=None,
                    subtype='html',
                    subtype_alternative=None,
                    headers=None)
            self.send_email(cr, uid, message_hrmanager, mail_server_id=mail_server_ids[0], context=context)
            stage_id = crm_case_stage_obj.search(cr, uid, [('name', '=', 'Sales Assignment')])
            crm_obj.write(cr, uid, crm_id, {'stage_id': stage_id[0]}, context=context)
            return True

class project_photos(osv.Model):
    
    _name = "project.photos"
    
    def send_email(self, cr, uid, message, mail_server_id, context):
        '''
           This method sends mail using information given in message 
        '''
        obj_mail_server = self.pool.get('ir.mail_server')
        obj_mail_server.send_email(cr, uid, message=message, mail_server_id=mail_server_id, context=context)
    
    def use_project_photo(self, cr ,uid, ids, context=None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        cash_bonus_obj = self.pool.get('cash.bonus')
        user_obj = self.pool.get('res.users')
        user_rec = user_obj.browse(cr, uid, uid, context=context)
        project_photo_data = self.browse(cr, uid, ids, context=context)[0]
        partner_data = partner_obj.browse(cr, uid, project_photo_data.crm_lead_id.partner_id.id, context=context)
        vals={'name': 'Cash Bonus for picture used in marketing or for SunPro Solar website!', 'cash': 5, 'res_partner_id':partner_data.id}
        cash_bonus_create_id = cash_bonus_obj.create(cr, uid, vals, context= context)
        self.write(cr, uid, ids, {'use_photo': True}, context=context)
        
        obj_mail_server = self.pool.get('ir.mail_server')
        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
        if not mail_server_ids:
            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
        email_from = mail_server_record.smtp_user
        email_to = [user_rec.company_id and user_rec.company_id.info_email_id or 'info@sunpro-solar.com']
        if not email_from:
            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
        subject_line = 'Customer ' + tools.ustr(partner_data.name or '') + ' you get Cash Bonus of $5 for project picture.'
        message_body = 'Hello,<br/><br/>Photo '+ project_photo_data.name +' is used for picture used in marketing or for SunPro Solar website!.<br/><br/>Customer Information<br/><br/>First Name : ' + tools.ustr(partner_data.name) + '<br/><br/>Last Name : ' + tools.ustr(partner_data.last_name) + '<br/><br/>Address : '+ tools.ustr(partner_data.street) + ', ' + tools.ustr(partner_data.street2) + ', '+ tools.ustr(partner_data.city_id and partner_data.city_id.name or '') + ', '+ tools.ustr(partner_data.city_id and partner_data.city_id.state_id and partner_data.city_id.state_id.name or '') + ', '+ tools.ustr(partner_data.city_id and partner_data.city_id.country_id and partner_data.city_id.country_id.name or '') + ', '+ tools.ustr(partner_data.city_id and partner_data.city_id.zip or '') + '<br/><br/>Email : '+ tools.ustr(partner_data.email) + '<br/><br/>Mobile : ' + tools.ustr(partner_data.mobile) + '<br/><br/>Photo Information : <br/><br/>Photo Name:'+ project_photo_data.name +'<br/><br/> Photo Tag line:'+ project_photo_data.tag_line +'<br/><br/> Thank You.'
        message_hrmanager = obj_mail_server.build_email(
        email_from=email_from,
        email_to=email_to,
        subject=subject_line,
        body=message_body,
        body_alternative=message_body,
        email_cc=None,
        email_bcc=None,
        attachments=None,
        references=None,
        object_id=None,
        subtype='html',
        subtype_alternative=None,
        headers=None)
        self.send_email(cr, uid, message_hrmanager, mail_server_id=mail_server_ids[0], context=context)
        return True
    
    def onchange_photo_fname(self, cr, uid, ids, photo_fname, context=None):
        values = {}
        values = {"name": photo_fname}
        return {'value' : values}
    
    _columns = {
        'name' : fields.char('Name'),
        'photo' : fields.binary("Photo"),
        'photo_fname':fields.char('File Name',size=256),
        'tag_line' : fields.char('Tagline'),
        'use_photo' : fields.boolean("Use Photo"),
        'crm_lead_id' : fields.many2one("crm.lead", "Lead")
    }
    
    _defaults = {
        'use_photo' : False
    }
    
    def create(self, cr, uid, vals, context=None):
        res = super(project_photos, self).create(cr, uid, vals, context=context)
        
        if not context:
            context = {}
        
        user_obj = self.pool.get('res.users')
        user_rec = user_obj.browse(cr, uid, uid, context=context)
        auto_email_id = user_rec.company_id.auto_email_id
        
        send_mail_obj = self.pool.get('send.send.mail')
        NO_REC_MSG = 'No Auto email ID defined in Company Configuration !'
        SUB_LINE = 'Notification For uploded Project Photo.'
        MSG_BODY = 'Hello Admin,<br/>' + user_rec.name + ' uploaded a photo as a project photo.' + '<br/><br/>The Photo is successfully Uploded.<br/><br/> Thank You.'
        send_mail_obj.send(cr, uid, NO_REC_MSG, SUB_LINE, MSG_BODY, auto_email_id, context=context)
        
        return res

class res_company(osv.Model):
    
    _inherit = "res.company"
    
    def _get_years_40_offset_tree(self, cr, uid, ids, name, args, context=None):
        res = {}
        years_40_offset_tree = 0.0
        for data in self.browse(cr, uid, ids, context):
            years_40_offset_tree = data.annual_equvi_tree * 40
            res[data.id] = years_40_offset_tree
        return res
    
    def _get_annnual_co2_car(self, cr, uid, ids, name, args, context=None):
        res = {}
        annnual_co2_car = 0.0
        for data in self.browse(cr, uid, ids, context):
            annnual_co2_car = data.medium_pollusion * data.avg_yearly_miles
            res[data.id] = annnual_co2_car
        return res
    
    def _get_annual_home_ele(self, cr, uid, ids, name, args, context=None):
        res = {}
        annual_home_ele = 0.0
        for data in self.browse(cr, uid, ids, context):
            annual_home_ele = data.factor_home_ele_annual * data.avg_co2_ele
            res[data.id] = annual_home_ele
        return res
    
    _columns = {
        'auto_email_id' : fields.char("Auto Email ID", help= "Auto Email ID is used when project photo is uploaded, Project Review is received, Friend Reference is added"),
        'admin_email_id' : fields.char("Admin Email ID", help="Admin Email Id is used when customer request details"),
        'engineering_email_id' : fields.char("Engineering Email ID", help="Engineering Email Id is used when Query generated"),
        'info_email_id' : fields.char("Info Email ID", help="Info Email Id is used when Query generated or customer request to contact"),
        'care_maintance' : fields.binary("Care & Maintenance"),
        'avg_co2_ele': fields.float("Average CO2 emitted to produce Electricity(lbs)"),
        'annual_equvi_tree': fields.float("Annual offset of One Growing Tree(lbs)"),
        'years_40_offset_tree': fields.function(_get_years_40_offset_tree, type="float", string="40 Years Offset of One Growing Tree(lbs)"),
        'medium_pollusion': fields.float("Medium Car CO2 Pollution per Mile(lbs)"),
        'avg_yearly_miles': fields.float("Average Yearly Miles Driven(Miles)"),
        'annnual_co2_car': fields.function(_get_annnual_co2_car, type="float", string="Annual CO2 for Medium Car(lbs)"),
        'factor_home_ele_annual': fields.float('Factor to count Average Yearly Home Electricity'),
        'annual_home_ele': fields.function(_get_annual_home_ele, type="float", string="Average Yearly Home Electricity(lbs)"),
        'avg_light_bulb': fields.float("Average Yearly Light Bulb(KWh)"),
        'avg_comp': fields.float("Average Yearly Computer((KWh))"),
        'emmision_gas': fields.float("Emissions from a Gallon of Gas(lbs)"),
        'fedral_tax':fields.float('Fedral Tax'),
        'sales_tax':fields.float('Sales Tax'),
        'monitoring_links' : fields.one2many('monitoring.links','res_company_id',"Monitoring Links")
    }
    
    _defaults = {
        'avg_co2_ele':1.34,
        'emmision_gas':19.4,
        'annual_equvi_tree':50,
        'avg_yearly_miles': 15000,
        'avg_light_bulb':116.8,
        'factor_home_ele_annual':8900,
        'annual_home_ele': 11926,
        'avg_comp':1,
        'medium_pollusion':1.1,
        'avg_yearly_miles':15000
    }
    
class monitoring_links(osv.Model):
    
    _name="monitoring.links"
    
    _columns = {
                'name': fields.char("Name"),
                'link': fields.char("Link"),
                'res_company_id': fields.many2one('res.company','Company')
                }
    
class SendMail(osv.Model):
    
    _name = "send.send.mail"
    
    def send_email(self, cr, uid, message, mail_server_id, context):
        '''
           This method sends mail using information given in message 
        '''
        obj_mail_server = self.pool.get('ir.mail_server')
        obj_mail_server.send_email(cr, uid, message=message, mail_server_id=mail_server_id, context=context)
        
    def send(self, cr, uid, NO_RECEIVER_ERROR, SUBJECT_LINE, MESSAGE_BODY, AUTO_EMAIL_ID=None, context=None):
        obj_mail_server = self.pool.get('ir.mail_server')
        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
        if not mail_server_ids:
            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
        email_from = mail_server_record.smtp_user
        if not email_from:
            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
        if not AUTO_EMAIL_ID:
            raise osv.except_osv(_('Warning'), _(NO_RECEIVER_ERROR))
        else:
            message_user = obj_mail_server.build_email(
                email_from=email_from,
                email_to=[AUTO_EMAIL_ID],
                subject=SUBJECT_LINE,
                body=MESSAGE_BODY,
                body_alternative=MESSAGE_BODY,
                email_cc=None,
                email_bcc=None,
                attachments=None,
                references=None,
                object_id=None,
                subtype='html',
                subtype_alternative=None,
                headers=None)
            self.send_email(cr, uid, message_user, mail_server_id=mail_server_ids[0], context=context)

class project_reviews(osv.Model):
    
    _name = "project.reviews"
    
    def use_project_review_website(self, cr ,uid, ids, context=None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        cash_bonus_obj = self.pool.get('cash.bonus')
        review_data = self.browse(cr, uid, ids, context=context)[0]
        partner_data = partner_obj.browse(cr, uid, review_data.crm_lead_id.partner_id.id, context=context)
        vals={'name': 'Cash bonus for your review is used on SunPro Solar\'s Website!', 'cash': 25, 'res_partner_id':partner_data.id}
        cash_bonus_create_id = cash_bonus_obj.create(cr, uid, vals, context= context)
        self.write(cr, uid, ids, {'use_review_website': True}, context=context)
        return True
    
    def use_project_review_marketing(self, cr ,uid, ids, context=None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        cash_bonus_obj = self.pool.get('cash.bonus')
        review_data = self.browse(cr, uid, ids, context=context)[0]
        partner_data = partner_obj.browse(cr, uid, review_data.crm_lead_id.partner_id.id, context=context)
        vals={'name': 'Cash bonus for your for review is used for other marketing material.', 'cash': 100, 'res_partner_id':partner_data.id}
        cash_bonus_create_id = cash_bonus_obj.create(cr, uid, vals, context= context)
        self.write(cr, uid, ids, {'use_review_Marketing': True}, context=context)
        return True
    
    _columns = {
        'name' : fields.char("Name"),
        'use_review_website': fields.boolean('Use Review for website'),
        'use_review_Marketing': fields.boolean('Use Review for Marketing Material'),
        'crm_lead_id' : fields.many2one("crm.lead", "Lead"),
    }
    
    def create(self, cr, uid, vals, context=None):
        res = super(project_reviews, self).create(cr, uid, vals, context=context)
        
        if not context:
            context = {}
        
        user_obj = self.pool.get('res.users')
        user_rec = user_obj.browse(cr, uid, uid, context=context)
        auto_email_id = user_rec.company_id.auto_email_id
        
        send_mail_obj = self.pool.get('send.send.mail')
        NO_REC_MSG = 'No Auto email ID defined in Company Configuration !'
        SUB_LINE = 'Notification For Project Review.'
        MSG_BODY = 'Hello Admin,<br/>' + user_rec.name + ' uploaded a project review.' + '<br/><br/>The review is : <br/>"' + vals.get('name') + '"<br/> Thank You.'
        send_mail_obj.send(cr, uid, NO_REC_MSG, SUB_LINE, MSG_BODY, auto_email_id, context=context)
        return res
    
class submit_question(osv.Model):
    
    _name = "submit.question"
    
    _columns = {
                'name' : fields.text("Question"),
                'crm_lead_id' : fields.many2one("crm.lead", "Lead"),
    }
    
class cash_bonus(osv.Model):
    
    _name = "cash.bonus"
    
    _columns = {
                'name' : fields.text("Tag line"),
                'cash' : fields.float('Cash'),
                'res_partner_id' : fields.many2one("res.partner", "Partner"),
    }
    
    
class friend_reference(osv.Model):
    
    _name = "friend.reference"
    
    _columns = {
        'name' : fields.char("First Name"),
        'lname' : fields.char("Last Name"),
        'phone' : fields.char("Phone"),
        'email' : fields.char('Email'),
        'crm_lead_id' : fields.many2one("crm.lead", "Lead"),
    }
    
    def create(self, cr, uid, vals, context=None):
        res = super(friend_reference, self).create(cr, uid, vals, context=context)
        
        if not context:
            context = {}
        
        user_obj = self.pool.get('res.users')
        user_rec = user_obj.browse(cr, uid, uid, context=context)
        auto_email_id = user_rec.company_id.info_email_id
        friend_email_id = vals.get('email')
        fname = vals.get('name')
        lname = vals.get('lname')
        
        send_mail_obj = self.pool.get('send.send.mail')
        NO_REC_MSG = 'No Auto email ID defined in Company Configuration !'
        SUB_LINE = 'Notification For Friend Reference.'
        MSG_BODY = 'Hello Admin,<br/>' + user_rec.name + ' added friend reference.' + '<br/><br/>The reference is : <br/>' + fname + " " + lname + "<br/>Email : " + friend_email_id + '<br/> Thank You.'
        send_mail_obj.send(cr, uid, NO_REC_MSG, SUB_LINE, MSG_BODY, auto_email_id, context=context)
        
        NO_REC_MSG = 'Invalid friend Email ID !'
        SUB_LINE = 'Notification For Friend Reference.'
        MSG_BODY = 'Hello Admin,<br/>' + user_rec.name + ' added friend reference.' + '<br/><br/>The reference is : <br/>' + fname + " " + lname + "<br/>Email : " + friend_email_id + '<br/> Thank You.'
        send_mail_obj.send(cr, uid, NO_REC_MSG, SUB_LINE, MSG_BODY, auto_email_id, context=context)


class product_pricelist_item(osv.Model):
    
    _inherit = 'product.pricelist.item'
    
    _columns = {
            'daily_minimum_charges': fields.float('Daily Minumum Charges', digits=(12,5)),
            'monthly_minimum_charges': fields.float('Monthly Minumum Charges', digits=(12,5)),
            'daily_meter_charges': fields.float('Daily Meter Charges', digits=(12,5)),
            'monthly_meter_charges': fields.float('Monthly Meter Charges', digits=(12,5)),
            'tier1': fields.float('Tier1',digits=(12,5)),
            'off_peak_tier2': fields.float('Off-Peak/Tier2' , digits=(12,5)),
            'part_peak_tier3': fields.float('Part-Peak/Tier3', digits=(12,5)),
            'peak_tier4': fields.float('Peak Tier4', digits=(12,5)),
            'stage_changes': fields.float('Stage Changes', digits=(12,5)),
            'rate_stablization': fields.float('Rate Stablization'),
            'surcharge_3': fields.float('Surcharge 3'),
            'surcharge_4': fields.float('Surcharge 4'),
            'surcharge_5': fields.float('Surcharge 5'),
            'surcharge_6': fields.float('Surcharge 6'),
            'summer_qty': fields.float('Summer Quantity'),
            'winter_qty': fields.float('Winter Quantity'),
    }

class product_pricelist(osv.osv):
    _inherit = 'product.pricelist'
    
    def price_get_multi(self, cr, uid, pricelist_ids, products_by_qty_by_partner, context=None):
        """multi products 'price_get'.
           @param pricelist_ids:
           @param products_by_qty:
           @param partner:
           @param context: {
             'date': Date of the pricelist (%Y-%m-%d),}
           @return: a dict of dict with product_id as key and a dict 'price by pricelist' as value
        """

        def _create_parent_category_list(id, lst):
            if not id:
                return []
            parent = product_category_tree.get(id)
            if parent:
                lst.append(parent)
                return _create_parent_category_list(parent, lst)
            else:
                return lst
        # _create_parent_category_list

        if context is None:
            context = {}
        if not context.get('get_field'):
            return super(product_pricelist, self).price_get_multi(cr, uid, pricelist_ids, products_by_qty_by_partner, context=context)
        date = context.get('date') or time.strftime('%Y-%m-%d')

        currency_obj = self.pool.get('res.currency')
        product_obj = self.pool.get('product.product')
        product_category_obj = self.pool.get('product.category')
        product_uom_obj = self.pool.get('product.uom')
        supplierinfo_obj = self.pool.get('product.supplierinfo')
        price_type_obj = self.pool.get('product.price.type')

        # product.pricelist.version:
        if not pricelist_ids:
            pricelist_ids = self.pool.get('product.pricelist').search(cr, uid, [], context=context)

        pricelist_version_ids = self.pool.get('product.pricelist.version').search(cr, uid, [
                                                        ('pricelist_id', 'in', pricelist_ids),
                                                        '|',
                                                        ('date_start', '=', False),
                                                        ('date_start', '<=', date),
                                                        '|',
                                                        ('date_end', '=', False),
                                                        ('date_end', '>=', date),
                                                    ])
        if len(pricelist_ids) != len(pricelist_version_ids):
            raise osv.except_osv(_('Warning!'), _("At least one pricelist has no active version !\nPlease create or activate one."))

        # product.product:
        product_ids = [i[0] for i in products_by_qty_by_partner]
        #products = dict([(item['id'], item) for item in product_obj.read(cr, uid, product_ids, ['categ_id', 'product_tmpl_id', 'uos_id', 'uom_id'])])
        products = product_obj.browse(cr, uid, product_ids, context=context)
        products_dict = dict([(item.id, item) for item in products])

        # product.category:
        product_category_ids = product_category_obj.search(cr, uid, [])
        product_categories = product_category_obj.read(cr, uid, product_category_ids, ['parent_id'])
        product_category_tree = dict([(item['id'], item['parent_id'][0]) for item in product_categories if item['parent_id']])

        results = {}
        for product_id, qty, partner in products_by_qty_by_partner:
            if not qty:
                qty = 0
            for pricelist_id in pricelist_ids:
                price = False

                tmpl_id = products_dict[product_id].product_tmpl_id and products_dict[product_id].product_tmpl_id.id or False

                categ_id = products_dict[product_id].categ_id and products_dict[product_id].categ_id.id or False
                categ_ids = _create_parent_category_list(categ_id, [categ_id])
                if categ_ids:
                    categ_where = '(categ_id IN (' + ','.join(map(str, categ_ids)) + '))'
                else:
                    categ_where = '(categ_id IS NULL)'

                if partner:
                    partner_where = 'base <> -2 OR %s IN (SELECT name FROM product_supplierinfo WHERE product_id = %s) '
                    partner_args = (partner, tmpl_id)
                else:
                    partner_where = 'base <> -2 '
                    partner_args = ()

                cr.execute(
                    'SELECT i.*, pl.currency_id '
                    'FROM product_pricelist_item AS i, '
                        'product_pricelist_version AS v, product_pricelist AS pl '
                    'WHERE (product_tmpl_id IS NULL OR product_tmpl_id = %s) '
                        'AND (product_id IS NULL OR product_id = %s) '
                        'AND (' + categ_where + ' OR (categ_id IS NULL)) '
                        'AND (' + partner_where + ') '
                        'AND price_version_id = %s '
                        'AND (min_quantity IS NULL OR min_quantity <= %s) '
                        'AND i.price_version_id = v.id AND v.pricelist_id = pl.id '
                    'ORDER BY sequence',
                    (tmpl_id, product_id) + partner_args + (pricelist_version_ids[0], qty))
                res1 = cr.dictfetchall()
                uom_price_already_computed = False
                value1 = 0.0
                for res in res1:
                    value1 = res[context.get('get_field')]
                results[product_id] = {pricelist_id: value1}
        return results
