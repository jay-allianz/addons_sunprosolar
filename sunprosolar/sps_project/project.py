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
from tools.translate import _

class project_project(osv.Model):
    
    _inherit = "project.project"
    
    def _get_state(self, cr, uid, ids, name, args, context=None):
        res = {}
        stage_obj = self.pool.get('project.task')
        for data in self.browse(cr, uid, ids):
            if not data.tasks:
                res[data.id] = False
            else:
                res[data.id] = [x.stage_id.id for x in data.tasks][0]
        return res
    
    def _get_task_stage(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('project.task').browse(cr, uid, ids, context=context):
            result[line.project_id.id] = True
        return result.keys()

    _columns = {
#                'project_task_stage': fields.related('tasks', 'stage_id', type='many2one', store=True,relation='project.task.type', string='Project Task Stage'),
                'project_task_stage': fields.function(_get_state, type='many2one', store={
                    'project.project': (lambda self, cr, uid, ids, c={}: ids, ['tasks'], 20),
                    'project.task': (_get_task_stage, ['stage_id'], 20),
                    },relation='project.task.type', string='Project Task Stage'),
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
        if not vals.get('stage_id', None):
            return super(project_task, self).write(cr, uid, ids, vals, context=context)
            
        task_stage_type = stage_pool.search(cr, uid, [('name','in',['Installation','Installation Complete','Final Inspection','Monitoring','Invoicing','Wrap Up'])],context=context)
        if vals.get('stage_id', False) and vals['stage_id'] in task_stage_type:
            for task in self.browse(cr, uid, ids, context=context):
                if task.project_id:
                    if task.project_id.analytic_account_id:
                        if task.project_id.analytic_account_id.sale_id:
                            sale_order_data = task.project_id.analytic_account_id.sale_id
                            if not sale_order_data.shipped:
                                raise osv.except_osv(_('Stage Restriction'), _('You can not goto Installation stage without delivering the products!'))
            
        
        task_stage_type = stage_pool.search(cr, uid, [('name','in',['Invoicing','Wrap Up'])],context=context)
        if vals.get('stage_id', False) and vals['stage_id'] in task_stage_type:
            for task in self.browse(cr, uid, ids, context=context):
                if task.project_id:
                    if task.project_id.analytic_account_id:
                        if task.project_id.analytic_account_id.sale_id:
                            sale_order_data = task.project_id.analytic_account_id.sale_id
                            if not sale_order_data.invoice_ids:
                                raise osv.except_osv(_('Stage Restriction'), _('You can not goto invoicing stage without creating invoice!'))
        

        if vals.get('stage_id', False):
            for task_rec in self.browse(cr, uid, ids, context=context):
                rec = stage_pool.browse(cr, uid, vals.get('stage_id'), context=context)
                if rec.color:
                    vals.update({'color' : rec.color})
                    project_obj.write(cr, uid, [task_rec.project_id.id], {'color':rec.color}, context=context)
        
        return super(project_task, self).write(cr, uid, ids, vals, context=context)

