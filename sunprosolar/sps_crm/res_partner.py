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
import pytz
from dateutil import tz
import datetime

from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


def _offset_format_timestamp1(src_tstamp_str, src_format, dst_format, ignore_unparsable_time=True, context=None):
    """
    Convert a source timestamp string into a destination timestamp string, attempting to apply the
    correct offset if both the server and local timezone are recognized, or no
    offset at all if they aren't or if tz_offset is false (i.e. assuming they are both in the same TZ).

    @param src_tstamp_str: the str value containing the timestamp.
    @param src_format: the format to use when parsing the local timestamp.
    @param dst_format: the format to use when formatting the resulting timestamp.
    @param server_to_client: specify timezone offset direction (server=src and client=dest if True, or client=src and server=dest if False)
    @param ignore_unparsable_time: if True, return False if src_tstamp_str cannot be parsed
                                   using src_format or formatted using dst_format.

    @return: destination formatted timestamp, expressed in the destination timezone if possible
            and if tz_offset is true, or src_tstamp_str if timezone offset could not be determined.
    """
    if not src_tstamp_str:
        return False

    res = src_tstamp_str
    if src_format and dst_format:
        try:
            # dt_value needs to be a datetime.datetime object (so no time.struct_time or mx.DateTime.DateTime here!)
            dt_value = datetime.datetime.strptime(src_tstamp_str,src_format)
            if context.get('tz',False):
                try:
                    import pytz
                    src_tz = pytz.timezone(context['tz'])
                    dst_tz = pytz.timezone('UTC')
                    src_dt = src_tz.localize(dt_value, is_dst=True)
                    dt_value = src_dt.astimezone(dst_tz)
                except Exception,e:
                    pass
            res = dt_value.strftime(dst_format)
        except Exception,e:
            # Normal ways to end up here are if strptime or strftime failed
            if not ignore_unparsable_time:
                return False
            pass
    return res

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
                    event_dict = {'id': event.id,'name': event.name, 'start_date': event.date, 'end_date':event.date_deadline, 'status': event.status, 'event_time': event.event_time}
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
            if res_users_data.tz:
                to_zone = tz.gettz(res_users_data.tz)
            else:
                to_zone = tz.gettz('UTC')
            print "to_zone>>>>",to_zone
            final_start_date = _offset_format_timestamp1(start_date, '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M', ignore_unparsable_time=True, context={'tz':to_zone}):
            final_end_date = _offset_format_timestamp1(start_date, '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M', ignore_unparsable_time=True, context={'tz':to_zone}):    
#            utc = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M').replace(tzinfo=pytz.timezone(to_zone))
#            utc1 = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M').replace(tzinfo=pytz.timezone(to_zone))
#            
#                s_date = utc.astimezone('UTC')
#                e_date = utc1.astimezone('UTC')
#                
#                    final_start_date = datetime.datetime.strptime(s_date_temp[0], '%Y-%m-%d %H:%M')-datetime.timedelta(hours=int(h_m[0])*2)-datetime.timedelta(minutes=int(h_m[1])*2)
#                    
#                    e_date_temp = str(e_date).rsplit('+')
#                    h_m1 = str(e_date_temp[1]).rsplit(':')
#                    final_end_date = datetime.datetime.strptime(e_date_temp[0], '%Y-%m-%d %H:%M')-datetime.timedelta(hours=int(h_m1[0])*2)-datetime.timedelta(minutes=int(h_m1[1])*2)
#                else:
#                    date_s = datetime.datetime.strftime(s_date, '%Y-%m-%d %H:%M')
#                    s_date_temp = str(s_date).rsplit('-')
#                    temp_tz = s_date_temp[3]
#                    h_m = str(temp_tz).rsplit(':')
#                    final_start_date = datetime.datetime.strptime(date_s, '%Y-%m-%d %H:%M')+datetime.timedelta(hours=int(h_m[0]))+datetime.timedelta(minutes=int(h_m[1]))
#                    
#                    date_e = datetime.datetime.strftime(e_date, '%Y-%m-%d %H:%M')
#                    e_date_temp = str(e_date).rsplit('-')
#                    temp_tz_e_date = e_date_temp[3]
#                    h_m1 = str(temp_tz_e_date).rsplit(':')
#                    final_end_date = datetime.datetime.strptime(date_e, '%Y-%m-%d %H:%M')+datetime.timedelta(hours=int(h_m1[0]))+datetime.timedelta(minutes=int(h_m1[1]))
            
            data = crm_obj.browse(cr, uid, [max(crm_ids)], context=context)[0]
            if data.ref:
                vals = {'name': event_name, 'date': final_start_date,'date_deadline': final_end_date, 'status': status, 'event_time': event_time, 'sale_order_id': data.ref.id}
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
        res_users_data = self.browse(cr, uid, user_id, context=context)
        if event_id:
            utc = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M').replace(tzinfo=pytz.timezone('UTC'))
            utc1 = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M').replace(tzinfo=pytz.timezone('UTC'))
            if res_users_data.tz:
                to_zone = tz.gettz(res_users_data.tz)
                s_date = utc.astimezone(to_zone)
                e_date = utc1.astimezone(to_zone)
                if str(s_date).find('+') != -1:
                    s_date_temp = str(s_date).rsplit('+')
                    h_m = str(s_date_temp[1]).rsplit(':')
                    final_start_date = datetime.datetime.strptime(s_date_temp[0], '%Y-%m-%d %H:%M')-datetime.timedelta(hours=int(h_m[0])*2)-datetime.timedelta(minutes=int(h_m[1])*2)
                    
                    e_date_temp = str(e_date).rsplit('+')
                    h_m1 = str(e_date_temp[1]).rsplit(':')
                    final_end_date = datetime.datetime.strptime(e_date_temp[0], '%Y-%m-%d %H:%M')-datetime.timedelta(hours=int(h_m1[0])*2)-datetime.timedelta(minutes=int(h_m1[1])*2)
                else:
                    date_s = datetime.datetime.strftime(s_date, '%Y-%m-%d %H:%M')
                    s_date_temp = str(s_date).rsplit('-')
                    temp_tz = s_date_temp[3]
                    h_m = str(temp_tz).rsplit(':')
                    final_start_date = datetime.datetime.strptime(date_s, '%Y-%m-%d %H:%M')+datetime.timedelta(hours=int(h_m[0]))+datetime.timedelta(minutes=int(h_m[1]))
                    
                    date_e = datetime.datetime.strftime(e_date, '%Y-%m-%d %H:%M')
                    e_date_temp = str(e_date).rsplit('-')
                    temp_tz_e_date = e_date_temp[3]
                    h_m1 = str(temp_tz_e_date).rsplit(':')
                    final_end_date = datetime.datetime.strptime(date_e, '%Y-%m-%d %H:%M')+datetime.timedelta(hours=int(h_m1[0]))+datetime.timedelta(minutes=int(h_m1[1]))
            calender_obj.write(cr, uid, event_id, {'name' : event_name, 'date' : final_start_date, 'date_deadline': final_end_date, 'event_time': event_time,'status' : state }, context=context)
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
    