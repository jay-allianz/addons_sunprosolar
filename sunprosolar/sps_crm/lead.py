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
    
    def _reponsible_user(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for u in self.browse(cr, uid, ids, context=context):
            partner = self.pool.get('res.users').browse(cr, uid,uid,context=context)
            user = partner.name
            res[u.id] =  user
        return res
    
    _columns = {
         'last_name': fields.char('Last Name', size=32),
         'utility_company': fields.boolean('Utility Company'),
         'acc_no':fields.char('Account Number', size=32),
         'meter_no': fields.char('Meter Number', size=32),
         'bill_average': fields.float(' Electric Bill Average'),
         'bill_month': fields.selection([('12_month', '12 Months'),('24_month','24 Months')], 'Months for Bill Average'),
         'bill_total': fields.float('Electric Bills Total', help="Electric Bills Total 12-24-months depending on utility company"),
         'rate_plan': fields.char('Rate Plan', size=32),
         'home_note': fields.text('Note'),
         'electricity_note': fields.text('Note'),
         'marketing_note': fields.text('Note'),
         'accounting_note': fields.text('Note'),
         'system_note': fields.text('Note'),
         'home': fields.selection([ ('own','Own Home'),
                                    ('rent', 'Renting')],
                                    string='Home'),
         'quote': fields.boolean('Had a Solar Quote?', help = 'Checked if customer have Solar Quotation of any other Company.'),
         'quote_info': fields.many2one('company.quotation','Quotation Information'),
         'heat_home': fields.selection([('natural_gas','Natural Gas'),('propane','Propane'),('all_electric','All Electric')], 'Heat Home Technique'),
#         'heat_home': fields.many2one('heat.home','Heat Home Technique'),
         'home_sq_foot': fields.float('Home Sq-Footage'),
         'age_house_year': fields.integer('Age of House'),
         'age_house_month': fields.integer('Age of House month'),
#         'roof_type': fields.many2one('roof.type','Type of Roof '),
         'roof_type':fields.selection([('s_family', 'Single Family'),('Mobil','Mobil'),('manufactured','Manufactured')], 'Type Of Roof',),
#         'roof_type': fields.char('Type Of Roof', size=32),
         'time_own_year': fields.integer('Owned Home Time',help="How long have you owned your home?"),   
         'time_own_month': fields.integer('Owned home Time month'),
         'pool': fields.boolean('Is Pool?',help="Have a pool or not? Checked if Yes."),
         'spent_money': fields.float('Money spent to Heat Home',help='How much spent to heat home?'),
         'equity': fields.boolean('Equity',help="Do you have equity in your home? Checked if Yes."),
         'tilt': fields.integer('Tilt'),
         'azimuth': fields.integer('Azimuth'),
#         'contract_id' : fields.many2one('account.analytic.account','Contract'),
         'estimate_shade': fields.integer('Estimated Shading'),
         'ahj': fields.selection([('structural', 'Structural'),('electrical','Electrical')], 'AHJ',help="Authority Having Jurisdiction"),
         'utility_bill' : fields.boolean('Utility Bill',help="Checked Utility bill to sign customer contract."),
#         'bill_ids' : fields.one2many('utility.bill','lead_id','Certificate'),
        'lead_source': fields.char('Lead Source', size=32),
        'level_of_lead': fields.many2one('crm.case.stage', 'Level Of Lead'),
        'schedule_appointment': fields.date('Schedule Appointment'),
        'outcome_appointment': fields.date('Outcome of The Appointment'),
#        'marketing_note': fields.text('Notes'),
        'qualified': fields.boolean('Qualification Data?'),
        'annual_income': fields.float('Annual Income'),
        'tax_liability': fields.float('Tax Liability'),
        'credit_source': fields.float('Credit Source'),
        'property_tax': fields.float('Property Tax'),
        'type_of_sale': fields.selection([('cash','Cash'),('sun_power_lease','Sun Power Lease'),('cpf','CPF'),('wells_fargo','Wells Fargo'),('admirals_bank','Admirals Bank'),('hero','Hero'),('others','Others')], 'Type Of Sale'),
        'deadline': fields.date('Deadline'),
        'deposit': fields.float('Deposit'),
        'federal_tax': fields.selection([('yes','Yes'),('no','No')],'Federal Tax Advantage?'),
        'attachment_ids': fields.many2many('ir.attachment', 'email_template_attachment_sps_rel', 'mail_template_id','attach_id', 'Attachments'),
        'type_of_module': fields.char('Type Of Modules', size=36),
        'inverter': fields.char('Inverter', size=32),
        'main_ele_serviece_panel': fields.char('Main Electrical Service Panel information', size=32),
        'see_lead_home_note': fields.boolean('See Lead Home Note'),
        'crm_lead_home_note_ids': fields.one2many('crm.lead.home.description', 'name', 'Notes'),
        'see_lead_electricity_note': fields.boolean('See Lead Electricity Note'),
        'crm_lead_electricity_note_ids': fields.one2many('crm.lead.electricity.description', 'name', 'Notes'),
        'see_lead_marketing_note': fields.boolean('See Lead Marketing Note'),
        'crm_lead_marketing_note_ids': fields.one2many('crm.lead.marketing.description', 'name', 'Notes'),
        'see_lead_accounting_note': fields.boolean('See Lead Accounting Note'),
        'crm_lead_accounting_note_ids': fields.one2many('crm.lead.accounting.description', 'name', 'Notes'),
        'see_lead_system_note': fields.boolean('See Lead System Note'),
        'crm_lead_system_note_ids': fields.one2many('crm.lead.system.description', 'name', 'Notes'),
        'see_lead_all_note': fields.boolean('See Lead All Note'),
        'crm_lead_all_tabs_note_ids': fields.one2many('crm.lead.all.tabs.description', 'name', 'Notes'),
        'responsible_user': fields.function(_reponsible_user,type='char', method=True, string="Responsible User for Appointment", help="Responsible User for Appointment setup"),
        }
    
    _defaults = {
            'name': '/'
    }
    
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
        opportunity = self.pool.get('crm.lead')
        opportunity_ids = context.get('active_ids', [])
        self.write(cr,uid,opportunity_ids,{"type":"lead"})
        return opportunity.redirect_lead_view(cr, uid, opportunity_ids[0], context=context)
        
    def send_email(self, cr, uid, message, mail_server_id, context):
        '''
           This method sends mail using information given in message 
        '''
        obj_mail_server = self.pool.get('ir.mail_server')
        obj_mail_server.send_email(cr, uid, message=message, mail_server_id=mail_server_id, context=context)
    
    def salesteam_send_email(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        schedule_mail_object = self.pool.get('mail.message')
        data_obj = self.pool.get('ir.model.data')
        group_object = self.pool.get('res.groups')
        obj_mail_server = self.pool.get('ir.mail_server')
        crm_case_stage_obj = self.pool.get('crm.case.stage')
        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
        if not mail_server_ids:
            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
        email_from = mail_server_record.smtp_user
        if not email_from:
            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
        email_to=[]
        for data in self.browse(cr, uid, ids, context):
            if not data.section_id.member_ids:
                raise osv.except_osv(_('Warning'), _('There is no sale team member define in section !'))
            else:
                for member in data.section_id.member_ids:
                    if not member.email:
                        raise osv.except_osv(_('Warning'), _('%s team member have no email defined !' % member.name))
                    else:
                        email_to.append(member.email)
            subject_line = 'New Customer ' + tools.ustr(data.partner_id.name) + ' ' + tools.ustr(data.last_name) + ' Comes.'
            message_body = 'Hello,<br/><br/>There is a new customer comes.<br/><br/>Customer Information<br/><br/>First Name : ' + tools.ustr(data.contact_name) + '<br/><br/>Last Name : ' + tools.ustr(data.last_name) + '<br/><br/>Address : ' + tools.ustr(data.street) + ', ' + tools.ustr(data.street2) + ', ' + tools.ustr(data.city) + ', ' + tools.ustr(data.state_id.name) + ', ' + tools.ustr(data.zip) + ', ' + tools.ustr(data.country_id.name) + '<br/><br/>Email : ' + tools.ustr(data.email_from) + '<br/><br/>Mobile : ' + tools.ustr(data.mobile) + '<br/><br/> Thank You.'
        message_hrmanager  = obj_mail_server.build_email(
            email_from=email_from, 
            email_to=email_to, 
            subject=subject_line, 
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
        #schedule_mail_object.schedule_with_attach(cr, uid, email_from, email_to, subject_line, message_body, subtype="html", context=context)
        stage_id = crm_case_stage_obj.search(cr, uid, [('name','=','Sales Notified')])
        self.write(cr, uid, ids, {'stage_id': stage_id[0]})
        return True
    
    def create(self, cr, uid, vals, context=None):
        if not context:
            context = {}
        type_context= context.get('default_type')
        if type_context == 'opportunity':
            crm_case_stage_obj = self.pool.get('crm.case.stage')
            stage_id = crm_case_stage_obj.search(cr, uid, [('name','=','Initial Contact')])
            vals.update({'stage_id': stage_id[0]})
            return super(crm_lead, self).create(cr, uid, vals, context=context)
        
        res = super(crm_lead, self).create(cr, uid, vals, context=context)
        
        if res and vals and vals.get('home_note'):
            self.pool.get('crm.lead.home.description').create(cr, uid, {
                                                                'name': res,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['home_note']
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'name': res,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['home_note']
                                                            })
        if res and vals and vals.get('electricity_note'):
            self.pool.get('crm.lead.electricity.description').create(cr, uid, {
                                                                'name': res,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['electricity_note']
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'name': res,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['electricity_note']
                                                            })
        if res and vals and vals.get('marketing_note'):
            self.pool.get('crm.lead.marketing.description').create(cr, uid, {
                                                                'name': res,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['marketing_note']
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'name': res,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['marketing_note']
                                                            })
        if res and vals and vals.get('accounting_note'):
            self.pool.get('crm.lead.accounting.description').create(cr, uid, {
                                                                'name': res,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['accounting_note']
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'name': res,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['accounting_note']
                                                            })
        if res and vals and vals.get('system_note'):
            self.pool.get('crm.lead.system.description').create(cr, uid, {
                                                                'name': res,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['system_note']
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'name': res,
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals['system_note']
                                                            })
        
        return res

    def write(self, cr, uid, ids, vals, context=None):
        if vals and vals.get('home_note'):
            self.pool.get('crm.lead.home.description').create(cr, uid, {
                                                                'name': ids[0],
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('home_note')
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'name': ids[0],
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('home_note')
                                                            })
        if vals and vals.get('electricity_note'):
            self.pool.get('crm.lead.electricity.description').create(cr, uid, {
                                                                'name': ids[0],
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('electricity_note')
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'name': ids[0],
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('electricity_note')
                                                            })
        if vals and vals.get('marketing_note'):
            self.pool.get('crm.lead.marketing.description').create(cr, uid, {
                                                                'name': ids[0],
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('marketing_note')
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'name': ids[0],
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('marketing_note')
                                                            })
        if vals and vals.get('accounting_note'):
            self.pool.get('crm.lead.accounting.description').create(cr, uid, {
                                                                'name': ids[0],
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('accounting_note')
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'name': ids[0],
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('accounting_note')
                                                            })
        if vals and vals.get('system_note'):
            self.pool.get('crm.lead.system.description').create(cr, uid, {
                                                                'name': ids[0],
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('system_note')
                                                            })
            self.pool.get('crm.lead.all.tabs.description').create(cr, uid, {
                                                                'name': ids[0],
                                                                'date': datetime.datetime.today(),
                                                                'notes': vals.get('system_note')
                                                            })
        return super(crm_lead, self).write(cr, uid, ids, vals, context=context)

    def view_lead_home_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': True, 'see_lead_electricity_note': False, 'see_lead_marketing_note': False, 'see_lead_accounting_note': False, 'see_lead_system_note': False, 'see_lead_all_note': False})
        return True

    def view_lead_electricity_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': False, 'see_lead_electricity_note': True, 'see_lead_marketing_note': False, 'see_lead_accounting_note': False, 'see_lead_system_note': False, 'see_lead_all_note': False})
        return True

    def view_lead_marketing_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': False, 'see_lead_electricity_note': False, 'see_lead_marketing_note': True, 'see_lead_accounting_note': False, 'see_lead_system_note': False, 'see_lead_all_note': False})
        return True
    
    def view_lead_accounting_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': False, 'see_lead_electricity_note': False, 'see_lead_marketing_note': False, 'see_lead_accounting_note': True, 'see_lead_system_note': False, 'see_lead_all_note': False})
        return True
    
    def view_lead_system_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': False, 'see_lead_electricity_note': False, 'see_lead_marketing_note': False, 'see_lead_accounting_note': False, 'see_lead_system_note': True, 'see_lead_all_note': False})
        return True

    def view_lead_all_tab_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': False, 'see_lead_electricity_note': False, 'see_lead_marketing_note': False, 'see_lead_accounting_note': False, 'see_lead_system_note': False, 'see_lead_all_note': True})
        return True

    def exit_notes(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'see_lead_home_note': False, 'see_lead_electricity_note': False, 'see_lead_marketing_note': False, 'see_lead_accounting_note': False, 'see_lead_system_note': False, 'see_lead_all_note': False})
        return True
crm_lead()

class crm_lead_home_description(osv.osv):

    """ Model for CRM Lead Home Information Notes. """

    _name = 'crm.lead.home.description'

    _columns = {
            'name': fields.many2one('crm.lead','Name'),
            'date': fields.datetime('Date Time'),
            'notes': fields.text('Note')
    }
crm_lead_home_description()

class crm_lead_electricity_description(osv.osv):

    """ Model for CRM Lead Electricity Information Notes. """

    _name = 'crm.lead.electricity.description'

    _columns = {
            'name': fields.many2one('crm.lead','Name'),
            'date': fields.datetime('Date Time'),
            'notes': fields.text('Note')
    }
crm_lead_home_description()

class crm_lead_marketing_description(osv.osv):

    """ Model for CRM Lead Marketing Information Notes. """

    _name = 'crm.lead.marketing.description'

    _columns = {
            'name': fields.many2one('crm.lead','Name'),
            'date': fields.datetime('Date Time'),
            'notes': fields.text('Note')
    }
crm_lead_marketing_description()

class crm_lead_accounting_description(osv.osv):

    """ Model for CRM Lead Accounting Information Notes. """

    _name = 'crm.lead.accounting.description'

    _columns = {
            'name': fields.many2one('crm.lead','Name'),
            'date': fields.datetime('Date Time'),
            'notes': fields.text('Note')
    }
crm_lead_accounting_description()

class crm_lead_system_description(osv.osv):

    """ Model for CRM Lead System Information Notes. """

    _name = 'crm.lead.system.description'

    _columns = {
            'name': fields.many2one('crm.lead','Name'),
            'date': fields.datetime('Date Time'),
            'notes': fields.text('Note')
    }
crm_lead_system_description()

class crm_lead_all_tabs_description(osv.osv):

    """ Model for CRM Lead All Tab Information Notes. """

    _name = 'crm.lead.all.tabs.description'

    _columns = {
            'name': fields.many2one('crm.lead','Name'),
            'date': fields.datetime('Date Time'),
            'notes': fields.text('Note')
    }
crm_lead_all_tabs_description()

class company_quotation(osv.osv):
    """ Model for Product. """
    _name = "company.quotation"
    _description= "Other Company Quotation Information."
    _rec_name="company_name"
    
    _columns = {
        'company_name': fields.many2one('res.company','Company Name'),
        'product_ids' : fields.many2many('product.product', 'product_lead_rel', 'pro_id','lead_id','Equipments',help="Select or create equipments offered by the Company."),
        'quote_amount' : fields.float('Quoted Amount'),
        }
company_quotation()

#class heat_home(osv.osv):
#    """ Model for Heat home. """
#    _name = "heat.home"
#    _description= "Heat Home technique Information."
#    
#    _columns = {
#        'name': fields.char('Technique Name'),
#        'description': fields.text('Description'),
#        }
#heat_home()

class roof_type(osv.osv):
    """ Model for Heat home. """
    _name = "roof.type"
    _description= "Type of Roof Information."
    
    _columns = {
        'name': fields.char('Technique Name'),
        'description': fields.text('Description'),
        }
roof_type()

#class account_analytic_account(osv.osv):
#    
#    _inherit="account.analytic.account"
#    
#    _columns = {
#            'contract_id':fields.char('Contract ID'),
#            'contract_date': fields.date('Contract Date'),
#            'type_of_finance': fields.many2one('account.account.type','Type of Financing '),
#            'amount': fields.float('Contract Amount'),
#            'deposit' :fields. float('Deposit Collected'),
#            'planet': fields.selection([('lease','Lease'),('ppa','PPA')], 'Plant'),
#            'power': fields.selection([('sun_power','Sun Power'),('cpf','CPF')], 'Plant'),
#            
##            'equipment_ids': fields.one2many('equipment.line','equipment_id','Equipments'),
##            'product_ids' : fields.many2many('product.product', 'product_account_rel', 'product_id','prod_id','Products'),
#            'members': fields.many2many('res.users', 'project_user_relation', 'project_id', 'uid', 'Project Members'),
#        }
#account_analytic_account()

class crm_opportunity2phonecall(osv.osv_memory):
    """Converts Opportunity to Phonecall"""
    _inherit = 'crm.opportunity2phonecall'

    def action_schedule(self, cr, uid, ids, context=None):
        action_res = super(crm_opportunity2phonecall, self).action_schedule(cr, uid, ids, context=context)
        stage_id = self.pool.get('crm.case.stage').search(cr, uid, [('name','=','Initial Contact')])
        self.pool.get('crm.lead').write(cr, uid, context.get('active_ids'), {'stage_id': stage_id[0]})
        return action_res

crm_opportunity2phonecall()

class crm_make_sale(osv.osv_memory):

    _inherit = 'crm.make.sale'

#    def makeOrder(self, cr, uid, ids, context=None):
#        """
#        This function  create Quotation on given case.
#        @param self: The object pointer
#        @param cr: the current row, from the database cursor,
#        @param uid: the current user’s ID for security checks,
#        @param ids: List of crm make sales' ids
#        @param context: A standard dictionary for contextual values
#        @return: Dictionary value of created sales order.
#        """
#        order_res = super(crm_make_sale, self).makeOrder(cr, uid, ids, context=context)
#        data = context and context.get('active_ids', []) or []
#        case_obj = self.pool.get('crm.lead')
#        crm_case_stage_obj = self.pool.get('crm.case.stage')
#        if order_res['res_id']:
#            for case in case_obj.browse(cr, uid, data, context=context):
#                self.pool.get('sale.order').write(cr, uid, [order_res['res_id']], {'project_id': case.contract_id.id})
##        stage_id = crm_case_stage_obj.search(cr, uid, [('name','=','Proposition')])
##        case_obj.write(cr, uid, data, {'stage_id': stage_id[0]})
#        return order_res

crm_make_sale()

class project_project(osv.osv):
    
    _inherit = 'project.project'
    
    def create(self, cr, uid, vals, context=None):
        if context is None: context = {}
        project_id = super(project_project, self).create(cr, uid, vals, context=context)
        if vals and vals.get('analytic_account_id'):
            for account in self.pool.get('account.analytic.account').browse(cr, uid, [vals['analytic_account_id']]):
                member_list=[]
                for member in account.members:
                    member_list.append((4,member.id))
                    self.write(cr, uid, [project_id], {'members': member_list})
        return project_id
    
project_project()

class res_partner(osv.osv):
    """ Model for Partner. """
    _inherit = "res.partner"
    
    _columns = {
        'spouse': fields.many2one('res.partner',string='Secondary Customer',  help="Secondary Customer (spouse) in case he/she exist."),
        }
    
res_partner()

class crm_meeting(osv.Model):
    """ Model for CRM meetings """
    _inherit = 'crm.meeting'
    
    _columns = {
            'meeting_type': fields.selection([('appointment','Appointment'),('assistance','Assistance'),('general_meeting','General Meeting')], 'Meeting Type'),
            'appointment_outcome': fields.selection([('qualified_sit','Qualified Sit'),('1_leg_sit','1-leg sit'),('n_q','NQ'),('sale','Sale'),('r_s','Reset'),('n_s','No Show'),('cxl','Cancel')], 'Outcome from Appointment',help="Qualified Sit(All decision makers are present)"\
                                                                                                                                                                        "\n1-leg sit(Not all decision makers are present)\n NQ(Not Qualified)"\
                                                                                                                                                                        "\nSALE(We sold a system)\n Reset(appointment reset or wants to reset their appointment.)"\
                                                                                                                                                                        "\n No show (Energy consultant went to the appointment and no one was home)"\
                                                                                                                                                                        "\n Cancel (Appointment canceled and does not want to be reset at this time)]"),
            'cancel_reason': fields.text('Reason for Cancellation'),
    }
    
    _defaults = {
            'name': '/',
            'meeting_type': 'general_meeting',
    }
    
    def create(self, cr, uid, ids, context=None):
        res = super(crm_meeting, self).create(cr, uid, ids, context=context)
        if context.get('default_opportunity_id'):
            crm_case_stage_obj = self.pool.get('crm.case.stage')
            opo_obj= self.pool.get('crm.lead')
            stage_id = crm_case_stage_obj.search(cr, uid, [('name','=','Appointment Set')])
            opo_obj.write(cr, uid, [context.get('default_opportunity_id')], {'stage_id': stage_id[0]})
        return res

crm_meeting()

