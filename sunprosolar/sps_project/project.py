# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
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
                'project_task_stage': fields.related('tasks', 'stage_id', type='many2one', store=True,relation='project.task.type', string='Project Task Stage'),
                 }
    
project_project()

class product_task_type(osv.Model):
    
    _inherit = 'project.task.type'
    
    _columns = {
        'color' : fields.selection([(0,'White'),(1,'Gray'),(2,'Coral '),(3,'Yellow'),(4,'LimeGreen '),
                                    (5,'Aquamarine'),(6,'Sky Blue'),(7,'CornflowerBlue'),(8,'Orchid'),(9,'Pink')], 'Stage Color')
    }

class project_task(osv.Model):
    
    _inherit = 'project.task'
    
    def create(self, cr, uid, vals, context=None):
        stage_pool = self.pool.get('project.task.type')
        project_obj = self.pool.get('project.project')
        if vals.get('stage_id', False):
            rec = stage_pool.browse(cr, uid, vals.get('stage_id'), context=context)
            if rec.color:
                vals.update({'color' : rec.color})
                project_obj.write(cr, uid, vals.get('project_id'), {'color':rec.color}, context=context)
        return super(project_task, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        stage_pool = self.pool.get('project.task.type')
        project_obj = self.pool.get('project.project')
        procurement_obj = self.pool.get('procurement.order')
        if context is None:
            context = {}
        if vals.get('stage_id', False):
                for task_rec in self.browse(cr, uid, ids, context=context):
                    rec = stage_pool.browse(cr, uid, vals.get('stage_id'), context=context)
                    if rec.color:
                        vals.update({'color' : rec.color})
                        project_obj.write(cr, uid, [task_rec.project_id.id], {'color':rec.color}, context=context)
        if context.get('default_project_id'):
            project_id = context.get('default_project_id')
            project_data = project_obj.browse(cr, uid, project_id, context=context)
            task_stage_type = stage_pool.search(cr, uid, [('name','=','Installation')],context=context)
            if vals.get('stage_id', False) and vals['stage_id'] in task_stage_type:
                if project_data:
                    if project_data.analytic_account_id:
                        if project_data.analytic_account_id.sale_id:
                            sale_order_data = project_data.analytic_account_id.sale_id
                            procurement_ids = procurement_obj.search(cr, uid, [('origin','=', sale_order_data.name)])
                            procurement_data = procurement_obj.browse(cr, uid, procurement_ids, context=context)
                            for procurement in procurement_data:
                                if procurement.procure_method == "make_to_order":
                                    if procurement.purchase_id:
                                        if procurement.purchase_id.shipped == False:
                                            raise osv.except_osv(_('Stage Restriction'), _('You can not goto Installation stage without before received the products!'))
                                    else:
                                        raise osv.except_osv(_('Stage Restriction'), _('You can not goto Installation stage without before run the procurements!'))
            project_task_data = self.browse(cr, uid, ids,context=context)
            if not vals.get('stage_id', None):
                return super(project_project, self).write(cr, uid, ids, vals, context=context)
            task_type = stage_pool.search(cr, uid, [('name','=','Invoicing')],context=context)
            if vals.get('stage_id', False) and vals['stage_id'] in task_type:
                invoice_obj = self.pool.get('account.invoice.line')
                invoice_ids = invoice_obj.search(cr, uid, [('account_analytic_id', '=', project_task_data[0].project_id.analytic_account_id.id)], context=context)
                if not invoice_ids:
                    raise osv.except_osv(_('Stage Restriction'), _('You can not goto invoicing stage without creating invoice!'))
        return super(project_task, self).write(cr, uid, ids, vals, context=context)

