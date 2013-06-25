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
         'contract_id': fields.many2one('hr.contract', 'Contract', help="The contract for which applied this input"),
         'quote': fields.boolean('Had a Solar Quote?', help = 'Checked if customer have Solar Quotation of any other Company.'),
         'quote_info': fields.many2one('company.quotation','Quotation Information'),
         'heat_home': fields.many2one('heat.home','Heat Home Technique'),
         'home_sq_foot': fields.float('Home Sq-Footage'),
         'age_house_year': fields.integer('Age of House'),
         'age_house_month': fields.integer('Age of House month'),
         'roof_type': fields.many2one('roof.type','Type of Roof '),
         'tilt': fields.char('Tilt'),
         'azimuth': fields.float('Azimuth'),
         'estimate_shade': fields.float('Estimated Shading'),
         'utility_bill' : fields.boolean('utility_bill',help="Checked if Utility bill of 12 months are collected from the customer."),
#         'bill_ids' : fields.one2many('utility.bill','lead_id','Certificate'),
        
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

#class utility_bill(osv.osv):
#    
#    _name = "utility.bill"
#    
#    _columns = {
#        'lead_id' : fields.many2one('crm.lead', 'Student'),
#        'description' : fields.char('Description',size=50),
#        'bill' : fields.binary('Bill',required =True)
#                }
#utility_bill()


class hr_contract(osv.osv):
    """ Model for contract. """
    _inherit = "hr.contract"
    
    _columns = {

        }
    
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

