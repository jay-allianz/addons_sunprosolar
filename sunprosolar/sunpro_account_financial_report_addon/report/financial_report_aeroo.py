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

class Parser(account_balance):
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
        
        self.debit_total = 0.00
        self.credit_total = 0.00
        
        self.comp_debit_total = 0.00
        self.comp_credit_total = 0.00
        
        self.bal1 = 0.00
        self.bal2 = 0.00
        self.bal3 = 0.00
        self.bal4 = 0.00
        self.bal5 = 0.00
        
        self.tot_other_income1 = 0.00
        self.tot_other_income2 = 0.00
        self.tot_other_income3 = 0.00
        self.tot_other_income4 = 0.00
        self.tot_other_income5 = 0.00
        
        self.gross_profit1 = 0.00
        self.gross_profit2 = 0.00
        self.gross_profit3 = 0.00
        self.gross_profit4 = 0.00
        self.gross_profit5 = 0.00
        
        self.total_exp1 = 0.00
        self.total_exp2 = 0.00
        self.total_exp3 = 0.00
        self.total_exp4 = 0.00
        self.total_exp5 = 0.00
        
        self.net_profit1 = 0.00
        self.net_profit2 = 0.00
        self.net_profit3 = 0.00
        self.net_profit4 = 0.00
        self.net_profit5 = 0.00
        
        self.othexp1 = 0.00
        self.othexp2 = 0.00
        self.othexp3 = 0.00
        self.othexp4 = 0.00
        self.othexp5 = 0.00
        
        self.exp1 = 0.00
        self.exp2 = 0.00
        self.exp3 = 0.00
        self.exp4 = 0.00
        self.exp5 = 0.00
        
        self.total_balance_sheet_balance1 = 0.00
        self.total_balance_sheet_balance2 = 0.00
        self.total_balance_sheet_balance3 = 0.00
        self.total_balance_sheet_balance4 = 0.00
        self.total_balance_sheet_balance5 = 0.00
        
        self.total_liabilities_equity1 = 0.00
        self.total_liabilities_equity2 = 0.00
        self.total_liabilities_equity3 = 0.00
        self.total_liabilities_equity4 = 0.00
        self.total_liabilities_equity5 = 0.00
        
        self.bal_mon1 = 0.00
        self.bal_mon2 = 0.00
        self.bal_mon3 = 0.00
        self.bal_mon4 = 0.00
        self.bal_mon5 = 0.00
        self.bal_mon6 = 0.00
        self.bal_mon7 = 0.00
        self.bal_mon8 = 0.00
        self.bal_mon9 = 0.00
        self.bal_mon10 = 0.00
        self.bal_mon11 = 0.00
        self.bal_mon12 = 0.00
        self.bal_mon13 = 0.00
        
        self.gross_profit_mon1 = 0.00
        self.gross_profit_mon2 = 0.00
        self.gross_profit_mon3 = 0.00
        self.gross_profit_mon4 = 0.00
        self.gross_profit_mon5 = 0.00
        self.gross_profit_mon6 = 0.00
        self.gross_profit_mon7 = 0.00
        self.gross_profit_mon8 = 0.00
        self.gross_profit_mon9 = 0.00
        self.gross_profit_mon10 = 0.00
        self.gross_profit_mon11 = 0.00
        self.gross_profit_mon12 = 0.00
        self.gross_profit_mon13 = 0.00
        
        self.exp_mon1 = 0.00
        self.exp_mon2 = 0.00
        self.exp_mon3 = 0.00
        self.exp_mon4 = 0.00
        self.exp_mon5 = 0.00
        self.exp_mon6 = 0.00
        self.exp_mon7 = 0.00
        self.exp_mon8 = 0.00
        self.exp_mon9 = 0.00
        self.exp_mon10 = 0.00
        self.exp_mon11 = 0.00
        self.exp_mon12 = 0.00
        self.exp_mon13 = 0.00
        
        self.total_exp_mon1 = 0.00
        self.total_exp_mon2 = 0.00
        self.total_exp_mon3 = 0.00
        self.total_exp_mon4 = 0.00
        self.total_exp_mon5 = 0.00
        self.total_exp_mon6 = 0.00
        self.total_exp_mon7 = 0.00
        self.total_exp_mon8 = 0.00
        self.total_exp_mon9 = 0.00
        self.total_exp_mon10 = 0.00
        self.total_exp_mon11 = 0.00
        self.total_exp_mon12 = 0.00
        self.total_exp_mon13 = 0.00
        
        self.tot_taxes1 = 0.00
        self.tot_taxes2 = 0.00
        self.tot_taxes3 = 0.00
        self.tot_taxes4 = 0.00
        self.tot_taxes5 = 0.00
        self.tot_taxes6 = 0.00
        self.tot_taxes7 = 0.00
        self.tot_taxes8 = 0.00
        self.tot_taxes9 = 0.00
        self.tot_taxes10 = 0.00
        self.tot_taxes11 = 0.00
        self.tot_taxes12 = 0.00
        self.tot_taxes13 = 0.00
        
        self.tot_other_exp1 = 0.00
        self.tot_other_exp2 = 0.00
        self.tot_other_exp3 = 0.00
        self.tot_other_exp4 = 0.00
        self.tot_other_exp5 = 0.00
        self.tot_other_exp6 = 0.00
        self.tot_other_exp7 = 0.00
        self.tot_other_exp8 = 0.00
        self.tot_other_exp9 = 0.00
        self.tot_other_exp10 = 0.00
        self.tot_other_exp11 = 0.00
        self.tot_other_exp12 = 0.00
        self.tot_other_exp13 = 0.00
        
        self.tot_oth_income1 = 0.00
        self.tot_oth_income2 = 0.00
        self.tot_oth_income3 = 0.00
        self.tot_oth_income4 = 0.00
        self.tot_oth_income5 = 0.00
        self.tot_oth_income6 = 0.00
        self.tot_oth_income7 = 0.00
        self.tot_oth_income8 = 0.00
        self.tot_oth_income9 = 0.00
        self.tot_oth_income10 = 0.00
        self.tot_oth_income11 = 0.00
        self.tot_oth_income12 = 0.00
        self.tot_oth_income13 = 0.00
        
        self.net_profit_mon1 = 0.00
        self.net_profit_mon2 = 0.00
        self.net_profit_mon3 = 0.00
        self.net_profit_mon4 = 0.00
        self.net_profit_mon5 = 0.00
        self.net_profit_mon6 = 0.00
        self.net_profit_mon7 = 0.00
        self.net_profit_mon8 = 0.00
        self.net_profit_mon9 = 0.00
        self.net_profit_mon10 = 0.00
        self.net_profit_mon11 = 0.00
        self.net_profit_mon12 = 0.00
        self.net_profit_mon13 = 0.00
        
        self.total_balance_sheet_balance_mon1 = 0.00
        self.total_balance_sheet_balance_mon2 = 0.00
        self.total_balance_sheet_balance_mon3 = 0.00
        self.total_balance_sheet_balance_mon4 = 0.00
        self.total_balance_sheet_balance_mon5 = 0.00
        self.total_balance_sheet_balance_mon6 = 0.00
        self.total_balance_sheet_balance_mon7 = 0.00
        self.total_balance_sheet_balance_mon8 = 0.00
        self.total_balance_sheet_balance_mon9 = 0.00
        self.total_balance_sheet_balance_mon10 = 0.00
        self.total_balance_sheet_balance_mon11 = 0.00
        self.total_balance_sheet_balance_mon12 = 0.00
        self.total_balance_sheet_balance_mon13 = 0.00
        
        self.equity_mon1 = 0.00
        self.equity_mon2 = 0.00
        self.equity_mon3 = 0.00
        self.equity_mon4 = 0.00
        self.equity_mon5 = 0.00
        self.equity_mon6 = 0.00
        self.equity_mon7 = 0.00
        self.equity_mon8 = 0.00
        self.equity_mon9 = 0.00
        self.equity_mon10 = 0.00
        self.equity_mon11 = 0.00
        self.equity_mon12 = 0.00
        self.equity_mon13 = 0.00
        
        
        self.total_liabilities_equity_mon1 = 0.00
        self.total_liabilities_equity_mon2 = 0.00
        self.total_liabilities_equity_mon3 = 0.00
        self.total_liabilities_equity_mon4 = 0.00
        self.total_liabilities_equity_mon5 = 0.00
        self.total_liabilities_equity_mon6 = 0.00
        self.total_liabilities_equity_mon7 = 0.00
        self.total_liabilities_equity_mon8 = 0.00
        self.total_liabilities_equity_mon9 = 0.00
        self.total_liabilities_equity_mon10 = 0.00
        self.total_liabilities_equity_mon11 = 0.00
        self.total_liabilities_equity_mon12 = 0.00
        self.total_liabilities_equity_mon13 = 0.00
        
        self.exp1 = 0.00
        self.exp2 = 0.00
        self.exp3 = 0.00
        self.exp4 = 0.00
        self.exp5 = 0.00
        
        self.taxes1 = 0.00
        self.taxes2 = 0.00
        self.taxes3 = 0.00
        self.taxes4 = 0.00
        self.taxes5 = 0.00
        
        self.othexp1 = 0.00
        self.othexp2 = 0.00
        self.othexp3 = 0.00
        self.othexp4 = 0.00
        self.othexp5 = 0.00
        
        
        self.net_income_loss = 0.00
        self.total_balance_of_bs = 0.00
        self.net_profit_loss_periodic = 0.00
        self.total_balance_of_bs_periodic = 0.00
        self.total_liabilities_equity_new = 0.00
        self.liab = 0.00
        self.equ = 0.00
        self.total_liab_periodic = 0.00
        self.total_equ_periodic = 0.00
        self.total_liab_equ_periodic = 0.00
        self.profit_loss_comp1 = 0.00
        self.profit_loss_comp0 = 0.00
        self.total_liab_comp0 = 0.00
        self.total_liab_comp1 = 0.00
        self.total_equ_comp0 = 0.00
        self.total_equ_comp1 = 0.00
        self.total_liab_equ_comp0 = 0.00
        self.total_liab_equ_comp1 = 0.00
#        
#        self.context = context
        
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_debit' : self.get_debit,
            'get_total_debit' : self.get_total_debit,
            'get_credit' : self.get_credit,
            'get_total_credit' : self.get_total_credit,
            'get_comp_debit' : self.get_comp_debit,
            'get_total_comp_debit' : self.get_total_comp_debit,
            'get_comp_credit' : self.get_comp_credit,
            'get_total_comp_credit' : self.get_total_comp_credit
        })
        
    def get_debit(self, debit, level, type, name):
        if type in ['other', 'liquidity', 'receivable', 'payable']: 
            self.debit_total += debit
        return debit
    
    def get_total_debit(self):
        return self.debit_total
    
    def get_credit(self, credit, level, type, name):
        if type in ['other', 'liquidity', 'receivable', 'payable']: 
            self.credit_total += credit
        return credit
    
    def get_total_credit(self):
        return self.credit_total
            
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
        bal = []
        bal_list = []
        dict = {}
#        if 'earning_account' in form and not isinstance(form['earning_account'], int):
#            form['earning_account'] = form['earning_account'][0]
        def _get_children_and_consol(cr, uid, ids, level, context={}, change_sign=False):
            aa_obj = self.pool.get('account.account')
            ids2=[]
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
#
        if form['columns'] == 'qtr':
            tot_bal1 = 0.0
            tot_bal2 = 0.0
            tot_bal3 = 0.0
            tot_bal4 = 0.0
            tot_bal5 = 0.0

        elif form['columns'] == 'thirteen':
            tot_bal1 = 0.0
            tot_bal2 = 0.0
            tot_bal3 = 0.0
            tot_bal4 = 0.0
            tot_bal5 = 0.0
            tot_bal6 = 0.0
            tot_bal7 = 0.0
            tot_bal8 = 0.0
            tot_bal9 = 0.0
            tot_bal10 = 0.0
            tot_bal11 = 0.0
            tot_bal12 = 0.0
            tot_bal13 = 0.0

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
                                    self.bal1 = self.bal1 + res.get('bal1')
                                    self.bal2 = self.bal2 + res.get('bal2')
                                    self.bal3 = self.bal3 + res.get('bal3')
                                    self.bal4 = self.bal4 + res.get('bal4')
                                    self.bal5 = self.bal5 + res.get('bal5')
                                bal1 = []
                                bal2 = []
                                bal3 = []
                                bal4 = []
                                bal5 = []
                                for res_acc in result_acc:
                                    if res_acc.get('name')=='Total Net Ordinary Income':
                                        balance_res1 = res_acc.get('bal1')
                                        balance_res2 = res_acc.get('bal2')
                                        balance_res3 = res_acc.get('bal3')
                                        balance_res4 = res_acc.get('bal4')
                                        balance_res5 = res_acc.get('bal5')
                                        bal1.append(balance_res1)
                                        bal2.append(balance_res2)
                                        bal3.append(balance_res3)
                                        bal4.append(balance_res4)
                                        bal5.append(balance_res5)
                                if len(bal1) > 0:
                                    self.gross_profit1 = bal1[0]
                                if len(bal2) > 0:
                                    self.gross_profit2 = bal2[0]
                                if len(bal3) > 0:
                                    self.gross_profit3 = bal3[0]
                                if len(bal4) > 0:
                                    self.gross_profit4 = bal4[0]
                                if len(bal5) > 0:
                                    self.gross_profit5 = bal5[0]
                                for acc in account_obj.browse(self.cr, self.uid, acc_ids):
                                    if acc.name == 'Cost Of Goods Sold' or acc.name == 'Cost of Sales' and acc.user_type.name == 'Income View' or acc.user_type.name == 'Income':
                                        if res.get('name').lower() == 'total cost of sales':
                                            result_acc.append({'id': False, 'name': ''})
                                    
                                    if acc.name == 'Expense' or acc.name.lower() == 'expense' and acc.user_type.name == 'Expense' or acc.user_type.name == 'Expense View':
                                        self.exp1 = res.get('bal1')
                                        self.exp2 = res.get('bal2')
                                        self.exp3 = res.get('bal3')
                                        self.exp4 = res.get('bal4')
                                        self.exp5 = res.get('bal5')
                                    
                                    if acc.name == 'Taxes' or acc.name.lower() == 'taxes' and acc.user_type.name == 'Expense' or acc.user_type.name == 'Expense View':
                                        self.taxes1 = res.get('bal1')
                                        self.taxes2 = res.get('bal2')
                                        self.taxes3 = res.get('bal3')
                                        self.taxes4 = res.get('bal4')
                                        self.taxes5 = res.get('bal5')
                                        
                                    if acc.name == 'Other Expense' or acc.name.lower() == 'other expense' and acc.user_type.name == 'Expense' or acc.user_type.name == 'Expense View':
                                        self.othexp1 = res.get('bal1')
                                        self.othexp2 = res.get('bal2')
                                        self.othexp3 = res.get('bal3')
                                        self.othexp4 = res.get('bal4')
                                        self.othexp5 = res.get('bal5')
                                        
                                    if acc.name == 'Other Income' or acc.name.lower() == 'other income' and acc.user_type.name == 'Income' or acc.user_type.name == 'Income View':
                                        self.tot_other_income1 = res.get('bal1')
                                        self.tot_other_income2 = res.get('bal2')
                                        self.tot_other_income3 = res.get('bal3')
                                        self.tot_other_income4 = res.get('bal4')
                                        self.tot_other_income5 = res.get('bal5')
                                        
                                self.total_exp1 = self.exp1 + self.taxes1 + self.othexp1
                                self.total_exp2 = self.exp2 + self.taxes2 + self.othexp2
                                self.total_exp3 = self.exp3 + self.taxes3 + self.othexp3
                                self.total_exp4 = self.exp4 + self.taxes4 + self.othexp4
                                self.total_exp5 = self.exp5 + self.taxes5 + self.othexp5
                                
                                if res.get('total')== True and res.get('type') == 'view' and res.get('level') == 1:
                                    self.net_profit1 += res.get('bal1')
                                    self.net_profit1 += res.get('bal2')
                                    self.net_profit1 += res.get('bal3')
                                    self.net_profit1 += res.get('bal4')
                                    self.net_profit1 += res.get('bal5')


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
                        report_data = wiz_rep.browse(self.cr, self.uid, self.context.get('active_id'))
                        for ytd_acc_data in report_data.account_list:
                            if ytd_acc_data.type == 'view':
                                parent_id = ytd_acc_data.parent_id.id
                        parent_acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',False)])
                        child_acc_ids = account_obj.search(self.cr, self.uid, ['|',('parent_id','in',parent_acc_ids),('level','=',1)])
                        for acc_data in account_obj.browse(self.cr, self.uid, child_acc_ids):
                            if parent_id == acc_data.id:
                                acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',acc_data.id)])
                                if res.get('total') == True and res.get('type') == 'view' and res.get('parent_id') == acc_data.id:
                                    self.total_balance_sheet_balance1 = self.total_balance_sheet_balance1 + res.get('bal1')
                                    self.total_balance_sheet_balance2 = self.total_balance_sheet_balance2 + res.get('bal2')
                                    self.total_balance_sheet_balance3 = self.total_balance_sheet_balance3 + res.get('bal3')
                                    self.total_balance_sheet_balance4 = self.total_balance_sheet_balance4 + res.get('bal4')
                                    self.total_balance_sheet_balance5 = self.total_balance_sheet_balance5 + res.get('bal5')
                                self.total_liabilities_equity1 = self.total_balance_sheet_balance1
                                self.total_liabilities_equity2 = self.total_balance_sheet_balance2
                                self.total_liabilities_equity3 = self.total_balance_sheet_balance3
                                self.total_liabilities_equity4 = self.total_balance_sheet_balance4
                                self.total_liabilities_equity5 = self.total_balance_sheet_balance5
                
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
#                         res.update({
#                             'balance': self.exchange(d-c), 
#                         })
                        res.update({
                            'dbr13': self.exchange(d), 
                            'cdr13': self.exchange(c), 
                            'bal13': self.exchange(b), 
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
                                    self.bal_mon1 = self.bal_mon1 + res.get('bal1')
                                    self.bal_mon2 = self.bal_mon2 + res.get('bal2')
                                    self.bal_mon3 = self.bal_mon3 + res.get('bal3')
                                    self.bal_mon4 = self.bal_mon4 + res.get('bal4')
                                    self.bal_mon5 = self.bal_mon5 + res.get('bal5')
                                    self.bal_mon6 = self.bal_mon6 + res.get('bal6')
                                    self.bal_mon7 = self.bal_mon7 + res.get('bal7')
                                    self.bal_mon8 = self.bal_mon8 + res.get('bal8')
                                    self.bal_mon9 = self.bal_mon9 + res.get('bal9')
                                    self.bal_mon10 = self.bal_mon10 + res.get('bal10')
                                    self.bal_mon11 = self.bal_mon11 + res.get('bal11')
                                    self.bal_mon12 = self.bal_mon12 + res.get('bal12')
                                    self.bal_mon13 = self.bal_mon13 + res.get('bal13')
                                bal1 = []
                                bal2 = []
                                bal3 = []
                                bal4 = []
                                bal5 = []
                                bal6 = []
                                bal7 = []
                                bal8 = []
                                bal9 = []
                                bal10 = []
                                bal11 = []
                                bal12 = []
                                bal13 = []
                                for res_acc in result_acc:
                                    if res_acc.get('name')=='Total Net Ordinary Income':
                                        balance_res1 = res_acc.get('bal1')
                                        balance_res2 = res_acc.get('bal2')
                                        balance_res3 = res_acc.get('bal3')
                                        balance_res4 = res_acc.get('bal4')
                                        balance_res5 = res_acc.get('bal5')
                                        balance_res6 = res_acc.get('bal6')
                                        balance_res7 = res_acc.get('bal7')
                                        balance_res8 = res_acc.get('bal8')
                                        balance_res9 = res_acc.get('bal9')
                                        balance_res10 = res_acc.get('bal10')
                                        balance_res11 = res_acc.get('bal11')
                                        balance_res12 = res_acc.get('bal12')
                                        balance_res13 = res_acc.get('bal13')
                                        
                                        bal1.append(balance_res1)
                                        bal2.append(balance_res2)
                                        bal3.append(balance_res3)
                                        bal4.append(balance_res4)
                                        bal5.append(balance_res5)
                                        bal6.append(balance_res6)
                                        bal7.append(balance_res7)
                                        bal8.append(balance_res8)
                                        bal9.append(balance_res9)
                                        bal10.append(balance_res10)
                                        bal11.append(balance_res11)
                                        bal12.append(balance_res12)
                                        bal13.append(balance_res13)
                                        
                                if len(bal1) > 0:
                                    self.gross_profit_mon1 = bal1[0]
                                if len(bal2) > 0:
                                    self.gross_profit_mon2 = bal2[0]
                                if len(bal3) > 0:
                                    self.gross_profit_mon3 = bal3[0]
                                if len(bal4) > 0:
                                    self.gross_profit_mon4 = bal4[0]
                                if len(bal5) > 0:
                                    self.gross_profit_mon5 = bal5[0]
                                if len(bal6) > 0:
                                    self.gross_profit_mon6 = bal6[0]
                                if len(bal7) > 0:
                                    self.gross_profit_mon7 = bal7[0]
                                if len(bal8) > 0:
                                    self.gross_profit_mon8 = bal8[0]
                                if len(bal9) > 0:
                                    self.gross_profit_mon9 = bal9[0]
                                if len(bal10) > 0:
                                    self.gross_profit_mon10 = bal10[0]
                                if len(bal11) > 0:
                                    self.gross_profit_mon11 = bal11[0]
                                if len(bal12) > 0:
                                    self.gross_profit_mon12 = bal12[0]
                                if len(bal13) > 0:
                                    self.gross_profit_mon13 = bal13[0]
                                    
                                for acc in account_obj.browse(self.cr, self.uid, acc_ids):
                                    if acc.name == 'Cost Of Goods Sold' or acc.name == 'Cost of Sales' and acc.user_type.name == 'Income View' or acc.user_type.name == 'Income':
                                        if res.get('name').lower() == 'total cost of sales':
                                            result_acc.append({'id': False, 'name': ''})
                                    
                                    if acc.name == 'Expense' or acc.name.lower() == 'expense' and acc.user_type.name == 'Expense' or acc.user_type.name == 'Expense View':
                                        self.exp_mon1 = res.get('bal1')
                                        self.exp_mon2 = res.get('bal2')
                                        self.exp_mon3 = res.get('bal3')
                                        self.exp_mon4 = res.get('bal4')
                                        self.exp_mon5 = res.get('bal5')
                                        self.exp_mon6 = res.get('bal6')
                                        self.exp_mon7 = res.get('bal7')
                                        self.exp_mon8 = res.get('bal8')
                                        self.exp_mon9 = res.get('bal9')
                                        self.exp_mon10 = res.get('bal10')
                                        self.exp_mon11 = res.get('bal11')
                                        self.exp_mon12 = res.get('bal12')
                                        self.exp_mon13 = res.get('bal13')
                                        
                                    if acc.name == 'Taxes' or acc.name.lower() == 'taxes' and acc.user_type.name == 'Expense' or acc.user_type.name == 'Expense View':
                                        self.tot_taxes1 = res.get('bal1')
                                        self.tot_taxes2 = res.get('bal2')
                                        self.tot_taxes3 = res.get('bal3')
                                        self.tot_taxes4 = res.get('bal4')
                                        self.tot_taxes5 = res.get('bal5')
                                        self.tot_taxes6 = res.get('bal6')
                                        self.tot_taxes7 = res.get('bal7')
                                        self.tot_taxes8 = res.get('bal8')
                                        self.tot_taxes9 = res.get('bal9')
                                        self.tot_taxes10 = res.get('bal10')
                                        self.tot_taxes11 = res.get('bal11')
                                        self.tot_taxes12 = res.get('bal12')
                                        self.tot_taxes13 = res.get('bal13')
                                        
                                    if acc.name == 'Other Expense' or acc.name.lower() == 'other expense' and acc.user_type.name == 'Expense' or acc.user_type.name == 'Expense View':
                                        self.tot_other_exp1 = res.get('bal1')
                                        self.tot_other_exp2 = res.get('bal2')
                                        self.tot_other_exp3 = res.get('bal3')
                                        self.tot_other_exp4 = res.get('bal4')
                                        self.tot_other_exp5 = res.get('bal5')
                                        self.tot_other_exp6 = res.get('bal6')
                                        self.tot_other_exp7 = res.get('bal7')
                                        self.tot_other_exp8 = res.get('bal8')
                                        self.tot_other_exp9 = res.get('bal9')
                                        self.tot_other_exp10 = res.get('bal10')
                                        self.tot_other_exp11 = res.get('bal11')
                                        self.tot_other_exp12 = res.get('bal12')
                                        self.tot_other_exp13 = res.get('bal13')
                                        
                                    if acc.name == 'Other Income' or acc.name.lower() == 'other income' and acc.user_type.name == 'Income' or acc.user_type.name == 'Income View':
                                        self.tot_oth_income1 = res.get('bal1')
                                        self.tot_oth_income2 = res.get('bal2')
                                        self.tot_oth_income3 = res.get('bal3')
                                        self.tot_oth_income4 = res.get('bal4')
                                        self.tot_oth_income5 = res.get('bal5')
                                        self.tot_oth_income6 = res.get('bal6')
                                        self.tot_oth_income7 = res.get('bal7')
                                        self.tot_oth_income8 = res.get('bal8')
                                        self.tot_oth_income9 = res.get('bal9')
                                        self.tot_oth_income10 = res.get('bal10')
                                        self.tot_oth_income11 = res.get('bal11')
                                        self.tot_oth_income12 = res.get('bal12')
                                        self.tot_oth_income13 = res.get('bal13')
                                        
                                self.total_exp_mon1 = self.exp_mon1 + self.tot_taxes1 + self.tot_other_exp1
                                self.total_exp_mon2 = self.exp_mon2 + self.tot_taxes2 + self.tot_other_exp2
                                self.total_exp_mon3 = self.exp_mon3 + self.tot_taxes3 + self.tot_other_exp3
                                self.total_exp_mon4 = self.exp_mon4 + self.tot_taxes4 + self.tot_other_exp4
                                self.total_exp_mon5 = self.exp_mon5 + self.tot_taxes5 + self.tot_other_exp5
                                self.total_exp_mon6 = self.exp_mon6 + self.tot_taxes6 + self.tot_other_exp6
                                self.total_exp_mon7 = self.exp_mon7 + self.tot_taxes7 + self.tot_other_exp7
                                self.total_exp_mon8 = self.exp_mon8 + self.tot_taxes8 + self.tot_other_exp8
                                self.total_exp_mon9 = self.exp_mon9 + self.tot_taxes9 + self.tot_other_exp9
                                self.total_exp_mon10 = self.exp_mon10 + self.tot_taxes10 + self.tot_other_exp10
                                self.total_exp_mon11 = self.exp_mon11 + self.tot_taxes11 + self.tot_other_exp11
                                self.total_exp_mon12 = self.exp_mon12 + self.tot_taxes12 + self.tot_other_exp12
                                self.total_exp_mon13 = self.exp_mon13 + self.tot_taxes13 + self.tot_other_exp13
                                            
                        if res.get('total')== True and res.get('type') == 'view' and res.get('level') == 1:
                            self.net_profit_mon1 += res.get('bal1')
                            self.net_profit_mon2 += res.get('bal2')
                            self.net_profit_mon3 += res.get('bal3')
                            self.net_profit_mon4 += res.get('bal4')
                            self.net_profit_mon5 += res.get('bal5')
                            self.net_profit_mon6 += res.get('bal6')
                            self.net_profit_mon7 += res.get('bal7')
                            self.net_profit_mon8 += res.get('bal8')
                            self.net_profit_mon9 += res.get('bal9')
                            self.net_profit_mon10 += res.get('bal10')
                            self.net_profit_mon11 += res.get('bal11')
                            self.net_profit_mon12 += res.get('bal12')
                            self.net_profit_mon13 += res.get('bal13')

                                    
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
                        
                        report_data = wiz_rep.browse(self.cr, self.uid, self.context.get('active_id'))
                        for ytd_acc_data in report_data.account_list:
                            if ytd_acc_data.type == 'view':
                                parent_id = ytd_acc_data.parent_id.id
                        parent_acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',False)])
                        child_acc_ids = account_obj.search(self.cr, self.uid, ['|',('parent_id','in',parent_acc_ids),('level','=',1)])
                        for acc_data in account_obj.browse(self.cr, self.uid, child_acc_ids):
                            if parent_id == acc_data.id:
                                acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',acc_data.id)])
                                if acc_data.user_type.name == 'Liability' and acc_data.type == 'view':
                                    if res.get('total') == True and res.get('type') == 'view':
                                        if res.get('name').lower() == 'total liabilities':
                                            self.total_balance_sheet_balance_mon1 = res.get('bal1')
                                            self.total_balance_sheet_balance_mon2 = res.get('bal2')
                                            self.total_balance_sheet_balance_mon3 = res.get('bal3')
                                            self.total_balance_sheet_balance_mon4 = res.get('bal4')
                                            self.total_balance_sheet_balance_mon5 = res.get('bal5')
                                            self.total_balance_sheet_balance_mon6 = res.get('bal6')
                                            self.total_balance_sheet_balance_mon7 = res.get('bal7')
                                            self.total_balance_sheet_balance_mon8 = res.get('bal8')
                                            self.total_balance_sheet_balance_mon9 = res.get('bal9')
                                            self.total_balance_sheet_balance_mon10 = res.get('bal10')
                                            self.total_balance_sheet_balance_mon11 = res.get('bal11')
                                            self.total_balance_sheet_balance_mon12 = res.get('bal12')
                                            self.total_balance_sheet_balance_mon13 = res.get('bal13')
                                            
                                        if res.get('name').lower() == 'total equity':
                                            self.equity_mon1 = res.get('bal1')
                                            self.equity_mon1 = res.get('bal2')
                                            self.equity_mon1 = res.get('bal3')
                                            self.equity_mon1 = res.get('bal4')
                                            self.equity_mon1 = res.get('bal5')
                                            self.equity_mon1 = res.get('bal6')
                                            self.equity_mon1 = res.get('bal7')
                                            self.equity_mon1 = res.get('bal8')
                                            self.equity_mon1 = res.get('bal9')
                                            self.equity_mon1 = res.get('bal10')
                                            self.equity_mon1 = res.get('bal11')
                                            self.equity_mon1 = res.get('bal12')
                                            self.equity_mon1 = res.get('bal13')
                                self.total_liabilities_equity_mon1 = self.total_balance_sheet_balance_mon1 + self.equity_mon1
                                self.total_liabilities_equity_mon2 = self.total_balance_sheet_balance_mon2 + self.equity_mon2
                                self.total_liabilities_equity_mon3 = self.total_balance_sheet_balance_mon3 + self.equity_mon3
                                self.total_liabilities_equity_mon4 = self.total_balance_sheet_balance_mon4 + self.equity_mon4
                                self.total_liabilities_equity_mon5 = self.total_balance_sheet_balance_mon5 + self.equity_mon5
                                self.total_liabilities_equity_mon6 = self.total_balance_sheet_balance_mon6 + self.equity_mon6
                                self.total_liabilities_equity_mon7 = self.total_balance_sheet_balance_mon7 + self.equity_mon7
                                self.total_liabilities_equity_mon8 = self.total_balance_sheet_balance_mon8 + self.equity_mon8
                                self.total_liabilities_equity_mon9 = self.total_balance_sheet_balance_mon9 + self.equity_mon9
                                self.total_liabilities_equity_mon10 = self.total_balance_sheet_balance_mon10 + self.equity_mon10
                                self.total_liabilities_equity_mon11 = self.total_balance_sheet_balance_mon11 + self.equity_mon11
                                self.total_liabilities_equity_mon12 = self.total_balance_sheet_balance_mon12 + self.equity_mon12
                                self.total_liabilities_equity_mon13 = self.total_balance_sheet_balance_mon13 + self.equity_mon13
                                
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
                                if res.get('total') == True and res.get('type') == 'view':
                                    self.bal = self.bal + res.get('balance')
                                bal = []
                                for res_acc in result_acc:
                                    if res_acc.get('name')=='Total Net Ordinary Income':
                                        balance_res = res_acc.get('balance')
                                        bal.append(balance_res)
                                if len(bal) > 0 :
                                    self.gross_profit = bal[0]
#                                self.gross_profit = self.bal
                                
                                for acc in account_obj.browse(self.cr, self.uid, acc_ids):
                                    if acc.name == 'Cost Of Goods Sold' or acc.name == 'Cost of Sales' and acc.user_type.name == 'Income View' or acc.user_type.name == 'Income':
                                        if res.get('name').lower() == 'total cost of sales':
                                            result_acc.append({'id': False, 'name': ''})
                                    
                                    if acc.user_type.name == 'Expense' or acc.user_type.name == 'Expense View':
                                        self.total_exp = (self.exp_credit + self.exp_debit) + (self.other_exp_credit + self.other_exp_debit)
                                    self.net_profit = self.gross_profit - ((self.other_income_credit + self.other_income_debit) + self.total_exp)
                                
                                
                        if res.get('total')== True and res.get('type') == 'view' and res.get('level') == 1:
                            self.net_income_loss += res.get('balance')
                        
                    else:
                        res.update({
                            'balance': self.exchange(b), 
                        })
                        report_data = wiz_rep.browse(self.cr, self.uid, self.context.get('active_id'))
                        for ytd_acc_data in report_data.account_list:
                            if ytd_acc_data.type == 'view':
                                parent_id = ytd_acc_data.parent_id.id
                            else:
                                parent_id = ytd_acc_data.parent_id.id
                        parent_acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',False)])
                        child_acc_ids = account_obj.search(self.cr, self.uid, ['|',('parent_id','in',parent_acc_ids),('level','=',1)])
                        for acc_data in account_obj.browse(self.cr, self.uid, child_acc_ids):
                            if parent_id == acc_data.id:
                                acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',acc_data.id)])
                                if res.get('total') == True and res.get('type') == 'view' and res.get('parent_id') == acc_data.id:
                                    self.total_balance_sheet_balance = self.total_balance_sheet_balance + res.get('balance')
                                self.total_liabilities_equity = self.total_balance_sheet_balance
                        
                        if res.get('total') == True and res.get('type') == 'view' and res.get('level') == 1 and res.get('name') == 'Total Liabilities':
                            self.liab = res.get('balance')
                            
                        if res.get('total') == True and res.get('type') == 'view' and res.get('level') == 1 and res.get('name') == 'Total Equity':
                            self.equ = res.get('balance')
                            
                        self.total_liabilities_equity_new = self.liab + self.equ
                    if form['inf_type'] == 'TB' and form['columns'] == 'two':
                        res.update({
                            'balance': self.exchange(b), 
                        })
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
                if to_include and form['columns']=='four' and form['inf_type'] == 'GL' and res['type'] in ('other', 'liquidity', 'receivable', 'payable'):
                    res['mayor'] = self._get_analytic_ledger(res, ctx=ctx_end)
                elif to_include and form['periodic_columns']=='four' and form['inf_type'] == 'GL' and res['type'] in ('other', 'liquidity', 'receivable', 'payable'):
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
            total_profit_loss = self.net_income_loss
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
                'ytd' : total_profit_loss, 
            }
            if form['columns'] =='qtr':
                self.total_profit_loss.update({
                    'bal1' : self.net_profit1,
                    'bal2' : self.net_profit2,
                    'bal3' : self.net_profit3,
                    'bal4' : self.net_profit4,
                    'bal5' : self.net_profit5,
                })
                
            if form['columns'] =='thirteen':
                self.total_profit_loss.update({
                    'bal1' : self.net_profit_mon1,
                    'bal2' : self.net_profit_mon2,
                    'bal3' : self.net_profit_mon3,
                    'bal4' : self.net_profit_mon4,
                    'bal5' : self.net_profit_mon5,
                    'bal6' : self.net_profit_mon6,
                    'bal7' : self.net_profit_mon7,
                    'bal8' : self.net_profit_mon8,
                    'bal9' : self.net_profit_mon9,
                    'bal10' : self.net_profit_mon10,
                    'bal11' : self.net_profit_mon11,
                    'bal12' : self.net_profit_mon12,
                    'bal13' : self.net_profit_mon13,
                })
            result_acc.append(self.total_profit_loss)
            
            
            total_liab_equ = self.total_liabilities_equity_new + self.net_income_loss
            self.total_liab_equ = {
                'balance' : total_liab_equ, 
                'id' : False, 
                'type' : 'view', 
                'code' : '', 
                'name' : 'Total Liabilities & Equity', 
                'parent_id' : False, 
                'level' : 1, 
                'credit' : 0.0, 
                'debit' : 0.0, 
                'label' : False, 
                'mayor' : [], 
                'total' :True, 
                'change_sign' : 1, 
                'balanceinit' : 0.0, 
                'ytd' : total_liab_equ, 
            }
            result_acc.append(self.total_liab_equ)
            
        else:
            if not form['afr_id'][1] == 'Balance Sheet':
                if not form['inf_type'] == 'TB':
                    total_net_profit = self.net_income_loss
    #                        dbr3 = self.gross_profit_dbr3
                    self.net_profit_dict = {
                        'balance' : total_net_profit, 
                        'id': False, 
                        'type' : 'view', 
                        'code' : '', 
                        'name' : 'Net Income(Loss)', 
                        'parent_id' : False, 
                        'level' : 1, 
                        'credit' : 0.0, 
                        'debit' : 0.0, 
                        'label' : False, 
                        'mayor' : [], 
                        'total' :True, 
                        'change_sign' : 1, 
                        'balanceinit' : 0.0, 
                        'ytd' : total_net_profit, 
                    }
                    if form['columns'] =='qtr':
                        self.net_profit_dict.update({
                            'bal1' : self.net_profit1,
                            'bal2' : self.net_profit2,
                            'bal3' : self.net_profit3,
                            'bal4' : self.net_profit4,
                            'bal5' : self.net_profit5,
                        })
                    if form['columns'] =='thirteen':
                         self.net_profit_dict.update({
                            'bal1' : self.net_profit_mon1,
                            'bal2' : self.net_profit_mon2,
                            'bal3' : self.net_profit_mon3,
                            'bal4' : self.net_profit_mon4,
                            'bal5' : self.net_profit_mon5,
                            'bal6' : self.net_profit_mon6,
                            'bal7' : self.net_profit_mon7,
                            'bal8' : self.net_profit_mon8,
                            'bal9' : self.net_profit_mon9,
                            'bal10' : self.net_profit_mon10,
                            'bal11' : self.net_profit_mon11,
                            'bal12' : self.net_profit_mon12,
                            'bal13' : self.net_profit_mon13,
                        })
                    result_acc.append(self.net_profit_dict)
        return result_acc
    
    def get_profit(self, bal):
        return bal
    
    def get_comp_debit(self, comp_debit, level, type, name):
        if type in ['other', 'liquidity', 'receivable', 'payable']: 
            self.comp_debit_total += comp_debit
        return comp_debit
    
    def get_total_comp_debit(self):
        return self.comp_debit_total
    
    def get_comp_credit(self, comp_credit, level, type, name):
        if type in ['other', 'liquidity', 'receivable', 'payable']: 
            self.comp_credit_total += comp_credit
        return comp_credit
    
    def get_total_comp_credit(self):
        return self.comp_credit_total
    
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

                    # Check the condition for the Comparision 1
                    
                    if form['inf_type'] == 'IS':# and  form['periodic_columns'] == 'one':
                        res.update({
                            'compr0_balance': self.exchange(compr0_d-compr0_c), 
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
                                    self.bal = self.bal + res.get('compr0_balance')
                                bal = []
                                for res_acc in result_acc:
                                    if res_acc.get('name')=='Total Net Ordinary Income':
                                        balance_res = res_acc.get('compr0_balance')
                                        bal.append(balance_res)
                                if len(bal) > 0 :
                                    self.gross_profit = bal[0]
#                                self.gross_profit = self.bal
                                for acc in account_obj.browse(self.cr, self.uid, acc_ids):
                                    if acc.name == 'Cost Of Goods Sold' or acc.name == 'Cost of Sales' and acc.user_type.name == 'Income View' or acc.user_type.name == 'Income':
                                        if res.get('name').lower() == 'total cost of sales':
                                            result_acc.append({'id': False, 'name': ''})
                                    
                                    if acc.user_type.name == 'Expense' or acc.user_type.name == 'Expense View':
                                        self.total_exp = (self.exp_credit + self.exp_debit) + (self.other_exp_credit + self.other_exp_debit)
                                    self.comp0_net_profit = self.gross_profit - ((self.other_income_credit + self.other_income_debit) + self.total_exp)
                        if res.get('total')== True and res.get('type') == 'view' and res.get('level') == 1:
                            self.profit_loss_comp0 = res.get('compr0_balance')
                    else:
                        res.update({
                            'compr0_balance': self.exchange(compr0_b), 
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
                                if res.get('total') == True and res.get('type') == 'view' and res.get('parent_id') == acc_data.id:
                                    self.total_balance_sheet_balance = self.total_balance_sheet_balance + res.get('compr0_balance')
                                self.total_liabilities_equity = self.total_balance_sheet_balance
                        
                        if res.get('total')== True and res.get('type') == 'view' and res.get('level') == 1 and res.get('name') == 'Total Liabilities':
                            self.total_liab_comp0 = res.get('compr0_balance')
                    	if res.get('total')== True and res.get('type') == 'view' and res.get('level') == 1 and res.get('name') == 'Total Equity':
                            self.total_equ_comp0 = res.get('compr0_balance')
                    
                      	self.total_liab_equ_comp0 = self.total_liab_comp0 + self.total_equ_comp0
                
                # Check the condition for the Comparision 2
                
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
                                    self.bal = self.bal + res.get('compr1_balance')
                                bal = []
                                for res_acc in result_acc:
                                    if res_acc.get('name')=='Total Net Ordinary Income':
                                        balance_res = res_acc.get('compr1_balance')
                                        bal.append(balance_res)
                                if len(bal) > 0 :
                                    self.gross_profit = bal[0]
#                                self.gross_profit = self.bal
                                for acc in account_obj.browse(self.cr, self.uid, acc_ids):
                                    if acc.name == 'Cost Of Goods Sold' or acc.name == 'Cost of Sales' and acc.user_type.name == 'Income View' or acc.user_type.name == 'Income':
                                        if res.get('name').lower() == 'total cost of sales':
                                            result_acc.append({'id': False, 'name': ''})
                                    
                                    if acc.user_type.name == 'Expense' or acc.user_type.name == 'Expense View':
                                        self.total_exp = (self.exp_credit + self.exp_debit) + (self.other_exp_credit + self.other_exp_debit)
                                    self.comp1_net_profit = self.gross_profit - ((self.other_income_credit + self.other_income_debit) + self.total_exp)
                        if res.get('total')== True and res.get('type') == 'view' and res.get('level') == 1:
                            self.profit_loss_comp1 = res.get('compr1_balance')           
                    else:
                        res.update({
                            'compr1_balance': self.exchange(compr1_b), 
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
                                if res.get('total') == True and res.get('type') == 'view' and res.get('parent_id') == acc_data.id:
                                    self.total_balance_sheet_balance = self.total_balance_sheet_balance + res.get('compr1_balance')
                                self.total_liabilities_equity = self.total_balance_sheet_balance
                        
                        if res.get('total')== True and res.get('type') == 'view' and res.get('level') == 1 and res.get('name') == 'Total Liabilities':
                            self.total_liab_comp1 = res.get('compr1_balance')
                    	if res.get('total')== True and res.get('type') == 'view' and res.get('level') == 1 and res.get('name') == 'Total Equity':
                            self.total_equ_comp1 = res.get('compr1_balance')
                    
                      	self.total_liab_equ_comp1 = self.total_liab_comp1 + self.total_equ_comp1
                        
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
                
                # Check condition for Single Columns
            
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
                            for acc in account_obj.browse(self.cr, self.uid, acc_ids):
                                if acc.name == 'Cost Of Goods Sold' or acc.name == 'Cost of Sales' and acc.user_type.name == 'Income View' or acc.user_type.name == 'Income':
                                    if res.get('name').lower() == 'total cost of sales':
                                        result_acc.append({'id': False, 'name': ''})
                                if acc.user_type.name == 'Expense' or acc.user_type.name == 'Expense View':
                                    self.total_exp = (self.exp_credit + self.exp_debit) + (self.taxes_credit + self.taxes_debit) + (self.other_exp_credit + self.other_exp_debit)
                                self.net_profit = self.gross_profit - ((self.other_income_credit + self.other_income_debit) + self.total_exp)
                    if res.get('total')== True and res.get('type') == 'view' and res.get('level') == 1:
                            self.net_profit_loss_periodic += res.get('balance')
                else:
                    res.update({
                        'balance': self.exchange(b), 
                    })
                    report_data = wiz_rep.browse(self.cr, self.uid, self.context.get('active_id'))
                    for ytd_acc_data in report_data.account_list:
                        if ytd_acc_data.type == 'view':
                            parent_id = ytd_acc_data.parent_id.id
                        else:
                            parent_id = ytd_acc_data.parent_id.id
                    parent_acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',False)])
                    child_acc_ids = account_obj.search(self.cr, self.uid, ['|',('parent_id','in',parent_acc_ids),('level','=',1)])
                    for acc_data in account_obj.browse(self.cr, self.uid, child_acc_ids):
                        if parent_id == acc_data.id:
                            acc_ids = account_obj.search(self.cr, self.uid, [('parent_id','=',acc_data.id)])
                            if res.get('total') == True and res.get('type') == 'view' and res.get('parent_id') == acc_data.id:
                                self.total_balance_sheet_balance = self.total_balance_sheet_balance + res.get('balance')
                            self.total_liabilities_equity = self.total_balance_sheet_balance
                            
                    if res.get('total')== True and res.get('type') == 'view' and res.get('level') == 1 and res.get('name') == 'Total Liabilities':
                            self.total_liab_periodic = res.get('balance')
                    if res.get('total')== True and res.get('type') == 'view' and res.get('level') == 1 and res.get('name') == 'Total Equity':
                            self.total_equ_periodic = res.get('balance')
                    
                    self.total_liab_equ_periodic = self.total_liab_periodic + self.total_equ_periodic

                if form['inf_type'] == 'TB' and form['periodic_columns'] == 'two':
                        res.update({
                            'balance': self.exchange(b), 
                        })

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
                if to_include and form['periodic_columns']=='four' and form['inf_type'] == 'GL' and res['type'] in ('other', 'liquidity', 'receivable', 'payable'):
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
            self.comparison1_lines(form_copy, 0)
            total_profit_loss = self.net_profit_loss_periodic
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
                'ytd' : total_profit_loss, 
            }
#            
            if form['compr0_fiscalyear_id']:
                total_comp0_profit_loss = self.profit_loss_comp0
                self.total_profit_loss.update({
                    'compr0_balance' : total_comp0_profit_loss,
                    'compr0_balanceinit' : 0.00,
                    'compr0_debit' : 0.00,
                    'compr0_credit' : 0.00,
                    'compr0_ytd' : self.profit_loss_comp0,
                })
#            
            if form['compr1_fiscalyear_id']:
                total_comp1_profit_loss = self.profit_loss_comp1
                self.total_profit_loss.update({
                    'compr1_balance' : total_comp1_profit_loss,
                    'compr1_balanceinit' : 0.00,
                    'compr1_debit' : 0.00,
                    'compr1_credit' : 0.00,
                    'compr1_ytd' : self.profit_loss_comp1,
                })
            result_acc.append(self.total_profit_loss)
            
            total_liab_equ_periodic = self.total_liab_equ_periodic + self.net_profit_loss_periodic
            self.total_lbeq = {
                'balance' : total_liab_equ_periodic, 
                'id' : False, 
                'type' : 'view', 
                'code' : '', 
                'name' : 'Total Liabilities & Equity', 
                'parent_id' : False, 
                'level' : 1, 
                'credit' : 0.0, 
                'debit' : 0.0, 
                'label' : False, 
                'mayor' : [], 
                'total' :True, 
                'change_sign' : 1, 
                'balanceinit' : 0.0, 
                'ytd' : total_liab_equ_periodic, 
            }
            
            total_comp0_liabilities_equity = self.total_liab_equ_comp0 + self.profit_loss_comp0
            total_comp1_liabilities_equity = self.total_liab_equ_comp1 + self.profit_loss_comp1
            
            if form['compr0_fiscalyear_id']:
                self.total_lbeq.update({
                    'compr0_balance' : total_comp0_liabilities_equity,
                    'compr0_balanceinit' : 0.00,
                    'compr0_debit' : 0.00,
                    'compr0_credit' : 0.00,
                    'compr0_ytd' : total_comp0_liabilities_equity
                })
                
            if form['compr1_fiscalyear_id']:
                self.total_lbeq.update({
                    'compr1_balance' : total_comp1_liabilities_equity,
                    'compr1_balanceinit' : 0.00,
                    'compr1_debit' : 0.00,
                    'compr1_credit' : 0.00,
                    'compr1_ytd' : total_comp1_liabilities_equity
                })
            
            result_acc.append(self.total_lbeq)
        else:
            if not form['afr_id'][1] == 'General Ledger':
                if not form['afr_id'][1] == 'Trial Balance':
                    if not form['afr_id'][1] == 'Balance Sheet':
                        if not form['inf_type'] == 'TB':
                            total_gross_profit = self.net_profit_loss_periodic
                            self.net_profit_dict = {
                                'balance' : total_gross_profit, 
                                'id'        : False, 
                                'type' : 'view', 
                                'code' : '', 
                                'name' : 'Net Profit(Loss)', 
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
                            
                            
                            if form['compr0_fiscalyear_id']:
                                self.net_profit_dict.update({
                                    'compr0_balance' : self.profit_loss_comp0,
                                    'compr0_balanceinit' : 0.00,
                                    'compr0_debit' : 0.00,
                                    'compr0_credit' : 0.00,
                                    'compr0_ytd' : self.profit_loss_comp0,
                                })
                            if form['compr1_fiscalyear_id']:
                                self.net_profit_dict.update({
                                    'compr1_balance' : self.profit_loss_comp1,
                                    'compr1_balanceinit' : 0.00,
                                    'compr1_debit' : 0.00,
                                    'compr1_credit' : 0.00,
                                    'compr1_ytd' : self.profit_loss_comp1,
                                })
                            
                            result_acc.append(self.net_profit_dict)
        return result_acc

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: