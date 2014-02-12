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

class sale_order(osv.Model):

    _inherit = "sale.order"
    
    _columns = {
          'contract_id' : fields.many2one('account.analytic.account', 'Contract'),
          'color': fields.integer('Color Index'),
          'company_currency': fields.related('company_id', 'currency_id', type='many2one', string='Currency', readonly=True, relation="res.currency"),
          'planned_revenue': fields.float('Expected Revenue', track_visibility='always'),
#          'contract_id' : fields.one2many('account.analytic.account','sale_child','Contract'),
          'state': fields.selection([
                ('draft', 'Draft Quotation'),
                ('sent', 'Quotation Sent'),
                ('contract_generated', 'Contract Generated'),
                ('contract_signed', 'Contract Signed'),
                ('manual', 'Sale to Invoice'),
                ('financing_type','Financing Type'),
                ('site_inspection', 'Site Inspection'),
                ('progress', 'Sales Order'),
                ('cancel', 'Cancelled'),
                ], 'Status', readonly=True, track_visibility='onchange',
                help="Gives the status of the quotation or sales order. \nThe exception status is automatically set when a cancel operation occurs in the processing of a document linked to the sales order. \nThe 'Waiting Schedule' status is set when the invoice is confirmed but waiting for the scheduler to run on the order date.", select=True),
         'engineering': fields.selection([('yes', 'Yes'), ('no', 'No')], 'Engineering May be structural or Electrical'),
         'confirm_original': fields.selection([('no_changes', 'No changes'), ('change', 'Changes Made')], 'Confirmation of original Design'),
         'contract_signing_date' : fields.datetime('Contract Signing Date'),
         'inspection_done_date' : fields.datetime('Inspection Done Date'),
         'insp_after_72_hour' : fields.boolean('Inspection After 72 Hours '),
    }
    
    _defaults = {
            'engineering': 'yes',
            
    }
    
    def send_email(self, cr, uid, message, mail_server_id, context):
        '''
           This method sends mail using information given in message 
        '''
        obj_mail_server = self.pool.get('ir.mail_server')
        obj_mail_server.send_email(cr, uid, message=message, mail_server_id=mail_server_id, context=context)

    def contract_generate(self, cr, uid, ids, context=None):
        ana_acc_obj = self.pool.get('account.analytic.account')
        task_obj = self.pool.get('project.task')
        project_obj = self.pool.get('project.project')
        cur_rec = self.browse(cr, uid, ids, context=context)[0]
        if not cur_rec.order_line:
            raise osv.except_osv(_('Error'), _('To generate contract you have to define order line!'))
        vals = {
            'name' : cur_rec.partner_id.name,
            'partner_id' : cur_rec.partner_id.id,
            'use_tasks' : True,
        }
        context['creation_from_sps'] = True
        proj_acc_analy_id = ana_acc_obj.create(cr, uid, vals, context=context)
        project_id = project_obj.search(cr, uid, [('analytic_account_id','=',proj_acc_analy_id)], context=context)[0]
        task_vals = {
            'name' : cur_rec.partner_id.name,
            'project_id':project_id,
        }
        self.write(cr, uid, ids, {'state': 'contract_generated','project_id': proj_acc_analy_id})
        return True
    
    def contract_sign(self, cr, uid, ids, context=None):
        cur_time = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        self.write(cr, uid, ids, {'state': 'contract_signed', 'contract_signing_date':cur_time})
        proj_id = self.browse(cr, uid, ids, context=context)[0].project_id.id
        ana_acc_obj = self.pool.get('account.analytic.account')
        ana_acc_obj.write(cr, uid, [proj_id], {'contract_date' : cur_time})
        return True
    
    def document_collected(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'financing_type'})
        return True
    
    def done_inspection(self, cr, uid, ids, context=None):
        cur_time = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        cur_rec = self.browse(cr, uid, ids, context=context)[0]
        done_within_72 = False
        if cur_rec:
            cont_should_sign_date = datetime.now()-timedelta(days=3)
            cont_actual_sign_date = datetime.strptime(cur_rec.contract_signing_date, DEFAULT_SERVER_DATETIME_FORMAT)
            if cont_actual_sign_date < cont_should_sign_date :
                done_within_72 = True
        self.write(cr, uid, ids, {'inspection_done_date':cur_time,'insp_after_72_hour' : done_within_72})
        return True
    
    def is_inspection_done_in_72_hours(self, cr, uid, automatic=False, use_new_cursor=False, context=None):
        cur_time = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        sale_order_ids = self.search(cr, uid, [('contract_signing_date','!=',False),('insp_after_72_hour','=',False),('inspection_done_date','=',False)], context=context)
        for sale_order in self.browse(cr, uid, sale_order_ids, context=context):
            cont_actual_sign_date = datetime.strptime(sale_order.contract_signing_date, DEFAULT_SERVER_DATETIME_FORMAT)
            cont_should_sign_date = datetime.now()-timedelta(days=3)
            done_within_72 = False
            if cont_actual_sign_date < cont_should_sign_date :
                done_within_72 = True
            self.write(cr, uid, [sale_order.id], {'insp_after_72_hour' : done_within_72}, context=context)
        return True
    
    def change_sent_customer(self, cr, uid, ids, context=None):
        contract_obj = self.pool.get('account.analytic.account')
        
#            schedule_mail_object = self.pool.get('mail.message')
#            data_obj = self.pool.get('ir.model.data')
#            group_object = self.pool.get('res.groups')
#            obj_mail_server = self.pool.get('ir.mail_server')
#            mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
#            if not mail_server_ids:
#                raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
#            mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
#            email_from = mail_server_record.smtp_user
#            if not email_from:
#                raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
#            member_email_list=[]
#            for data in self.browse(cr, uid, ids):
#                if not data.contract_id.members:
#                    raise osv.except_osv(_('Warning'), _('There is no project team member define in contract !'))
#                else:
#                    for member in data.contract_id.members:
#                        if not member.email:
#                            raise osv.except_osv(_('Warning'), _('%s team member have no email defined !' % member.name))
#                        else:
#                            member_email_list.append(member.email)
#                
#                message_body = 'Hello,<br/><br/>New site inspection needs to be done.<br/><br/>Contract Information<br/><br/>Contract ID : ' + tools.ustr(data.contract_id.contract_id) + '<br/><br/>Contract Amount : ' + tools.ustr(data.contract_id.amount) + '<br/><br/>Deposite Amount : ' + tools.ustr(data.contract_id.deposit) + '<br/><br/> Thank You.'
#            message_hrmanager  = obj_mail_server.build_email(
#                email_from=email_from, 
#                email_to=member_email_list, 
#                subject='New site inspection needs to be done', 
#                body=message_body, 
#                body_alternative=message_body, 
#                email_cc=None, 
#                email_bcc=None, 
#                attachments=None, 
#                references = None, 
#                object_id=None, 
#                subtype='html', 
#                subtype_alternative=None, 
#                headers=None)
#            self.send_email(cr, uid, message_hrmanager, mail_server_id=mail_server_ids[0], context=context)
        return True
    
    def site_inspection_mail(self, cr, uid, ids, context=None):
        schedule_mail_object = self.pool.get('mail.message')
        data_obj = self.pool.get('ir.model.data')
        group_object = self.pool.get('res.groups')
        obj_mail_server = self.pool.get('ir.mail_server')
        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
        if not mail_server_ids:
            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
        email_from = mail_server_record.smtp_user
        if not email_from:
            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
        member_email_list = []
        for data in self.browse(cr, uid, ids):
            if not data.project_id.members:
                raise osv.except_osv(_('Warning'), _('There is no project team member define in contract !'))
            else:
                for member in data.project_id.members:
                    if not member.email:
                        raise osv.except_osv(_('Warning'), _('%s team member have no email defined !' % member.name))
                    else:
                        member_email_list.append(member.email)
            
            message_body = 'Hello,<br/><br/>New site inspection needs to be done.<br/><br/>Contract Information<br/><br/>Contract ID : ' + tools.ustr(data.project_id.contract_id) + '<br/><br/>Contract Amount : ' + tools.ustr(data.project_id.amount) + '<br/><br/>Deposite Amount : ' + tools.ustr(data.project_id.deposit) + '<br/><br/> Thank You.'
        message_hrmanager = obj_mail_server.build_email(
            email_from=email_from,
            email_to=member_email_list,
            subject='New site inspection needs to be done',
            body=message_body,
            body_alternative=message_body,
            email_cc=None,
            email_bcc=None,
            attachments=None,
            references=None,
            object_id=None,
            subtype='html',
            subtype_alternative=None,
            headers=None)
        self.send_email(cr, uid, message_hrmanager, mail_server_id=mail_server_ids[0], context=context)
        self.write(cr, uid, ids, {'state': 'site_inspection'})
        return True

class account_analytic_account(osv.Model):
    
    _inherit = "account.analytic.account"
    
    _columns = {
            'contract_id':fields.char('Contract ID'),
            'sale_id': fields.many2one('sale.order', 'Sale Order'),
            'contract_date': fields.date('Contract Date'),
            'type_of_finance': fields.many2one('account.account.type', 'Type of Financing '),
            'amount': fields.float('Contract Amount'),
            'deposit' :fields. float('Deposit Collected'),
            'planet': fields.selection([('lease', 'Lease'), ('ppa', 'PPA')], 'Plant'),
            'power': fields.selection([('sun_power', 'Sun Power'), ('cpf', 'CPF')], 'Plant'),
            'type': fields.selection([('view','Analytic View'), ('normal','Analytic Account'),('contract','Contract or Project'),('template','Template of Contract'),('opportunity','Opportunity')], 'Type of Account', required=True,
                                 help="If you select the View Type, it means you won\'t allow to create journal entries using that account.\n"\
                                  "The type 'Analytic account' stands for usual accounts that you only want to use in accounting.\n"\
                                  "If you select Contract or Project, it offers you the possibility to manage the validity and the invoicing options for this account.\n"\
                                  "The special type 'Template of Contract' allows you to define a template with default data that you can reuse easily."),
#            'equipment_ids': fields.one2many('equipment.line','equipment_id','Equipments'),
#            'product_ids' : fields.many2many('product.product', 'product_account_rel', 'product_id','prod_id','Products'),
            'members': fields.many2many('res.users', 'project_user_relation', 'project_id', 'uid', 'Project Members'),
        }

class sale_order_line(osv.Model):
    _inherit = 'sale.order.line'
    
    _columns = {
            'no_module': fields.integer('No of Module'),
            'no_inverter':fields.integer('No of Inverter')
        }

    def invoice_line_create(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        create_ids = []
        sales = set()
        vals = {}
        for line in self.browse(cr, uid, ids, context=context):
            order_price = line.order_id.amount_total
            vals = self._prepare_order_line_invoice_line(cr, uid, line, False, context)
        vals.update({
                     'product_id': False,
                     'price_unit' : order_price,
                     'name': 'Sun Pro Solar Products',
                     'quantity': 1,
                     })
        if vals:
            inv_id = self.pool.get('account.invoice.line').create(cr, uid, vals, context=context)
            self.write(cr, uid, [line.id], {'invoice_lines': [(4, inv_id)]}, context=context)
            sales.add(line.order_id.id)
            create_ids.append(inv_id)
    # Trigger workflow events
        wf_service = netsvc.LocalService("workflow")
        for sale_id in sales:
            wf_service.trg_write(uid, 'sale.order', sale_id, cr)
        return create_ids
