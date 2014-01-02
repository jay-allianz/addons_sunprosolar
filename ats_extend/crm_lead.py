# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
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

from openerp.addons.base_status.base_stage import base_stage
from openerp.osv import fields, osv, orm
from base.res.res_partner import format_address
from openerp.tools.translate import _

class crm_lead(base_stage, format_address, osv.osv):
    """ CRM Lead Case """
    _inherit = "crm.lead"

    def _convert_opportunity_data(self, cr, uid, lead, customer, section_id=False, context=None):
        crm_stage = self.pool.get('crm.case.stage')
        contact_id = False
        if customer:
            contact_id = self.pool.get('res.partner').address_get(cr, uid, [customer.id])['default']
        if not section_id:
            section_id = lead.section_id and lead.section_id.id or False
        val = {
            'planned_revenue': lead.planned_revenue,
            'probability': lead.probability,
            'name': lead.name,
            'partner_id': customer and customer.id or False,
            'user_id': (lead.user_id and lead.user_id.id),
#            'type': 'opportunity',
            'date_action': fields.datetime.now(),
            'date_open': fields.datetime.now(),
            'email_from': customer and customer.email or lead.email_from,
            'phone': customer and customer.phone or lead.phone,
            'state':"open"
        }
        stage_id = crm_stage.search(cr, uid, [('state','=','open')])
        stage = crm_stage.browse(cr, uid, stage_id)
        s_id =''
        for stage_status in stage:
            s_id = stage_status.id
        if stage_id:
            val['stage_id'] = s_id
        return val
    
    def redirect_opportunity_view(self, cr, uid, opportunity_id, context=None):
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
            'res_id': int(opportunity_id),
            'view_id': False,
            'views': [(form_view or False, 'form'),
                    (tree_view or False, 'tree'),
                    (False, 'calendar'), (False, 'graph')],
            'type': 'ir.actions.act_window',
        }
