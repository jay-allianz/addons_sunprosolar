from openerp.osv import osv, fields

class account_partner_ledger(osv.osv_memory):
    
    _inherit = 'account.partner.ledger'
    
    def check_report_aeroo(self, cr, uid, ids, context=None):
        data = super(account_partner_ledger, self).check_report(cr, uid, ids, context=context)['datas']
        return { 'type': 'ir.actions.report.xml', 'report_name': 'partner_ledger_aeroo_report', 'datas': data}


