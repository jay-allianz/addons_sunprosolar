# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

class project2phonecall(osv.osv_memory):
    """Converts Project to Phonecall"""
    _inherit = 'project.phonecall2phonecall'
    _name = 'project.project2phonecall'
    _description = 'Project to Phonecall'

    def default_get(self, cr, uid, fields, context=None):
        pro_obj = self.pool.get('project.project')

        record_ids = context and context.get('active_ids', []) or []
        res = {}
        res.update({'action': 'log', 'date': time.strftime('%Y-%m-%d %H:%M:%S')})
        for pro in pro_obj.browse(cr, uid, record_ids, context=context):
            if 'name' in fields:
                res.update({'name': pro.name})
            if 'user_id' in fields:
                res.update({'user_id': pro.user_id and pro.user_id.id or False})
            if 'partner_id' in fields:
                res.update({'partner_id': pro.partner_id and pro.partner_id.id or False})
            if 'note' in fields:
                res.update({'note': pro.description})
            if 'contact_name' in fields:
                res.update({'contact_name': pro.partner_id and pro.partner_id.name or False})
            if 'phone' in fields:
                res.update({'phone': pro.partner_id.phone or (pro.partner_id and pro.partner_id.phone or False)})
        return res

    def action_schedule(self, cr, uid, ids, context=None):
        value = {}
        if context is None:
            context = {}
        phonecall = self.pool.get('project.phonecall')
        project_ids = context and context.get('active_ids') or []
        project = self.pool.get('project.project')
        data = self.browse(cr, uid, ids, context=context)[0]
        call_ids = project.schedule_phonecall(cr, uid, project_ids, data.date, data.name, \
                data.note, data.phone, data.contact_name, data.user_id and data.user_id.id or False, \
                action=data.action, context=context)
        return {'type': 'ir.actions.act_window_close'}

project2phonecall()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
