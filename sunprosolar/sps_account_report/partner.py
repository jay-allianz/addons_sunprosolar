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

from openerp.osv import fields, osv
from openerp.tools.translate import _
import time

class res_partner(osv.Model):

    def compute_mtd_sale(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for partner in self.browse(cursor, user, ids, context=context):
            sale_obj = self.pool.get('sale.order')
            order_ids = sale_obj.search(cursor, user, [('partner_id', '=', partner.id), ('state', '!=', 'draft')], context=context)
            current_month = time.strftime("%m")
            current_year = time.strftime("%Y")
            total = 0.0
            for sale in sale_obj.browse(cursor, user, order_ids, context=context):
                sale_date = sale.date_order
                sale_day = time.strptime(sale_date, '%Y-%m-%d')
                if int(sale_day[1]) == int(current_month) and int(sale_day[0]) == int(current_year):
                    total += sale.amount_total
            res[partner.id] = total
        return res

    def compute_ytd_sale(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for partner in self.browse(cursor, user, ids, context=context):
            sale_obj = self.pool.get('sale.order')
            order_ids = sale_obj.search(cursor, user, [('partner_id', '=', partner.id), ('state', '!=', 'draft')], context=context)
            current_year = time.strftime("%Y")
            total = 0.0
            for sale in sale_obj.browse(cursor, user, order_ids, context=context):
                sale_date = sale.date_order
                sale_day = time.strptime(sale_date, '%Y-%m-%d')
                if int(sale_day[0]) == int(current_year):
                    total += sale.amount_total
            res[partner.id] = total
        return res
    _inherit = 'res.partner'
    _columns = {
        'sale_order_ids' : fields.one2many('sale.order', 'partner_id', 'Sale Order History'),
        'mtd_sales' : fields.function(compute_mtd_sale, type='float', string='MTD Sales',
                store={
                'res.partner': (lambda self, cr, uid, ids, c={}: ids, ['sale_order_ids'], 20),
                'res.partner.mtd_sales': (compute_mtd_sale, ['ids'], 20),
            },),
        'ytd_sales' : fields.function(compute_ytd_sale, type='float', string='YTD Sales',),
         'shipping_ids': fields.one2many('res.partner', 'parent_id', 'Shipping Address', domain=[('active', '=', True), ('type', '=', 'delivery')]),
    }

class sale_order(osv.Model):

    _inherit = 'sale.order'
    _columns = {
        'sale_order_id' : fields.many2one('res.partner', 'Order Id')
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
