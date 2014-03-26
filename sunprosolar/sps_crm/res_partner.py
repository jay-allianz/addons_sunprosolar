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
import tools

class res_user(osv.Model):
    
    _inherit = "res.users"
    
#    def login(self, cr, uid, id, login_name, password, context= None):
#        if not context:
#            context = {}
#        res_users_data = self.browse(cr, uid, id, context=context)[0]
#        if res_users_data.login == login_name and res_users_data.password == password:
#            return id
#        else:
#            return False
        
#    def read(self, cr, uid, user_id, context= None):
#        if not context:
#            context = {}
#        print "read called>>>"
#        address = ' '
#        partner_info = {}
#        partner_obj = self.pool.get('res.partner')
#        res_users_data = self.browse(cr, uid, user_id, context=context)[0]
#        partner_id = res_users_data.partner_id.id
#        if partner_id:
#            partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
#            address = str(partner_data.street) + ', ' + str(partner_data.street2) + ', '+ str(partner_data.city_id and partner_data.city_id.name or '') + ', '+str(partner_data.city_id and partner_data.city_id.state_id and partner_data.city_id.state_id.name or '') + ', '+str(partner_data.city_id and partner_data.city_id.country_id and partner_data.city_id.country_id.name or '') + ', '+str(partner_data.city_id and partner_data.city_id.zip or '')
#           
#            partner_info = {'id': partner_data.id,
#                            'name': partner_data.name, 
#                            'middle_name': partner_data.middle_name,
#                            'last_name': partner_data.last_name,
#                            'company': partner_data.parent_id.name,
#                            'address':address,
#                            'email':partner_data.email,
#                            'mobile': partner_data.mobile,
#                            'fax': partner_data.fax,
#                            }
#            return partner_info
#        
    def read_company(self, cr, uid, user_id, context=None):
        if not context:
            context = {}
        address = ' '
        company_info = {}
        partner_obj = self.pool.get('res.partner')
        res_users_data = self.browse(cr, uid, user_id, context=context)[0]
        partner_id = res_users_data.partner_id.id
        if partner_id:
            partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
            res_company_data = partner_data.parent_id
            address = str(res_company_data.street) + ', ' + str(res_company_data.street2) + ', '+ str(res_company_data.city_id and res_company_data.city_id.name or '') + ', '+str(res_company_data.city_id and res_company_data.city_id.state_id and res_company_data.city_id.state_id.name or '') + ', '+str(res_company_data.city_id and res_company_data.city_id.country_id and res_company_data.city_id.country_id.name or '') + ', '+str(res_company_data.city_id and res_company_data.city_id.zip or '')
            company_info = {'id':res_company_data.id,
                            'name': res_company_data.name, 
                            'address':address,
                            'email':res_company_data.email,
                            'mobile': res_company_data.mobile,
                            'fax': res_company_data.fax,
                            'website':res_company_data.website
                            }
        return company_info
    
    def get_all_information(self, cr, uid, user_id, context= None):
        if not context:
            context = {}
        address = ' '
        result = {}
        partner_info = {}
        crm_lead_info = []
        sale_order_info = []
        project_status = ' '
        crm_obj = self.pool.get('crm.lead')
        partner_obj = self.pool.get('res.partner')
        sale_order_obj = self.pool.get('sale.order')
        project_obj = self.pool.get('project.project')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        if res_users_data.partner_id:
            partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
            address = str(res_users_data.partner_id.street) + ', ' + str(res_users_data.partner_id.street2) + ', '+ str(res_users_data.partner_id.city_id and res_users_data.partner_id.city_id.name or '') + ', '+str(res_users_data.partner_id.city_id and res_users_data.partner_id.city_id.state_id and res_users_data.partner_id.city_id.state_id.name or '') + ', '+str(res_users_data.partner_id.city_id and res_users_data.partner_id.city_id.country_id and res_users_data.partner_id.city_id.country_id.name or '') + ', '+str(res_users_data.partner_id.city_id and res_users_data.partner_id.city_id.zip or '')
           
            partner_info = {'partner_id' : res_users_data.partner_id.id,
                            'name': res_users_data.partner_id.name or '', 
                            'middle_name': res_users_data.partner_id.middle_name or '',
                            'last_name': res_users_data.partner_id.last_name or '',
                            'company': res_users_data.partner_id.parent_id.name or '',
                            'address':address or '',
                            'email':res_users_data.partner_id.email or '',
                            'mobile': res_users_data.partner_id.mobile or '',
                            'fax': res_users_data.partner_id.fax or '',
                            }
            crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
            crm_data = crm_obj.browse(cr, uid, crm_ids, context=context)
            for data in crm_data:
                crm_lead_info.append(data.id)
                project_ids = project_obj.search(cr, uid, [('name','=',data.partner_id.name)], context=context)
                if project_ids:
                    project_data = project_obj.browse(cr, uid, project_ids, context=context)
                    project_status = project_data[0].tasks and project_data[0].tasks[0].stage_id.name or 'draft'
                else:
                    sale_order_ids = sale_order_obj.search(cr, uid, [('partner_id','=',data.partner_id.id)],context=context)
                    if sale_order_ids:
                        sale_data = sale_order_obj.browse(cr, uid, sale_order_ids, context=context)
                        project_status = sale_data[0].state
                    else:
                        project_status = data.stage_id and data.stage_id.name or 'draft'
                
            sale_order_ids = sale_order_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
            sale_order_data = sale_order_obj.browse(cr, uid, sale_order_ids, context= context)
            for sale_data in sale_order_data:
                sale_order_info.append(sale_data.id)
                
            result = {'partner_info': partner_info,
                      'lead_info': crm_lead_info and crm_lead_info[0] or False,
                      'sale_info':sale_order_info and sale_order_info[0] or False,
                      'project_status': project_status}
        return result
        
    def upload_review(self, cr, uid, user_id, review, context= None):
        if not context:
            context = {}
        print "review>>>>",review
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        review_obj = self.pool.get('project.reviews')
        new_review_id = False
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        if crm_ids:
            vals = {
                    'crm_lead_id' : crm_ids[0],
                    'name' : review
            }
            new_review_id= review_obj.create(cr, uid, vals, context= context)
#        crm_obj.write(cr, uid, crm_ids[0], {'project_review_ids': [(6,0,[new_review_id])]})
        if new_review_id:
            return new_review_id
        else:
            False
            
    def refer_friends(self, cr, uid, user_id, ref, context= None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        ref_obj = self.pool.get('friend.reference')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        vals = {
               'name' : ref.get('name'),
               'lname' : ref.get('lname'),
               'phone' : ref.get('phone'),
               'email' : ref.get('email'),
               'crm_lead_id' : crm_ids[0]
        }
        new_ref_id= ref_obj.create(cr, uid, vals, context= context)
        crm_obj.write(cr, uid, crm_ids[0], {'friend_refer_ids': [(6,0,[new_ref_id])]})
        if new_ref_id:
            return new_ref_id
        else:
            False
            
    def submit_question(self, cr, uid, user_id, question, context= None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        ref_obj = self.pool.get('friend.reference')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        vals = {
               'name' : question.get('name'),
               'crm_lead_id' : crm_ids[0]
        }
        new_ref_id= ref_obj.create(cr, uid, vals, context= context)
        crm_obj.write(cr, uid, crm_ids[0], {'submit_que_ids': [(6,0,[new_ref_id])]})
        if new_ref_id:
            return new_ref_id
        else:
            False
        
    
    def send_email(self, cr, uid, message, mail_server_id, context):
        '''
           This method sends mail using information given in message 
        '''
        obj_mail_server = self.pool.get('ir.mail_server')
        obj_mail_server.send_email(cr, uid, message=message, mail_server_id=mail_server_id, context=context)
     
    def request_detailed(self, cr, uid, user_id, context= None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        crm_data = crm_obj.browse(cr, uid, crm_ids, context=context)
        
        obj_mail_server = self.pool.get('ir.mail_server')
        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
        if not mail_server_ids:
            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
        email_from = mail_server_record.smtp_user
        email_to = ['administration@sunpro-solar.com']
        if not email_from:
            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
        for data in crm_data:
            subject_line = 'Customer ' + tools.ustr(data.partner_id and data.partner_id.name or '') + '.'
            message_body = 'Hello,<br/><br/>There is a customer requesting a detailed status of their current project..<br/><br/>Customer Information<br/><br/>First Name : ' + tools.ustr(data.contact_name) + '<br/><br/>Last Name : ' + tools.ustr(data.last_name) + '<br/><br/>Address : '+ tools.ustr(data.street) + ', ' + tools.ustr(data.street2) + ', '+ tools.ustr(data.city_id and data.city_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.state_id and data.city_id.state_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.country_id and data.city_id.country_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.zip or '') + '<br/><br/>Email : '+ tools.ustr(data.email_from) + '<br/><br/>Mobile : ' + tools.ustr(data.mobile) + '<br/><br/> Thank You.'
            message_hrmanager = obj_mail_server.build_email(
            email_from=email_from,
            email_to=email_to,
            subject=subject_line,
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
        return True
    
    def query_generated(self, cr, uid, user_id, context= None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        crm_data = crm_obj.browse(cr, uid, crm_ids, context=context)
        
        obj_mail_server = self.pool.get('ir.mail_server')
        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
        if not mail_server_ids:
            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
        email_from = mail_server_record.smtp_user
        email_to = ['engineering@sunpro-solar.com','info@sunpro-solar.com']
        if crm_data[0] and crm_data[0].user_id:
            email_to.append(crm_data[0].user_id.email)
        if not email_from:
            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
        for data in crm_data:
            subject_line = 'Customer ' + tools.ustr(data.partner_id and data.partner_id.name or '') + '.'
            message_body = 'Hello,<br/><br/>There is a customer have issues with the proposed layout and need to be contacted before the job moves forward.<br/><br/>Customer Information<br/><br/>First Name : ' + tools.ustr(data.contact_name) + '<br/><br/>Last Name : ' + tools.ustr(data.last_name) + '<br/><br/>Address : '+ tools.ustr(data.street) + ', ' + tools.ustr(data.street2) + ', '+ tools.ustr(data.city_id and data.city_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.state_id and data.city_id.state_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.country_id and data.city_id.country_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.zip or '') + '<br/><br/>Email : '+ tools.ustr(data.email_from) + '<br/><br/>Mobile : ' + tools.ustr(data.mobile) + '<br/><br/> Thank You.'
            message_hrmanager = obj_mail_server.build_email(
            email_from=email_from,
            email_to=email_to,
            subject=subject_line,
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
        return True

    def request_contact(self, cr, uid, user_id, context= None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        crm_data = crm_obj.browse(cr, uid, crm_ids, context=context)
        
        obj_mail_server = self.pool.get('ir.mail_server')
        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
        if not mail_server_ids:
            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
        email_from = mail_server_record.smtp_user
        email_to = ['info@sunpro-solar.com']
        if not email_from:
            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
        for data in crm_data:
            subject_line = 'Customer ' + tools.ustr(data.partner_id and data.partner_id.name or '') + '.'
            message_body = 'Hello,<br/><br/>There is a customer requesting to contact.<br/><br/>Customer Information<br/><br/>First Name : ' + tools.ustr(data.contact_name) + '<br/><br/>Last Name : ' + tools.ustr(data.last_name) + '<br/><br/>Address : '+ tools.ustr(data.street) + ', ' + tools.ustr(data.street2) + ', '+ tools.ustr(data.city_id and data.city_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.state_id and data.city_id.state_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.country_id and data.city_id.country_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.zip or '') + '<br/><br/>Email : '+ tools.ustr(data.email_from) + '<br/><br/>Mobile : ' + tools.ustr(data.mobile) + '<br/><br/> Thank You.'
            message_hrmanager = obj_mail_server.build_email(
            email_from=email_from,
            email_to=email_to,
            subject=subject_line,
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
        return True
    
    