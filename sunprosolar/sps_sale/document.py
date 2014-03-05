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
    
class doc_required(osv.Model):
    
    _name="doc.required"
    
    _columns={
        'doc_id': fields.many2one("account.account.type"),
        'name' : fields.char("Document Name"),
#        'doc_ids': fields.one2many('ir.attachment','document_id1',"Document" ),
        'collected' : fields.boolean("Collected"),
        'days_to_collect': fields.integer("Days to Collect"),
        'notify_customer': fields.many2one("res.partner","Notify Customer when Collected"),
        'notify_users': fields.many2many("res.users", "part_document_rel", "part_id", 'document_id',"Notify Users When Collected")
    }
    
    def write(self, cr, uid, ids, vals, context=None):
        if not vals.get('doc_ids', None):
            return super(doc_required, self).write(cr, uid, ids, vals, context=context)
        vals.update({'collected' : True})
        cur_rec = self.browse(cr, uid, ids, context=context)[0]
        customer = cur_rec.notify_customer
        users = cur_rec.notify_users
        send_mail_obj = self.pool.get('send.send.mail')
        if customer:
            if customer.email:
                NO_REC_MSG = ''
                SUB_LINE = 'Notification for Document Upload.'
                MSG_BODY = 'Hello ' + customer.name + ',<br/><br/>' + ' Your Document named ' + cur_rec.name + '.<br/><br/> Have been successfully Uploaded.<br/><br/> Thank You.'
                send_mail_obj.send(cr, uid, NO_REC_MSG, SUB_LINE, MSG_BODY, customer.email, context=context)
                
        if users:
            for user in users:
                if user.email:
                    NO_REC_MSG1 = ''
                    SUB_LINE1 = 'Notification for Document Upload.'
                    MSG_BODY1 = 'Hello ' + user.name +',<br/>' +  ' The Document named ' + cur_rec.name + '.<br/><br/> Have been successfully Uploaded.<br/><br/> Thank You.'
                    send_mail_obj.send(cr, uid, NO_REC_MSG1, SUB_LINE1, MSG_BODY1, user.email, context=context)
        return super(doc_required, self).write(cr, uid, ids, vals, context=context)

#class ir_attachment(osv.Model):
#    
#    _inherit = "ir.attachment"
#    
#    _columns ={
#            'document_id1': fields.many2one("doc.required","Document")
#    }
    
class account_account_type(osv.Model):
    
    _inherit= "account.account.type"
    
    _columns={
        'doc_req_ids' : fields.one2many('doc.required', 'doc_id', 'Required Documents'),
    }
    