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
from openerp.tools.translate import _

class crm_make_sale(osv.osv_memory):
    
    _inherit = 'crm.make.sale'
    
    def makeOrder(self, cr, uid, ids, context=None):
        
        if context is None:
            context = {}
        
        lead_obj = self.pool.get('crm.lead')
        sale_order_line_obj = self.pool.get('sale.order.line')
        sale_order_obj = self.pool.get('sale.order')
        data = context and context.get('active_ids', []) or []
        
        module_line = {}
        inv_line = {}
        order = {}
        
        lead = lead_obj.browse(cr, uid, context.get('active_id'), context=context)
        make_sale = self.browse(cr, uid, ids[0], context=context).partner_id
        partner = sale_order_obj.onchange_partner_id(cr, uid, ids, make_sale.id, context=context)
        utility_company_id = False
        if lead.utility_company_id and lead.utility_company_id.property_product_pricelist:
            utility_company_id = lead.utility_company_id.property_product_pricelist.id
        if self.browse(cr, uid, ids[0], context=context).close:
                lead_obj.case_close(cr, uid, data)
        order = {
            'partner_id' : make_sale.id,
            'pricelist_id' : utility_company_id,
            'partner_invoice_id' : partner.get('value').get('partner_invoice_id'),
            'partner_shipping_id' : partner.get('value').get('partner_shipping_id'),
        }
        order_id = sale_order_obj.create(cr,uid,order,context=context)
        
        for solar_line in lead.solar_ids:
            
            module_line = {
                'product_id' : solar_line.module_product_id.id,
                'name' : solar_line.module_product_id.name,
                'product_uom_qty' : solar_line.num_of_module,
                'no_module' : solar_line.num_of_module,
                'price_unit' : ((solar_line.module_product_id.pv_module_power_stc * solar_line.module_product_id.cost_per_stc_watt) + (solar_line.module_product_id.pv_module_power_stc * solar_line.module_product_id.labor_per_stc_watt) + (solar_line.module_product_id.pv_module_power_stc * solar_line.module_product_id.materials_per_stc)) * (1 + solar_line.module_product_id.markup/100),     
                'type' : solar_line.module_product_id.procure_method,
                'order_id' : order_id
            }

            inv_line = {
                'product_id' : solar_line.inverter_product_id.id,
                'name' : solar_line.inverter_product_id.name,
                'product_uom_qty' : solar_line.num_of_invertor,
                'no_inverter' : solar_line.num_of_invertor,
                'price_unit' : ((solar_line.inverter_product_id.power_rating * solar_line.inverter_product_id.cost_per_ac_capacity_watt ) + (solar_line.inverter_product_id.power_rating * solar_line.inverter_product_id.labor_per_ac_watt) + (solar_line.inverter_product_id.power_rating * solar_line.inverter_product_id.materials_per_stc)),
                'type' : solar_line.inverter_product_id.procure_method,
                'order_id' : order_id
            }
            sale_order_line_obj.create(cr, uid, module_line, context=context)
            sale_order_line_obj.create(cr, uid, inv_line, context=context)
        return {
            'domain': str([('id', 'in', [order_id])]),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'sale.order',
            'view_id': False,
            'res_id' : order_id,
            'type': 'ir.actions.act_window',
            'name' : _('Quotation'),
        }