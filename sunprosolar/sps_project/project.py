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
from datetime import date, timedelta, datetime
from dateutil import parser, rrule
import addons
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import logging
import base64
import netsvc
WEB_LINK_URL = "db=%s&uid=%s&pwd=%s&id=%s&state=%s&action_id=%s"

class project_project(osv.Model):
    
    _inherit = "project.project"
    
    _columns = {
                'project_task_stage': fields.related('tasks', 'state', type='related', string='Project Task Stage'),
                 }
project_project()


class product_task_type(osv.Model):
    
    _inherit = 'project.task.type'
    
    _columns = {
        'color' : fields.selection([(0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),
                                    (5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9')], 'Stage Color')
    }

class project_task(osv.Model):
    
    _inherit = 'project.task'
    
    def create(self, cr, uid, vals, context=None):
        stage_pool = self.pool.get('project.task.type')
        if vals.get('stage_id', False):
            rec = stage_pool.browse(cr, uid, vals.get('stage_id'), context=context)
            if rec.color:
                vals.update({'color' : rec.color})
        return super(project_task, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        stage_pool = self.pool.get('project.task.type')
        if vals.get('stage_id', False):
            rec = stage_pool.browse(cr, uid, vals.get('stage_id'), context=context)
            if rec.color:
                vals.update({'color' : rec.color})
        return super(project_task, self).write(cr, uid, ids, vals, context=context)
            

