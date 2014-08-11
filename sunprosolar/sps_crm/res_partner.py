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
                            'name': str(res_users_data.partner_id.name or '') + ' ' + str(res_users_data.partner_id.middle_name or '') + ' ' + str(res_users_data.partner_id.last_name or ''), 
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
        mail_mail = self.pool.get('mail.mail')
        email_template_obj = self.pool.get('email.template')
        crm_obj = self.pool.get('crm.lead')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id        
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        if crm_ids:
            crm_object = crm_obj.browse(cr, uid, [max(crm_ids)], context=context)
            if crm_object[0].ref:

                data = crm_object[0].ref
                if data.state == 'permit':
                    sale_order_obj.write(cr, uid, crm_object[0].ref.id, {'state': 'city'},context=context)
                    
                    template_id = self.pool.get('ir.model.data').get_object(cr, uid, 'sps_crm', 'customer_accept_plan', context=context)
                    template_values = email_template_obj.generate_email(cr, uid, template_id, user_id, context=context)
                    email_to_list = [res_users_data.company_id and res_users_data.company_id.engineering_email_id or 'engineering@sunpro-solar.com',res_users_data.company_id and res_users_data.company_id.admin_email_id or 'administration@sunpro-solar.com']
                    for email_to in email_to_list:
                        template_values.update({'email_to': email_to})
                        msg_id = mail_mail.create(cr, uid, template_values, context=context)
                        mail_mail.send(cr, uid, [msg_id], context=context)
                return True
        return False
    
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
        crm_data = crm_obj.browse(cr, uid, [max(crm_ids)], context=context)
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
        monitoring_links_list = []
        monitoring_links = {}
        no_of_invertor = 0
        crm_obj = self.pool.get('crm.lead')
        partner_obj = self.pool.get('res.partner')
        sale_order_obj = self.pool.get('sale.order')
        project_obj = self.pool.get('project.project')
        user_obj = self.pool.get('res.users')
        
        res_users_data = self.browse(cr, uid, user_id, context=context)
        auto_email_id = res_users_data.company_id and res_users_data.company_id.auto_email_id or ''
        admin_email_id = res_users_data.company_id and res_users_data.company_id.auto_email_id or ''
        engineering_email_id = res_users_data.company_id and res_users_data.company_id.auto_email_id or ''
        care_maintance = res_users_data.company_id and res_users_data.company_id.care_maintance or ''
        for links in res_users_data.company_id and res_users_data.company_id.monitoring_links:
            monitoring_links_list.append({'name': links.name, 'link': links.link})
        
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
            if crm_ids:
                data = crm_obj.browse(cr, uid, [max(crm_ids)], context=context)[0]
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
                    
                    if solar_data.tilt_degree == 's':
                        faceing='South'
                    elif solar_data.tilt_degree == 'n':
                        faceing='North'
                    elif solar_data.tilt_degree == 'ne':
                        faceing='North-East'
                    elif solar_data.tilt_degree == 'e':
                        faceing='East'
                    elif solar_data.tilt_degree == 'se':
                        faceing='South-East'
                    elif solar_data.tilt_degree == 'sw':
                        faceing='South-West'
                    elif solar_data.tilt_degree == 'w':
                        faceing='West'
                    elif solar_data.tilt_degree == 'nw':
                        faceing='North-West'
                    else:
                        faceing = ''
                    
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

                
                if data.ref:
                    sale_order_info.append(data.ref.id)
                    analytic_account = data.ref.project_id and data.ref.project_id.id
                    if analytic_account:
                        project_ids = project_obj.search(cr, uid, [('analytic_account_id','=',analytic_account)])
                        if project_ids:
                            project_data = project_obj.browse(cr, uid, project_ids, context=context)
                            project_status = project_data[0].tasks and project_data[0].tasks[0].stage_id.name
                    else:        
                        project_status = 'Waiting Goods'

                    sale_data = data.ref
                    if project_status == 'Waiting Goods':
                        if sale_data.shipped:
                            project_status = 'delivered'
                        elif sale_data.procurement_ids:
                            for procurements in sale_data.procurement_ids:
                                if procurements.state in ['confirmed','running','done']:
                                    project_status = 'material_ordered'
                                    break
                        else:
                            project_status = sale_data.state
                        
                        if project_status == 'progress':
                            project_status = 'permit_pack'
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
                        'average_sun_hour':data.site_avg_sun_hour,
                        'annual_production':data.annual_solar_prod_display,
                        'zip':res_users_data.partner_id.city_id and res_users_data.partner_id.city_id.zip or '',
                        'monitoring_links':monitoring_links_list
                        }
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
        mail_mail = self.pool.get('mail.mail')
        email_template_obj = self.pool.get('email.template')
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        crm_data = crm_obj.browse(cr, uid, [max(crm_ids)], context=context)
        
#        if res_users_data.partner_id:
#            partner_obj.write(cr, uid, partner_id, {'name': name, 'middle_name': middle_name, 'last_name': last_name, 'street': street, 'street2':street2, 'city_id': city_id, 'email':email, 'mobile': mobile, 'phone': phone, 'fax':fax},context=context)
#        for data in crm_data:
#            if data.type == 'lead':
#                crm_obj.write(cr, uid, crm_ids, {'contact_name': name, 'last_name': last_name, 'street': street, 'street2':street2, 'city_id': city_id, 'email':email, 'mobile': mobile, 'phone': phone, 'fax':fax},context=context)
#            if data.type == 'opportunity':
#                crm_obj.write(cr, uid, crm_ids, { 'contact_name': name,'street': street, 'street2':street2, 'city_id': city_id, 'email_from':email, 'mobile': mobile, 'phone': phone, 'fax':fax},context=context)
                
        template_id = self.pool.get('ir.model.data').get_object(cr, uid, 'sps_crm', 'customer_information', context=context)
        template_values = email_template_obj.generate_email(cr, uid, template_id, user_id, context=context)
        template_values.update({'email_to': res_users_data.company_id and res_users_data.company_id.info_email_id or 'info@sunpro-solar.com'})
        msg_id = mail_mail.create(cr, uid, template_values, context=context)
        mail_mail.send(cr, uid, [msg_id], context=context)
        
        
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
        if crm_ids:
            data = crm_obj.browse(cr, uid, [max(crm_ids)], context=context)[0]
            for doc_data in data.attachment_ids:
                if doc_data.visible_user == True:
                    documents.append({
                                 'file_name' : doc_data.name or '',
                                 'doc_file' : doc_data.datas or ''
                    })
            if data.ref:
                for attachment in data.ref.attachment_ids:
                    documents.append({
                                 'file_name' : attachment.name or '',
                                 'doc_file' : attachment.datas or ''
                    })
        
        return documents
    
    def get_event(self, cr, uid, user_id, context=None):
        if not context:
            context = {}
        event_dict = {}
        event_list=[]
        sale_order_obj = self.pool.get('sale.order')
        crm_obj = self.pool.get('crm.lead')
        
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        if crm_ids:
            data = crm_obj.browse(cr, uid, [max(crm_ids)], context=context)[0]
            if data.ref:
                sale_data = data.ref
                for event in sale_data.event_ids:
                    event_dict = {'id': event.id,'name': event.name, 'start_date': event.date, 'end_date':event.date_deadline, 'status': event.state, 'event_time': event.event_time}
                    event_list.append(event_dict)
                return event_list
        else:
            return event_list
        
    def add_event(self, cr, uid, user_id, event_name, start_date, end_date, status, event_time, context=None):
        if not context:
            context = {}
        sale_order_obj = self.pool.get('sale.order')
        calender_obj = self.pool.get('calendar.event')
        crm_obj = self.pool.get('crm.lead')
        
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        if crm_ids:
            data = crm_obj.browse(cr, uid, [max(crm_ids)], context=context)[0]
            if data.ref:
                vals = {'name': event_name, 'date': start_date,'date_deadline': end_date, 'state': status, 'event_time': event_time, 'sale_order_id': data.ref.id}
                new_calender_id = calender_obj.create(cr, uid, vals, context=context)
                if new_calender_id:
                    return new_calender_id
                else:
                    return False
        else:
            return False
    
    def deleteevent(self, cr, uid, user_id, event_id, context=None):
        if not context:
            context = {}
        calender_obj = self.pool.get('calendar.event')
        if event_id:
            calender_obj.unlink(cr, uid, event_id, context=context)
        return True

    def editevent(self, cr, uid, user_id, event_id, event_name, start_date, end_date, state, event_time, context=None):
        if not context:
            context = {}
        calender_obj = self.pool.get('calendar.event')
        if event_id:
            calender_obj.write(cr, uid, event_id, {'name' : event_name, 'date' : start_date, 'date_deadline': end_date, 'event_time': event_time,'state' : state }, context=context)
        return True
        

    def get_care_maintenance(self, cr, uid, user_id, context=None):
        if not context:
            context = {}
        res_users_data = self.browse(cr, uid, user_id, context=context)
        return {'file_name': res_users_data.company_id.care_maintance_fname,'care_maintance': res_users_data.company_id.care_maintance or False} 
    
    def upload_document(self, cr, uid, user_id, doc_name, doc_file, file_name='test.pdf', context=None):
        if not context:
            context = {}
        
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        attachement_obj = self.pool.get('ir.attachment')
        new_attachment_id = False
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        if crm_ids:
            data = crm_obj.browse(cr, uid, [max(crm_ids)], context=context)[0]
    
            vals_attachment = {
                        'name': file_name,
                        'description':doc_name,
                        'datas':doc_file,
                        'res_model':'crm.lead',
                        'res_id':data.id,
                        'visible_user':True
                }
            new_attachment_id = attachement_obj.create(cr, uid, vals_attachment, context=context)
            crm_obj.write(cr, uid, data.id, {'attachment_ids':[(4, new_attachment_id)]})
            if new_attachment_id:
                return new_attachment_id
            else:
                return False
        else:
            return False
    
    def get_project_photo(self, cr, uid, user_id, context = None):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        crm_obj = self.pool.get('crm.lead')
        project_photos = []
        res_users_data = self.browse(cr, uid, user_id, context=context)
        partner_id = res_users_data.partner_id.id
        crm_ids = crm_obj.search(cr, uid, [('partner_id','=', partner_id)],context=context)
        crm_data = crm_obj.browse(cr, uid, [max(crm_ids)], context=context)
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
                    'crm_lead_id' : max(crm_ids),
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
                    'crm_lead_id' : max(crm_ids),
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
                   'crm_lead_id' : max(crm_ids)
            }
            new_ref_id= ref_obj.create(cr, uid, vals, context= context)
            
        crm_vals ={
            'name': 'Lead for ' + name + ' ' + lname,
            'contact_name' : name,
            'last_name' : lname,
            'email_from' : email,
            'phone' : phone,
            'referred_by' : partner_id
        }
        crm_obj.create(cr, uid, crm_vals, context=context)
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
                   'crm_lead_id' : max(crm_ids)
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
    