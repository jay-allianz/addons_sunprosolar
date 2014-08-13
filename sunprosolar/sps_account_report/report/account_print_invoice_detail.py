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
from openerp.osv import osv
import time
from openerp.report import report_sxw
import datetime
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class sps_account_invoice_detail(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(sps_account_invoice_detail, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'sale_date_order': self.sale_date_order,
            'ship_date': self.ship_date,
            'find_shipper':self.find_shipper,
            'shipped_qty':self.shipped_qty,
            'bo_qty':self.bo_qty,
            'sale_order_line':self._sale_order_line,
        })

    def _sale_order_line(self,origin):
        order_line=[]
        if origin:
            sale_order_obj = self.pool.get('sale.order')
            sale_order_ids = sale_order_obj.search(self.cr, self.uid, [('name','=',origin)])
            if sale_order_ids:
                order_line = sale_order_obj.browse(self.cr, self.uid, sale_order_ids[0]).order_line
                return order_line
        return order_line

    def shipped_qty(self,invoice_id,invoice_line):
        sale_order_obj = self.pool.get('sale.order')
        invioce_obj = self.pool.get('account.invoice')
        picking_obj = self.pool.get('stock.picking.out')
        sale_order_ids = sale_order_obj.search(self.cr, self.uid, [('invoice_ids', 'in', [invoice_id])])
        ordered_qty = 0
        for sale_rec in sale_order_obj.browse(self.cr, self.uid,sale_order_ids):
             for picking in sale_rec.picking_ids:
                if picking.state =='done':
                    for line in picking.move_lines:
                        if line.name == invoice_line.name:
                            ordered_qty =  line.product_qty
        return ordered_qty

    def bo_qty(self,invoice_id,invoice_line):
        sale_order_obj = self.pool.get('sale.order')
        invioce_obj = self.pool.get('account.invoice')
        picking_obj = self.pool.get('stock.picking.out')
        sale_order_ids = sale_order_obj.search(self.cr, self.uid, [('invoice_ids', 'in', [invoice_id])])
        ordered_qty = 0
        for sale_rec in sale_order_obj.browse(self.cr, self.uid,sale_order_ids):
             for picking in sale_rec.picking_ids:
                if picking.state !='done':
                    for line in picking.move_lines:
                        if line.name == invoice_line.name:
                            ordered_qty =  line.product_qty
        return ordered_qty

    def sale_date_order(self,invoice_id):
        sale_order_obj = self.pool.get('sale.order')
        sale_order_ids = sale_order_obj.search(self.cr, self.uid, [('invoice_ids', 'in', [invoice_id])])
        if sale_order_ids:
            order_date = sale_order_obj.browse(self.cr, self.uid, sale_order_ids[0]).date_order
            return order_date
        return False
        
    def ship_date(self,origin,id):
        if not origin:
            return False
        picking_obj = self.pool.get('stock.picking.out')
        pick_ids = picking_obj.search(self.cr, self.uid, [('origin','=',origin)])
        if pick_ids:
            order_date = picking_obj.browse(self.cr, self.uid, pick_ids[0]).date
            return order_date
        return False

    def find_shipper(self,origin):
        if not origin:
            return False
        picking_obj = self.pool.get('stock.picking.out')
        users_obj = self.pool.get('res.users')
        pick_ids = picking_obj.search(self.cr, self.uid, [('origin','=',origin)])
        user_name = ''
        if pick_ids:
            self.cr.execute('select create_uid from stock_picking where id= %s' % (pick_ids[0]))
            user_id = map(lambda x: x[0], self.cr.fetchall())
            if user_id:
                user_name = users_obj.browse(self.cr, self.uid, user_id[0]).name
                return user_name
        else:
            return user_name 

report_sxw.report_sxw(
    'report.account.invoice.detail.webkit',
    'account.invoice',
    'addons/sps_account_report/report/account_print_invoice_detail.mako',
    parser=sps_account_invoice_detail
)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
