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

from openerp.osv import fields
from openerp.osv import osv
from openerp import tools
from openerp.tools.translate import _
import time

class hr_contract(osv.osv):
    """ Model for contract. """
    _inherit = "hr.contract"
    
    _columns = {
            'contract_id':fields.char('Contract ID'),
            'contract_date': fields.date('Contract Date'),
            'customer': fields.many2one('res.partner','Customer'),
            'type_of_finance': fields.many2one('account.account.type','Type of Financing '),
            'deposit' :fields. float('Deposit Collected'),
            'equipment_ids': fields.one2many('equipment.line','equipment_id','Equipments'),
            'project_id' : fields.many2one('project.project','Project', help="Select or Create a project related this contract.")
        }
    
    _defaults = {
        'contract_date': lambda *a: time.strftime("%Y-%m-%d"),
    }
    
hr_contract()

class equipment_line(osv.osv):
    
    _name = "equipment.line"
    
    _columns = {
       'equipment_id': fields.many2one('hr.contract', 'Contract Reference', required=True, ondelete='cascade', select=True, readonly=True, states={'draft':[('readonly',False)]}),
       'product_id': fields.many2one('product.product', 'Product', domain=[('sale_ok', '=', True)], change_default=True),
    }
equipment_line()

class project(osv.osv):
    
    _inherit = "project.project"
    
    _columns = {
                }