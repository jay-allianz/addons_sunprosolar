# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>).
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

class res_partner(osv.Model):
    
    _inherit = 'res.partner'
    
    _columns = {
                'sale_order_ids' : fields.one2many('sale.order','partner_id','Sale Order History'),
    }

class sale_order(osv.Model):
    
    _inherit = 'sale.order'

    _columns = {
                'sale_order_id' : fields.many2one('res.partner','Order Id')
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: