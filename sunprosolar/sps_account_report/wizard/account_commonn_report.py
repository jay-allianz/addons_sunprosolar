from osv import osv, fields

class account_partner_ledger(osv.osv_memory):
    
    _inherit = 'account.partner.ledger'
    
    _columns = {
        'partner_ids': fields.many2many('res.partner', 'account_partner_ledger_rel_sunpro', 'partner_id', 'id1', 'Accounts'),
    }
    
    def _print_report(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        data = self.pre_print_report(cr, uid, ids, data, context=context)
        data['form'].update(self.read(cr, uid, ids, ['initial_balance', 'filter', 'page_split', 'amount_currency'])[0])
        partner_ids = self.browse(cr, uid, ids[0], context=context).partner_ids
        partners = [part.id for part in partner_ids]
        data['form'].update({'partner_ids' : partners})
        if data['form']['page_split']:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'account.third_party_ledger1',
                'datas': data,
        }
        return {
                'type': 'ir.actions.report.xml',
                'report_name': 'account.third_party_ledger_other1',
                'datas': data,
        }
    
account_partner_ledger()