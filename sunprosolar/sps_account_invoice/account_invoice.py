from openerp.osv import osv, fields
from openerp.tools.translate import _
class account_invoice(osv.osv):
    
    _inherit = 'account.invoice'
    
    _columns = {
        'state': fields.selection([
            ('draft','Financing Type'),
            ('assign_financing_incharge','Assign Financing In-Charge'),
            ('proforma','Pro-forma'),
            ('proforma2','Pro-forma'),
            ('open','Open'),
            ('paid','Paid'),
            ('cancel','Cancelled'),
            ],'Status', select=True, readonly=True, track_visibility='onchange',
            help=' * The \'Draft\' status is used when a user is encoding a new and unconfirmed Invoice. \
            \n* The \'Financing Type\' status is used when a user is choosing the financing type. \
            \n* The \'Assign Financing In-Charge\' status is used when a user is assigning the in-charge for finance. \
            \n* The \'Pro-forma\' when invoice is in Pro-forma status,invoice does not have an invoice number. \
            \n* The \'Open\' status is used when user create invoice,a invoice number is generated.Its in open status till user does not pay invoice. \
            \n* The \'Paid\' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled. \
            \n* The \'Cancelled\' status is used when user cancel invoice.'),
        'financing_type_id' : fields.many2one('financing.type','Financing Type'),
        'doc_req_ids' : fields.one2many('document.require','invoice_id','Required Document'),
        'incharge_user_id' : fields.many2one('res.users','Financing In-Charge'),
    }
    
    def document_collected(self, cr, uid, ids, context=None):
        cur_rec = self.browse(cr, uid, ids, context=context)[0]
        res = True
        doc_names = ""
        if not cur_rec or not cur_rec.financing_type_id:
            raise osv.except_osv(_('Required Document !'),_("Please select the \'Financing Type\' for Document collection."))
        for document in cur_rec.doc_req_ids:
            if not document.document:
                res = False
                doc_names += document.document_id.name + "\n"
        if not res:
            raise osv.except_osv(_('Required Document !'),_("Following Required Document not collected : \n%s")%(doc_names) )
        self.write(cr, uid, ids, {'state': 'assign_financing_incharge'}, context=context)
        return True
    
    def onchange_financing_type(self, cr, uid, ids, financing_type_id, context=None):
        doc_req_obj = self.pool.get('document.require')
        if not ids:
            return {'value': {}}
        old_rec_len = len(self.browse(cr, uid,ids[0],context=context).doc_req_ids)
        if old_rec_len:
            doc_req_ids = doc_req_obj.search(cr, uid, [('invoice_id','=',ids[0])],context=context)
            doc_req_obj.unlink(cr, uid, doc_req_ids)
        fin_type_obj = self.pool.get('financing.type')
        fin_type_rec  = fin_type_obj.browse(cr, uid, financing_type_id, context=context)
        doc_ids = []
        for document in fin_type_rec.document_ids:
            vals = {
                'name' : document.name,
                'document_id' : document.id,
                'invoice_id' : ids[0],
            }
            doc_ids.append(doc_req_obj.create(cr, uid, vals, context=context))
        values = {'doc_req_ids' : doc_ids or False}
        return {'value' : values}
    
account_invoice()

class document_require(osv.osv):
    _name = "document.require"
    
    _columns = {
        'name' : fields.char('Name'),
        'document_id' : fields.many2one('document.document','Document Name'),
        'document' : fields.binary("Document"),
        'invoice_id' : fields.many2one('account.invoice','Invoice'),
    }

document_require()

class financing_type(osv.osv):
    
    _name = "financing.type"
    
    _columns = {
        'name' : fields.char('Name'),
        'document_ids' : fields.many2many('document.document','document_financing_type_rel','fin_type_id','doc_id','Documents'),
    }
    
financing_type()
    
class document_document(osv.osv):
    
    _name = "document.document"
    
    _columns = {
        'name' : fields.char('Name'),
        'document' : fields.binary("Document"),
        'collected' : fields.boolean("Collected"),
    }
    
document_document()