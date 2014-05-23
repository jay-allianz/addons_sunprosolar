# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Allianz Technology, A subsidiary of SAT Group, Inc.
#    Copyright (C) 2012 OpenERP SA (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from openerp.report import report_sxw

class invoice_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(invoice_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time, 
            'get_all_invoices':self.get_all_invoices,
            'get_invoice_amount':self.get_invoice_amount,
            'get_remaining_balance':self.get_remaining_balance
        })
        
    def get_all_invoices(self):
        invoices = []
        invoice_obj = self.pool.get('account.invoice')
        invoice_serach = invoice_obj.search(self.cr, self.uid, [])
        invoice_data = invoice_obj.browse(self.cr, self.uid, invoice_serach)
        for data in invoice_data:
            if data.payment_ids:
                invoices.append(data)
        return invoices
    
    
    def get_invoice_amount(self, invoice_data):
        return invoice_data.invoice_line[0].price_subtotal

    def get_remaining_balance(self,invoice_data):
        total = 0.0
        for payment in invoice_data.payment_ids:
            total += payment.credit
        result = invoice_data.invoice_line[0].price_subtotal - total
        return result
        
report_sxw.report_sxw('report.invoice.report', 'account.invoice', 'addons/sps_account_invoice/report/invoice_report.rml', parser=invoice_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: