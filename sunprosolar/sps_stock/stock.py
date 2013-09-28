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

from openerp.osv import osv, fields

class stock_warehouse(osv.osv):

    _inherit="stock.warehouse"
    
    _columns = {
          'alert_users_ids' : fields.many2many('res.users','warehouse_users_rel','user_id','warehouse_id','Alert Users'),
          }

class procurement_order(osv.osv):
    _inherit = 'procurement.order'

    def _procure_orderpoint_confirm(self, cr, uid, automatic=False, use_new_cursor=False, context=None, user_id=False):
        res = super(procurement_order, self)._procure_orderpoint_confirm(cr, uid, automatic=automatic, use_new_cursor=use_new_cursor, context=context, user_id=user_id)
        if context is None:
            context = {}
        orderpoint_obj = self.pool.get('stock.warehouse.orderpoint')
        emil_obj= self.pool.get('email.template')
        offset = 0
        ids = [1]
        while ids:
            ids = orderpoint_obj.search(cr, uid, [], offset=offset, limit=100)
            
            for op in orderpoint_obj.browse(cr, uid, ids, context=context):
                prods = self._product_virtual_get(cr, uid, op)
                if prods is None:
                    continue
                if prods < op.product_min_qty:
                    template_id = emil_obj.search(cr, uid, [('model_id.model','=','stock.warehouse.orderpoint')], context=context)
                    if template_id:
                        user_ids = op.warehouse_id.alert_users_ids
                        to_email= ''
                        for user in user_ids:
                            to_email+=user.email + ','
                            
                        emil_obj.write(cr,uid, template_id, {'email_to': to_email})
                        self.pool.get('email.template').send_mail(cr,uid,template_id[0],op.id,force_send=True, context=context)
            if ids:
                break
        return res