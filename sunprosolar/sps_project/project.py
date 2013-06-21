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

class project(osv.osv):
    _inherit = "project.project"
    
    _columns = {
                
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
            'default_partner_ids' : project.partner_id and [project.partner_id.id] or False,
            'default_user_id': uid,
            'default_name': project.name,
        }
        return res
    
project()

class task(osv.osv):
    _inherit= "project.task"
    
    _columns= {
               'contract_change': fields.boolean("Need Changes in Contract?",help="Checked if job can not be installed according to contract or need any changes."),
               'contract_id': fields.many2one('hr.contract', 'Contract', help="The contract for which applied this input"),
               }
task()

class hr_contract(osv.osv):
    """ Model for contract. """
    _inherit = "hr.contract"
    
    _columns = {

        }
