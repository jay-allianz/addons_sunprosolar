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
import time
import netsvc
from datetime import date, timedelta, datetime
import datetime
import tools
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class sale_order(osv.Model):

    _inherit = "sale.order"
    
    def onchange_financing_type(self, cr, uid, ids, financing_type_id, context=None):
        doc_req_obj = self.pool.get('doc.required')
        values = {}
        if not ids:
            return {'value': {}}
        old_rec_len = len(self.browse(cr, uid,ids[0],context=context).doc_req_ids)
        if old_rec_len:
            doc_req_ids = doc_req_obj.search(cr, uid, [('doc_sale_id','=',ids[0])],context=context)
            doc_req_obj.unlink(cr, uid, doc_req_ids)
        fin_type_obj = self.pool.get('financing.type')
        fin_type_rec  = fin_type_obj.browse(cr, uid, financing_type_id, context=context)
        doc_ids = []
        if financing_type_id:
            if fin_type_rec.document_ids:
                for document in fin_type_rec.document_ids:
                    vals = {
                        'doc_id' : document.id,
                        'days_to_collect' : document.days_to_collect,
                        'doc_sale_id' : ids[0],
                        'cowndown':document.days_to_collect,
                    }
                    doc_ids.append(doc_req_obj.create(cr, uid, vals, context=context))
                values = {'doc_req_ids' : doc_ids or False}
        return {'value' : values}
    
    _columns = {
          'contract_id' : fields.many2one('account.analytic.account', 'Contract'),
          'color': fields.integer('Color Index'),
          'company_currency': fields.related('company_id', 'currency_id', type='many2one', string='Currency', readonly=True, relation="res.currency"),
          'planned_revenue': fields.float('Expected Revenue', track_visibility='always'),
          'state': fields.selection([
                ('draft', 'Proposal'),
                ('sent', 'Proposal Sent'),
                ('contract_generated', 'Contract Generated'),
                ('follow_up','Follow Up'),
                ('contract_signed', 'Contract Signed'),
                ('project_management_notified','Project Management Notified'),
                ('manual', 'Sale to Invoice'),
                ('financing_type','Financing Type'),
                ('assign_financing_incharge','Assign Financing In-Charge'),
                ('site_inspection', 'Site Inspection'),
                ('permit','Permit'),
                ('city','City Submission'),
                ('drawing','Eng. Create/Modify Following Drawings'),
                ('permit_pack','Permit Pack'),
                ('progress', 'Sales Order'),
                ('cancel', 'Cancelled'),
                ], 'Status', readonly=True,
                help="Gives the status of the quotation or sales order. \nThe exception status is automatically set when a cancel operation occurs in the processing of a document linked to the sales order. \nThe 'Waiting Schedule' status is set when the invoice is confirmed but waiting for the scheduler to run on the order date.", select=True),
         'engineering': fields.selection([('yes', 'Yes'), ('no', 'No')], 'Engineering May be structural or Electrical'),
         'confirm_original': fields.selection([('no_changes', 'No changes'), ('change', 'Changes Made')], 'Confirmation of original Design'),
         'contract_signing_date' : fields.datetime('Contract Signing Date'),
         'inspection_done_date' : fields.datetime('Inspection Done Date'),
         'insp_after_72_hour' : fields.boolean('Inspection After 72 Hours '),
         'financing_type_id' : fields.many2one('financing.type','Financing Type'),
         'incharge_user_id' : fields.many2one('res.users','Financing In-Charge'),
         'procurement_ids': fields.one2many('procurement.order','sale_order_id','Procurements Created'),
         'ahj': fields.selection([('structural', 'Structural'), ('electrical', 'Electrical')], 'AHJ', help="Authority Having Jurisdiction"),
    }
    
    _defaults = {
            'engineering': 'yes',
    }
    
    def _create_pickings_and_procurements(self, cr, uid, order, order_lines, picking_id=False, context=None):
        """Create the required procurements to supply sales order lines, also connecting
        the procurements to appropriate stock moves in order to bring the goods to the
        sales order's requested location.

        If ``picking_id`` is provided, the stock moves will be added to it, otherwise
        a standard outgoing picking will be created to wrap the stock moves, as returned
        by :meth:`~._prepare_order_picking`.

        Modules that wish to customize the procurements or partition the stock moves over
        multiple stock pickings may override this method and call ``super()`` with
        different subsets of ``order_lines`` and/or preset ``picking_id`` values.

        :param browse_record order: sales order to which the order lines belong
        :param list(browse_record) order_lines: sales order line records to procure
        :param int picking_id: optional ID of a stock picking to which the created stock moves
                               will be added. A new picking will be created if ommitted.
        :return: True
        """
        move_obj = self.pool.get('stock.move')
        picking_obj = self.pool.get('stock.picking')
        procurement_obj = self.pool.get('procurement.order')
        proc_ids = []

        for line in order_lines:
            if line.state == 'done':
                continue

            date_planned = self._get_date_planned(cr, uid, order, line, order.date_order, context=context)

            if line.product_id:
                if line.product_id.type in ('product', 'consu'):
                    if not picking_id:
                        picking_id = picking_obj.create(cr, uid, self._prepare_order_picking(cr, uid, order, context=context))
                    move_id = move_obj.create(cr, uid, self._prepare_order_line_move(cr, uid, order, line, picking_id, date_planned, context=context))
                else:
                    # a service has no stock move
                    move_id = False

                proc_id = procurement_obj.create(cr, uid, self._prepare_order_line_procurement(cr, uid, order, line, move_id, date_planned, context=context))
                procurement_obj.write(cr, uid, proc_id, {"sale_order_id":order.id}, context=context)
                proc_ids.append(proc_id)
                line.write({'procurement_id': proc_id})
                self.ship_recreate(cr, uid, order, line, move_id, proc_id)

        wf_service = netsvc.LocalService("workflow")
        if picking_id:
            wf_service.trg_validate(uid, 'stock.picking', picking_id, 'button_confirm', cr)
        for proc_id in proc_ids:
            wf_service.trg_validate(uid, 'procurement.order', proc_id, 'button_confirm', cr)

        val = {}
        if order.state == 'shipping_except':
            val['state'] = 'progress'
            val['shipped'] = False

            if (order.order_policy == 'manual'):
                for line in order.order_line:
                    if (not line.invoiced) and (line.state not in ('cancel', 'draft')):
                        val['state'] = 'manual'
                        break
        order.write(val)
        return True
    
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
        lead_obj = self.pool.get('crm.lead')
        cur_rec = self.browse(cr, uid, ids, context=context)[0]
        reference = 'sale.order,' + str(cur_rec.id)
        lead_id = lead_obj.search(cr, uid, [('ref', '=', reference)],context= context)
        if lead_id:
            lead_data = lead_obj.browse(cr, uid, lead_id,context=context)[0]
        if not cur_rec.order_line:
            raise osv.except_osv(_('Error'), _('To generate contract you have to define order line!'))
        vals = {
            'name' : cur_rec.partner_id.name,
            'partner_id' : cur_rec.partner_id.id,
            'amount' : cur_rec.amount_total,
            'deposit' : lead_data and lead_data.down_payment_amt,
            'sale_id': cur_rec.id,
            'contract_date': datetime.datetime.today(),
            'use_tasks' : True,
        }
        context['creation_from_sps'] = True
        proj_acc_analy_id = ana_acc_obj.create(cr, uid, vals, context=context)
        project_id = project_obj.search(cr, uid, [('analytic_account_id','=',proj_acc_analy_id)], context=context)[0]
        task_vals = {
            'name' : cur_rec.partner_id.name,
            'project_id':project_id,
            'color': 4,
        }
        project_obj.write(cr, uid, project_id, {'color':4}, context=context)
        task_obj.create(cr, uid, task_vals, context=context)
        self.write(cr, uid, ids, {'state': 'contract_generated','project_id': proj_acc_analy_id})
        return True
    
    def contract_rejected(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'follow_up'})
        return True
    
    def drwaing(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'drawing'})
        return True
    
    def permit_pack(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'permit_pack'})
        return True
    
    def customer_appove(self, cr, uid, ids, context=None):
        cur_rec = self.browse(cr, uid, ids, context=context)[0]
        if not cur_rec.ahj:
            raise osv.except_osv(_('Warning !'),_("Please select AHJ(Authority Having Jurisdiction)."))
        self.write(cr, uid, ids, {'state': 'city'})
        return True
    
    def contract_sign(self, cr, uid, ids, context=None):
        cur_time = datetime.datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        self.write(cr, uid, ids, {'state': 'contract_signed', 'contract_signing_date':cur_time})
        proj_id = self.browse(cr, uid, ids, context=context)[0].project_id.id
        ana_acc_obj = self.pool.get('account.analytic.account')
        ana_acc_obj.write(cr, uid, [proj_id], {'contract_date' : cur_time})
        return True
    
    def document_collected(self, cr, uid, ids, context=None):
        cur_rec = self.browse(cr, uid, ids, context=context)[0]
        if not cur_rec.financing_type_id :
            raise osv.except_osv(_('Warning !'),_("Please select the \'Financing Type\' for Document collection."))
        elif cur_rec.required_document == False:
            raise osv.except_osv(_('Warning !'),_("Please select collect Required Documents."))
        self.write(cr, uid, ids, {'state': 'financing_type'})
        return True
    
    def assign_professional(self, cr, uid, ids, context=None):
        cur_rec = self.browse(cr, uid, ids, context=context)[0]
        if not cur_rec.incharge_user_id :
            raise osv.except_osv(_('Warning !'),_("Please select the 'Financing In-Charge'."))
        self.write(cr, uid, ids, {'state': 'assign_financing_incharge'})
        return True
    
    def done_inspection(self, cr, uid, ids, context=None):
        cur_time = datetime.datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        cur_rec = self.browse(cr, uid, ids, context=context)[0]
        done_within_72 = False
        if cur_rec:
            cont_should_sign_date = datetime.datetime.now()-timedelta(days=3)
            cont_actual_sign_date = datetime.datetime.strptime(cur_rec.contract_signing_date, DEFAULT_SERVER_DATETIME_FORMAT)
            if cont_actual_sign_date < cont_should_sign_date :
                done_within_72 = True
        self.write(cr, uid, ids, {'inspection_done_date':cur_time,'insp_after_72_hour' : done_within_72,'state': 'permit'})
        return True
    
    def is_inspection_done_in_72_hours(self, cr, uid, automatic=False, use_new_cursor=False, context=None):
        cur_time = datetime.datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        sale_order_ids = self.search(cr, uid, [('contract_signing_date','!=',False),('insp_after_72_hour','=',False),('inspection_done_date','=',False)], context=context)
        for sale_order in self.browse(cr, uid, sale_order_ids, context=context):
            cont_actual_sign_date = datetime.datetime.strptime(sale_order.contract_signing_date, DEFAULT_SERVER_DATETIME_FORMAT)
            cont_should_sign_date = datetime.datetime.now()-timedelta(days=3)
            done_within_72 = False
            if cont_actual_sign_date < cont_should_sign_date :
                done_within_72 = True
            self.write(cr, uid, [sale_order.id], {'insp_after_72_hour' : done_within_72}, context=context)
        return True
    
    def project_management_notified(self, cr, uid, ids, context=None):
        schedule_mail_object = self.pool.get('mail.message')
        data_obj = self.pool.get('ir.model.data')
        lead_obj = self.pool.get('crm.lead')
        group_object = self.pool.get('res.groups')
        obj_mail_server = self.pool.get('ir.mail_server')
        station = []
        tilt = []
        faceing = []
        product_module = []
        no_of_module = []
        product_inverter = []
        no_of_inverter = []
        solar_info = ' '
        mail_server_ids = obj_mail_server.search(cr, uid, [], context=context)
        if not mail_server_ids:
            raise osv.except_osv(_('Mail Error'), _('No mail server found!'))
        mail_server_record = obj_mail_server.browse(cr, uid, mail_server_ids)[0]
        email_from = mail_server_record.smtp_user
        if not email_from:
            raise osv.except_osv(_('Mail Error'), _('No mail found for smtp user!'))
        member_email_list = []
        for data in self.browse(cr, uid, ids):
            reference = 'sale.order,' + str(data.id)
            lead_id = lead_obj.search(cr, uid, [('ref', '=', reference)],context= context)
            for lead_data in lead_obj.browse(cr, uid, lead_id,context=context):
                for solar_data in lead_data.solar_ids:
                    station_temp = solar_data.loc_station_id and solar_data.loc_station_id.name
                    faceing_temp = solar_data.faceing and solar_data.faceing.tilt
                    tilt_temp = solar_data.tilt_degree
                    product_module_temp = solar_data.module_product_id and solar_data.module_product_id.name
                    no_of_module_temp = solar_data.num_of_module
                    product_inverter_temp = solar_data.inverter_product_id and solar_data.inverter_product_id.name
                    no_of_inverter_temp = solar_data.num_of_invertor
                    
                    station.append(str(station_temp))
                    tilt.append(str(tilt_temp))
                    faceing.append(str(faceing_temp))
                    product_module.append(str(product_module_temp))
                    no_of_module.append(str(no_of_module_temp))
                    product_inverter.append(str(product_inverter_temp))
                    no_of_inverter.append(str(no_of_inverter_temp))
                    
                    solar_info = 'Station: '+ str(station[0]) + ', Tilt/Azimuth: ' + str(tilt[0]) + ', Facing: ' + str(faceing[0]) + ', Module Name: ' + str(product_module[0]) + ', Number of Module: ' + str(no_of_module[0]) + ', Inverter Name: ' + str(product_inverter[0]) + ', Number of Inverter: ' + str(no_of_inverter[0]) + '.'
                    
                    station = []
                    tilt = []
                    faceing = []
                    product_module = []
                    no_of_module = []
                    product_inverter = []
                    no_of_inverter = []
        
            if not data.project_id.members:
                raise osv.except_osv(_('Warning'), _('There is no project team member define in contract !'))
            else:
                for member in data.project_id.members:
                    if not member.email:
                        raise osv.except_osv(_('Warning'), _('%s team member have no email defined !' % member.name))
                    else:
                        member_email_list.append(member.email)
            
            message_body = 'Hello,<br/><br/>Project Notification.<br/><br/>Customer Information<br/><br/>Name : ' + tools.ustr(data.partner_id.name) + '<br/><br/>Email : ' + tools.ustr(data.partner_id.email) + '<br/><br/>Phone : ' + tools.ustr(data.partner_id.phone) +'<br/><br/>Solar Information<br/><br/>'+ solar_info +' <br/><br/> Thank You.'
        message_hrmanager = obj_mail_server.build_email(
            email_from=email_from,
            email_to=member_email_list,
            subject='Project Notification',
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
        self.write(cr, uid, ids, {'state': 'project_management_notified'})
        return True
    
    def site_inspection_mail(self, cr, uid, ids, context=None):
        schedule_mail_object = self.pool.get('mail.message')
        data_obj = self.pool.get('ir.model.data')
        group_object = self.pool.get('res.groups')
        lead_obj = self.pool.get('crm.lead')
        obj_mail_server = self.pool.get('ir.mail_server')
        station = []
        tilt = []
        faceing = []
        product_module = []
        no_of_module = []
        product_inverter = []
        no_of_inverter = []
        solar_info = ''
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

            reference = 'sale.order,' + str(data.id)
            lead_id = lead_obj.search(cr, uid, [('ref', '=', reference)],context= context)
            for lead_data in lead_obj.browse(cr, uid, lead_id,context=context):
                for solar_data in lead_data.solar_ids:
                    station_temp = solar_data.loc_station_id and solar_data.loc_station_id.name
                    faceing_temp = solar_data.faceing and solar_data.faceing.tilt
                    tilt_temp = solar_data.tilt_degree
                    product_module_temp = solar_data.module_product_id and solar_data.module_product_id.name
                    no_of_module_temp = solar_data.num_of_module
                    product_inverter_temp = solar_data.inverter_product_id and solar_data.inverter_product_id.name
                    no_of_inverter_temp = solar_data.num_of_invertor
                    
                    station.append(str(station_temp))
                    tilt.append(str(tilt_temp))
                    faceing.append(str(faceing_temp))
                    product_module.append(str(product_module_temp))
                    no_of_module.append(str(no_of_module_temp))
                    product_inverter.append(str(product_inverter_temp))
                    no_of_inverter.append(str(no_of_inverter_temp))
                    
                    solar_info = 'Station: '+ str(station[0]) + ', Tilt/Azimuth: ' + str(tilt[0]) + ', Facing: ' + str(faceing[0]) + ', Module Name: ' + str(product_module[0]) + ', Number of Module: ' + str(no_of_module[0]) + ', Inverter Name: ' + str(product_inverter[0]) + ', Number of Inverter: ' + str(no_of_inverter[0])
                    
                    station = []
                    tilt = []
                    faceing = []
                    product_module = []
                    no_of_module = []
                    product_inverter = []
                    no_of_inverter = []
            
            message_body = 'Hello,<br/><br/>New site inspection needs to be done.<br/><br/>Contract Information<br/><br/>Contract ID : ' + tools.ustr(data.project_id.contract_id) + '<br/><br/>Contract Amount : ' + tools.ustr(data.project_id.amount) + '<br/><br/>Deposite Amount : ' + tools.ustr(data.project_id.deposit) + '<br/><br/>Customer Information<br/><br/>Name : ' + tools.ustr(data.partner_id.name) + '<br/><br/>Email : ' + tools.ustr(data.partner_id.email) + '<br/><br/>Phone : ' + tools.ustr(data.partner_id.phone) + '<br/><br/>Solar Information<br/><br/>'+ solar_info + '<br/><br/> Thank You.'
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
    
class financing_type(osv.osv):
    
    _name = "financing.type"
    
    _columns = {
        'name' : fields.char('Name'),
        'description': fields.text('Description'),
        'document_ids' : fields.many2many('documents.all','document_financing_type_rel','fin_type_id','doc_id','Documents'),
    }
    
class procurement_order(osv.Model):
    
    _inherit = 'procurement.order'
    
    _columns = {
            'sale_order_id' : fields.many2one('sale.order', 'Sale Order'),
    }

class account_analytic_account(osv.Model):
    
    _inherit = "account.analytic.account"
    
    _columns = {
            'contract_id':fields.char('Contract ID'),
            'sale_id': fields.many2one('sale.order', 'Sale Order'),
            'contract_date': fields.date('Contract Date'),

            'roof_vents_moved':fields.char("# of Roof Vents To Be Moved"),
            'dormers_moved':fields.char('# of Dormers To Be Moved'),
            'service_needed': fields.char('Service Upgrade Needed'),
            'trenching':fields.char('Trenching'),
            'mount':fields.selection([('Ground','Ground Mount'),('Roof','Roof Mount')],"Mount"),
            
            'amount': fields.float('Contract Amount'),
            'deposit' :fields. float('Deposit Collected'),
            'planet': fields.selection([('lease', 'Lease'), ('ppa', 'PPA')], 'Plant'),
            'power': fields.selection([('sun_power', 'Sun Power'), ('cpf', 'CPF')], 'Plant'),
            'type': fields.selection([('view','Analytic View'), ('normal','Analytic Account'),('contract','Contract or Project'),('template','Template of Contract'),('opportunity','Opportunity'),('lead','Lead')], 'Type of Account', required=True,
                                 help="If you select the View Type, it means you won\'t allow to create journal entries using that account.\n"\
                                  "The type 'Analytic account' stands for usual accounts that you only want to use in accounting.\n"\
                                  "If you select Contract or Project, it offers you the possibility to manage the validity and the invoicing options for this account.\n"\
                                  "The special type 'Template of Contract' allows you to define a template with default data that you can reuse easily."),
            'members': fields.many2many('res.users', 'project_user_relation', 'project_id', 'uid', 'Project Members'),
            'hoa': fields.boolean("HOA"),
            'csi': fields.boolean("CSI"),
            'type_install': fields.selection([('PV','PV'),('Pool','POOL'),('Hot Water','HOT WATER'),('Other','OTHER')],"Type of Install"),
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

