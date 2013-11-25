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
from openerp import tools
import re

class crm_lead2opportunity_partner(osv.osv_memory):

    _inherit = 'crm.lead2opportunity.partner'

    _columns = {
        'msg': fields.char('Note : ', size=64),
        }

    def default_get(self, cr, uid, fields, context=None):
        res = super(crm_lead2opportunity_partner,self).default_get(cr, uid, fields, context=context)
        if context is None:
            context = {}
        lead_obj = self.pool.get('crm.lead')
        for lead in lead_obj.browse(cr, uid, context.get('active_ids', []), context=context):
            property_tax = lead and lead.property_tax
            federal_tax = lead and lead.federal_tax
            mortgage = lead and lead.mortgage
            bankruptcy = lead and lead.bankruptcy
            rate_credit = lead and lead.rate_credit
            if property_tax =='yes' and federal_tax =='yes' and mortgage =='yes' and bankruptcy =='yes' and rate_credit in ['fair','good']:
                res.update({'msg': ""})
            else:
                res.update({'msg': "Customer is not qualified !"})
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: