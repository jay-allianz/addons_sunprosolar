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

from osv import fields, osv
import project
import time
import netsvc
import datetime
from tools.translate import _
import tools
from datetime import date, timedelta
from dateutil import parser, rrule
import addons
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import logging
import base64
import netsvc
WEB_LINK_URL = "db=%s&uid=%s&pwd=%s&id=%s&state=%s&action_id=%s"

AVAILABLE_PRIORITIES = [
    ('1', 'Highest'),
    ('2', 'High'),
    ('3', 'Normal'),
    ('4', 'Low'),
    ('5', 'Lowest'),
]

class project(osv.osv):
    _inherit = "project.project"
    
    _columns = {
                 'priority': fields.selection(project.AVAILABLE_PRIORITIES, 'Priority', select=True),
                }
    
    def action_makeMeeting(self, cr, uid, ids, context=None):
        """
        Open meeting's calendar view to schedule meeting on current project.
        :return dict: dictionary value for created Meeting view
        """
        project = self.browse(cr, uid, ids[0], context)
        
        res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid, 'sps_project', 'action_project_meeting', context)
        res['context'] = {
            'default_project_id': project.id,
            'default_partner_id': project.partner_id and project.partner_id.id or False,
            'default_user_id': uid,
            'default_name': project.name,
        }
        return res
    
    def schedule_phonecall(self, cr, uid, ids, schedule_time, call_summary, desc, phone, contact_name, user_id=False, action='schedule', context=None):
        """
        :param string action: ('schedule','Schedule a call'), ('log','Log a call')
        """
        phonecall = self.pool.get('project.phonecall')
        model_data = self.pool.get('ir.model.data')
        phonecall_dict = {}
        for project in self.browse(cr, uid, ids, context=context):
            if not user_id:
                user_id = project.user_id and project.user_id.id or False
            vals = {
                'name': call_summary,
                'project_id': project.id,
                'user_id': user_id or False,
                'description': desc or '',
                'date': schedule_time,
                'partner_id': project.partner_id and project.partner_id.id or False,
                'partner_phone': phone or project.phone or (project.partner_id and project.partner_id.phone or False),
                'partner_mobile': project.partner_id and project.partner_id.mobile or False,
                'priority': project.priority,
            }
            new_id = phonecall.create(cr, uid, vals, context=context)
            phonecall.case_open(cr, uid, [new_id], context=context)
            if action == 'log':
                phonecall.case_close(cr, uid, [new_id], context=context)
            phonecall_dict[project.id] = new_id
            self.schedule_phonecall_send_note(cr, uid, [project.id], new_id, action, context=context)
        return phonecall_dict
    
    def schedule_phonecall_send_note(self, cr, uid, ids, phonecall_id, action, context=None):
        phonecall = self.pool.get('crm.phonecall').browse(cr, uid, [phonecall_id], context=context)[0]
        if action == 'log': prefix = 'Logged'
        else: prefix = 'Scheduled'
        message = _("<b>%s a call</b> for the <em>%s</em>.") % (prefix, phonecall.date)
        return self.message_post(cr, uid, ids, body=message, context=context)
    
project()

class task(osv.osv):
    _inherit= "project.task"
    
    _columns= {
               'contract_change': fields.boolean("Need Changes in Contract?",help="Checked if job can not be installed according to contract or need any changes."),
               'contract_id': fields.many2one('hr.contract', 'Contract', help="The contract for which applied this input"),
               'sale_order' : fields.many2one('sale.order', 'Materials to Ordered'),
               }
task()

class hr_contract(osv.osv):
    """ Model for contract. """
    _inherit = "hr.contract"
    
    _columns = {

        }
    
class sale_order(osv.osv):
    """Model for Sale Order"""
    _inherit = "sale.order"
    
    _columns = {

        }
