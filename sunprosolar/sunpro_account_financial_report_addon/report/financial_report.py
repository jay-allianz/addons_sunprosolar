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

import time
import datetime
from openerp.report import report_sxw
from openerp.tools import config
from openerp.tools.translate import _
from openerp.osv import osv
from operator import itemgetter
from sunpro_account_financial_report.report.parser import account_balance

class account_balance_inherit(account_balance):
    def __init__(self, cr, uid, name, context):
        
        self.total_asset_credit = 0.00
        self.total_liabilities_credit = 0.00
        self.total_equity_credit = 0.00
        self.total_asset_debit = 0.00
        self.total_liabilities_debit = 0.00
        self.total_equity_debit = 0.00
        self.total_liabilities_equity = 0.00
        self.total_assets = 0.00
        
        self.rev_credit = 0.00
        self.rev_debit = 0.00
        self.cogs_credit = 0.00
        self.cogs_debit = 0.00
        self.gross_profit = 0.00
        self.bal = 0.00
        self.total_balance_sheet_balance = 0.00
            
        self.other_exp_credit = 0.00
        self.other_exp_debit = 0.00
        self.exp_credit = 0.00
        self.exp_debit = 0.00
        self.taxes_credit = 0.00
        self.taxes_debit = 0.00
        self.net_profit = 0.00
        self.total_exp = 0.00
        self.other_income_credit = 0.00
        self.other_income_debit = 0.00
#        self.tot_revenue = 0.00
#        self.tot_cogs = 0.00
#        self.gross_profit = 0.00
#        self.total_expense = 0.00
#        self.operating_expense = 0.00
#        self.taxes = 0.00
#        self.other_expense = 0.00
#        self.other_income = 0.00
#        self.net_profit = 0.00
#        self.tot_liabilities = 0.00
#        self.tot_equity = 0.00
#        self.tot_liabilities_equity = 0.00
#        self.profit_to_loss = 0.00
#        self.bal = 0.00
#        self.balance_sheet = 0.00
#        self.pro = 0.00
#        ######## Initialise Variable for Quarter Reports########
#        self.gross_profit_dbr1 = 0.00
#        self.gross_profit_dbr2 = 0.00
#        self.gross_profit_dbr3 = 0.00
#        self.gross_profit_dbr4 = 0.00
#        self.gross_profit_dbr5 = 0.00
#        self.tot_revenue_dbr1 = self.tot_revenue_dbr2 = self.tot_revenue_dbr3 = self.tot_revenue_dbr4 = self.tot_revenue_dbr5 = 0.00
#        self.tgcs_dbr1 = self.tgcs_dbr2 = self.tgcs_dbr3 = self.tgcs_dbr4 = self.tgcs_dbr5 = 0.00
#        self.opexpdbr1 = self.opexpdbr2 = self.opexpdbr3 = self.opexpdbr4 = self.opexpdbr5 = 0.00
#        self.taxdbr1 = self.taxdbr2 = self.taxdbr3 = self.taxdbr4 = self.taxdbr5 = 0.00
#        self.expdbr1 = self.expdbr2 = self.expdbr3 = self.expdbr4 = self.expdbr5 = 0.00
#        self.incomedbr1 = self.incomedbr2 = self.incomedbr3 = self.incomedbr4 = self.incomedbr5 = 0.00
#        self.total_expense_dbr1 = self.total_expense_dbr2 = self.total_expense_dbr3 = self.total_expense_dbr4 = self.total_expense_dbr5 = 0.00
#        self.net_profit_dbr1 = self.net_profit_dbr2 = self.net_profit_dbr3 = self.net_profit_dbr4 = self.net_profit_dbr5 = 0.00
#        self.liabilitiesdbr1 = self.liabilitiesdbr2 = self.liabilitiesdbr3 = self.liabilitiesdbr4 = self.liabilitiesdbr5 = 0.00
#        self.equitydbr1 = self.equitydbr2 = self.equitydbr3 = self.equitydbr4 = self.equitydbr5 = 0.00
#        self.total_liabilities_dbr1 = self.total_liabilities_dbr2 = self.total_liabilities_dbr3 = self.total_liabilities_dbr4 = self.total_liabilities_dbr5 = 0.00
#        
#        ######## Initialise Variable for Monthly Reports ########
#        self.gross_profit_mon_dbr1 = self.gross_profit_mon_dbr2 = self.gross_profit_mon_dbr3 = self.gross_profit_mon_dbr4 = self.gross_profit_mon_dbr5 = self.gross_profit_mon_dbr6 = self.gross_profit_mon_dbr7 = self.gross_profit_mon_dbr8 = self.gross_profit_mon_dbr9 = self.gross_profit_mon_dbr10 = self.gross_profit_mon_dbr11 = self.gross_profit_mon_dbr12 = self.gross_profit_mon_dbr13 = 0.00
#        self.tot_revenue_mon_dbr1 = self.tot_revenue_mon_dbr2 = self.tot_revenue_mon_dbr3 = self.tot_revenue_mon_dbr4 = self.tot_revenue_mon_dbr5 = self.tot_revenue_mon_dbr6 = self.tot_revenue_mon_dbr7 = self.tot_revenue_mon_dbr8 = self.tot_revenue_mon_dbr9 = self.tot_revenue_mon_dbr10 = self.tot_revenue_mon_dbr11 = self.tot_revenue_mon_dbr12 = self.tot_revenue_mon_dbr13 = 0.00
#        self.tgcs_mon_dbr1 = self.tgcs_mon_dbr2 = self.tgcs_mon_dbr3 = self.tgcs_mon_dbr4 = self.tgcs_mon_dbr5 = self.tgcs_mon_dbr6 = self.tgcs_mon_dbr7 = self.tgcs_mon_dbr8 = self.tgcs_mon_dbr9 = self.tgcs_mon_dbr10 = self.tgcs_mon_dbr11 = self.tgcs_mon_dbr12 = self.tgcs_mon_dbr13 = 0.00
#        self.opexpdbr1_mon_dbr1 = self.opexpdbr1_mon_dbr2 = self.opexpdbr1_mon_dbr3 = self.opexpdbr1_mon_dbr4 = self.opexpdbr1_mon_dbr5 = self.opexpdbr1_mon_dbr6 = self.opexpdbr1_mon_dbr7 = self.opexpdbr1_mon_dbr8 = self.opexpdbr1_mon_dbr9 = self.opexpdbr1_mon_dbr10 = self.opexpdbr1_mon_dbr11 = self.opexpdbr1_mon_dbr12 = self.opexpdbr1_mon_dbr13 = 0.00
#        self.taxdbr1_mon_dbr1 = self.taxdbr1_mon_dbr2 = self.taxdbr1_mon_dbr3 = self.taxdbr1_mon_dbr4 = self.taxdbr1_mon_dbr5 = self.taxdbr1_mon_dbr6 = self.taxdbr1_mon_dbr7 = self.taxdbr1_mon_dbr8 = self.taxdbr1_mon_dbr9 = self.taxdbr1_mon_dbr10 = self.taxdbr1_mon_dbr11 = self.taxdbr1_mon_dbr12 = self.taxdbr1_mon_dbr13 = 0.00
#        self.expdbr1_mon_dbr1 = self.expdbr1_mon_dbr2 = self.expdbr1_mon_dbr3 = self.expdbr1_mon_dbr4 = self.expdbr1_mon_dbr5 = self.expdbr1_mon_dbr6 = self.expdbr1_mon_dbr7 = self.expdbr1_mon_dbr8 = self.expdbr1_mon_dbr9 = self.expdbr1_mon_dbr10 = self.expdbr1_mon_dbr11 = self.expdbr1_mon_dbr12 = self.expdbr1_mon_dbr13 = 0.00
#        self.incomedbr1_mon_dbr1 = self.incomedbr1_mon_dbr2 = self.incomedbr1_mon_dbr3 = self.incomedbr1_mon_dbr4 = self.incomedbr1_mon_dbr5 = self.incomedbr1_mon_dbr6 = self.incomedbr1_mon_dbr7 = self.incomedbr1_mon_dbr8 = self.incomedbr1_mon_dbr9 = self.incomedbr1_mon_dbr10 = self.incomedbr1_mon_dbr11 = self.incomedbr1_mon_dbr12 = self.incomedbr1_mon_dbr13 = 0.00
#        self.total_expense_dbr1_mon_dbr1 = self.total_expense_dbr1_mon_dbr2 = self.total_expense_dbr1_mon_dbr3 = self.total_expense_dbr1_mon_dbr4 = self.total_expense_dbr1_mon_dbr5 = self.total_expense_dbr1_mon_dbr6 = self.total_expense_dbr1_mon_dbr7 = self.total_expense_dbr1_mon_dbr8 = self.total_expense_dbr1_mon_dbr9 = self.total_expense_dbr1_mon_dbr10 = self.total_expense_dbr1_mon_dbr11 = self.total_expense_dbr1_mon_dbr12 = self.total_expense_dbr1_mon_dbr13 = 0.00
#        self.net_profit_dbr1_mon_dbr1 = self.net_profit_dbr1_mon_dbr2 = self.net_profit_dbr1_mon_dbr3 = self.net_profit_dbr1_mon_dbr4 = self.net_profit_dbr1_mon_dbr5 = self.net_profit_dbr1_mon_dbr6 = self.net_profit_dbr1_mon_dbr7 = self.net_profit_dbr1_mon_dbr8 = self.net_profit_dbr1_mon_dbr9 = self.net_profit_dbr1_mon_dbr10 = self.net_profit_dbr1_mon_dbr11 = self.net_profit_dbr1_mon_dbr12 = self.net_profit_dbr1_mon_dbr13 = 0.00
#        self.liabilitiesdbr1_mon_dbr1 = self.liabilitiesdbr1_mon_dbr2 = self.liabilitiesdbr1_mon_dbr3 = self.liabilitiesdbr1_mon_dbr4 = self.liabilitiesdbr1_mon_dbr5 = self.liabilitiesdbr1_mon_dbr6 = self.liabilitiesdbr1_mon_dbr7 = self.liabilitiesdbr1_mon_dbr8 = self.liabilitiesdbr1_mon_dbr9 = self.liabilitiesdbr1_mon_dbr10 = self.liabilitiesdbr1_mon_dbr11 = self.liabilitiesdbr1_mon_dbr12 = self.liabilitiesdbr1_mon_dbr13 = 0.00
#        self.equitydbr1_mon = self.equitydbr2_mon = self.equitydbr3_mon = self.equitydbr4_mon = self.equitydbr5_mon = self.equitydbr6_mon = self.equitydbr7_mon  = self.equitydbr8_mon = self.equitydbr9_mon = self.equitydbr10_mon = self.equitydbr11_mon = self.equitydbr12_mon = self.equitydbr13_mon = 0.00
#        self.total_liabilities_dbr1_mon = self.total_liabilities_dbr2_mon = self.total_liabilities_dbr3_mon = self.total_liabilities_dbr4_mon = self.total_liabilities_dbr5_mon = self.total_liabilities_dbr6_mon = self.total_liabilities_dbr7_mon  = self.total_liabilities_dbr8_mon = self.total_liabilities_dbr9_mon = self.total_liabilities_dbr10_mon = self.total_liabilities_dbr11_mon = self.total_liabilities_dbr12_mon = self.total_liabilities_dbr13_mon = 0.00
#        
#        ######## Comp0 ########
#        self.comp0_tot_revenue = 0.00
#        self.comp0_tot_cogs = 0.00
#        self.comp0_gross_profit = 0.00
#        self.comp0_total_expense = 0.00
#        self.comp0_operating_expense = 0.00
#        self.comp0_taxes = 0.00
#        self.comp0_other_expense = 0.00
#        self.comp0_other_income = 0.00
#        self.comp0_net_profit = 0.00
#        self.comp0_tot_liabilities = 0.00
#        self.comp0_tot_equity = 0.00
#        self.comp0_tot_liabilities_equity = 0.00
#        self.comp0_profit_to_loss = 0.00
#        self.comp0_bal = 0.00
#        
#        ######## Comp1 ########
#        self.comp1_tot_revenue = 0.00
#        self.comp1_tot_cogs = 0.00
#        self.comp1_gross_profit = 0.00
#        self.comp1_total_expense = 0.00
#        self.comp1_operating_expense = 0.00
#        self.comp1_taxes = 0.00
#        self.comp1_other_expense = 0.00
#        self.comp1_other_income = 0.00
#        self.comp1_net_profit = 0.00
#        self.comp1_tot_liabilities = 0.00
#        self.comp1_tot_equity = 0.00
#        self.comp1_tot_liabilities_equity = 0.00
#        self.comp1_profit_to_loss = 0.00
#        self.comp1_bal = 0.00
#        
        super(account_balance_inherit, self).__init__(cr, uid, name, context)
            
    def lines(self, form, level=0):
        """
        Returns all the data needed for the report lines
        (account info plus debit/credit/balance in the selected period
        and the full year)
        """
        account_obj = self.pool.get('account.account')
        account_type_obj = self.pool.get('account.account.type')
        period_obj = self.pool.get('account.period')
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        wiz_rep = self.pool.get('wizard.report')
        afr_obj = self.pool.get('afr')
        self.show_earnings = False
        ids = []
        acc_ids = []
#        rev = 0.00
#        cogs = 0.00
#        opexp = 0.00
#        tax = 0.00
#        other_income = 0.00
#        other_expense = 0.00
#        tot_balance = 0.00
        bal = []
        bal_list = []
        dict = {}
#        if 'earning_account' in form and not isinstance(form['earning_account'], int):
#            form['earning_account'] = form['earning_account'][0]
        def _get_children_and_consol(cr, uid, ids, level, context={}, change_sign=False):
            aa_obj = self.pool.get('account.account')
            ids2=[]
#            ctx_bal =_ctx_end(self.context.copy())
#            ctx_in =_ctx_init(self.context.copy())
#            net_bal = 0.00
#            user_type = ['Revenue', 'Cost Of Goods Sold', 'Expense', 'Other Income', 'Other Expense']
#            acc_ids = aa_obj.search(self.cr, self.uid, [('type', '=', 'view'), ('level', '=', 1), ('user_type', 'in', user_type)])
#            for acc in acc_ids:
#                acc_data_browse = aa_obj.browse(self.cr, self.uid, acc, ctx_bal)
#                Aacc_data_browse = aa_obj.browse(self.cr, self.uid, acc, ctx_in)
#                bal = acc_data_browse.balance + Aacc_data_browse.balance
#                net_bal += bal

#            for acc in acc_ids:
#                acc_data_browse = aa_obj.browse(self.cr, self.uid, acc, ctx_bal)
#                Aacc_data_browse = aa_obj.browse(self.cr, self.uid, acc, ctx_in)
#                bal = acc_data_browse.balance + Aacc_data_browse.balance
#                if acc_data_browse.name.lower() == 'revenue':
#                    rev = bal
#                if acc_data_browse.name.lower() == 'cost of goods sold':
#                    cogs = bal
#                if acc_data_browse.name.lower() == 'operating expenses':
#                    opexp = bal
#                if acc_data_browse.name.lower() == 'taxes':
#                    tax = bal
#                if acc_data_browse.name.lower() == 'other income':
#                    other_income = bal
#                if acc_data_browse.name.lower() == 'other expense':
#                    other_expense = bal
#            tot_balance = rev + cogs + opexp + tax + other_income + other_expense
#            if form['inf_type'] == 'BS':
#                self.bal = net_bal
            for aa_brw in aa_obj.browse(cr, uid, ids, context):
                if aa_brw.child_id and aa_brw.level < level and aa_brw.type !='consolidation':
                    if not change_sign:
                        ids2.append([aa_brw.id, True, False, aa_brw])
                    ids2 += _get_children_and_consol(cr, uid, [x.id for x in aa_brw.child_id], level, context, change_sign=change_sign)
                    if change_sign:
                        ids2.append(aa_brw.id)
                    else:
                        ids2.append([aa_brw.id, False, True, aa_brw])
                else:
                    if change_sign:
                        ids2.append(aa_brw.id)
                    else:
                        ids2.append([aa_brw.id, True, True, aa_brw])
            return ids2

        #############################################################################
        # CONTEXT FOR ENDIND BALANCE                                                #
        #############################################################################

        def _ctx_end(ctx):
            ctx_end = ctx
            ctx_end['filter'] = form.get('filter', 'all')
            ctx_end['fiscalyear'] = fiscalyear.id
            #~ ctx_end['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',fiscalyear.id),('special','=',False)])
            
            if ctx_end['filter'] not in ['bydate', 'none']:
                special = self.special_period(form['periods'])
            else:
                special = False
            
            if form['filter'] in ['byperiod', 'all']:
                if special:
                    ctx_end['periods'] = period_obj.search(self.cr, self.uid, [('id', 'in', form['periods'] or ctx_end.get('periods', False))])
                else:
                    ctx_end['periods'] = period_obj.search(self.cr, self.uid, [('id','in',form['periods'] or ctx_end.get('periods',False))])
            if form['filter'] in ['bydate', 'all', 'none']:
                ctx_end['date_from'] = form['date_from']
                ctx_end['date_to'] = form['date_to']
            return ctx_end.copy()
        
        def missing_period(ctx_init):
            
            ctx_init['fiscalyear'] = fiscalyear_obj.search(self.cr, self.uid, [('date_stop', '<', fiscalyear.date_start)], order='date_stop') and \
                                fiscalyear_obj.search(self.cr, self.uid, [('date_stop', '<', fiscalyear.date_start)], order='date_stop')[-1] or []
            ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', ctx_init['fiscalyear']), ('date_stop', '<', fiscalyear.date_start)])
            return ctx_init
        #############################################################################
        # CONTEXT FOR INITIAL BALANCE                                               #
        #############################################################################
        
        def _ctx_init(ctx):
            ctx_init = self.context.copy()
            ctx_init['filter'] = form.get('filter', 'all')
            ctx_init['fiscalyear'] = fiscalyear.id

            if form['filter'] in ['byperiod', 'all']:
                ctx_init['periods'] = form['periods']
                if not ctx_init['periods']:
                    ctx_init = missing_period(ctx_init.copy())
                date_start = min([period.date_start for period in period_obj.browse(self.cr, self.uid, ctx_init['periods'])])
                ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', fiscalyear.id), ('date_stop', '<=', date_start)])
            elif form['filter'] in ['bydate']:
                ctx_init['date_from'] = fiscalyear.date_start
                ctx_init['date_to'] = form['date_from']
                ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', fiscalyear.id), ('date_stop', '<=', ctx_init['date_to'])])
            elif form['filter'] == 'none':
                ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', fiscalyear.id), ('special', '=', True)])
                date_start = min([period.date_start for period in period_obj.browse(self.cr, self.uid, ctx_init['periods'])])
                ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', fiscalyear.id), ('date_start', '<=', date_start), ('special', '=', True)])
            
            return ctx_init.copy()

        def z(n):
            return abs(n) < 0.005 and 0.0 or n
                

        self.from_currency_id = self.get_company_currency(form['company_id'] and type(form['company_id']) in (list, tuple) and form['company_id'][0] or form['company_id'])
        if not form['currency_id']:
            self.to_currency_id = self.from_currency_id
        else:
            self.to_currency_id = form['currency_id'] and type(form['currency_id']) in (list, tuple) and form['currency_id'][0] or form['currency_id']
        selected_accounts = []
        if form.has_key('account_list') and form['account_list']:
            selected_accounts = form['account_list']
            account_ids = form['account_list']
#            del form['account_list']
        
        credit_account_ids = self.get_company_accounts(form['company_id'] and type(form['company_id']) in (list, tuple) and form['company_id'][0] or form['company_id'], 'credit')
        
        debit_account_ids = self.get_company_accounts(form['company_id'] and type(form['company_id']) in (list, tuple) and form['company_id'][0] or form['company_id'], 'debit')

        if form.get('fiscalyear'):
            if type(form.get('fiscalyear')) in (list, tuple):
                fiscalyear = form['fiscalyear'] and form['fiscalyear'][0]
            elif type(form.get('fiscalyear')) in (int,):
                fiscalyear = form['fiscalyear']
        fiscalyear = fiscalyear_obj.browse(self.cr, self.uid, fiscalyear)

        ################################################################
        # Get the accounts                                             #
        ################################################################
        
        account_ids = _get_children_and_consol(self.cr, self.uid, account_ids, form['display_account_level'] and form['display_account_level'] or 100, self.context)
        
        credit_account_ids = _get_children_and_consol(self.cr, self.uid, credit_account_ids, 100, self.context, change_sign=True)
        
        debit_account_ids = _get_children_and_consol(self.cr, self.uid, debit_account_ids, 100, self.context, change_sign=True)
        
        credit_account_ids = list(set(credit_account_ids) - set(debit_account_ids))

        #
        # Generate the report lines (checking each account)
        #
        
        tot_check = False
        
        if not form['periods']:
            form['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',fiscalyear.id)],order='date_start asc')
            if not form['periods']:
                raise osv.except_osv(_('UserError'), _('The Selected Fiscal Year Does not have Regular Periods'))

        if form['columns'] == 'qtr':
            period_ids = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',fiscalyear.id)],order='date_start asc')
            a=0
            l=[]
            p=[]
            for x in period_ids:
                a+=1
                if a<3:
                        l.append(x)
                else:
                        l.append(x)
                        p.append(l)
                        l=[]
                        a=0
            
            #~ period_ids = p

        elif form['columns'] == 'thirteen':
            period_ids = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',fiscalyear.id)],order='date_start asc')

#        if form['columns'] == 'qtr':
#            tot_bal1 = 0.0
#            tot_bal2 = 0.0
#            tot_bal3 = 0.0
#            tot_bal4 = 0.0
#            tot_bal5 = 0.0
#
#        elif form['columns'] == 'thirteen':
#            tot_bal1 = 0.0
#            tot_bal2 = 0.0
#            tot_bal3 = 0.0
#            tot_bal4 = 0.0
#            tot_bal5 = 0.0
#            tot_bal6 = 0.0
#            tot_bal7 = 0.0
#            tot_bal8 = 0.0
#            tot_bal9 = 0.0
#            tot_bal10 = 0.0
#            tot_bal11 = 0.0
#            tot_bal12 = 0.0
#            tot_bal13 = 0.0

        else:
            
            ctx_init = _ctx_init(self.context.copy())
            ctx_end = _ctx_end(self.context.copy())

            tot_bin = 0.0
            tot_deb = 0.0
            tot_crd = 0.0
            tot_ytd = 0.0
            tot_eje = 0.0
        
        res = {}
        result_acc = []
        tot = {}   
        ############################For getting the net balance for earning account
        net_balance = 0.0   
        temp_earning = {}  
        net_bal_temp = {}
        earning_data = {}
        ################################net calculation ends
        for aa_id in account_ids:
            id = aa_id[0]
            #
            # Check if we need to include this level
            #
            if not form['display_account_level'] or aa_id[3].level <= form['display_account_level']:
                res = {
                'id'        : id, 
                'type'      : aa_id[3].type, 
                'code'      : aa_id[3].code, 
                'name'      : (aa_id[2] and not aa_id[1]) and 'Total %s'%(aa_id[3].name) or aa_id[3].name, 
                'parent_id' : aa_id[3].parent_id and aa_id[3].parent_id.id, 
                'level'     : aa_id[3].level, 
                'label'     : aa_id[1], 
                'total'     : aa_id[2], 
                'change_sign' : credit_account_ids and (id  in credit_account_ids and -1 or 1) or 1
                }
                if form['columns'] == 'qtr':
                    pn = 1
                    for p_id in p:
                        form['periods'] = p_id
                        
                        ctx_init = _ctx_init(self.context.copy())
                        aa_brw_init = account_obj.browse(self.cr, self.uid, id, ctx_init)
                        
                        ctx_end = _ctx_end(self.context.copy())
                        aa_brw_end  = account_obj.browse(self.cr, self.uid, id, ctx_end)
                        
                        if form['inf_type'] == 'IS':
                            d, c, b = map(z, [aa_brw_end.debit, aa_brw_end.credit, aa_brw_end.balance])
                            res.update({
                                'dbr%s'%pn: self.exchange(d), 
                                'cdr%s'%pn: self.exchange(c), 
                                'bal%s'%pn: self.exchange(b), 
                            })
                        else:
                            i, d, c = map(z, [aa_brw_init.balance, aa_brw_end.debit, aa_brw_end.credit])
                            b = z(i+d-c)
                            res.update({
                                'dbr%s'%pn: self.exchange(d), 
                                'cdr%s'%pn: self.exchange(c), 
                                'bal%s'%pn: self.exchange(b), 
                            })
                        pn +=1
            
                    form['periods'] = period_ids
                    
                    ctx_init = _ctx_init(self.context.copy())
                    aa_brw_init = account_obj.browse(self.cr, self.uid, id, ctx_init)
                    
                    ctx_end = _ctx_end(self.context.copy())
                    aa_brw_end  = account_obj.browse(self.cr, self.uid, id, ctx_end)
                    
                    if form['inf_type'] == 'IS':
                        d, c, b = map(z, [aa_brw_end.debit, aa_brw_end.credit, aa_brw_init.balance])
                        
#                        tot_revenue_dbr1 = tot_revenue_dbr2 = tot_revenue_dbr3 = tot_revenue_dbr4 = tot_revenue_dbr5 = 0.00
#                        tgcs_dbr1 = tgcs_dbr2 = tgcs_dbr3 = tgcs_dbr4 = tgcs_dbr5 = 0.00
                        res.update({
                            'balance': self.exchange(d-c), 
                        })
                        res.update({
                            'dbr5': self.exchange(d), 
                            'cdr5': self.exchange(c), 
                            'bal5': self.exchange(b), 
                        })
                        
#                        if res.get('name').lower() == 'total revenue':
#                            self.tot_revenue = b + float(res.get('balance'))
#                            self.tot_revenue_dbr1 = res.get('bal1')
#                            self.tot_revenue_dbr2 = res.get('bal2')
#                            self.tot_revenue_dbr3 = res.get('bal3')
#                            self.tot_revenue_dbr4 = res.get('bal4')
#                            self.tot_revenue_dbr5 = res.get('bal5')
#                        if res.get('name').lower() == 'total cost of goods sold':
#                            self.tot_cogs = res.get('balance')
#                            self.tgcs_dbr1 = res.get('bal1')
#                            self.tgcs_dbr2 = res.get('bal2')
#                            self.tgcs_dbr3 = res.get('bal3')
#                            self.tgcs_dbr4 = res.get('bal4')
#                            self.tgcs_dbr5 = res.get('bal5')
#                        self.gross_profit = abs(self.tot_revenue) - abs(self.tot_cogs)
#                        self.gross_profit_dbr1 = self.tot_revenue_dbr1 - self.tgcs_dbr1
#                        self.gross_profit_dbr2 = self.tot_revenue_dbr2 - self.tgcs_dbr2
#                        self.gross_profit_dbr3 = self.tot_revenue_dbr3 - self.tgcs_dbr3
#                        self.gross_profit_dbr4 = self.tot_revenue_dbr4 - self.tgcs_dbr4
#                        self.gross_profit_dbr5 = self.tot_revenue_dbr5 - self.tgcs_dbr5
#                        if res.get('name').lower() == 'total cost of goods sold':
#                            result_acc.append({'id': False, 'name': ''})
#                        if res.get('name').lower() == 'total operating expenses':
#                            self.operating_expense = res.get('balance')
#                            self.opexpdbr1 = res.get('bal1')
#                            self.opexpdbr2 = res.get('bal2')
#                            self.opexpdbr3 = res.get('bal3')
#                            self.opexpdbr4 = res.get('bal4')
#                            self.opexpdbr5 = res.get('bal5')
#                        if res.get('name').lower() == 'total taxes':
#                            self.taxes = res.get('balance')
#                            self.taxdbr1 = res.get('bal1')
#                            self.taxdbr2 = res.get('bal2')
#                            self.taxdbr3 = res.get('bal3')
#                            self.taxdbr4 = res.get('bal4')
#                            self.taxdbr5 = res.get('bal5')
#                        if res.get('name').lower() == 'total other expense':
#                            self.other_expense = res.get('balance')
#                            self.expdbr1 = res.get('bal1')
#                            self.expdbr2 = res.get('bal2')
#                            self.expdbr3 = res.get('bal3')
#                            self.expdbr4 = res.get('bal4')
#                            self.expdbr5 = res.get('bal5')
#                        if res.get('name').lower() == 'total other income':
#                            self.other_income = res.get('balance')
#                            self.incomedbr1 = res.get('bal1')
#                            self.incomedbr2 = res.get('bal2')
#                            self.incomedbr3 = res.get('bal3')
#                            self.incomedbr4 = res.get('bal4')
#                            self.incomedbr5 = res.get('bal5')
#                        self.total_expense = self.operating_expense + self.taxes + self.other_expense
#                        self.total_expense_dbr1 = self.opexpdbr1 + self.taxdbr1 + self.expdbr1
#                        self.total_expense_dbr2 = self.opexpdbr2 + self.taxdbr2 + self.expdbr2
#                        self.total_expense_dbr3 = self.opexpdbr3 + self.taxdbr3 + self.expdbr3
#                        self.total_expense_dbr4 = self.opexpdbr4 + self.taxdbr4 + self.expdbr4
#                        self.total_expense_dbr5 = self.opexpdbr5 + self.taxdbr5 + self.expdbr5
#                        
#                        self.net_profit = self.gross_profit + self.other_income - self.total_expense
#                        self.net_profit_dbr1 = abs(self.gross_profit_dbr1 - abs(self.incomedbr1 + self.total_expense_dbr1))
#                        self.net_profit_dbr2 = abs(self.gross_profit_dbr2 - abs(self.incomedbr2 + self.total_expense_dbr2))
#                        self.net_profit_dbr3 = abs(self.gross_profit_dbr3 - abs(self.incomedbr3 + self.total_expense_dbr3))
#                        self.net_profit_dbr4 = abs(self.gross_profit_dbr4 - abs(self.incomedbr4 + self.total_expense_dbr4))
#                        self.net_profit_dbr5 = abs(self.gross_profit_dbr5 - abs(self.incomedbr5 + self.total_expense_dbr5))
#                        form['net_profit1'] = self.net_profit_dbr1
#                        form['net_profit2'] = self.net_profit_dbr2
#                        form['net_profit3'] = self.net_profit_dbr3
#                        form['net_profit4'] = self.net_profit_dbr4
#                        form['net_profit5'] = self.net_profit_dbr5

                    else:
                        i, d, c = map(z, [aa_brw_init.balance, aa_brw_end.debit, aa_brw_end.credit])
                        b = z(i+d-c)
                        res.update({
                            'balance': self.exchange(d-c), 
                        })
                        res.update({
                            'dbr5': self.exchange(d), 
                            'cdr5': self.exchange(c), 
                            'bal5': self.exchange(b), 
                        })
#                        if res.get('name').lower() == 'total liabilities':
#                            self.tot_liabilities = res.get('balance')
#                            self.liabilitiesdbr1 = res.get('bal1')
#                            self.liabilitiesdbr2 = res.get('bal2')
#                            self.liabilitiesdbr3 = res.get('bal3')
#                            self.liabilitiesdbr4 = res.get('bal4')
#                            self.liabilitiesdbr5 = res.get('bal5')
#                        if res.get('name').lower() == 'total equity':
#                            self.tot_equity = res.get('balance')
#                            self.equitydbr1 = res.get('bal1')
#                            self.equitydbr2 = res.get('bal2')
#                            self.equitydbr3 = res.get('bal3')
#                            self.equitydbr4 = res.get('bal4')
#                            self.equitydbr5 = res.get('bal5')
#                        self.tot_liabilities_equity = self.tot_liabilities + self.tot_equity
#                        self.total_liabilities_dbr1 = self.liabilitiesdbr1 + self.equitydbr1
#                        self.total_liabilities_dbr2 = self.liabilitiesdbr2 + self.equitydbr2
#                        self.total_liabilities_dbr3 = self.liabilitiesdbr3 + self.equitydbr3
#                        self.total_liabilities_dbr4 = self.liabilitiesdbr4 + self.equitydbr4
#                        self.total_liabilities_dbr5 = self.liabilitiesdbr5 + self.equitydbr5
                
                elif form['columns'] == 'thirteen':
                    pn = 1
                    for p_id in period_ids:
                        form['periods'] = [p_id]
                        
                        ctx_init = _ctx_init(self.context.copy())
                        aa_brw_init = account_obj.browse(self.cr, self.uid, id, ctx_init)
                        
                        ctx_end = _ctx_end(self.context.copy())
                        aa_brw_end  = account_obj.browse(self.cr, self.uid, id, ctx_end)
                        
                        if form['inf_type'] == 'IS':
                            d, c, b = map(z, [aa_brw_end.debit, aa_brw_end.credit, aa_brw_end.balance])
                            res.update({
                                'dbr%s'%pn: self.exchange(d), 
                                'cdr%s'%pn: self.exchange(c), 
                                'bal%s'%pn: self.exchange(b), 
                            })
                            
                        else:
                            i, d, c = map(z, [aa_brw_init.balance, aa_brw_end.debit, aa_brw_end.credit])
                            b = z(i+d-c)
                            #For finding the earnings account
                            res.update({
                            'balance': self.exchange(d-c), 
                            })
                            res.update({
                                'dbr%s'%pn: self.exchange(d), 
                                'cdr%s'%pn: self.exchange(c), 
                                'bal%s'%pn: self.exchange(b), 
                            })
                        pn +=1
            
                    form['periods'] = period_ids
                    
                    ctx_init = _ctx_init(self.context.copy())
                    aa_brw_init = account_obj.browse(self.cr, self.uid, id, ctx_init)
                    
                    ctx_end = _ctx_end(self.context.copy())
                    aa_brw_end  = account_obj.browse(self.cr, self.uid, id, ctx_end)
                    
                    if form['inf_type'] == 'IS':
                        d, c, b = map(z, [aa_brw_end.debit, aa_brw_end.credit, aa_brw_init.balance])
                        res.update({
                            'balance': self.exchange(d-c), 
                        })
                        res.update({
                            'dbr13': self.exchange(d), 
                            'cdr13': self.exchange(c), 
                            'bal13': self.exchange(b), 
                        })
                        
#                        if res.get('name').lower() == 'total revenue':
#                            self.tot_revenue = b + float(res.get('balance'))
#                            self.tot_revenue_mon_dbr1 = res.get('bal1')
#                            self.tot_revenue_mon_dbr2 = res.get('bal2')
#                            self.tot_revenue_mon_dbr3 = res.get('bal3')
#                            self.tot_revenue_mon_dbr4 = res.get('bal4')
#                            self.tot_revenue_mon_dbr5 = res.get('bal5')
#                            self.tot_revenue_mon_dbr6 = res.get('bal6')
#                            self.tot_revenue_mon_dbr7 = res.get('bal7')
#                            self.tot_revenue_mon_dbr8 = res.get('bal8')
#                            self.tot_revenue_mon_dbr9 = res.get('bal9')
#                            self.tot_revenue_mon_dbr10 = res.get('bal10')
#                            self.tot_revenue_mon_dbr11 = res.get('bal11')
#                            self.tot_revenue_mon_dbr12 = res.get('bal12')
#                            self.tot_revenue_mon_dbr13 = res.get('bal13')
#                        if res.get('name').lower() == 'total cost of goods sold':
#                            self.tot_cogs = res.get('balance')
#                            self.tgcs_mon_dbr1 = res.get('bal1')
#                            self.tgcs_mon_dbr2 = res.get('bal2')
#                            self.tgcs_mon_dbr3 = res.get('bal3')
#                            self.tgcs_mon_dbr4 = res.get('bal4')
#                            self.tgcs_mon_dbr5 = res.get('bal5')
#                            self.tgcs_mon_dbr6 = res.get('bal6')
#                            self.tgcs_mon_dbr7 = res.get('bal7')
#                            self.tgcs_mon_dbr8 = res.get('bal8')
#                            self.tgcs_mon_dbr9 = res.get('bal9')
#                            self.tgcs_mon_dbr10 = res.get('bal10')
#                            self.tgcs_mon_dbr11 = res.get('bal11')
#                            self.tgcs_mon_dbr12 = res.get('bal12')
#                            self.tgcs_mon_dbr13 = res.get('bal13')
#                        self.gross_profit = abs(self.tot_revenue) - abs(self.tot_cogs)
#                        self.gross_profit_mon_dbr1 = abs(self.tot_revenue_mon_dbr1) - abs(self.tgcs_mon_dbr1)
#                        self.gross_profit_mon_dbr2 = abs(self.tot_revenue_mon_dbr2) - abs(self.tgcs_mon_dbr2)
#                        self.gross_profit_mon_dbr3 = abs(self.tot_revenue_mon_dbr3) - abs(self.tgcs_mon_dbr3)
#                        self.gross_profit_mon_dbr4 = abs(self.tot_revenue_mon_dbr4) - abs(self.tgcs_mon_dbr4)
#                        self.gross_profit_mon_dbr5 = abs(self.tot_revenue_mon_dbr5) - abs(self.tgcs_mon_dbr5)
#                        self.gross_profit_mon_dbr6 = abs(self.tot_revenue_mon_dbr6) - abs(self.tgcs_mon_dbr6)
#                        self.gross_profit_mon_dbr7 = abs(self.tot_revenue_mon_dbr7) - abs(self.tgcs_mon_dbr7)
#                        self.gross_profit_mon_dbr8 = abs(self.tot_revenue_mon_dbr8) - abs(self.tgcs_mon_dbr8)
#                        self.gross_profit_mon_dbr9 = abs(self.tot_revenue_mon_dbr9) - abs(self.tgcs_mon_dbr9)
#                        self.gross_profit_mon_dbr10 = abs(self.tot_revenue_mon_dbr10) - abs(self.tgcs_mon_dbr10)
#                        self.gross_profit_mon_dbr11 = abs(self.tot_revenue_mon_dbr11) - abs(self.tgcs_mon_dbr11)
#                        self.gross_profit_mon_dbr12 = abs(self.tot_revenue_mon_dbr12) - abs(self.tgcs_mon_dbr12)
#                        self.gross_profit_mon_dbr13 = abs(self.tot_revenue_mon_dbr13) - abs(self.tgcs_mon_dbr13)
#                        if res.get('name').lower() == 'total cost of goods sold':
#                            result_acc.append({'id': False, 'name': ''})
#                        if res.get('name').lower() == 'total operating expenses':
#                            self.operating_expense = res.get('balance')
#                            self.opexpdbr1_mon_dbr1 = res.get('bal1')
#                            self.opexpdbr1_mon_dbr2 = res.get('bal2')
#                            self.opexpdbr1_mon_dbr3 = res.get('bal3')
#                            self.opexpdbr1_mon_dbr4 = res.get('bal4')
#                            self.opexpdbr1_mon_dbr5 = res.get('bal5')
#                            self.opexpdbr1_mon_dbr6 = res.get('bal6')
#                            self.opexpdbr1_mon_dbr7 = res.get('bal7')
#                            self.opexpdbr1_mon_dbr8 = res.get('bal8')
#                            self.opexpdbr1_mon_dbr9 = res.get('bal9')
#                            self.opexpdbr1_mon_dbr10 = res.get('bal10')
#                            self.opexpdbr1_mon_dbr11 = res.get('bal11')
#                            self.opexpdbr1_mon_dbr12 = res.get('bal12')
#                            self.opexpdbr1_mon_dbr13 = res.get('bal13')
#                        if res.get('name').lower() == 'total taxes':
#                            self.taxes = res.get('balance')
#                            self.taxdbr1_mon_dbr1 = res.get('bal1')
#                            self.taxdbr1_mon_dbr2 = res.get('bal2')
#                            self.taxdbr1_mon_dbr3 = res.get('bal3')
#                            self.taxdbr1_mon_dbr4 = res.get('bal4')
#                            self.taxdbr1_mon_dbr5 = res.get('bal5')
#                            self.taxdbr1_mon_dbr6 = res.get('bal6')
#                            self.taxdbr1_mon_dbr7 = res.get('bal7')
#                            self.taxdbr1_mon_dbr8 = res.get('bal8')
#                            self.taxdbr1_mon_dbr9 = res.get('bal9')
#                            self.taxdbr1_mon_dbr10 = res.get('bal10')
#                            self.taxdbr1_mon_dbr11 = res.get('bal11')
#                            self.taxdbr1_mon_dbr12 = res.get('bal12')
#                            self.taxdbr1_mon_dbr13 = res.get('bal13')
#                        if res.get('name').lower() == 'total other expense':
#                            self.other_expense = res.get('balance')
#                            self.expdbr1_mon_dbr1 = res.get('bal1')
#                            self.expdbr1_mon_dbr2 = res.get('bal2')
#                            self.expdbr1_mon_dbr3 = res.get('bal3')
#                            self.expdbr1_mon_dbr4 = res.get('bal4')
#                            self.expdbr1_mon_dbr5 = res.get('bal5')
#                            self.expdbr1_mon_dbr6 = res.get('bal6')
#                            self.expdbr1_mon_dbr7 = res.get('bal7')
#                            self.expdbr1_mon_dbr8 = res.get('bal8')
#                            self.expdbr1_mon_dbr9 = res.get('bal9')
#                            self.expdbr1_mon_dbr10 = res.get('bal10')
#                            self.expdbr1_mon_dbr11 = res.get('bal11')
#                            self.expdbr1_mon_dbr12 = res.get('bal12')
#                            self.expdbr1_mon_dbr13 = res.get('bal13')
#                        if res.get('name').lower() == 'total other income':
#                            self.other_income = res.get('balance')
#                            self.incomedbr1_mon_dbr1 = res.get('bal1')
#                            self.incomedbr1_mon_dbr2 = res.get('bal2')
#                            self.incomedbr1_mon_dbr3 = res.get('bal3')
#                            self.incomedbr1_mon_dbr4 = res.get('bal4')
#                            self.incomedbr1_mon_dbr5 = res.get('bal5')
#                            self.incomedbr1_mon_dbr6 = res.get('bal6')
#                            self.incomedbr1_mon_dbr7 = res.get('bal7')
#                            self.incomedbr1_mon_dbr8 = res.get('bal8')
#                            self.incomedbr1_mon_dbr9 = res.get('bal9')
#                            self.incomedbr1_mon_dbr10 = res.get('bal10')
#                            self.incomedbr1_mon_dbr11 = res.get('bal11')
#                            self.incomedbr1_mon_dbr12 = res.get('bal12')
#                            self.incomedbr1_mon_dbr13 = res.get('bal13')
#                            
#                        self.total_expense = self.operating_expense + self.taxes + self.other_expense
#                        self.total_expense_dbr1_mon_dbr1 = self.opexpdbr1_mon_dbr1 + self.taxdbr1_mon_dbr1 + self.expdbr1_mon_dbr1
#                        self.total_expense_dbr1_mon_dbr2 = self.opexpdbr1_mon_dbr2 + self.taxdbr1_mon_dbr2 + self.expdbr1_mon_dbr2
#                        self.total_expense_dbr1_mon_dbr3 = self.opexpdbr1_mon_dbr3 + self.taxdbr1_mon_dbr3 + self.expdbr1_mon_dbr3
#                        self.total_expense_dbr1_mon_dbr4 = self.opexpdbr1_mon_dbr4 + self.taxdbr1_mon_dbr4 + self.expdbr1_mon_dbr4
#                        self.total_expense_dbr1_mon_dbr5 = self.opexpdbr1_mon_dbr5 + self.taxdbr1_mon_dbr5 + self.expdbr1_mon_dbr5
#                        self.total_expense_dbr1_mon_dbr6 = self.opexpdbr1_mon_dbr6 + self.taxdbr1_mon_dbr6 + self.expdbr1_mon_dbr6
#                        self.total_expense_dbr1_mon_dbr7 = self.opexpdbr1_mon_dbr7 + self.taxdbr1_mon_dbr7 + self.expdbr1_mon_dbr7
#                        self.total_expense_dbr1_mon_dbr8 = self.opexpdbr1_mon_dbr8 + self.taxdbr1_mon_dbr8 + self.expdbr1_mon_dbr8
#                        self.total_expense_dbr1_mon_dbr9 = self.opexpdbr1_mon_dbr9 + self.taxdbr1_mon_dbr9 + self.expdbr1_mon_dbr9
#                        self.total_expense_dbr1_mon_dbr10 = self.opexpdbr1_mon_dbr10 + self.taxdbr1_mon_dbr10 + self.expdbr1_mon_dbr10
#                        self.total_expense_dbr1_mon_dbr11 = self.opexpdbr1_mon_dbr11 + self.taxdbr1_mon_dbr11 + self.expdbr1_mon_dbr11
#                        self.total_expense_dbr1_mon_dbr12 = self.opexpdbr1_mon_dbr12 + self.taxdbr1_mon_dbr12 + self.expdbr1_mon_dbr12
#                        self.total_expense_dbr1_mon_dbr13 = self.opexpdbr1_mon_dbr13 + self.taxdbr1_mon_dbr13 + self.expdbr1_mon_dbr13
#                        
#                        self.net_profit = self.gross_profit + self.other_income - self.total_expense
#                        self.net_profit_dbr1_mon_dbr1 = abs(self.gross_profit_mon_dbr1 - abs(self.incomedbr1_mon_dbr1 + self.total_expense_dbr1_mon_dbr1))
#                        self.net_profit_dbr1_mon_dbr2 = abs(self.gross_profit_mon_dbr2 - abs(self.incomedbr1_mon_dbr2 + self.total_expense_dbr1_mon_dbr2))
#                        self.net_profit_dbr1_mon_dbr3 = abs(self.gross_profit_mon_dbr3 - abs(self.incomedbr1_mon_dbr3 + self.total_expense_dbr1_mon_dbr3))
#                        self.net_profit_dbr1_mon_dbr4 = abs(self.gross_profit_mon_dbr4 - abs(self.incomedbr1_mon_dbr4 + self.total_expense_dbr1_mon_dbr4))
#                        self.net_profit_dbr1_mon_dbr5 = abs(self.gross_profit_mon_dbr5 - abs(self.incomedbr1_mon_dbr5 + self.total_expense_dbr1_mon_dbr5))
#                        self.net_profit_dbr1_mon_dbr6 = abs(self.gross_profit_mon_dbr6 - abs(self.incomedbr1_mon_dbr6 + self.total_expense_dbr1_mon_dbr6))
#                        self.net_profit_dbr1_mon_dbr7 = abs(self.gross_profit_mon_dbr7 - abs(self.incomedbr1_mon_dbr7 + self.total_expense_dbr1_mon_dbr7))
#                        self.net_profit_dbr1_mon_dbr8 = abs(self.gross_profit_mon_dbr8 - abs(self.incomedbr1_mon_dbr8 + self.total_expense_dbr1_mon_dbr8))
#                        self.net_profit_dbr1_mon_dbr9 = abs(self.gross_profit_mon_dbr9 - abs(self.incomedbr1_mon_dbr9 + self.total_expense_dbr1_mon_dbr9))
#                        self.net_profit_dbr1_mon_dbr10 = abs(self.gross_profit_mon_dbr10 - abs(self.incomedbr1_mon_dbr10 + self.total_expense_dbr1_mon_dbr10))
#                        self.net_profit_dbr1_mon_dbr11 = abs(self.gross_profit_mon_dbr11 - abs(self.incomedbr1_mon_dbr11 + self.total_expense_dbr1_mon_dbr11))
#                        self.net_profit_dbr1_mon_dbr12 = abs(self.gross_profit_mon_dbr12 - abs(self.incomedbr1_mon_dbr12 + self.total_expense_dbr1_mon_dbr12))
#                        self.net_profit_dbr1_mon_dbr13 = abs(self.gross_profit_mon_dbr13 - abs(self.incomedbr1_mon_dbr13 + self.total_expense_dbr1_mon_dbr13))
#                        
#                        form['net_profit1'] = self.net_profit_dbr1_mon_dbr1
#                        form['net_profit2'] = self.net_profit_dbr1_mon_dbr2
#                        form['net_profit3'] = self.net_profit_dbr1_mon_dbr3
#                        form['net_profit4'] = self.net_profit_dbr1_mon_dbr4
#                        form['net_profit5'] = self.net_profit_dbr1_mon_dbr5
#                        form['net_profit6'] = self.net_profit_dbr1_mon_dbr6
#                        form['net_profit7'] = self.net_profit_dbr1_mon_dbr7
#                        form['net_profit8'] = self.net_profit_dbr1_mon_dbr8
#                        form['net_profit9'] = self.net_profit_dbr1_mon_dbr9
#                        form['net_profit10'] = self.net_profit_dbr1_mon_dbr10
#                        form['net_profit11'] = self.net_profit_dbr1_mon_dbr11
#                        form['net_profit12'] = self.net_profit_dbr1_mon_dbr12
#                        form['net_profit13'] = self.net_profit_dbr1_mon_dbr13
#                        
                        
                    else:
                        i, d, c = map(z, [aa_brw_init.balance, aa_brw_end.debit, aa_brw_end.credit])
                        b = z(i+d-c)
                        #For finding the earnings account
                        res.update({
                            'balance': self.exchange(d-c), 
                        })
                        res.update({
                            'dbr13': self.exchange(d), 
                            'cdr13': self.exchange(c), 
                            'bal13': self.exchange(b), 
                        })
#                        if res.get('name').lower() == 'total liabilities':
#                            self.tot_liabilities = res.get('balance')
#                            self.liabilitiesdbr1_mon_dbr1 = res.get('bal1')
#                            self.liabilitiesdbr1_mon_dbr2 = res.get('bal2')
#                            self.liabilitiesdbr1_mon_dbr3 = res.get('bal3')
#                            self.liabilitiesdbr1_mon_dbr4 = res.get('bal4')
#                            self.liabilitiesdbr1_mon_dbr5 = res.get('bal5')
#                            self.liabilitiesdbr1_mon_dbr6 = res.get('bal6')
#                            self.liabilitiesdbr1_mon_dbr7 = res.get('bal7')
#                            self.liabilitiesdbr1_mon_dbr8 = res.get('bal8')
#                            self.liabilitiesdbr1_mon_dbr9 = res.get('bal9')
#                            self.liabilitiesdbr1_mon_dbr10 = res.get('bal10')
#                            self.liabilitiesdbr1_mon_dbr11 = res.get('bal11')
#                            self.liabilitiesdbr1_mon_dbr12 = res.get('bal12')
#                            self.liabilitiesdbr1_mon_dbr13 = res.get('bal13')
#                        if res.get('name').lower() == 'total equity':
#                            self.tot_equity = res.get('balance')
#                            self.equitydbr1_mon = res.get('bal1')
#                            self.equitydbr2_mon = res.get('bal2')
#                            self.equitydbr3_mon = res.get('bal3')
#                            self.equitydbr4_mon = res.get('bal4')
#                            self.equitydbr5_mon = res.get('bal5')
#                            self.equitydbr6_mon = res.get('bal6')
#                            self.equitydbr7_mon = res.get('bal7')
#                            self.equitydbr8_mon = res.get('bal8')
#                            self.equitydbr9_mon = res.get('bal9')
#                            self.equitydbr10_mon = res.get('bal10')
#                            self.equitydbr11_mon = res.get('bal11')
#                            self.equitydbr12_mon = res.get('bal12')
#                            self.equitydbr13_mon = res.get('bal13')
#                        self.tot_liabilities_equity = self.tot_liabilities + self.tot_equity
#                        self.total_liabilities_dbr1_mon = self.liabilitiesdbr1_mon_dbr1 + self.equitydbr1_mon
#                        self.total_liabilities_dbr2_mon = self.liabilitiesdbr1_mon_dbr2 + self.equitydbr2_mon
#                        self.total_liabilities_dbr3_mon = self.liabilitiesdbr1_mon_dbr3 + self.equitydbr3_mon
#                        self.total_liabilities_dbr4_mon = self.liabilitiesdbr1_mon_dbr4 + self.equitydbr4_mon
#                        self.total_liabilities_dbr5_mon = self.liabilitiesdbr1_mon_dbr5 + self.equitydbr5_mon
#                        self.total_liabilities_dbr6_mon = self.liabilitiesdbr1_mon_dbr6 + self.equitydbr6_mon
#                        self.total_liabilities_dbr7_mon = self.liabilitiesdbr1_mon_dbr7 + self.equitydbr7_mon
#                        self.total_liabilities_dbr8_mon = self.liabilitiesdbr1_mon_dbr8 + self.equitydbr8_mon
#                        self.total_liabilities_dbr9_mon = self.liabilitiesdbr1_mon_dbr9 + self.equitydbr9_mon
#                        self.total_liabilities_dbr10_mon = self.liabilitiesdbr1_mon_dbr10 + self.equitydbr10_mon
#                        self.total_liabilities_dbr11_mon = self.liabilitiesdbr1_mon_dbr11 + self.equitydbr11_mon
#                        self.total_liabilities_dbr12_mon = self.liabilitiesdbr1_mon_dbr12 + self.equitydbr12_mon
#                        self.total_liabilities_dbr13_mon = self.liabilitiesdbr1_mon_dbr13 + self.equitydbr13_mon
                        
                
                else:
                    aa_brw_init = account_obj.browse(self.cr, self.uid, id, ctx_init)
                    aa_brw_end  = account_obj.browse(self.cr, self.uid, id, ctx_end)
                    i, d, c = map(z, [aa_brw_init.balance, aa_brw_end.debit, aa_brw_end.credit])
                    b = z(i+d-c)
                    res.update({
                        'balanceinit': self.exchange(i), 
                        'debit': self.exchange(d), 
                        'credit': self.exchange(c), 
                        'ytd': self.exchange(d-c), 
                    })
                    if form['inf_type'] == 'IS' and form['columns'] == 'one':
                        res.update({
                            'balance': self.exchange(d-c), 
                        })
                        report_data = wiz_rep.browse(self.cr, self.uid, self.context.get('active_id'))
                        for ytd_acc_data in report_data.account_list:
                            if ytd_acc_data.type == 'view':
                                parent_id = ytd_acc_data.parent_id.id
                        parent_acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',False)])
                        child_acc_ids = account_obj.search(self.cr, self.uid, ['|',('parent_id','in',parent_acc_ids),('level','=',1)])
                        for acc_data in account_obj.browse(self.cr, self.uid, child_acc_ids):
                            if parent_id == acc_data.id:
                                acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',acc_data.id)])
#                                a = res.get('total') == True
#                                b = res.get('type') == 'view'
                                if res.get('total') == True and res.get('type') == 'view':
                                    self.bal = self.bal + res.get('balance')
                                bal = []
                                for res_acc in result_acc:
                                    if res_acc.get('name')=='Total Net Ordinary Income':
                                        balance_res = res_acc.get('balance')
                                        bal.append(balance_res)
                                if len(bal) > 0 :
                                    self.gross_profit = bal[0]
                                for acc in account_obj.browse(self.cr, self.uid, acc_ids):
#                                    income_child_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',acc.id)])
#                                    if acc.user_type.name == 'Revenue' or acc.user_type.name == 'Income View' or acc.user_type.name == 'Income':
#                                        pass
#                                        bal += res.get('balance')
#                                    self.rev_credit += acc.credit
#                                    self.rev_debit += acc.debit
#                                if acc.user_type.name == 'Cost Of Goods Sold' or acc.user_type.name == 'Income View' or acc.user_type.name == 'Income':
#                                    self.cogs_credit += acc.credit
#                                    self.cogs_debit += acc.debit
#                                self.gross_profit = (self.rev_credit + self.cogs_credit) + (self.rev_debit + self.cogs_debit)
                                    if acc.name == 'Cost Of Goods Sold' or acc.name == 'Cost of Sales' and acc.user_type.name == 'Income View' or acc.user_type.name == 'Income':
                                        if res.get('name').lower() == 'total cost of sales':
                                            result_acc.append({'id': False, 'name': ''})
                                    
                                    if acc.user_type.name == 'Expense' or acc.user_type.name == 'Expense View':
                                        self.total_exp = (self.exp_credit + self.exp_debit) + (self.taxes_credit + self.taxes_debit) + (self.other_exp_credit + self.other_exp_debit)
                                    self.net_profit = self.gross_profit - ((self.other_income_credit + self.other_income_debit) + self.total_exp)
                                    
                    else:
                        res.update({
                            'balance': self.exchange(b), 
                        })
#                         report_data = wiz_rep.browse(self.cr, self.uid, self.context.get('active_id'))
#                         for ytd_acc_data in report_data.account_list:
#                             if ytd_acc_data.type == 'view':
#                                 parent_id = ytd_acc_data.parent_id.id
#                         parent_acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',False)])
#                         child_acc_ids = account_obj.search(self.cr, self.uid, ['|',('parent_id','in',parent_acc_ids),('level','=',1)])
#                         for acc_data in account_obj.browse(self.cr, self.uid, child_acc_ids):
#                             if parent_id == acc_data.id:
#                                 acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',acc_data.id)])
#                                 if res.get('total') == True and res.get('type') == 'view' and res.get('parent_id') == acc_data.id:
#                                     self.total_balance_sheet_balance = self.total_balance_sheet_balance + res.get('balance')
#                                 self.total_liabilities_equity = self.total_balance_sheet_balance
#                                for acc in account_obj.browse(self.cr, self.uid, acc_ids):
#                                    if acc.user_type.name == 'Assets' or acc.user_type.name == 'Asset' or acc.user_type.name == 'Asset View':
#                                        self.total_assets = res.get('balance')
#            #                                self.total_assets = self.total_asset_credit + self.total_asset_debit
#                                    if acc.user_type.name == 'Liabilities' or acc.user_type.name == 'Liability' or acc.user_type.name == 'Liability View':
#                                        self.total_liabilities_credit += acc.credit
#                                        self.total_liabilities_debit += acc.debit
#                                    if acc.user_type.name == 'Equity' or acc.user_type.name == 'Equity View':
#                                        self.total_equity_credit += acc.credit
#                                        self.total_equity_debit += acc.debit
#                        if res.get('name').lower() == 'total liabilities':
#                            self.tot_liabilities = res.get('balance')
#                        if res.get('name').lower() == 'total equity':
#                            self.tot_equity = res.get('balance')
#                        self.tot_liabilities_equity = self.tot_liabilities + self.tot_equity
                #
                # Check whether we must include this line in the report or not
                #
                to_include = False
                
                if form['columns'] in ('thirteen', 'qtr'):
                    to_test = [False]
                    if form['display_account'] == 'mov' and aa_id[3].parent_id:
                        # Include accounts with movements
                        for x in range(pn-1):
                            to_test.append(res.get('dbr%s'%x, 0.0) >= 0.005 and True or False)
                            to_test.append(res.get('cdr%s'%x, 0.0) >= 0.005 and True or False)
                        if any(to_test):
                            to_include = True
                        
                    elif form['display_account'] == 'bal' and aa_id[3].parent_id:
                        # Include accounts with balance
                        for x in range(pn-1):
                            to_test.append(res.get('bal%s'%x, 0.0) >= 0.005 and True or False)
                        if any(to_test):
                            to_include = True
                            
                    elif form['display_account'] == 'bal_mov' and aa_id[3].parent_id:
                        # Include accounts with balance or movements
                        for x in range(pn-1):
                            to_test.append(res.get('bal%s'%x, 0.0) >= 0.005 and True or False)
                            to_test.append(res.get('dbr%s'%x, 0.0) >= 0.005 and True or False)
                            to_test.append(res.get('cdr%s'%x, 0.0) >= 0.005 and True or False)
                        if any(to_test):
                            to_include = True
                    else:
                        # Include all accounts
                        to_include = True
                
                else:

                    if form['display_account'] == 'mov' and aa_id[3].parent_id:
                        # Include accounts with movements
                        if abs(d) >= 0.005 or abs(c) >= 0.005:
                            to_include = True
                    elif form['display_account'] == 'bal' and aa_id[3].parent_id:
                        # Include accounts with balance
                        if abs(b) >= 0.005:
                            to_include = True
                    elif form['display_account'] == 'bal_mov' and aa_id[3].parent_id:
                        # Include accounts with balance or movements
                        if abs(b) >= 0.005 or abs(d) >= 0.005 or abs(c) >= 0.005:
                            to_include = True
                    else:
                        # Include all accounts
                        to_include = True
                #~ ANALYTIC LEDGER
#                form['columns'] = 'four'
                if to_include and form['analytic_ledger'] and form['columns']=='four' and form['inf_type'] == 'BS' and res['type'] in ('other', 'liquidity', 'receivable', 'payable'):
                    res['mayor'] = self._get_analytic_ledger(res, ctx=ctx_end)
                elif to_include and form['analytic_ledger'] and form['periodic_columns']=='four' and form['inf_type'] == 'BS' and res['type'] in ('other', 'liquidity', 'receivable', 'payable'):
                    res['mayor'] = self._get_analytic_ledger(res, ctx=ctx_end)
                else:
                    res['mayor'] = []
                
                if to_include:
                    #result_acc.append(res)
                    if not ((res['id'] in [x['id'] for x in result_acc]) and (res['name'] in [x['name'] for x in result_acc])):
                        result_acc.append(res)
                    #
                    # Check whether we must sumarize this line in the report or not
                    #
#                    if form['tot_check'] and res['type'] == 'view' and res['level'] == 1 and (res['id'] not in tot):
#                        if form['columns'] == 'qtr':
#                            tot_check = True
#                            #~ tot[res['id']] = True
#                            tot_bal1 += res.get('bal1', 0.0)
#                            tot_bal2 += res.get('bal2', 0.0)
#                            tot_bal3 += res.get('bal3', 0.0)
#                            tot_bal4 += res.get('bal4', 0.0)
#                            tot_bal5 += res.get('bal5', 0.0)
#
#                        elif form['columns'] == 'thirteen':
#                            tot_check = True
#                            #~ tot[res['id']] = True
#                            tot_bal1 += res.get('bal1', 0.0)
#                            tot_bal2 += res.get('bal2', 0.0)
#                            tot_bal3 += res.get('bal3', 0.0)
#                            tot_bal4 += res.get('bal4', 0.0)
#                            tot_bal5 += res.get('bal5', 0.0)
#                            tot_bal6 += res.get('bal6', 0.0)
#                            tot_bal7 += res.get('bal7', 0.0)
#                            tot_bal8 += res.get('bal8', 0.0)
#                            tot_bal9 += res.get('bal9', 0.0)
#                            tot_bal10 += res.get('bal10', 0.0)
#                            tot_bal11 += res.get('bal11', 0.0)
#                            tot_bal12 += res.get('bal12', 0.0)
#                            tot_bal13 += res.get('bal13', 0.0)
#
#                        else:
#                            tot_check = True
#                            #~ tot[res['id']] = True
#                            tot_bin += res['balanceinit']
#                            tot_deb += res['debit']
#                            tot_crd += res['credit']
#                            tot_ytd += res['ytd']
#                            tot_eje += res['balance']
#        if tot_check:
#            str_label = form['lab_str']
#            res2 = {
#                    'id' : form['id'],
#                    'type' : 'view', 
#                    'name': (str_label), 
#                    'label': False, 
#                    'total': True, 
#            }
#            if form['columns'] == 'qtr':
#                res2.update(dict(
#                            bal1 = tot_bal1, 
#                            bal2 = tot_bal2, 
#                            bal3 = tot_bal3, 
#                            bal4 = tot_bal4, 
#                            bal5 = tot_bal5,))
#            elif form['columns'] == 'thirteen':
#                res2.update(dict(
#                            bal1 = tot_bal1, 
#                            bal2 = tot_bal2, 
#                            bal3 = tot_bal3, 
#                            bal4 = tot_bal4, 
#                            bal5 = tot_bal5, 
#                            bal6 = tot_bal6, 
#                            bal7 = tot_bal7, 
#                            bal8 = tot_bal8, 
#                            bal9 = tot_bal9, 
#                            bal10 = tot_bal10, 
#                            bal11 = tot_bal11, 
#                            bal12 = tot_bal12, 
#                            bal13 = tot_bal13,))
#
#            else:
#                aa_brw_init = account_obj.browse(self.cr, self.uid, id, ctx_init)
#                aa_brw_end  = account_obj.browse(self.cr, self.uid, id, ctx_end)
#
#                i, d, c = map(z, [aa_brw_init.balance, aa_brw_end.debit, aa_brw_end.credit])
#                b = z(i+d-c)
#                res2.update({
#                        
#                        'balance': net_balance, 
#                })
#            result_acc.append(res2)
#        if  form['inf_type'] == 'BS' and form['show_earning']:
#            if not self.show_earnings:
#                earning_obj = account_obj.browse(self.cr, self.uid, form['earning_account'])
#                res = {
#                    'id'        : earning_obj.id, 
#                    'type'      : 'view', 
#                    'code'      : earning_obj.code, 
#                    'name'      : earning_obj.name, 
#                    'parent_id' : earning_obj.parent_id and earning_obj.parent_id.id, 
#                    'level'     : earning_obj.level, 
#                    'label'     : False, 
#                    'total'     : True, 
#                    'change_sign' : 1
#                }
#                if form['columns'] in ('qtr', 'thirteen'):
#                    if form['columns'] =='qtr':
#                        pn = 5
#                    else:
#                        pn = 13
#                    while pn > 0:    
#                        res.update(earning_data[pn])
#                        pn -= 1
#                    result_acc.append(res)
#                else:
#                    res.update(earning_data[0])
#                    result_acc.append(res)
#            else:
#                if form['columns'] in ('qtr', 'thirteen'):
#                    has_parent = temp_earning['parent_id'] or False
#                    while has_parent:
#                        res_index_list = [(i, d) for i, d in enumerate(result_acc) if d['id'] == has_parent]
#                        parent = False
#                        for index in res_index_list:
#                            if form['columns'] =='qtr':
#                                pn = 5
#                            else:
#                                pn = 13
#                            while pn > 0:
#                                result_acc[index[0]].update({
#                                    'dbr%s'%pn: result_acc[index[0]]['dbr%s'%pn] + temp_earning['dbr%s_diff'%pn], 
#                                    'cdr%s'%pn: result_acc[index[0]]['cdr%s'%pn] + temp_earning['cdr%s_diff'%pn], 
#                                    'bal%s'%pn: abs(result_acc[index[0]]['bal%s'%pn]) + temp_earning['bal%s_diff'%pn], 
#                                })
#                                pn -= 1
#                            parent = result_acc[index[0]]['parent_id']
#                        has_parent = parent or False
#                else:
#                    has_parent = temp_earning['parent_id'] or False
#                    while has_parent:
#                        res_index_list = [(i, d) for i, d in enumerate(result_acc) if d['id'] == has_parent]
#                        parent = False
#                        for index in res_index_list:
#                            result_acc[index[0]].update({
#                                'balanceinit': abs(result_acc[index[0]]['balanceinit']) + temp_earning['bal_init_diff'], 
#                                'debit': abs(result_acc[index[0]]['debit']) + temp_earning['dbr_diff'], 
#                                'credit': abs(result_acc[index[0]]['credit']) + temp_earning['cdr_diff'], 
#                                'ytd': abs(result_acc[index[0]]['ytd']) + temp_earning['ytd_diff'], 
#                                'balance': abs(result_acc[index[0]]['balance']) + temp_earning['bal_diff'], 
#                            })
#                            parent = result_acc[index[0]]['parent_id']
#                        has_parent = parent or False
        afr_list = []
        if form['inf_type'] == 'BS':
            afr_ids = afr_obj.search(self.cr, self.uid, [('name', '=', 'Income Statement')])
            if afr_ids:
                afr_data = afr_obj.browse(self.cr, self.uid, afr_ids[0]).account_ids
                for afr_id in afr_data:
                    afr_list.append(afr_id.id)
            form['account_list'] = afr_list
            form_copy = form.copy()
            form_copy['inf_type'] = 'IS'
            self.lines(form_copy, 0)
            total_profit_loss = self.net_profit
            
            self.total_profit_loss = {
                'balance' : total_profit_loss, 
                'id' : False, 
                'type' : 'view', 
                'code' : '', 
                'name' : 'Net Income (Loss)', 
                'parent_id' : False, 
                'level' : 1, 
                'credit' : 0.0, 
                'debit' : 0.0, 
                'label' : False, 
                'mayor' : [], 
                'total' :True, 
                'change_sign' : 1, 
                'balanceinit' : 0.0, 
                'ytd' :  total_profit_loss, 
            }
#            if form['columns'] =='qtr':
#                self.total_profit_loss.update({
#                    'bal1' : form_copy.get('net_profit1'),
#                    'bal2' : form_copy.get('net_profit2'),
#                    'bal3' : form_copy.get('net_profit3'),
#                    'bal4' : form_copy.get('net_profit4'),
#                    'bal5' : form_copy.get('net_profit5'),
#                })
                
#            if form['columns'] =='thirteen':
#                self.total_profit_loss.update({
#                    'bal1' : form_copy.get('net_profit1'),
#                    'bal2' : form_copy.get('net_profit2'),
#                    'bal3' : form_copy.get('net_profit3'),
#                    'bal4' : form_copy.get('net_profit4'),
#                    'bal5' : form_copy.get('net_profit5'),
#                    'bal6' : form_copy.get('net_profit6'),
#                    'bal7' : form_copy.get('net_profit7'),
#                    'bal8' : form_copy.get('net_profit8'),
#                    'bal9' : form_copy.get('net_profit9'),
#                    'bal10' : form_copy.get('net_profit10'),
#                    'bal11' : form_copy.get('net_profit11'),
#                    'bal12' : form_copy.get('net_profit12'),
#                    'bal13' : form_copy.get('net_profit13'),
#                })
            result_acc.append(self.total_profit_loss)
            a = []
            for res_acc in result_acc:
                if res_acc.get('name')=='Total Liabilities and Equity':
                    index_1 = result_acc.index(res_acc)
                    a.append(index_1)
            for ele in a:
                result_acc.insert(ele,self.total_profit_loss)
                result_acc.pop(ele+2)
#            
            total_liabilities_equity = self.total_liabilities_equity + self.net_profit
#            if form['columns'] =='qtr':
#                total_liabilities_equity = self.tot_liabilities_equity + self.net_profit
#                total_liabilities_equitydbr1 = self.total_liabilities_dbr1 + form_copy.get('net_profit1')
#                total_liabilities_equitydbr2 = self.total_liabilities_dbr2 + form_copy.get('net_profit2')
#                total_liabilities_equitydbr3 = self.total_liabilities_dbr3 + form_copy.get('net_profit3')

#                total_liabilities_equitydbr4 = self.total_liabilities_dbr4 + form_copy.get('net_profit4')
#                total_liabilities_equitydbr5 = self.total_liabilities_dbr5 + form_copy.get('net_profit5')
                
#            if form['columns'] =='thirteen':
#                total_liabilities_equity = self.tot_liabilities_equity + self.net_profit
#                total_liabilities_mon_equitydbr1 = self.total_liabilities_dbr1_mon + form_copy.get('net_profit1')
#                total_liabilities_mon_equitydbr2 = self.total_liabilities_dbr2_mon + form_copy.get('net_profit2')
#                total_liabilities_mon_equitydbr3 = self.total_liabilities_dbr3_mon + form_copy.get('net_profit3')
#                total_liabilities_mon_equitydbr4 = self.total_liabilities_dbr4_mon + form_copy.get('net_profit4')
#                total_liabilities_mon_equitydbr5 = self.total_liabilities_dbr5_mon + form_copy.get('net_profit5')
#                total_liabilities_mon_equitydbr6 = self.total_liabilities_dbr6_mon + form_copy.get('net_profit6')
#                total_liabilities_mon_equitydbr7 = self.total_liabilities_dbr7_mon + form_copy.get('net_profit7')
#                total_liabilities_mon_equitydbr8 = self.total_liabilities_dbr8_mon + form_copy.get('net_profit8')
#                total_liabilities_mon_equitydbr9 = self.total_liabilities_dbr9_mon + form_copy.get('net_profit9')
#                total_liabilities_mon_equitydbr10 = self.total_liabilities_dbr10_mon + form_copy.get('net_profit10')
#                total_liabilities_mon_equitydbr11 = self.total_liabilities_dbr11_mon + form_copy.get('net_profit11')
#                total_liabilities_mon_equitydbr12 = self.total_liabilities_dbr12_mon + form_copy.get('net_profit12')
#                total_liabilities_mon_equitydbr13 = self.total_liabilities_dbr13_mon + form_copy.get('net_profit13')
                
            self.total_liabilities_equity = {
                'balance' : total_liabilities_equity, 
                'id'        : False, 
                'type' : 'view', 
                'code' : '', 
                'name' : 'Total Liabilities & Owners Equity', 
                'parent_id' : False, 
                'level' : 1, 
                'credit' : 0.0, 
                'debit' : 0.0, 
                'label' : False, 
                'mayor' : [], 
                'total' :True, 
                'change_sign' : 1, 
                'balanceinit' : 0.0, 
                'ytd' : total_liabilities_equity 
            }
#            if form['columns'] =='qtr':
#                self.total_liabilities_equity.update({
#                    'bal1' : total_liabilities_equitydbr1,
#                    'bal2' : total_liabilities_equitydbr2,
#                    'bal3' : total_liabilities_equitydbr3,
#                    'bal4' : total_liabilities_equitydbr4,
#                    'bal5' : total_liabilities_equitydbr5,
#                })
#            if form['columns'] =='thirteen':
#                self.total_liabilities_equity.update({
#                    'bal1' : total_liabilities_mon_equitydbr1,
#                    'bal2' : total_liabilities_mon_equitydbr2,
#                    'bal3' : total_liabilities_mon_equitydbr3,
#                    'bal4' : total_liabilities_mon_equitydbr4,
#                    'bal5' : total_liabilities_mon_equitydbr5,
#                    'bal6' : total_liabilities_mon_equitydbr6,
#                    'bal7' : total_liabilities_mon_equitydbr7,
#                    'bal8' : total_liabilities_mon_equitydbr8,
#                    'bal9' : total_liabilities_mon_equitydbr9,
#                    'bal10' : total_liabilities_mon_equitydbr10,
#                    'bal11' : total_liabilities_mon_equitydbr11,
#                    'bal12' : total_liabilities_mon_equitydbr12,
#                    'bal13' : total_liabilities_mon_equitydbr13,
#                })
                
#            result_acc.append(self.total_liabilities_equity)
            
        else:
            if not form['afr_id'][1] == 'Balance Sheet':
#                if {'id': False, 'name': ''} not in result_acc:
#                    raise osv.except_osv(_('Configuration Error'), _('Please configure all type of Revenue, Cost Of Goods Sold, Expense, Income and Taxes accounts for Income Statement !'))
#                bal = []
                for res_acc in result_acc:
                    if res_acc.get('name')=='Total Net Ordinary Income':
                        index = result_acc.index(res_acc)
                        result_acc.insert(index+11,res_acc)
                        result_acc.pop(index)
#                        balance = res_acc.get('balance')
#                bal.append(balance)
                total_gross_profit = self.gross_profit
#                total_gross_profit = self.gross_profit
#                dbr3 = self.gross_profit_dbr3
                self.gross_profit_dict = {
                    'balance' : total_gross_profit, 
                    'id'        : False, 
                    'type' : 'view', 
                    'code' : '', 
                    'name' : 'Gross Profit', 
                    'parent_id' : False, 
                    'level' : 1, 
                    'credit' : 0.0, 
                    'debit' : 0.0, 
                    'label' : False, 
                    'mayor' : [], 
                    'total' :True, 
                    'change_sign' : 1, 
                    'balanceinit' : 0.0, 
                    'ytd' : total_gross_profit, 
                }
#                if form['columns'] =='qtr':
#                    self.gross_profit_dict.update({
#                        'bal1': self.gross_profit_dbr1,
#                        'bal2': self.gross_profit_dbr2,
#                        'bal3': self.gross_profit_dbr3,
#                        'bal4': self.gross_profit_dbr4,
#                        'bal5': self.gross_profit_dbr5,
#                    })
                    
#                if form['columns'] =='thirteen':
#                    self.gross_profit_dict.update({
#                        'bal1': self.gross_profit_mon_dbr1,
#                        'bal2': self.gross_profit_mon_dbr2,
#                        'bal3': self.gross_profit_mon_dbr3,
#                        'bal4': self.gross_profit_mon_dbr4,
#                        'bal5': self.gross_profit_mon_dbr5,
#                        'bal6': self.gross_profit_mon_dbr6,
#                        'bal7': self.gross_profit_mon_dbr7,
#                        'bal8': self.gross_profit_mon_dbr8,
#                        'bal9': self.gross_profit_mon_dbr9,
#                        'bal10': self.gross_profit_mon_dbr10,
#                        'bal11': self.gross_profit_mon_dbr11,
#                        'bal12': self.gross_profit_mon_dbr12,
#                        'bal13': self.gross_profit_mon_dbr13,
#                    })
    #                pn = 1
    #                for p_id in p:
    #                    i, d, c = map(z, [aa_brw_init.balance, aa_brw_end.debit, aa_brw_end.credit])
    #                    print 'I,D,C', i,d,c
    #                    b = z(i+d-c)
    #                    self.gross_profit_dict.update({
    #                                    'dbr%s'%pn: self.exchange(d), 
    #                                    'cdr%s'%pn: self.exchange(c), 
    #                                    'bal%s'%pn: self.exchange(b), #'bal%s'%pn: total_gross_profit,self.exchange(b) 
    #                                })
    #                    pn += 1
                
    #             pn = 1
    #                for p_id in p:
    #                    if form['inf_type'] == 'IS':
    #                        d, c, b = map(z, [aa_brw_end.debit, aa_brw_end.credit, aa_brw_end.balance])
    #                        res.update({
    #                            'dbr%s'%pn: self.exchange(d), 
    #                            'cdr%s'%pn: self.exchange(c), 
    #                            'bal%s'%pn: self.exchange(b), 
    #                        })
    #                    pn += 1
#                result_acc.insert(index+2, self.gross_profit_dict)
#                result_acc.append(self.gross_profit_dict)
#                result_acc.pop(index)
            
            tot_expense = self.total_exp
##            expdbr3 = self.total_expense_dbr3
            self.tot_exp = {
                'balance' : tot_expense, 
                'id'        : False, 
                'type' : 'view', 
                'code' : '', 
                'name' : 'Total Expense', 
                'parent_id' : False, 
                'level' : 1, 
                'credit' : 0.0, 
                'debit' : 0.0, 
                'label' : False, 
                'mayor' : [], 
                'total' :True, 
                'change_sign' : 1, 
                'balanceinit' : 0.0, 
                'ytd' : tot_expense 
            }
#            if form['columns'] =='qtr':
#                self.tot_exp.update({
#                    'bal1': self.total_expense_dbr1,
#                    'bal2': self.total_expense_dbr2,
#                    'bal3': self.total_expense_dbr3,
#                    'bal4': self.total_expense_dbr4,
#                    'bal5': self.total_expense_dbr5,
#                })
                
#            if form['columns'] =='thirteen':
#                self.tot_exp.update({
#                    'bal1': self.total_expense_dbr1_mon_dbr1,
#                    'bal2': self.total_expense_dbr1_mon_dbr2,
#                    'bal3': self.total_expense_dbr1_mon_dbr3,
#                    'bal4': self.total_expense_dbr1_mon_dbr4,
#                    'bal5': self.total_expense_dbr1_mon_dbr5,
#                    'bal6': self.total_expense_dbr1_mon_dbr6,
#                    'bal7': self.total_expense_dbr1_mon_dbr7,
#                    'bal8': self.total_expense_dbr1_mon_dbr8,
#                    'bal9': self.total_expense_dbr1_mon_dbr9,
#                    'bal10': self.total_expense_dbr1_mon_dbr10,
#                    'bal11': self.total_expense_dbr1_mon_dbr11,
#                    'bal12': self.total_expense_dbr1_mon_dbr12,
#                })
#            result_acc.append(self.tot_exp)
#            
            net_profit = self.net_profit
#            net_profit_dbr3 = self.net_profit_dbr3
            self.tot_net_prodict = {
                'balance' : net_profit, 
                'id'        : False, 
                'type' : 'view', 
                'code' : '', 
                'name' : 'Net Profit', 
                'parent_id' : False, 
                'level' : 1, 
                'credit' : 0.0, 
                'debit' : 0.0, 
                'label' : False, 
                'mayor' : [], 
                'total' :True, 
                'change_sign' : 1, 
                'balanceinit' : 0.0, 
                'ytd' : net_profit #abs(self.gross_profit - abs(self.other_income + self.total_expense))
                
            }
#            if form['columns'] =='qtr':
#                self.tot_net_prodict.update({
#                    'bal1': self.net_profit_dbr1,
#                    'bal2': self.net_profit_dbr2,
#                    'bal3': self.net_profit_dbr3,
#                    'bal4': self.net_profit_dbr4,
#                    'bal5': self.net_profit_dbr5,
#                })
                
#            if form['columns'] =='thirteen':
#                self.tot_net_prodict.update({
#                    'bal1': self.net_profit_dbr1_mon_dbr1,
#                    'bal2': self.net_profit_dbr1_mon_dbr2,
#                    'bal3': self.net_profit_dbr1_mon_dbr3,
#                    'bal4': self.net_profit_dbr1_mon_dbr4,
#                    'bal5': self.net_profit_dbr1_mon_dbr5,
#                    'bal6': self.net_profit_dbr1_mon_dbr6,
#                    'bal7': self.net_profit_dbr1_mon_dbr7,
#                    'bal8': self.net_profit_dbr1_mon_dbr8,
#                    'bal9': self.net_profit_dbr1_mon_dbr9,
#                    'bal10': self.net_profit_dbr1_mon_dbr10,
#                    'bal11': self.net_profit_dbr1_mon_dbr11,
#                    'bal12': self.net_profit_dbr1_mon_dbr12,
#                    'bal13': self.net_profit_dbr1_mon_dbr13,
#                })
#            result_acc.append(self.tot_net_prodict)
        return result_acc
    
    def get_profit(self, bal):
        return bal
    
    def comparison1_lines(self, form, level=0):
        """
        Returns all the data needed for the report lines
        (account info plus debit/credit/balance in the selected period
        and the full year)
        """
        account_obj = self.pool.get('account.account')
        period_obj = self.pool.get('account.period')
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        afr_obj = self.pool.get('afr')
        wiz_rep = self.pool.get('wizard.report')
        self.show_earnings = False
#        if 'earning_account' in form and not isinstance(form['earning_account'], int):
#            form['earning_account'] = form['earning_account'][0]
        periodic_bal = 0.00
        def _get_children_and_consol(cr, uid, ids, level, context={}, change_sign=False):
            aa_obj = self.pool.get('account.account')
            ids2=[]
#            ctx_bal =_ctx_end(self.context.copy())
#            ctx_in =_ctx_init(self.context.copy())
#            net_bal = 0.00
#            user_type = ['Revenue', 'Cost Of Goods Sold', 'Expense', 'Other Income', 'Other Expense']
#            acc_ids = aa_obj.search(self.cr, self.uid, [('type', '=', 'view'), ('level', '=', 1), ('user_type', 'in', user_type)])
#            for acc in acc_ids:
#                acc_data_browse = aa_obj.browse(self.cr, self.uid, acc, ctx_bal)
#                Aacc_data_browse = aa_obj.browse(self.cr, self.uid, acc, ctx_in)
#                periodic_bal = acc_data_browse.balance 
#                net_bal += periodic_bal
#            acc_ids = aa_obj.search(self.cr, self.uid, [('type', '=', 'view'), ('level', '=', 1)])
#            for acc in acc_ids:
#                acc_data_browse = aa_obj.browse(self.cr, self.uid, acc, ctx_bal)
#                Aacc_data_browse = aa_obj.browse(self.cr, self.uid, acc, ctx_in)
#                bal = acc_data_browse.balance + Aacc_data_browse.balance
#                if acc_data_browse.name.lower() == 'revenue':
#                    rev = bal
#                if acc_data_browse.name.lower() == 'cost of goods sold':
#                    cogs = bal
#                if acc_data_browse.name.lower() == 'operating expenses':
#                    opexp = bal
#                if acc_data_browse.name.lower() == 'taxes':
#                    tax = bal
#                if acc_data_browse.name.lower() == 'other income':
#                    other_income = bal
#                if acc_data_browse.name.lower() == 'other expense':
#                    other_expense = bal
#            tot_balance = rev + cogs + opexp + tax + other_income + other_expense
#            if form['inf_type'] == 'BS':
#                self.bal = net_bal
            for aa_brw in aa_obj.browse(cr, uid, ids, context):
                if aa_brw.child_id and aa_brw.level < level and aa_brw.type !='consolidation':
                    if not change_sign:
                        ids2.append([aa_brw.id, True, False, aa_brw])
                    ids2 += _get_children_and_consol(cr, uid, [x.id for x in aa_brw.child_id], level, context, change_sign=change_sign)
                    if change_sign:
                        ids2.append(aa_brw.id) 
                    else:
                        ids2.append([aa_brw.id, False, True, aa_brw])
                else:
                    if change_sign:
                        ids2.append(aa_brw.id) 
                    else:
                        ids2.append([aa_brw.id, True, True, aa_brw])
            return ids2

        #############################################################################
        # CONTEXT FOR ENDIND BALANCE                                                #
        #############################################################################

        def _ctx_end(ctx):
            ctx_end = ctx
            ctx_end['filter'] = form.get('filter', 'all')
            ctx_end['fiscalyear'] = fiscalyear.id
            #~ ctx_end['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',fiscalyear.id),('special','=',False)])
            
            if ctx_end['filter'] not in ['bydate', 'none']:
                special = self.special_period(form['periods'])
            else:
                special = False
            
            if form['filter'] in ['byperiod', 'all']:
                if special:
                    ctx_end['periods'] = period_obj.search(self.cr, self.uid, [('id', 'in', form['periods'] or ctx_end.get('periods', False))])
                else:
                    ctx_end['periods'] = period_obj.search(self.cr, self.uid, [('id','in',form['periods'] or ctx_end.get('periods',False))])
                    
            if form['filter'] in ['bydate', 'all', 'none']:
                ctx_end['date_from'] = form['date_from']
                ctx_end['date_to'] = form['date_to']
            return ctx_end.copy()
        
        def compr0_ctx_end(ctx):
            ctx_end = ctx
            if form['compr0_filter'] and form['compr0_fiscalyear_id']:
                    ctx_end['filter'] = form.get('compr0_filter', 'all')
                    ctx_end['fiscalyear'] = compr0_fiscalyear.id
                    if ctx_end['filter'] not in ['bydate', 'none']:
                        special = self.special_period(form['compr0_periods'])
                    else:
                        special = False
                    
                    if form['compr0_filter'] in ['byperiod', 'all']:
                        if special:
                            ctx_end['periods'] = period_obj.search(self.cr, self.uid, [('id', 'in', form['compr0_periods'] or ctx_end.get('periods', False))])
                        else:
                            ctx_end['periods'] = period_obj.search(self.cr, self.uid, [('id','in',form['compr0_periods'] or ctx_end.get('periods',False))])
                            
                    if form['compr0_filter'] in ['bydate', 'all', 'none']:
                        ctx_end['date_from'] = form['compr0_date_from']
                        ctx_end['date_to'] = form['compr0_date_to']
                
            return ctx_end.copy()
        
        def compr1_ctx_end(ctx):
            ctx_end = ctx
            if form['compr1_filter'] and form['compr1_fiscalyear_id']:
                    ctx_end['filter'] = form.get('compr1_filter', 'all')
                    ctx_end['fiscalyear'] = compr1_fiscalyear.id
                    if ctx_end['filter'] not in ['bydate', 'none']:
                        special = self.special_period(form['compr1_periods'])
                    else:
                        special = False
                    
                    if form['compr1_filter'] in ['byperiod', 'all']:
                        if special:
                            ctx_end['periods'] = period_obj.search(self.cr, self.uid, [('id', 'in', form['compr1_periods'] or ctx_end.get('periods', False))])
                        else:
                            ctx_end['periods'] = period_obj.search(self.cr, self.uid, [('id','in',form['compr1_periods'] or ctx_end.get('periods',False))])
                            
                    if form['compr1_filter'] in ['bydate', 'all', 'none']:
                        ctx_end['date_from'] = form['compr1_date_from']
                        ctx_end['date_to'] = form['compr1_date_to']
                
            return ctx_end.copy()
        
        def missing_period(ctx_init):
            ctx_init['fiscalyear'] = fiscalyear_obj.search(self.cr, self.uid, [('date_stop', '<', fiscalyear.date_start)], order='date_stop') and \
                                fiscalyear_obj.search(self.cr, self.uid, [('date_stop', '<', fiscalyear.date_start)], order='date_stop')[-1] or []
            ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', ctx_init['fiscalyear']), ('date_stop', '<', fiscalyear.date_start)])
            return ctx_init
        
        def compr0_missing_period(ctx_init):
            ctx_init['compr0_fiscalyear'] = fiscalyear_obj.search(self.cr, self.uid, [('date_stop', '<', compr0_fiscalyear.date_start)], order='date_stop') and \
                                fiscalyear_obj.search(self.cr, self.uid, [('date_stop', '<', compr0_fiscalyear.date_start)], order='date_stop')[-1] or []
            ctx_init['compr0_periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', ctx_init['compr0_fiscalyear']), ('date_stop', '<', compr0_fiscalyear.date_start)])
            return ctx_init
        
        def compr1_missing_period(ctx_init):
            ctx_init['compr1_fiscalyear'] = fiscalyear_obj.search(self.cr, self.uid, [('date_stop', '<', compr1_fiscalyear.date_start)], order='date_stop') and \
                                fiscalyear_obj.search(self.cr, self.uid, [('date_stop', '<', compr1_fiscalyear.date_start)], order='date_stop')[-1] or []
            ctx_init['compr1_periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', ctx_init['compr1_fiscalyear']), ('date_stop', '<', compr1_fiscalyear.date_start)])
            return ctx_init
        #############################################################################
        # CONTEXT FOR INITIAL BALANCE                                               #
        #############################################################################
        
        def _ctx_init(ctx):
            ctx_init = self.context.copy()
            ctx_init['filter'] = form.get('filter', 'all')
            ctx_init['fiscalyear'] = fiscalyear.id

            if form['filter'] in ['byperiod', 'all']:
                ctx_init['periods'] = form['periods']
                if not ctx_init['periods']:
                    ctx_init = missing_period(ctx_init.copy())
                date_start = min([period.date_start for period in period_obj.browse(self.cr, self.uid, ctx_init['periods'])])
                ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', fiscalyear.id), ('date_stop', '<=', date_start)])
            elif form['filter'] in ['bydate']:
                ctx_init['date_from'] = fiscalyear.date_start
                ctx_init['date_to'] = form['date_from']
                ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', fiscalyear.id), ('date_stop', '<=', ctx_init['date_to'])])
            elif form['filter'] == 'none':
                ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', fiscalyear.id), ('special', '=', True)])
                date_start = min([period.date_start for period in period_obj.browse(self.cr, self.uid, ctx_init['periods'])])
                ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', fiscalyear.id), ('date_start', '<=', date_start), ('special', '=', True)])
           
            return ctx_init.copy()
        
        def compr0_ctx_init(ctx):
            ctx_init = self.context.copy()
            ctx_init['filter'] = form.get('compr0_filter', 'all')
            ctx_init['fiscalyear'] = compr0_fiscalyear.id
            if form['compr0_fiscalyear_id']:
                if form['compr0_filter'] in ['byperiod', 'all']:
                    ctx_init['periods'] = form['compr0_periods']
                    if not ctx_init['periods']:
                        ctx_init = compr0_missing_period(ctx_init.copy())
                    date_start = min([period.date_start for period in period_obj.browse(self.cr, self.uid, ctx_init['periods'])])
                    ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', compr0_fiscalyear.id), ('date_stop', '<=', date_start)])
                elif form['compr0_filter'] in ['bydate']:
                    ctx_init['date_from'] = compr0_fiscalyear.date_start
                    ctx_init['date_to'] = form['compr0_date_to']
                    ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', compr0_fiscalyear.id), ('date_stop', '<=', ctx_init['date_to'])])
                elif form['compr0_filter'] == 'none':
                    ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', compr0_fiscalyear.id), ('special', '=', True)])
                    date_start = min([period.date_start for period in period_obj.browse(self.cr, self.uid, ctx_init['periods'])])
                    ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', compr0_fiscalyear.id), ('date_start', '<=', date_start), ('special', '=', True)])
            return ctx_init.copy()
        
        def compr1_ctx_init(ctx):
            ctx_init = self.context.copy()
            ctx_init['filter'] = form.get('compr1_filter', 'all')
            ctx_init['fiscalyear'] = compr1_fiscalyear.id
            if form['compr1_fiscalyear_id']:
                if form['compr1_filter'] in ['byperiod', 'all']:
                    ctx_init['periods'] = form['compr1_periods']
                    if not ctx_init['periods']:
                        ctx_init = compr1_missing_period(ctx_init.copy())
                    date_start = min([period.date_start for period in period_obj.browse(self.cr, self.uid, ctx_init['periods'])])
                    ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', compr1_fiscalyear.id), ('date_stop', '<=', date_start)])
                elif form['compr1_filter'] in ['bydate']:
                    ctx_init['date_from'] = compr0_fiscalyear.date_start
                    ctx_init['date_to'] = form['compr1_date_to']
                    ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', compr1_fiscalyear.id), ('date_stop', '<=', ctx_init['date_to'])])
                elif form['compr1_filter'] == 'none':
                    ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', compr1_fiscalyear.id), ('special', '=', True)])
                    date_start = min([period.date_start for period in period_obj.browse(self.cr, self.uid, ctx_init['periods'])])
                    ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', compr1_fiscalyear.id), ('date_start', '<=', date_start), ('special', '=', True)])
            return ctx_init.copy()
        
        def z(n):
            return abs(n) < 0.005 and 0.0 or n
                

        self.from_currency_id = self.get_company_currency(form['company_id'] and type(form['company_id']) in (list, tuple) and form['company_id'][0] or form['company_id'])
        if not form['currency_id']:
            self.to_currency_id = self.from_currency_id
        else:
            self.to_currency_id = form['currency_id'] and type(form['currency_id']) in (list, tuple) and form['currency_id'][0] or form['currency_id']
        selected_accounts = []
        if form.has_key('account_list') and form['account_list']:
            selected_accounts = form['account_list']
            account_ids = form['account_list']
#            del form['account_list']
        
        credit_account_ids = self.get_company_accounts(form['company_id'] and type(form['company_id']) in (list, tuple) and form['company_id'][0] or form['company_id'], 'credit')
        
        debit_account_ids = self.get_company_accounts(form['company_id'] and type(form['company_id']) in (list, tuple) and form['company_id'][0] or form['company_id'], 'debit')
        
        if form.get('fiscalyear'):
            if type(form.get('fiscalyear')) in (list, tuple):
                fiscalyear = form['fiscalyear'] and form['fiscalyear'][0]
            elif type(form.get('fiscalyear')) in (int,):
                fiscalyear = form['fiscalyear']
        fiscalyear = fiscalyear_obj.browse(self.cr, self.uid, fiscalyear)
        
        if form.get('compr0_fiscalyear_id'):
            if type(form.get('compr0_fiscalyear_id')) in (list, tuple):
                compr0_fiscalyear = form['compr0_fiscalyear_id'] and form['compr0_fiscalyear_id'][0]
            elif type(form.get('compr0_fiscalyear_id')) in (int,):
                compr0_fiscalyear = form['compr0_fiscalyear_id']
            compr0_fiscalyear = fiscalyear_obj.browse(self.cr, self.uid, compr0_fiscalyear)

        if form.get('compr1_fiscalyear_id'):
            if type(form.get('compr1_fiscalyear_id')) in (list, tuple):
                compr1_fiscalyear = form['compr1_fiscalyear_id'] and form['compr1_fiscalyear_id'][0]
            elif type(form.get('compr1_fiscalyear_id')) in (int,):
                compr1_fiscalyear = form['compr1_fiscalyear_id']
            compr1_fiscalyear = fiscalyear_obj.browse(self.cr, self.uid, compr1_fiscalyear)
        
        ################################################################
        # Get the accounts                                             #
        ################################################################
        account_ids = _get_children_and_consol(self.cr, self.uid, account_ids, form['display_account_level'] and form['display_account_level'] or 100, self.context)
        
        credit_account_ids = _get_children_and_consol(self.cr, self.uid, credit_account_ids, 100, self.context, change_sign=True)
        
        debit_account_ids = _get_children_and_consol(self.cr, self.uid, debit_account_ids, 100, self.context, change_sign=True)
        
        credit_account_ids = list(set(credit_account_ids) - set(debit_account_ids))

        #
        # Generate the report lines (checking each account)
        #
        tot_check = False
        if not form['periods']:
            form['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',fiscalyear.id)],order='date_start asc')
            if not form['periods']:
                raise osv.except_osv(_('UserError'), _('The Selected Fiscal Year Does not have Regular Periods'))
        
        if form['compr0_fiscalyear_id']:
            if  not form['compr0_periods']:
                form['compr0_periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',compr0_fiscalyear.id)],order='date_start asc')
                if not form['compr0_periods']:
                    raise osv.except_osv(_('UserError'), _('The Selected Fiscal Year Does not have Regular Periods'))
        
        if form['compr1_fiscalyear_id']:
            if not form['compr1_periods']:
                form['compr1_periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',compr1_fiscalyear.id)],order='date_start asc')
                if not form['compr1_periods']:
                    raise osv.except_osv(_('UserError'), _('The Selected Fiscal Year Does not have Regular Periods'))
            
        ctx_init = _ctx_init(self.context.copy())
        ctx_end = _ctx_end(self.context.copy())
        if form['compr0_fiscalyear_id']:
            compr0_ctx_init = compr0_ctx_init(self.context.copy())
            compr0_ctx_end = compr0_ctx_end(self.context.copy())

        if form['compr1_fiscalyear_id']:
            compr1_ctx_init = compr1_ctx_init(self.context.copy())
            compr1_ctx_end = compr1_ctx_end(self.context.copy())
            
        tot_bin = 0.0
        tot_deb = 0.0
        tot_crd = 0.0
        tot_ytd = 0.0
        tot_eje = 0.0
        
        res = {}
        result_acc = []
        tot = {}        
        
        ############################For getting the net balance for earning account
        net_balance = 0.0   
        temp_earning = {}  
        net_bal_temp = {}
        earning_data = {}
#        if form['show_earning']:
#            
#            net_bal_temp[0]={
#                    'ctx_init': ctx_init, 
#                    'ctx_end': ctx_end, 
#                    'balanceinit': 0.0, 
#                    'debit': 0.0, 
#                    'credit': 0.0, 
#                    'ytd': 0.0, 
#                    'balance':0.0
#                }
#            earning_data[0]={
#                    'balanceinit': 0.0, 
#                    'debit': 0.0, 
#                    'credit': 0.0, 
#                    'ytd': 0.0, 
#                    'balance':0.0}
#            for par_id in selected_accounts:
#                
#                aa_brw_init = account_obj.browse(self.cr, self.uid, par_id, ctx_init)
#                aa_brw_end  = account_obj.browse(self.cr, self.uid, par_id, ctx_end)
#                
#                i, d, c = map(z, [aa_brw_init.balance, aa_brw_end.debit, aa_brw_end.credit])
#                b = z(i+d-c)
#                net_bal_temp[0].update({
#                    'balanceinit': self.exchange(i) + net_bal_temp[0]['balanceinit'], 
#                    'debit': self.exchange(d) + net_bal_temp[0]['debit'], 
#                    'credit': self.exchange(c) + net_bal_temp[0]['credit'], 
#                    'ytd': self.exchange(d-c) + net_bal_temp[0]['ytd'], 
#                    'balance':self.exchange(b) + net_bal_temp[0]['balance'], 
#                })
#                earning_init = account_obj.browse(self.cr, self.uid, form['earning_account'], ctx_init)
#                earning_end  = account_obj.browse(self.cr, self.uid, form['earning_account'], ctx_end)
#                
#            ei, ed, ec = map(z, [earning_init.balance, earning_end.debit, earning_end.credit])
#            eb = z(ei+ed-ec)
#            earning_data[0].update({
#                'balanceinit': self.exchange(ei) + net_bal_temp[0]['balanceinit'], 
#                'debit': self.exchange(ed) + net_bal_temp[0]['debit'], 
#                'credit': self.exchange(ec) + net_bal_temp[0]['credit'], 
#                'ytd': self.exchange(ed-ec) + net_bal_temp[0]['ytd'], 
#                'balance':self.exchange(eb) + net_bal_temp[0]['balance'], 
#            })
        
        for aa_id in account_ids:
            id = aa_id[0]
            #
            # Check if we need to include this level
            #
            if not form['display_account_level'] or aa_id[3].level <= form['display_account_level']:
                res = {
                'id'        : id, 
                'type'      : aa_id[3].type, 
                'code'      : aa_id[3].code, 
                'name'      : (aa_id[2] and not aa_id[1]) and 'Total %s'%(aa_id[3].name) or aa_id[3].name, 
                'parent_id' : aa_id[3].parent_id and aa_id[3].parent_id.id, 
                'level'     : aa_id[3].level, 
                'label'     : aa_id[1], 
                'total'     : aa_id[2], 
                'change_sign' : credit_account_ids and (id  in credit_account_ids and -1 or 1) or 1
                }
                aa_brw_init = account_obj.browse(self.cr, self.uid, id, ctx_init)
                aa_brw_end  = account_obj.browse(self.cr, self.uid, id, ctx_end)

                if form['compr0_fiscalyear_id']:
                    compr0_aa_brw_init = account_obj.browse(self.cr, self.uid, id, compr0_ctx_init)
                    compr0_aa_brw_end  = account_obj.browse(self.cr, self.uid, id, compr0_ctx_end)
                    if (not form['compr1_fiscalyear_id']==True) :
                        compr0_i, compr0_d, compr0_c = map(z, [0.00, compr0_aa_brw_end.debit, compr0_aa_brw_end.credit])
                    else:
                        compr0_i, compr0_d, compr0_c = map(z, [compr0_aa_brw_init.balance, compr0_aa_brw_end.debit, compr0_aa_brw_end.credit])
                    compr0_b = z(compr0_i+compr0_d-compr0_c)
                    res.update({
                    'compr0_balanceinit': self.exchange(compr0_i), 
                    'compr0_debit': self.exchange(compr0_d), 
                    'compr0_credit': self.exchange(compr0_c), 
                    'compr0_ytd': self.exchange(compr0_d-compr0_c), 
                    })
#                    if form['inf_type'] == 'IS' and  form['columns'] == 'one':
                    if form['inf_type'] == 'IS':# and  form['periodic_columns'] == 'one':
                        res.update({
                            'compr0_balance': self.exchange(compr0_d-compr0_c), 
                        })
#                        if res.get('name').lower() == 'total revenue':
#                            self.comp0_tot_revenue = compr0_b
#                        if res.get('name').lower() == 'cost of goods sold':
#                            self.comp0_tot_cogs = res.get('compr0_balance')
#                        self.comp0_gross_profit = abs(self.comp0_tot_revenue) - abs(self.comp0_tot_cogs)
#                        if res.get('name').lower() == 'total cost of goods sold':
#                            result_acc.append({'id': False, 'name': ''})
#                        if res.get('name').lower() == 'total operating expenses':
#                            self.comp0_operating_expense = res.get('compr0_balance')
#                        if res.get('name').lower() == 'total taxes':
#                            self.comp0_taxes = res.get('compr0_balance')
#                        if res.get('name').lower() == 'total other expense':
#                            self.comp0_other_expense = res.get('compr0_balance')
#                        if res.get('name').lower() == 'total other income':
#                            self.comp0_other_income = res.get('compr0_balance')
#                        self.comp0_total_expense = self.comp0_operating_expense + self.comp0_taxes + self.comp0_other_expense
#                        self.comp0_net_profit = abs(self.comp0_gross_profit - abs(self.comp0_other_income + self.comp0_total_expense))
#                        form['comp0_net_profit'] = self.comp0_net_profit
                    else:
                        res.update({
                            'compr0_balance': self.exchange(compr0_b), 
                        })
#                        if res.get('name').lower() == 'total liabilities':
#                            self.comp0_tot_liabilities = res.get('compr0_balance')
#                        if res.get('name').lower() == 'total equity':
#                            self.comp0_tot_equity = res.get('compr0_balance')
#                        self.comp0_tot_liabilities_equity = self.comp0_tot_liabilities + self.comp0_tot_equity
                
                if form['compr1_fiscalyear_id']:
                    compr1_aa_brw_init = account_obj.browse(self.cr, self.uid, id, compr1_ctx_init)
                    compr1_aa_brw_end  = account_obj.browse(self.cr, self.uid, id, compr1_ctx_end)
                    compr1_i, compr1_d, compr1_c = map(z, [0.00, compr1_aa_brw_end.debit, compr1_aa_brw_end.credit])
                    compr1_b = z(compr1_i+compr1_d-compr1_c)
                    res.update({
                    'compr1_balanceinit': self.exchange(compr1_i), 
                    'compr1_debit': self.exchange(compr1_d), 
                    'compr1_credit': self.exchange(compr1_c), 
                    'compr1_ytd': self.exchange(compr1_d-compr1_c), 
                    })
#                    if form['inf_type'] == 'IS' and  form['columns'] == 'one':
                    if form['inf_type'] == 'IS' and  form['periodic_columns'] == 'one':
                        res.update({
                            'compr1_balance': self.exchange(compr1_d-compr1_c), 
                        })
#                        if res.get('name').lower() == 'total revenue':
#                            self.comp1_tot_revenue = compr1_b
#                        if res.get('name').lower() == 'cost of goods sold':
#                            self.comp1_tot_cogs = res.get('compr1_balance')
#                        self.comp1_gross_profit = abs(self.comp1_tot_revenue) - abs(self.comp1_tot_cogs)
#                        if res.get('name').lower() == 'total cost of goods sold':
#                            result_acc.append({'id': False, 'name': ''})
#                        if res.get('name').lower() == 'total operating expenses':
#                            self.comp1_operating_expense = res.get('compr1_balance')
#                        if res.get('name').lower() == 'total taxes':
#                            self.comp1_taxes = res.get('compr1_balance')
#                        if res.get('name').lower() == 'total other expense':
#                            self.comp1_other_expense = res.get('compr1_balance')
#                        if res.get('name').lower() == 'total other income':
#                            self.comp1_other_income = res.get('compr1_balance')
#                        self.comp1_total_expense = self.comp1_operating_expense + self.comp1_taxes + self.comp1_other_expense
#                        self.comp1_net_profit = abs(self.comp1_gross_profit - abs(self.comp1_other_income + self.comp1_total_expense))
#                        form['comp1_net_profit'] = self.comp1_net_profit
                    else:
                        res.update({
                            'compr1_balance': self.exchange(compr1_b), 
                        })
#                        if res.get('name').lower() == 'total liabilities':
#                            self.comp1_tot_liabilities = res.get('compr1_balance')
#                        if res.get('name').lower() == 'total equity':
#                            self.comp1_tot_equity = res.get('compr1_balance')
#                        self.comp1_tot_liabilities_equity = self.comp1_tot_liabilities + self.comp1_tot_equity
                    if form['inf_type'] == 'TB' and  form['periodic_columns'] == 'two':
                        res.update({
                            'compr1_balance': self.exchange(compr1_b), 
                        })
                        
                if (not form['compr0_fiscalyear_id']) == True and (not form['compr1_fiscalyear_id']==True) :
                    i, d, c = map(z, [0.00, aa_brw_end.debit, aa_brw_end.credit])
                else:
                    i, d, c = map(z, [aa_brw_init.balance, aa_brw_end.debit, aa_brw_end.credit])
                b = z(i+d-c)
                res.update({
                    'balanceinit': self.exchange(i), 
                    'debit': self.exchange(d), 
                    'credit': self.exchange(c), 
                    'ytd': self.exchange(d-c), 
                })
            
#                if form['inf_type'] == 'IS' and  form['columns'] == 'one':
                if form['inf_type'] == 'IS' and  form['periodic_columns'] == 'one':
                    res.update({
                        'balance': self.exchange(d-c), 
                    })
                    report_data = wiz_rep.browse(self.cr, self.uid, self.context.get('active_id'))
                    for ytd_acc_data in report_data.account_list:
                        if ytd_acc_data.type == 'view':
                            parent_id = ytd_acc_data.parent_id.id
                    parent_acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',False)])
                    child_acc_ids = account_obj.search(self.cr, self.uid, ['|',('parent_id','in',parent_acc_ids),('level','=',1)])
                    for acc_data in account_obj.browse(self.cr, self.uid, child_acc_ids):
                        if parent_id == acc_data.id:
                            acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',acc_data.id)])
                            if res.get('total') == True and res.get('type') == 'view':
                                self.bal = self.bal + res.get('balance')
                                bal = []
                                for res_acc in result_acc:
                                    if res_acc.get('name')=='Total Net Ordinary Income':
                                        balance_res = res_acc.get('balance')
                                        bal.append(balance_res)
                                if len(bal) > 0 :
                                    self.gross_profit = bal[0]
#                            self.gross_profit = self.bal
                            for acc in account_obj.browse(self.cr, self.uid, acc_ids):
                                if acc.name == 'Cost Of Goods Sold' or acc.name == 'Cost of Sales' and acc.user_type.name == 'Income View' or acc.user_type.name == 'Income':
                                    if res.get('name').lower() == 'total cost of sales':
                                        result_acc.append({'id': False, 'name': ''})
                                if acc.user_type.name == 'Expense' or acc.user_type.name == 'Expense View':
                                    self.total_exp = (self.exp_credit + self.exp_debit) + (self.taxes_credit + self.taxes_debit) + (self.other_exp_credit + self.other_exp_debit)
                                self.net_profit = self.gross_profit - ((self.other_income_credit + self.other_income_debit) + self.total_exp)
#                    if res.get('name').lower() == 'total revenue':
#                            self.tot_revenue = b
#                    if res.get('name').lower() == 'cost of goods sold':
#                        self.tot_cogs = res.get('balance')
#                    self.gross_profit = abs(self.tot_revenue) - abs(self.tot_cogs)
#                    if res.get('name').lower() == 'total cost of goods sold':
#                        result_acc.append({'id': False, 'name': ''})
#                    if res.get('name').lower() == 'total operating expenses':
#                        self.operating_expense = res.get('balance')
#                    if res.get('name').lower() == 'total taxes':
#                        self.taxes = res.get('balance')
#                    if res.get('name').lower() == 'total other expense':
#                        self.other_expense = res.get('balance')
#                    if res.get('name').lower() == 'total other income':
#                        self.other_income = res.get('balance')
#                    self.total_expense = self.operating_expense + self.taxes + self.other_expense
#                    self.net_profit = abs(self.gross_profit - abs(self.other_income + self.total_expense))
#                    form['periodic_net_profit_one'] = self.net_profit
#                elif form['inf_type'] == 'BS' and form['show_earning'] and form['earning_account'] == id:
#                        self.show_earnings = True
#                        res.update({
#                            'balanceinit': self.exchange(earning_data[0]['balanceinit'])+ \
#                                        2 * res['change_sign'] * self.exchange(i), 
#                            'debit': self.exchange(earning_data[0]['debit']) + \
#                                        2 * res['change_sign'] * self.exchange(d), 
#                            'credit': self.exchange(earning_data[0]['credit'])+ \
#                                        2 * res['change_sign'] * self.exchange(c), 
#                            'ytd': self.exchange(earning_data[0]['ytd']) + \
#                                        2 * res['change_sign'] * self.exchange(d-c), 
#                            'balance': self.exchange(earning_data[0]['balance']) + \
#                                        2 * res['change_sign'] * self.exchange(b)
#                        })
#                        temp_earning.update({
#                                'change_sign': res['change_sign'], 
#                                'earning': self.exchange(b), 
#                                'bal_init_diff': res['balanceinit'] - (self.exchange(i)* res['change_sign']), 
#                                'dbr_diff': res['debit'] - (self.exchange(d)), #* res['change_sign']),
#                                'cdr_diff': res['credit'] - (self.exchange(c)), #* res['change_sign']),
#                                'ytd_diff':  res['ytd'] - (self.exchange(d-c)* res['change_sign']), 
#                                'net_bal': res['balance'], 
#                                'bal_diff': res['balance'] - (self.exchange(b) * res['change_sign']), 
#                                'parent_id': aa_brw_init.parent_id and aa_brw_init.parent_id.id or False, 
#                        })
                else:
                    res.update({
                        'balance': self.exchange(b), 
                    })
#                     report_data = wiz_rep.browse(self.cr, self.uid, self.context.get('active_id'))
#                     for ytd_acc_data in report_data.account_list:
#                         if ytd_acc_data.type == 'view':
#                             parent_id = ytd_acc_data.parent_id.id
#                     parent_acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',False)])
#                     child_acc_ids = account_obj.search(self.cr, self.uid, ['|',('parent_id','in',parent_acc_ids),('level','=',1)])
#                     for acc_data in account_obj.browse(self.cr, self.uid, child_acc_ids):
#                         if parent_id == acc_data.id:
#                             acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',acc_data.id)])
#                             if res.get('total') == True and res.get('type') == 'view' and res.get('parent_id') == acc_data.id:
#                                 self.total_balance_sheet_balance = self.total_balance_sheet_balance + res.get('balance')
#                             self.total_liabilities_equity = self.total_balance_sheet_balance
#                    if res.get('name').lower() == 'total liabilities':
#                        self.tot_liabilities = res.get('balance')
#                    if res.get('name').lower() == 'total equity':
#                        self.tot_equity = res.get('balance')
#                    self.tot_liabilities_equity = self.tot_liabilities + self.tot_equity

                #
                # Check whether we must include this line in the report or not
                #
                to_include = False
                

                if form['display_account'] == 'mov' and aa_id[3].parent_id:
                    # Include accounts with movements
                    if abs(d) >= 0.005 or abs(c) >= 0.005:
                        to_include = True
                elif form['display_account'] == 'bal' and aa_id[3].parent_id:
                    # Include accounts with balance
                    if abs(b) >= 0.005:
                        to_include = True
                elif form['display_account'] == 'bal_mov' and aa_id[3].parent_id:
                    # Include accounts with balance or movements
                    if abs(b) >= 0.005 or abs(d) >= 0.005 or abs(c) >= 0.005:
                        to_include = True
                else:
                    # Include all accounts
                    to_include = True
                
                #~ ANALYTIC LEDGER
#                if to_include and form['analytic_ledger'] and form['columns']=='four' and form['inf_type'] == 'BS' and res['type'] in ('other', 'liquidity', 'receivable', 'payable'):
                if to_include and form['analytic_ledger'] and form['periodic_columns']=='four' and form['inf_type'] == 'BS' and res['type'] in ('other', 'liquidity', 'receivable', 'payable'):
                    res['mayor'] = self._get_analytic_ledger(res, ctx=ctx_end)
                else:
                    res['mayor'] = []
                if to_include:
                    if not ((res['id'] in [x['id'] for x in result_acc]) and (res['name'] in [x['name'] for x in result_acc])):
                        result_acc.append(res)
#                    result_acc.append(res)
                    #
                    # Check whether we must sumarize this line in the report or not
                    #
                    if form['tot_check'] and res['type'] == 'view' and res['level'] == 1 and (res['id'] not in tot):
                        tot_check = True
                        #~ tot[res['id']] = True
                        tot_bin += res['balanceinit']
                        tot_deb += res['debit']
                        tot_crd += res['credit']
                        tot_ytd += res['ytd']
                        tot_eje += res['balance']

#        if tot_check:
#            str_label = form['lab_str']
#            res2 = {
#                    'id' : form['id'],
#                    'type' : 'view', 
#                    'name': (str_label), 
#                    'label': False, 
#                    'total': True, 
#                    'balanceinit': tot_bin, 
#                    'debit': tot_deb, 
#                    'credit': tot_crd, 
#                    'ytd': tot_ytd, 
#                    'balance': tot_eje, 
#            }
#            aa_brw_init = account_obj.browse(self.cr, self.uid, id, ctx_init)
#            aa_brw_end  = account_obj.browse(self.cr, self.uid, id, ctx_end)
#
#            i, d, c = map(z, [aa_brw_init.balance, aa_brw_end.debit, aa_brw_end.credit])
#            b = z(i+d-c)
#            res2.update({
#                    
#                    'balance': net_balance, 
#            })
#            result_acc.append(res2)
#        if  form['inf_type'] == 'BS' and form['show_earning']:
#            if not self.show_earnings:
#                earning_obj = account_obj.browse(self.cr, self.uid, form['earning_account'])
#                res = {
#                    'id'        : earning_obj.id, 
#                    'type'      : 'view', 
#                    'code'      : earning_obj.code, 
#                    'name'      : earning_obj.name, 
#                    'parent_id' : earning_obj.parent_id and earning_obj.parent_id.id, 
#                    'level'     : earning_obj.level, 
#                    'label'     : False, 
#                    'total'     : True, 
#                    'change_sign' : 1
#                }
#                res.update(earning_data[0])
#                result_acc.append(res)
#            else:
#                has_parent = temp_earning['parent_id'] or False
#                while has_parent:
#                    res_index_list = [(i, d) for i, d in enumerate(result_acc) if d['id'] == has_parent]
#                    parent = False
#                    for index in res_index_list:
#                        result_acc[index[0]].update({
#                            'balanceinit': abs(result_acc[index[0]]['balanceinit']) + temp_earning['bal_init_diff'], 
#                            'debit': abs(result_acc[index[0]]['debit']) + temp_earning['dbr_diff'], 
#                            'credit': abs(result_acc[index[0]]['credit']) + temp_earning['cdr_diff'], 
#                            'ytd': abs(result_acc[index[0]]['ytd']) + temp_earning['ytd_diff'], 
#                            'balance': abs(result_acc[index[0]]['balance']) + temp_earning['bal_diff'], 
#                        })
#                        parent = result_acc[index[0]]['parent_id']
#                    has_parent = parent or False
        afr_list = []
        if form['inf_type'] == 'BS':
            afr_ids = afr_obj.search(self.cr, self.uid, [('name', '=', 'Income Statement')])

            if afr_ids:
                afr_data = afr_obj.browse(self.cr, self.uid, afr_ids[0]).account_ids
                for afr_id in afr_data:
                    afr_list.append(afr_id.id)
            form['account_list'] = afr_list
            form_copy = form.copy()
            form_copy['inf_type'] = 'IS'
            self.lines(form_copy, 0)
#            self.comparison1_lines(form_copy, 0)
##            total_profit_loss = abs(form_copy.get('periodic_net_profit_one'))
            total_profit_loss = self.net_profit
#            total_comp0_profit_loss = self.comp0_net_profit
#            total_comp1_profit_loss = self.comp1_net_profit
            self.total_profit_loss = {
                'balance' : total_profit_loss, 
                'id' : False, 
                'type' : 'view', 
                'code' : '', 
                'name' : 'Net Income (Loss)', 
                'parent_id' : False, 
                'level' : 1, 
                'credit' : 0.0, 
                'debit' : 0.0, 
                'label' : False, 
                'mayor' : [], 
                'total' :True, 
                'change_sign' : 1, 
                'balanceinit' : 0.0, 
                'ytd' :  total_profit_loss, 
            }
#            
#            if form['compr0_fiscalyear_id']:
#                self.total_profit_loss.update({
#                    'compr0_balance' : total_comp0_profit_loss,
#                    'compr0_balanceinit' : 0.00,
#                    'compr0_debit' : 0.00,
#                    'compr0_credit' : 0.00,
#                    'compr0_ytd' : self.comp0_net_profit,
#                })
#            
#            if form['compr1_fiscalyear_id']:
#                self.total_profit_loss.update({
#                    'compr1_balance' : total_comp1_profit_loss,
#                    'compr1_balanceinit' : 0.00,
#                    'compr1_debit' : 0.00,
#                    'compr1_credit' : 0.00,
#                    'compr1_ytd' : self.comp1_net_profit,
#                })
            result_acc.append(self.total_profit_loss)
            a = []
            for res_acc in result_acc:
                if res_acc.get('name')=='Total Liabilities and Equity':
                    index_1 = result_acc.index(res_acc)
                    a.append(index_1)
            for ele in a:
                result_acc.insert(ele,self.total_profit_loss)
                result_acc.pop(ele+2)
#            
            total_liabilities_equity = self.total_liabilities_equity + self.net_profit
#            total_comp0_liabilities_equity = self.comp0_tot_liabilities_equity + abs(self.comp0_net_profit)
#            total_comp1_liabilities_equity = self.comp1_tot_liabilities_equity + abs(self.comp1_net_profit)
            self.total_liabilities_equity = {
                'balance' : total_liabilities_equity, 
                'id'        : False, 
                'type' : 'view', 
                'code' : '', 
                'name' : 'Total Liabilities & Owners Equity', 
                'parent_id' : False, 
                'level' : 1, 
                'credit' : 0.0, 
                'debit' : 0.0, 
                'label' : False, 
                'mayor' : [], 
                'total' :True, 
                'change_sign' : 1, 
                'balanceinit' : 0.0, 
                'ytd' : total_liabilities_equity 
            }
#            
#            if form['compr0_fiscalyear_id']:
#                self.total_liabilities_equity.update({
#                    'compr0_balance' : total_comp0_liabilities_equity,
#                    'compr0_balanceinit' : 0.00,
#                    'compr0_debit' : 0.00,
#                    'compr0_credit' : 0.00,
#                    'compr0_ytd' : self.comp0_tot_liabilities + abs(self.comp0_net_profit)
#                })
#                
#            if form['compr1_fiscalyear_id']:
#                self.total_liabilities_equity.update({
#                    'compr1_balance' : total_comp1_liabilities_equity,
#                    'compr1_balanceinit' : 0.00,
#                    'compr1_debit' : 0.00,
#                    'compr1_credit' : 0.00,
#                    'compr1_ytd' : self.comp1_tot_liabilities + abs(self.comp1_net_profit)
#                })
#            result_acc.append(self.total_liabilities_equity)
#            dict = {'balance': 0.0, 'code': '69', 'name': 'Total Other Income/Expense', 'level': 1, 'credit': 0.0, 'debit': 0.0, 'label': False, 'parent_id': 310, 'mayor': [], 'change_sign': 1, 'balanceinit': 0.0, 'ytd': 0.0, 'total': True, 'type': 'view', 'id': 586}
#            index = result_acc.index(dict)
#            result_acc.pop(index)
#            dict_expence = {'balance': 0.0, 'code': '80', 'name': 'Total Other Expense', 'level': 2, 'credit': 0.0, 'debit': 0.0, 'label': False, 'parent_id': 586, 'mayor': [], 'change_sign': 1, 'balanceinit': 0.0, 'ytd': 0.0, 'total': True, 'type': 'view', 'id': 590}
#            index_exp = result_acc.index(dict_expence)
#            result_acc.pop(index_exp)
#            
        else:
            if not form['afr_id'][1] == 'Balance Sheet':
#                if {'id': False, 'name': ''} not in result_acc:
#                        raise osv.except_osv(_('Configuration Error'), _('Please configure all type of Revenue, Cost Of Goods Sold, Expense, Income and Taxes accounts for Income Statement !'))
#                index = result_acc.index({'id': False, 'name': ''})
                for res_acc in result_acc:
                    if res_acc.get('name')=='Total Net Ordinary Income':
                        index = result_acc.index(res_acc)
                        result_acc.insert(index+11,res_acc)
                        result_acc.pop(index)
                
                total_gross_profit = self.gross_profit
#                total_comp0_gross_profit = self.comp0_gross_profit
#                total_comp1_gross_profit = self.comp1_gross_profit
                self.gross_profit_dict = {
                    'balance' : total_gross_profit, 
                    'id'        : False, 
                    'type' : 'view', 
                    'code' : '', 
                    'name' : 'Gross Profit', 
                    'parent_id' : False, 
                    'level' : 1, 
                    'credit' : 0.0, 
                    'debit' : 0.0, 
                    'label' : False, 
                    'mayor' : [], 
                    'total' :True, 
                    'change_sign' : 1, 
                    'balanceinit' : 0.0, 
                    'ytd' : total_gross_profit 
                }
#                
#                if form['compr0_fiscalyear_id']:
#                    self.gross_profit_dict.update({
#                        'compr0_balance' : total_comp0_gross_profit,
#                        'compr0_balanceinit' : 0.00,
#                        'compr0_debit' : 0.00,
#                        'compr0_credit' : 0.00,
#                        'compr0_ytd' : abs(self.comp0_tot_revenue - self.comp0_tot_cogs),
#                    })
#                if form['compr1_fiscalyear_id']:
#                    self.gross_profit_dict.update({
#                        'compr1_balance' : total_comp1_gross_profit,
#                        'compr1_balanceinit' : 0.00,
#                        'compr1_debit' : 0.00,
#                        'compr1_credit' : 0.00,
#                        'compr1_ytd' : abs(self.comp1_tot_revenue - self.comp1_tot_cogs),
#                    })
#                result_acc.insert(index+2, self.gross_profit_dict)
#                result_acc.append(self.gross_profit_dict)
#                result_acc.pop(index)
#                
                tot_expense = self.total_exp
#                tot_comp0_expense = self.comp0_total_expense
#                tot_comp1_expense = self.comp1_total_expense
                self.tot_exp = {
                    'balance' : tot_expense, 
                    'id'        : False, 
                    'type' : 'view', 
                    'code' : '', 
                    'name' : 'Total Expense', 
                    'parent_id' : False, 
                    'level' : 1, 
                    'credit' : 0.0, 
                    'debit' : 0.0, 
                    'label' : False, 
                    'mayor' : [], 
                    'total' :True, 
                    'change_sign' : 1, 
                    'balanceinit' : 0.0, 
                    'ytd' : tot_expense 
                }
#                
#                if form['compr0_fiscalyear_id']:
#                    self.tot_exp.update({
#                        'compr0_balance' : tot_comp0_expense,
#                        'compr0_balanceinit' : 0.00,
#                        'compr0_debit' : 0.00,
#                        'compr0_credit' : 0.00,
#                        'compr0_ytd' : abs(self.comp0_operating_expense + self.comp0_taxes + self.comp0_other_expense),
#                    })
#                    
#                if form['compr1_fiscalyear_id']:
#                    self.tot_exp.update({
#                        'compr1_balance' : tot_comp1_expense,
#                        'compr1_balanceinit' : 0.00,
#                        'compr1_debit' : 0.00,
#                        'compr1_credit' : 0.00,
#                        'compr1_ytd' : abs(self.comp1_operating_expense + self.comp1_taxes + self.comp1_other_expense),
#                    })
#                    
#                result_acc.append(self.tot_exp)
#                
                net_profit = self.net_profit
#                net_comp0_profit = self.comp0_net_profit
#                net_comp1_profit = self.comp1_net_profit
                self.tot_net_prodict = {
                    'balance' : net_profit, 
                    'id'        : False, 
                    'type' : 'view', 
                    'code' : '', 
                    'name' : 'Net Profit', 
                    'parent_id' : False, 
                    'level' : 1, 
                    'credit' : 0.0, 
                    'debit' : 0.0, 
                    'label' : False, 
                    'mayor' : [], 
                    'total' :True, 
                    'change_sign' : 1, 
                    'balanceinit' : 0.0, 
                    'ytd' : net_profit 
                }
#                if form['compr0_fiscalyear_id']:
#                    self.tot_net_prodict.update({
#                        'compr0_balance' : net_comp0_profit,
#                        'compr0_balanceinit' : 0.00,
#                        'compr0_debit' : 0.00,
#                        'compr0_credit' : 0.00,
#                        'compr0_ytd' : abs(self.comp0_gross_profit + self.comp0_other_income - self.comp0_total_expense),
#                    })
#                    
#                if form['compr1_fiscalyear_id']:
#                    self.tot_net_prodict.update({
#                        'compr1_balance' : net_comp1_profit,
#                        'compr1_balanceinit' : 0.00,
#                        'compr1_debit' : 0.00,
#                        'compr1_credit' : 0.00,
#                        'compr1_ytd' : abs(self.comp1_gross_profit + self.comp1_other_income - self.comp1_total_expense),
#                    })
#    
                
#                result_acc.append(self.tot_net_prodict)
                
        return result_acc
    
    
report_sxw.report_sxw('report.afr.1cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/balance_full.rml', 
                       parser=account_balance_inherit, 
                       header=False)

report_sxw.report_sxw('report.afr.2cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/balance_full_2_cols.rml', 
                       parser=account_balance_inherit, 
                       header=False)

report_sxw.report_sxw('report.afr.4cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/balance_full_4_cols.rml', 
                       parser=account_balance_inherit, 
                       header=False)

report_sxw.report_sxw('report.afr.analytic.ledger.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/balance_full_4_cols_analytic_ledger.rml', 
                       parser=account_balance_inherit, 
                       header=False)
                       
report_sxw.report_sxw('report.afr.5cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/balance_full_5_cols.rml', 
                       parser=account_balance_inherit, 
                       header=False)
                       
report_sxw.report_sxw('report.afr.qtrcols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/balance_full_qtr_cols.rml', 
                       parser=account_balance_inherit, 
                       header=False)

report_sxw.report_sxw('report.afr.13cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/balance_full_13_cols.rml', 
                       parser=account_balance_inherit, 
                       header=False)

report_sxw.report_sxw('report.periodic1.1cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/periodic_financial_report.rml', 
                       parser=account_balance_inherit, 
                       header=False)


report_sxw.report_sxw('report.periodic3.4cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/periodic_financial_report_3_4cols.rml', 
                       parser=account_balance_inherit, 
                       header=False)

report_sxw.report_sxw('report.periodic2.4cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/periodic_financial_report_4cols.rml', 
                       parser=account_balance_inherit, 
                       header=False)

report_sxw.report_sxw('report.periodic2.2cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/periodic_financial_report_2_2cols.rml', 
                       parser=account_balance_inherit, 
                       header=False)

report_sxw.report_sxw('report.periodic1.2cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/periodic_financial_report_2cols.rml', 
                       parser=account_balance_inherit, 
                       header=False)

report_sxw.report_sxw('report.periodic3.1cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/periodic_financial_report_3.rml', 
                       parser=account_balance_inherit, 
                       header=False)

report_sxw.report_sxw('report.periodic2.1cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/periodic_financial_report_2.rml', 
                       parser=account_balance_inherit, 
                       header=False)

report_sxw.report_sxw('report.periodic.2cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/periodic_financial_report_1_2cols.rml', 
                       parser=account_balance_inherit, 
                       header=False)

report_sxw.report_sxw('report.periodic.4cols.inherit', 
                      'wizard.report', 
                      'addons/sunpro_account_financial_report/report/periodic_financial_report_1_4cols.rml', 
                       parser=account_balance_inherit, 
                       header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: