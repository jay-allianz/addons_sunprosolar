# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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

class module_master(osv.Model):
    
    _name="module.master"
    
    _columns = {
            'name' : fields.char('Name'),
            'description': fields.text('Description')
          }
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The name of the Product Module must be unique !')
    ]

class product_invertor_brand(osv.Model):

    _name="product.invertor.brand"

    _columns = {
            'name' : fields.char('Name'),
            'description': fields.text('Description')
          }
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The name of the Inverter Brand must be unique !')
    ]

class product_brand(osv.Model):

    _name="product.brand"
    
    _columns = {
            'name' : fields.char('Name'),
            'description': fields.text('Description')
          }
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The name of the Brand must be unique !')
    ]

class product_product(osv.Model):

    _inherit="product.product"
    
    _columns = {
            'product_group' : fields.selection([('module', 'Module'),('inverter','Inverter'),('others','Others')], 'Product Group',help="In which group the product belongs to?",required=True),
#            'pv_module_name' : fields.many2one("module.master",'PV Module Name'),
#            'no_module': fields.integer('No of Module'),
            'brand_module': fields.many2one("product.brand","Brand"),
            'pv_module_power_stc': fields.float("PV Module Power STC (KW)"),
            'module_ptc_rating':fields.float("Module PTC rating (KW)"),
            'module_hieght':fields.float("Module Height (CM)"),
            'module_width':fields.float("Module Width (CM)"),
            'module_weight':fields.float("Module Weight (LBS)"),
            'panel_area': fields.float("Solar Panel Area (Meter2)"),
#            'module_stc_dc_rating': fields.float("Module STC-DC Ratings (KW)"),
            'module_ptc_dc_rating': fields.float("Module PTC-DC Ratings (KW)"),
            'cost_per_stc_watt': fields.float("Cost Per STC Watt ($)"),
            'labor_per_stc_watt': fields.float("Labor Per STC Watt ($)"),
            'materials_per_stc': fields.float("Materials Per STC ($)"),
            'markup': fields.float("Markup (%)"),
            'invertor_name': fields.char("Inverter name"),
            'brand_invertor': fields.many2one("product.invertor.brand","Brand"),
            'no_invertor': fields.integer("Number of Inverters"),
            'cec_efficiency': fields.float("CEC Efficiency (%)"),
            'power_rating': fields.float("Power Rating (AC Capacity watt)"),
            'meter': fields.boolean("Meter"),
            'cost_per_ac_capacity_watt':fields.float("Cost Per AC capacity Watt ($)"),
            'labor_per_ac_watt':fields.float("Labor Per AC Watt ($)"),
            'materials_per_ac_watt':fields.float("Materials Per AC Watt ($)"),

          }
    
    _defaults={
        'product_group':'others'
    }


class product_pricelist_item(osv.osv):
    _inherit= 'product.pricelist.item'
    
    _columns = {
            'min_quantity': fields.float('Min. Quantity',digits=(16, 5), required=True, help="Specify the minimum quantity that needs to be bought/sold for the rule to apply."),
       } 