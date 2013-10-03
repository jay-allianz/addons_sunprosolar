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

class sale_order(osv.osv):

    _inherit="sale.order"
    
    _columns = {
          'contract_id' : fields.many2one('account.analytic.account','Contract'),
#          'contract_id' : fields.one2many('account.analytic.account','sale_child','Contract'),
          'state': fields.selection([
                ('draft', 'Draft Quotation'),
                ('sent', 'Quotation Sent'),
                ('contract_generated','Contract Generated'),
                ('contract_signed','Contract Signed'),
                ('manual', 'Sale to Invoice'),
                ('site_inspection','Site Inspection'),
                ('progress', 'Sales Order'),
                ], 'Status', readonly=True, track_visibility='onchange',
                help="Gives the status of the quotation or sales order. \nThe exception status is automatically set when a cancel operation occurs in the processing of a document linked to the sales order. \nThe 'Waiting Schedule' status is set when the invoice is confirmed but waiting for the scheduler to run on the order date.", select=True),
         'engineering': fields.selection([('yes','Yes'),('no','No')],'Engineering May be structural or Electrical'),
         'confirm_original': fields.selection([('no_changes','No changes'),('change','Changes Made')],'Confirmation of original Design'),


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
        self.write(cr, uid, ids, {'state': 'contract_generated'})
        return True
    
    def contract_sign(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'contract_signed'})
        return True
    
    def change_sent_customer(self, cr, uid, ids, context=None):
        print "context=========",context
        contract_obj=self.pool.get('account.analytic.account')
        
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
        member_email_list=[]
        for data in self.browse(cr, uid, ids):
            if not data.contract_id.members:
                raise osv.except_osv(_('Warning'), _('There is no project team member define in contract !'))
            else:
                for member in data.contract_id.members:
                    if not member.email:
                        raise osv.except_osv(_('Warning'), _('%s team member have no email defined !' % member.name))
                    else:
                        member_email_list.append(member.email)
            
            message_body = 'Hello,<br/><br/>New site inspection needs to be done.<br/><br/>Contract Information<br/><br/>Contract ID : ' + tools.ustr(data.contract_id.contract_id) + '<br/><br/>Contract Amount : ' + tools.ustr(data.contract_id.amount) + '<br/><br/>Deposite Amount : ' + tools.ustr(data.contract_id.deposit) + '<br/><br/> Thank You.'
        message_hrmanager  = obj_mail_server.build_email(
            email_from=email_from, 
            email_to=member_email_list, 
            subject='New site inspection needs to be done', 
            body=message_body, 
            body_alternative=message_body, 
            email_cc=None, 
            email_bcc=None, 
            attachments=None, 
            references = None, 
            object_id=None, 
            subtype='html', 
            subtype_alternative=None, 
            headers=None)
        self.send_email(cr, uid, message_hrmanager, mail_server_id=mail_server_ids[0], context=context)
        self.write(cr, uid, ids, {'state': 'site_inspection'})
        return True
    
       
    
sale_order()

class account_analytic_account(osv.osv):
    
    _inherit="account.analytic.account"
    
    _columns = {
            'contract_id':fields.char('Contract ID'),
            'sale_id': fields.many2one('sale.order','Sale Order'),
            'contract_date': fields.date('Contract Date'),
            'type_of_finance': fields.many2one('account.account.type','Type of Financing '),
            'amount': fields.float('Contract Amount'),
            'deposit' :fields. float('Deposit Collected'),
            'planet': fields.selection([('lease','Lease'),('ppa','PPA')], 'Plant'),
            'power': fields.selection([('sun_power','Sun Power'),('cpf','CPF')], 'Plant'),
#            'equipment_ids': fields.one2many('equipment.line','equipment_id','Equipments'),
#            'product_ids' : fields.many2many('product.product', 'product_account_rel', 'product_id','prod_id','Products'),
            'members': fields.many2many('res.users', 'project_user_relation', 'project_id', 'uid', 'Project Members'),
        }
    
account_analytic_account()

