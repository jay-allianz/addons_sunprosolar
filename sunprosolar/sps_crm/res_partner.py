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
import base64

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
    
    def get_user_manual(self, cr, uid, user_id, context=None):
        if not context:
            context = {}
        attachements = {}
        attachment_list = []
        product_attachment = {}
        crm_obj = self.pool.get('crm.lead')
        attachment_obj = self.pool.get('ir.attachment')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        crm_data = crm_obj.browse(cr, uid, crm_ids, context=context)
        for data in crm_data:
            for solar_data in data.solar_ids:
                if solar_data.module_product_id:
                    attachment_ids = attachment_obj.search(cr, uid, [('res_model','=','product.product'),('res_id','=',solar_data.module_product_id.id)],context=context)
                    attachment_data = attachment_obj.browse(cr, uid, attachment_ids, context=context)
                    for module_data in attachment_data:
                        product_attachment = { 'product_name':solar_data.module_product_id.name, 'product_fname':module_data.name, 'product_file': module_data.datas}
                        attachment_list.append(product_attachment)
                if solar_data.inverter_product_id:
                    attachment_ids = attachment_obj.search(cr, uid, [('res_model','=','product.product'),('res_id','=',solar_data.inverter_product_id.id)],context=context)
                    attachment_data = attachment_obj.browse(cr, uid, attachment_ids, context=context)
                    for invertor_data in attachment_data:
                        product_attachment = { 'product_name':solar_data.inverter_product_id.name, 'product_fname':invertor_data.name, 'product_file': invertor_data.datas}
                        attachment_list.append(product_attachment)
        attachements = {'attachments' : attachment_list}
        return attachements
    
    def my_shade_study(self, cr, uid, user_id, context=None):
        if not context:
            context = {}
        partner_doc = {}
        partner_document_list = []
        partner_obj = self.pool.get('res.partner')
        attachment_obj = self.pool.get('ir.attachment')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        attachment_ids = attachment_obj.search(cr, uid, [('res_model','=','res.partner'),('res_id','=',partner_id)],context=context)
        attachment_data = attachment_obj.browse(cr, uid, attachment_ids, context=context)
        for data in attachment_data:
            partner_doc = {'doc_name': data.name, 'doc_file': data.datas}
            partner_document_list.append(partner_doc)
        return partner_document_list
    
    def get_all_information(self, cr, uid, user_id, context= None):
        if not context:
            context = {}
        address = ' '
        result = {}
        new_info = {}
        partner_info = {}
        crm_lead_info = []
        solar_info = {}
        solar_info_list = []
        sale_order_info = []
        intial_photo = ''
        final_photo = ''
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
        user_obj = self.pool.get('res.users')
        
        user_rec = user_obj.browse(cr, uid, uid, context=context)
        auto_email_id = user_rec.company_id and user_rec.company_id.auto_email_id or ''
        admin_email_id = user_rec.company_id and user_rec.company_id.auto_email_id or ''
        engineering_email_id = user_rec.company_id and user_rec.company_id.auto_email_id or ''
        care_maintance = user_rec.company_id and user_rec.company_id.care_maintance or ''
        
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
                            'monitoring_website' : res_users_data.website or ''
                            }
            crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
            if crm_ids:
                data = crm_obj.browse(cr, uid, crm_ids, context=context)[0]
                bill_saving = 0
                if data.intial_photo:
                    intial_photo = data.intial_photo
                else:
#                    iconfile_intial = open(tools.config['addons_path']+"sps_crm/images/intial_photo.jpg", "rb")
#                    icondata_intial = iconfile_intial.read()
                    intial_photo = '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'
                    #base64.b64encode(icondata_intial)
                if data.final_photo:
                    final_photo = data.final_photo
                else:
#                    iconfile_final = open(tools.config['addons_path']+"sps_crm/images/final_photo.jpg", "rb")
#                    icondata_final = iconfile_final.read()
                    final_photo = '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'
                    #base64.b64encode(icondata_final)
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
                new_info = {'miles_not_driven':res_users_data.company_id.avg_yearly_miles*data.number_of_years,
                        'year': data.number_of_years,
                        'cars_off_roads':data.cars_off_roads*data.number_of_years,
                        'tree_planting_equi':data.tree_planting_equi*data.number_of_years,
                        'co2_offset_pounds':data.co2_offset_pounds*data.number_of_years,
                        'bill_saving':bill_saving,
                        'auto_email_id':auto_email_id,
                        'admin_email_id':admin_email_id,
                        'engineering_email_id':engineering_email_id,
                        'care_maintance': care_maintance
                        }    
            sale_order_ids = sale_order_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
            sale_order_data = sale_order_obj.browse(cr, uid, sale_order_ids, context= context)
            for sale_data in sale_order_data:
                sale_order_info.append(sale_data.id)
            result = {'partner_info': partner_info,
                      'lead_info': crm_lead_info and crm_lead_info[0] or False,
                      'initial_photo': intial_photo,
                      'final_photo' : final_photo,
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
        crm_obj = self.pool.get('crm.lead')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        crm_data = crm_obj.browse(cr, uid, crm_ids, context=context)
        
        if res_users_data.partner_id:
            partner_obj.write(cr, uid, partner_id, {'name': name, 'middle_name': middle_name, 'last_name': last_name, 'street': street, 'street2':street2, 'city_id': city_id, 'email':email, 'mobile': mobile, 'phone': phone, 'fax':fax},context=context)
        for data in crm_data:
            if data.type == 'lead':
                crm_obj.write(cr, uid, crm_ids, {'contact_name': name, 'last_name': last_name, 'street': street, 'street2':street2, 'city_id': city_id, 'email':email, 'mobile': mobile, 'phone': phone, 'fax':fax},context=context)
            if data.type == 'opportunity':
                crm_obj.write(cr, uid, crm_ids, { 'contact_name': name,'street': street, 'street2':street2, 'city_id': city_id, 'email_from':email, 'mobile': mobile, 'phone': phone, 'fax':fax},context=context)
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
        mail_mail = self.pool.get('mail.mail')
        email_template_obj = self.pool.get('email.template')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        
        template_id = self.pool.get('ir.model.data').get_object(cr, uid, 'sps_crm', 'request_detailed', context=context)
        template_values = email_template_obj.generate_email(cr, uid, template_id, user_id, context=context)
        template_values.update({'email_to': res_users_data.company_id and res_users_data.company_id.admin_email_id or 'administration@sunpro-solar.com'})
        msg_id = mail_mail.create(cr, uid, template_values, context=context)
        mail_mail.send(cr, uid, [msg_id], context=context)
        return True
    
    def query_generated(self, cr, uid, user_id, context= None):
        if not context:
            context = {}
        mail_mail = self.pool.get('mail.mail')
        email_template_obj = self.pool.get('email.template')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        
        template_id = self.pool.get('ir.model.data').get_object(cr, uid, 'sps_crm', 'query_generated', context=context)
        template_values = email_template_obj.generate_email(cr, uid, template_id, user_id, context=context)
        email_to_list = [res_users_data.company_id and res_users_data.company_id.engineering_email_id or 'engineering@sunpro-solar.com',res_users_data.company_id and res_users_data.company_id.info_email_id or 'info@sunpro-solar.com']
        for email_to in email_to_list:
            template_values.update({'email_to': email_to})
            msg_id = mail_mail.create(cr, uid, template_values, context=context)
            mail_mail.send(cr, uid, [msg_id], context=context)
        return True
    
    def request_contact(self, cr, uid, user_id, context= None):
        if not context:
            context = {}
        mail_mail = self.pool.get('mail.mail')
        email_template_obj = self.pool.get('email.template')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        
        template_id = self.pool.get('ir.model.data').get_object(cr, uid, 'sps_crm', 'request_contact', context=context)
        template_values = email_template_obj.generate_email(cr, uid, template_id, user_id, context=context)
        template_values.update({'email_to': res_users_data.company_id and res_users_data.company_id.info_email_id or 'info@sunpro-solar.com'})
        msg_id = mail_mail.create(cr, uid, template_values, context=context)
        mail_mail.send(cr, uid, [msg_id], context=context)
        return True
    
    #    def request_detailed(self, cr, uid, user_id, context= None):
#        if not context:
#            context = {}
#        partner_obj = self.pool.get('res.partner')
#        crm_obj = self.pool.get('crm.lead')
#        email_to = []
#        res_users_data = self.browse(cr, uid, user_id, context=context)
#        partner_id = res_users_data.partner_id.id
#        partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
#        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
#        crm_data = crm_obj.browse(cr, uid, crm_ids, context=context)
#        
#        obj_mail_server = self.pool.get('ir.mail_server')
#        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
#        if not mail_server_ids:
#            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
#        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
#        email_from = mail_server_record.smtp_user
#        email_to = [res_users_data.company_id and res_users_data.company_id.admin_email_id or 'administration@sunpro-solar.com']
#        if not email_from:
#            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
#        for data in crm_data:
#            subject_line = 'Customer ' + tools.ustr(data.partner_id and data.partner_id.name or '') + '.'
#            message_body = 'Hello,<br/><br/>There is a customer requesting a detailed status of their current project.<br/><br/>Customer Information<br/><br/>First Name : ' + tools.ustr(data.contact_name) + '<br/><br/>Last Name : ' + tools.ustr(data.last_name) + '<br/><br/>Address : '+ tools.ustr(data.street) + ', ' + tools.ustr(data.street2) + ', '+ tools.ustr(data.city_id and data.city_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.state_id and data.city_id.state_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.country_id and data.city_id.country_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.zip or '') + '<br/><br/>Email : '+ tools.ustr(data.email_from) + '<br/><br/>Mobile : ' + tools.ustr(data.mobile) + '<br/><br/> Thank You.'
#            message_hrmanager = obj_mail_server.build_email(
#            email_from=email_from,
#            email_to=email_to,
#            subject=subject_line,
#            body=message_body,
#            body_alternative=message_body,
#            email_cc=None,
#            email_bcc=None,
#            attachments=None,
#            references=None,
#            object_id=None,
#            subtype='html',
#            subtype_alternative=None,
#            headers=None)
#            self.send_email(cr, uid, message_hrmanager, mail_server_id=mail_server_ids[0], context=context)
#        return True
    
#    def query_generated(self, cr, uid, user_id, context= None):
#        if not context:
#            context = {}
#        partner_obj = self.pool.get('res.partner')
#        crm_obj = self.pool.get('crm.lead')
#        email_to = []
#        res_users_data = self.browse(cr, uid, user_id, context=context)
#        partner_id = res_users_data.partner_id.id
#        partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
#        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
#        crm_data = crm_obj.browse(cr, uid, crm_ids, context=context)
#        
#        obj_mail_server = self.pool.get('ir.mail_server')
#        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
#        if not mail_server_ids:
#            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
#        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
#        email_from = mail_server_record.smtp_user
#        email_to.append(res_users_data.company_id and res_users_data.company_id.engineering_email_id or 'engineering@sunpro-solar.com')
#        email_to.append(res_users_data.company_id and res_users_data.company_id.info_email_id or 'info@sunpro-solar.com')
#        if crm_data[0] and crm_data[0].user_id:
#            email_to.append(crm_data[0].user_id.email)
#        if not email_from:
#            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
#        for data in crm_data:
#            subject_line = 'Customer ' + tools.ustr(data.partner_id and data.partner_id.name or '') + '.'
#            message_body = 'Hello,<br/><br/>There is a customer have issues with the proposed layout and need to be contacted before the job moves forward.<br/><br/>Customer Information<br/><br/>First Name : ' + tools.ustr(data.contact_name) + '<br/><br/>Last Name : ' + tools.ustr(data.last_name) + '<br/><br/>Address : '+ tools.ustr(data.street) + ', ' + tools.ustr(data.street2) + ', '+ tools.ustr(data.city_id and data.city_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.state_id and data.city_id.state_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.country_id and data.city_id.country_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.zip or '') + '<br/><br/>Email : '+ tools.ustr(data.email_from) + '<br/><br/>Mobile : ' + tools.ustr(data.mobile) + '<br/><br/> Thank You.'
#            message_hrmanager = obj_mail_server.build_email(
#            email_from=email_from,
#            email_to=email_to,
#            subject=subject_line,
#            body=message_body,
#            body_alternative=message_body,
#            email_cc=None,
#            email_bcc=None,
#            attachments=None,
#            references=None,
#            object_id=None,
#            subtype='html',
#            subtype_alternative=None,
#            headers=None)
#            self.send_email(cr, uid, message_hrmanager, mail_server_id=mail_server_ids[0], context=context)
#        return True

#    def request_contact(self, cr, uid, user_id, context= None):
#        if not context:
#            context = {}
#        partner_obj = self.pool.get('res.partner')
#        crm_obj = self.pool.get('crm.lead')
#        email_to = []
#        res_users_data = self.browse(cr, uid, user_id, context=context)
#        partner_id = res_users_data.partner_id.id
#        partner_data = partner_obj.browse(cr, uid, partner_id, context=context)
#        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
#        crm_data = crm_obj.browse(cr, uid, crm_ids, context=context)
#        
#        obj_mail_server = self.pool.get('ir.mail_server')
#        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
#        if not mail_server_ids:
#            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
#        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
#        email_from = mail_server_record.smtp_user
#        email_to = [res_users_data.company_id and res_users_data.company_id.info_email_id or 'info@sunpro-solar.com']
#        if not email_from:
#            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
#        for data in crm_data:
#            subject_line = 'Customer ' + tools.ustr(data.partner_id and data.partner_id.name or '') + '.'
#            message_body = 'Hello,<br/><br/>There is a customer requesting to contact.<br/><br/>Customer Information<br/><br/>First Name : ' + tools.ustr(data.contact_name) + '<br/><br/>Last Name : ' + tools.ustr(data.last_name) + '<br/><br/>Address : '+ tools.ustr(data.street) + ', ' + tools.ustr(data.street2) + ', '+ tools.ustr(data.city_id and data.city_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.state_id and data.city_id.state_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.country_id and data.city_id.country_id.name or '') + ', '+ tools.ustr(data.city_id and data.city_id.zip or '') + '<br/><br/>Email : '+ tools.ustr(data.email_from) + '<br/><br/>Mobile : ' + tools.ustr(data.mobile) + '<br/><br/> Thank You.'
#            message_hrmanager = obj_mail_server.build_email(
#            email_from=email_from,
#            email_to=email_to,
#            subject=subject_line,
#            body=message_body,
#            body_alternative=message_body,
#            email_cc=None,
#            email_bcc=None,
#            attachments=None,
#            references=None,
#            object_id=None,
#            subtype='html',
#            subtype_alternative=None,
#            headers=None)
#            self.send_email(cr, uid, message_hrmanager, mail_server_id=mail_server_ids[0], context=context)
#        return True
    
    