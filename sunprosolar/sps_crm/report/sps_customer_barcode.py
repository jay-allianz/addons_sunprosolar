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

class customer_barcode(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(customer_barcode, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'product_get': self._product_get 
        })
        
    def _product_get(self, order_line):
        result = False
        if order_line:
            result = order_line.product_id.name
        for product in order_line:
            result += product.product_id.name
        return result
    
report_sxw.report_sxw('report.customer.sale.barcode', 'sale.order', 'addons/sps_crm/report/sps_customer_barcode.rml', parser=customer_barcode, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: