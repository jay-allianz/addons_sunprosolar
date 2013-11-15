# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2013 Serpent Consulting Services (<http://serpentcs.com>).
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
from openerp.osv import osv, fields

class wizard_report(osv.osv_memory):
    _inherit = "wizard.report"
    _columns = {
        'show_earning': fields.boolean('Is this a Balance Sheet ?'),
        'earning_account': fields.many2one('account.account', 'If so, please select a Retained Earnings Acct.'),
        'inf_type': fields.selection([('BS','Balance Sheet'),('IS','Income Statement'),('TB', 'Trail Balance'),('GL', 'General Ledger')],'Type',required=True),
    }
    _defaults = {
        'show_earning': False
    }
    
#    def periodic_print_report(self, cr, uid, ids, data, context=None):
#        res = super(wizard_report, self).periodic_print_report(cr, uid, ids, data, context=context)
#        print 'RREEESSS',res
#        if res['report_name'] == 'periodic1.1cols':
#            res['report_name'] = 'periodic.1cols.inherit'
#        return res

    def print_report(self, cr, uid, ids, data, context=None):
        res = super(wizard_report, self).print_report(cr, uid, ids, data, context=context)
#        print "res:::::of print report:::",res
        if res['report_name'] == 'afr.1cols':
            res['report_name'] = 'afr.1cols.inherit'
        if res['report_name'] == 'afr.2cols':
            res['report_name'] = 'afr.2cols.inherit'
        if res['report_name'] == 'afr.analytic.ledger':
            res['report_name'] = 'afr.analytic.ledger.inherit'
        if res['report_name'] == 'afr.4cols':
            res['report_name'] = 'afr.4cols.inherit'
        if res['report_name'] == 'afr.5cols':
            res['report_name'] = 'afr.5cols.inherit'
        if res['report_name'] == 'afr.qtrcols':
            res['report_name'] = 'afr.qtrcols.inherit'
        if res['report_name'] == 'afr.13cols':
            res['report_name'] = 'afr.13cols.inherit'
        return res
    
    def print_report_aeroo(self, cr, uid, ids, data, context=None):
        res = super(wizard_report, self).print_report(cr, uid, ids, data, context=context)
        print "call meyhod????Aerrooo",res
        res['datas']['ids'] = [1]
        if res['report_name'] == 'afr.1cols':
            res['report_name'] = 'balance.full.aeroo'
        if res['report_name'] == 'afr.2cols':
            res['report_name'] = 'balance.full.two.aeroo'
        if res['report_name'] == 'afr.analytic.ledger':
            res['report_name'] = 'analytic.ledger.aeroo'
        if res['report_name'] == 'afr.4cols':
            res['report_name'] = 'afr.4cols.inherit'
        if res['report_name'] == 'afr.5cols':
            res['report_name'] = 'afr.5cols.inherit'
        if res['report_name'] == 'afr.qtrcols':
            res['report_name'] = 'balance.qtr.aeroo'
        if res['report_name'] == 'afr.13cols':
            res['report_name'] = 'balance.monthly.aeroo'
        return res
    
    def periodic_print_report(self, cr, uid, ids, data, context=None):
        res = super(wizard_report, self).periodic_print_report(cr, uid, ids, data, context=context)
        if res['report_name'] == 'periodic1.1cols':
            res['report_name'] = 'periodic1.1cols.inherit'
        if res['report_name'] == 'periodic.2cols':
            res['report_name'] = 'periodic.2cols.inherit'
        if res['report_name'] == 'periodic2.1cols':
            res['report_name'] = 'periodic2.1cols.inherit'
        if res['report_name'] == 'periodic3.1cols':
            res['report_name'] = 'periodic3.1cols.inherit'
        if res['report_name'] == 'periodic1.2cols':
            res['report_name'] = 'periodic1.2cols.inherit'
        if res['report_name'] == 'periodic2.2cols':
            res['report_name'] = 'periodic2.2cols.inherit'
        if res['report_name'] == 'afr.analytic.ledger':
            res['report_name'] = 'afr.analytic.ledger.inherit'
        if res['report_name'] == 'periodic.4cols':
            res['report_name'] = 'periodic.4cols.inherit'
        if res['report_name'] == 'periodic2.4cols':
            res['report_name'] = 'periodic2.4cols.inherit'
        if res['report_name'] == 'periodic3.4cols':
            res['report_name'] = 'periodic3.4cols.inherit'
        return res

    def periodic_print_report_aeroo(self, cr, uid, ids, data, context=None):
        res = super(wizard_report, self).periodic_print_report(cr, uid, ids, data, context=context)
        res['datas']['ids'] = [1]
        if res['report_name'] == 'periodic1.1cols':
            res['report_name'] = 'periodic1.1cols.aeroo'
        if res['report_name'] == 'periodic.2cols':
            res['report_name'] = 'periodic.two.aeroo'
        if res['report_name'] == 'periodic2.1cols':
            res['report_name'] = 'periodic.financial.report.two.aeroo'
        if res['report_name'] == 'periodic3.1cols':
            res['report_name'] = 'periodic.financial.report.three.aeroo'
        if res['report_name'] == 'periodic1.2cols':
            res['report_name'] = 'periodic1.2cols.inherit'
        if res['report_name'] == 'periodic2.2cols':
            res['report_name'] = 'periodic2.2cols.inherit'
        if res['report_name'] == 'afr.analytic.ledger':
            res['report_name'] = 'analytic.ledger.aeroo'
        if res['report_name'] == 'periodic.4cols':
            res['report_name'] = 'periodic.4cols.inherit'
        if res['report_name'] == 'periodic2.4cols':
            res['report_name'] = 'periodic2.4cols.inherit'
        if res['report_name'] == 'periodic3.4cols':
            res['report_name'] = 'periodic3.4cols.inherit'
        return res

wizard_report()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
