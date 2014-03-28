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
    
    def read_company(self, cr, uid, user_id, context=None):
        if not context:
            context = {}
        address = ' '
        company_info = {}
        partner_obj = self.pool.get('res.partner')
        res_users_data = self.browse(cr, uid, user_id, context=context)
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
    
    def get_user_info(self, cr, uid, user_id, context= None):
        if not context:
            context = {}
        address = ' '
        partner_info = {}
        res_users_data = self.browse(cr, uid, user_id, context=context)
        if res_users_data.partner_id:
            partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
            address = str(res_users_data.partner_id.street) + ', ' + str(res_users_data.partner_id.street2) + ', '+ str(res_users_data.partner_id.city_id and res_users_data.partner_id.city_id.name or '') + ', '+str(res_users_data.partner_id.city_id and res_users_data.partner_id.city_id.state_id and res_users_data.partner_id.city_id.state_id.name or '') + ', '+str(res_users_data.partner_id.city_id and res_users_data.partner_id.city_id.country_id and res_users_data.partner_id.city_id.country_id.name or '') + ', '+str(res_users_data.partner_id.city_id and res_users_data.partner_id.city_id.zip or '')
            partner_info = {'partner_id' : res_users_data.partner_id.id,
                            'name': res_users_data.partner_id.name or '', 
                            'middle_name': res_users_data.partner_id.middle_name or '',
                            'last_name': res_users_data.partner_id.last_name or '',
                            'company': res_users_data.partner_id.parent_id.name or '',
                            'street': res_users_data.partner_id.street or '',
                            'street2': res_users_data.partner_id.street2 or '',
                            'city' : res_users_data.partner_id.city_id and res_users_data.partner_id.city_id.id or 1,
                            'phone' : res_users_data.partner_id.phone or '',
                            'email':res_users_data.partner_id.email or '',
                            'mobile': res_users_data.partner_id.mobile or '',
                            'fax': res_users_data.partner_id.fax or '',
                            'login': res_users_data.login or '',
                            
                            }
        return partner_info
    
    def customer_accept_plan(self,cr,uid, user_id, context=None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        sale_order_obj = self.pool.get('sale.order')
        
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        sale_order_ids = sale_order_obj.search(cr, uid, [('partner_id','=',partner_id)],context=context)
        sale_data = sale_order_obj.browse(cr, uid, sale_order_ids, context=context)
        for data in sale_data:
            if data.state == 'permit':
                sale_order_obj.write(cr, uid, sale_order_ids, {'state': 'city'},context=context)
        return True
            
    
    def get_all_information(self, cr, uid, user_id, context= None):
        if not context:
            context = {}
        address = ' '
        result = {}
        partner_info = {}
        crm_lead_info = []
        solar_info = {}
        solar_info_list = []
        sale_order_info = []
        project_status = ' '
        tilt = ' '
        faceing  = ' '
        module_id = None
        module_name = ' '
        no_of_module = 0
        invertor_id = None
        invertor_name = ' '
        no_of_invertor = 0
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
                            'street': res_users_data.partner_id.street or '',
                            'street2': res_users_data.partner_id.street2 or '',
                            'city' : res_users_data.partner_id.city_id and res_users_data.partner_id.city_id.id or 1,
                            'phone' : res_users_data.partner_id.phone or '',
                            'email':res_users_data.partner_id.email or '',
                            'mobile': res_users_data.partner_id.mobile or '',
                            'fax': res_users_data.partner_id.fax or '',
                            'login': res_users_data.login or '',
                            }
            crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
            crm_data = crm_obj.browse(cr, uid, crm_ids, context=context)
            bill_saving=0
            for data in crm_data:
                crm_lead_info.append(data.id)
                for solar_data in data.solar_ids:
                    tilt = solar_data.faceing.tilt or ''
                    faceing  = solar_data.tilt_degree or ''
                    module_id = solar_data.module_product_id and solar_data.module_product_id.id or ''
                    module_name = solar_data.module_product_id and solar_data.module_product_id.name or ''
                    no_of_module = solar_data.num_of_module or ''
                    invertor_id = solar_data.inverter_product_id and solar_data.inverter_product_id.id or ''
                    invertor_name = solar_data.inverter_product_id and solar_data.inverter_product_id.name or ''
                    no_of_invertor = solar_data.num_of_invertor or ''
                    solar_info = {'tilt': tilt, 'faceing': faceing, 'module_id': module_id, 'module_name':module_name, 'no_of_module':no_of_module, 'invertor_id':invertor_id, 'invertor_name':invertor_name,'no_of_invertor':no_of_invertor}
                    solar_info_list.append(solar_info)
                for cost_rebate in data.cost_rebate_ids:
                    bill_saving += cost_rebate.elec_bill_savings
                    
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
            new_info = {'year': data.number_of_years, 'cars_off_roads':data.cars_off_roads, 'tree_planting_equi':data.tree_planting_equi, 'co2_offset_pounds':data.co2_offset_pounds, 'bill_saving':bill_saving}    
            sale_order_ids = sale_order_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
            sale_order_data = sale_order_obj.browse(cr, uid, sale_order_ids, context= context)
            for sale_data in sale_order_data:
                sale_order_info.append(sale_data.id)
                
            result = {'partner_info': partner_info,
                      'lead_info': crm_lead_info and crm_lead_info[0] or False,
                      'sale_info': sale_order_info and sale_order_info[0] or False,
                      'solar_info': solar_info_list,
                      'project_status': project_status,
                      'new_info':new_info,
                      
                      }
        return result
    
    def update_customer_information(self, cr, uid, user_id, name, middle_name, last_name, street, street2, city_id, email, mobile, phone, fax, context = None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        if res_users_data.partner_id:
            partner_obj.write(cr, uid, partner_id, {'name': name, 'middle_name': middle_name, 'last_name': last_name, 'street': street, 'street2':street2, 'city_id': city_id, 'email':email, 'mobile': mobile, 'phone': phone, 'fax':fax},context=context)
        return True
    
    def get_all_document(self, cr, uid, user_id, context = None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')

        documents = []
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        crm_data = crm_obj.browse(cr, uid, crm_ids, context=context)
        for data in crm_data:
            for doc_data in data.doc_req_ids:
                documents.append({
                             'id': doc_data.id,
                             'doc_name' : doc_data.doc_id.name or '',
                             'file_name' : doc_data.document_id.name or '',
                             'doc_file' : doc_data.document_id.datas or ''
                })
        return documents
    
    def upload_document(self, cr, uid, user_id, doc_name, doc_file, context=None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        doc_all_obj = self.pool.get('documents.all')
        doc_obj = self.pool.get('document.required')
        attachement_obj = self.pool.get('ir.attachment')
        new_document_id = False
        doc_all_vals = {
                        'name': doc_name
                        }
        doc_all_new_id = doc_all_obj.create(cr, uid, doc_all_vals, context=context)
        vals_attachment = {
                           'name': doc_name,
                           'datas':doc_file
                           }
        attachemnt_id = attachement_obj.create(cr, uid, vals_attachment, context=context)
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        if doc_all_new_id and attachemnt_id:
            vals = {
                    'crm_lead_id' : crm_ids[0],
                    'doc_id' : doc_all_new_id,
                    'document_id': attachemnt_id,
                    'partner_id': partner_id
            }
            new_document_id= doc_obj.create(cr, uid, vals, context= context)
#            crm_obj.write(cr, uid, crm_ids, {'doc_req_ids': [(6,0,[new_document_id])]})
        if new_document_id:
            return new_document_id
        else:
            False
            
    def get_project_photo(self, cr, uid, user_id, context = None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        project_photos = []
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        crm_data = crm_obj.browse(cr, uid, crm_ids, context=context)
        for data in crm_data:
            for project_photos_data in data.project_photo_ids:
                project_photos.append({
                             'id': project_photos_data.id,
                             'name' : project_photos_data.name,
                             'tagline' : project_photos_data.tag_line,
                             'photo' : project_photos_data.photo
                })
        return project_photos
        
    def upload_project_photo(self ,cr, uid, user_id, project_photo_name, project_photo_tagline, project_photo_file, context=None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        peoject_photo_obj = self.pool.get('project.photos')
        new_peoject_photo_id = False
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        if crm_ids:
            vals = {
                    'crm_lead_id' : crm_ids[0],
                    'name' : project_photo_name,
                    'tag_line': project_photo_tagline,
                    'photo' : project_photo_file,
            }
            new_peoject_photo_id= peoject_photo_obj.create(cr, uid, vals, context= context)
#        crm_obj.write(cr, uid, crm_ids, {'project_photo_ids': [(6,0,[new_peoject_photo_id])]})
        if new_peoject_photo_id:
            return new_peoject_photo_id
        else:
            return False
 
 
    def upload_review(self, cr, uid, user_id, review, context= None):
        if not context:
            context = {}
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
#        crm_obj.write(cr, uid, crm_ids, {'project_review_ids': [(6,0,[new_review_id])]})
        if new_review_id:
            return new_review_id
        else:
            return False
            
    def refer_friends(self, cr, uid, user_id, name, lname, phone, email, context= None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        ref_obj = self.pool.get('friend.reference')
        new_ref_id = False
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        if crm_ids:
            vals = {
                   'name' : name,
                   'lname' : lname,
                   'phone' : phone,
                   'email' : email,
                   'crm_lead_id' : crm_ids[0]
            }
            new_ref_id= ref_obj.create(cr, uid, vals, context= context)
#        crm_obj.write(cr, uid, crm_ids, {'friend_refer_ids': [(6,0,[new_ref_id])]})
        if new_ref_id:
            return new_ref_id
        else:
            return False
            
    def submit_question(self, cr, uid, user_id, question, context= None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        ref_obj = self.pool.get('submit.question')
        new_ref_id = False
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        if crm_ids:
            vals = {
                   'name' : question,
                   'crm_lead_id' : crm_ids[0]
            }
            new_ref_id= ref_obj.create(cr, uid, vals, context= context)
#        crm_obj.write(cr, uid, crm_ids, {'submit_que_ids': [(6,0,[new_ref_id])]})
        if new_ref_id:
            return new_ref_id
        else:
            return False
        
    
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
        email_to = []
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
        email_to = [res_users_data.company_id and res_users_data.company_id.admin_email_id or 'administration@sunpro-solar.com']
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
        email_to = []
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
        email_to.append(res_users_data.company_id and res_users_data.company_id.engineering_email_id or 'engineering@sunpro-solar.com')
        email_to.append(res_users_data.company_id and res_users_data.company_id.info_email_id or 'info@sunpro-solar.com')
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
        email_to = []
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
        email_to = [res_users_data.company_id and res_users_data.company_id.info_email_id or 'info@sunpro-solar.com']
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
    
    