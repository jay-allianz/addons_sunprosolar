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

class cash_bonus(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(cash_bonus, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_total_bonus': self._get_total_bonus 
        })
        
    def _get_total_bonus(self, cash_bonus_lines):
        result = 0.0
        if cash_bonus_lines:
            for line in cash_bonus_lines:
                result += line.cash
        return result
    
report_sxw.report_sxw('report.cash.bonus', 'res.partner', 'addons/sps_crm/report/sps_cash_bonus.rml', parser=cash_bonus)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: