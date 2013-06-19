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

class crm_lead(osv.osv):
    """ Model for CRM Lead. """
    _inherit = "crm.lead"
    
    _columns = {

         'acc_no':fields.integer('Account Number'),
         'meter_no': fields.char('Meter Number'),
         'bill_average': fields.float(' Electric Bill Average'),
         'bill_total': fields.float('Electric Bills Total', help="Electric Bills Total 12-24-months depending on utility company"),
         'rate_plan': fields.float('Rate Plan'),
         'home': fields.selection([ ('own','Own Home'),
                                    ('rent', 'Renting')],
                                    string='Home'),
         'quote': fields.boolean('Had a Solar Quote?', help = 'Checked if customer have Solar Quatation of any other Company.'),
         'quote_info': fields.many2one('company.qutation','Quatation Information'),
         'heat_home': fields.many2one('heat.home','Heat Home Technique'),
         'home_sq_foot': fields.float('Home Sq-Footage'),
         'age_house_year': fields.integer('Age of House'),
         'age_house_month': fields.integer('Age of House month'),
         'roof_type': fields.many2one('roof.type','Type of Roof '),
         'tilt': fields.char('Tilt'),
         'azimuth': fields.float('Azimuth'),
         'estimate_shade': fields.float('Estimated Shading'),
        }
    
    def _convert_lead(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        opportunity = self.pool.get('crm.lead')
        res = False
        opportunity_ids = vals.get('lead_ids', [])
        for opportunity_id in opportunity_ids:
            res = opportunity._convert_lead(cr, uid, [opportunity_id], context=context)
        print "===================res===================",res
        return True
    
    def redirect_lead_view(self, cr, uid, lead_id, context=None):
        models_data = self.pool.get('ir.model.data')

        # Get opportunity views
        dummy, form_view = models_data.get_object_reference(cr, uid, 'crm', 'crm_case_form_view_leads')
        dummy, tree_view = models_data.get_object_reference(cr, uid, 'crm', 'crm_case_tree_view_leads')
        return {
            'name': _('Lead'),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'crm.lead',
            'domain': [('type', '=', 'lead')],
            'res_id': int(lead_id),
            'view_id': False,
            'views': [(form_view or False, 'form'),
                      (tree_view or False, 'tree'),
                      (False, 'calendar'), (False, 'graph')],
            'type': 'ir.actions.act_window',
        }
    
    def type_change(self, cr, uid, ids, context=None):
        """
        Convert opportunity to lead.
        """
        if context is None:
            context = {}
        context.update({
            'active_model': 'crm.lead',
            'active_ids': ids,
             
        })
        print "context===================",context
        opportunity = self.pool.get('crm.lead')
        opportunity_ids = context.get('active_ids', [])
#        data = self.browse(cr, uid, ids, context=context)[0]
        self._convert_lead(cr, uid, ids, {'opportunity_ids': opportunity_ids}, context=context)
        print "::::::::::::::opportunity_ids:::::::::::::::::",opportunity_ids
        print "opportunity.redirect_lead_view(cr, uid, opportunity_ids[0], context=context)",opportunity.redirect_lead_view(cr, uid, opportunity_ids[0], context=context)
        return opportunity.redirect_lead_view(cr, uid, opportunity_ids[0], context=context)
        
        
        

    
    def new_mail_send1(self, cr, uid, ids, context=None):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'sps_crm', 'email_template_sales_person_mail')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False 
        if context is None:
            context = {}
        ctx = context.copy()
        ans = [x.user_id for x in self.browse(cr,uid, ids,context=context)]
        print ans
        ctx.update({
            'default_model': 'crm.lead',
            'default_res_id': ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        })
        
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
    
        
        
crm_lead()

class crm_lead2opportunity_partner(osv.osv_memory):
    _inherit = "crm.lead2opportunity.partner"
    
    _columns = {
         'user_id': fields.many2one('res.users', 'Sales Leader to send Email',required=True),
        }
    
#    def new_mail_send1(self, cr, uid, ids, context=None):
#        '''
#        This function opens a window to compose an email, with the edi sale template message loaded by default
#        '''
#        print "+++++++++++new_mail_send called++++++++++++++"
#        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
#        ir_model_data = self.pool.get('ir.model.data')
#        print "-------------ir_model_data-----------------",ir_model_data
#        try:
#            print "================================="
#            template_id = ir_model_data.get_object_reference(cr, uid, 'sps_crm', 'email_template_lead2opportunity_mail')[1]
#            print "==============================template_id================================",template_id
#        except ValueError:
#            template_id = False
#        try:
#            print "!!!!!!!!!!!!!!!!!!!!"
#            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
#            print "!!!!!!!!!compose_form_id!!!!!!!!",compose_form_id
#        except ValueError:
#            compose_form_id = False 
#        if context is None:
#            context = {}
#        ctx = context.copy()
#        print "~~~~~~~~~~~~~~~~~~~~~ctx~~~~~~~~~~~~~~~~~~~~~~~~~~",ctx
#        ans = [x.user_id for x in self.browse(cr,uid, ids,context=context)]
#        print "ids:::::::::::::::::::::::::::::::::",ids
#        print ans
#        ctx.update({
#            'default_model': 'crm.lead2opportunity.partner',
#            'default_res_id': ids[0],
#            'default_use_template': bool(template_id),
#            'default_template_id': template_id,
##            'default_composition_mode': 'comment',
##            'default_partner_ids' : [x.user_id.id for x in self.browse(cr,uid, ids,context=context)]
#        })
#        
#        return {
#            'type': 'ir.actions.act_window',
#            'view_type': 'form',
#            'view_mode': 'form',
#            'res_model': 'mail.compose.message',
#            'views': [(compose_form_id, 'form')],
#            'view_id': compose_form_id,
#            'target': 'new',
#            'context': ctx,
#        }

    
    
    def send_email(self, cr, uid, message, mail_server_id, context):
        '''
           Sends mail using information given in message 
        '''
        obj_mail_server = self.pool.get('ir.mail_server')
        obj_mail_server.send_email(cr, uid, message=message, mail_server_id=mail_server_id, context=context)

#    def new_mail_send(self, cr, uid, ids, context=None):
#        
#        print "action_apply Called.####$$$$$$$$$$$$$$$$$$$$$$$$"
#        
#        obj_mail_server = self.pool.get('ir.mail_server')
#        obj_crm_lead=self.pool.get('crm.lead')
#        data_lead = obj_crm_lead.browse(cr, uid, ids[0], context=context)
#        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
#        
#        if not mail_server_ids:
#            raise osv.except_osv(_('Mail Error'), _('No mail outgoing mail server specified!'))
#        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids[0])
#        
#        data = self.browse(cr, uid, ids[0], context=context)
#        print "data--------------",data
#        user_id = data.user_id.email
#        work_email = []
#        new_lead = []
#        
#        work_email.append(str(user_id))
#        print "work_email=======",work_email
#        
##        new_lead += '<tr><td width="100%%">' + data_lead.name + '</td></tr><tr><td width="100%%">' + data_lead.partner_id + '</td></tr><tr><td width="5%%">' + data_lead.street + '</td><td width="5%%">' + data_lead.street2 + '</td><td width="5%%">' + data_lead.city + '</td><td width="5%%">' + data_lead.state_id + '</td><td width="5%%">' + data_lead.zip + '</td><td width="20%%">' + data_lead.country_id +'</td><td width="20%%">' + data_lead.acc_no +'</td><td width="5%%">' + data_lead.meter_no +'</td></tr>'
#        start_mail = """Hi,<br/><br/>These is new Lead to process.<br/><br/>
#        <table>
#         <tr><td width="25%%"> Lead Description </td><td width="20%%">Customer</td><td width="5%%">Address</td><td width="5%%"></td><td width="5%%">City</td><td width="5%%">State</td><td width="5%%">Zip Code</td><td width="5%%">Country</td><td width="5%%">Electricity Account No.</td><td width="5%%">Electricity Meter No.</td>"""
#        final_saleperson_mail_body = start_mail  + "</table><br/><br/>Thank You.<br/><br/>SunPro Solar Lead Team <b>"+ cr.dbname +"</b>"
#        message_saleperson_mail  = obj_mail_server.build_email(
#            email_from = mail_server_record.smtp_user, 
#            email_to = work_email, 
#            subject = 'Notification : New Lead to process.', 
#            body = final_saleperson_mail_body, 
#            body_alternative=final_saleperson_mail_body, 
#            email_cc = None,
#            email_bcc = None, 
#            attachments = None, 
#            references = None, 
#            object_id = None, 
#            subtype = 'html', 
#            subtype_alternative = None, 
#            headers = None)
#        self.send_email(cr, uid, message_saleperson_mail, mail_server_id=mail_server_ids[0], context=context)
#        return True
        
crm_lead2opportunity_partner()

class company_qutation(osv.osv):
    """ Model for Product. """
    _name = "company.qutation"
    _description= "Other Copany Quatation Information."
    _rec_name="company_name"
    
    _columns = {
        'company_name': fields.many2one('res.company','Company Name'),
        'product_ids' : fields.many2many('product.product', 'product_lead_rel', 'pro_id','lead_id','Equipments',help="Select or create equipments offered by the Company."),
        'quote_amount' : fields.float('Quoted Amount')
        }
company_qutation()

class heat_home(osv.osv):
    """ Model for Heat home. """
    _name = "heat.home"
    _description= "Heat Home technique Information."
    
    _columns = {
        'name': fields.char('Technique Name'),
        'description': fields.text('Description'),
        }
heat_home()

class roof_type(osv.osv):
    """ Model for Heat home. """
    _name = "roof.type"
    _description= "Type of Roof Information."
    
    _columns = {
        'name': fields.char('Technique Name'),
        'description': fields.text('Description'),
        }
roof_type()



     
