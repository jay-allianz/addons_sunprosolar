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
import addons
import tools

AVAILABLE_STATES = [
    ('draft', 'Quotation'),
    ('New Lead', 'New Lead'),
    ('Sales Assignment', 'Sales Assignment'),
    ('Disqualified', 'Disqualified'),
    ('Initial Contact', 'Initial Contact'),
    ('Appointment Setup', 'Appointment Setup'),
    ('sent', 'Quotation Sent'),
    ('contract_generated', 'Contract Generated'),
    ('contract_signed', 'Contract Signed'),
    ('project_management_notified','Project Management Notified'),
    ('manual', 'Sale to Invoice'),
    ('financing_type','Financing Type'),
    ('site_inspection', 'Site Inspection'),
    ('progress', 'Sales Order'),
    ('assign_financing_incharge', 'Assign Financing Incharge'),
    ('follow_up','Follow Up'),
    ('permit','Permit'),
    ('city','City Submission'),
    ('drawing','Eng. Create/Modify Following Drawings'),
    ('permit_pack','Permit Pack'),
    ('cancel', 'Cancelled'),
    ('Installation', 'Installation'),
    ('Final Inspection', 'Final Inspection'),
    ('Monitoring', 'Monitoring'),
    ('Invoicing', 'Invoicing'),
    ('Wrap Up', 'Wrap Up'),
]

class sps_state(osv.Model):
    _name = 'sps.state'
    _columns = {
        'name' : fields.char('State', size=64),
        'code' : fields.char('Code', size=64),
        'sequence' : fields.integer('Sequence'),
        }
    _order = 'sequence'
    
class sps_dashboard(osv.Model):
    _name = "sps.dashboard"
    _description = "Sunpro Solar Statistics"
    _auto = False
    
    def _read_group_stage_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        stage_obj = self.pool.get('sps.state')
        stage_ids = stage_obj.search(cr, uid, [], context=context)
        stages = stage_obj.read(cr, uid, stage_ids, context=context)
        result = stage_obj.name_get(cr, uid, stage_ids, context=context)
        fold = {}
        return result, fold

    
    def _get_state(self, cr, uid, ids, name, args, context=None):
        res = {}
        stage_obj = self.pool.get('sps.state')
        for data in self.browse(cr, uid, ids):
            stage_id = stage_obj.search(cr, uid, [('code','=',data.state)])
            res[data.id] = stage_id and stage_id[0]
        return res
    
    _columns = {
        'name' : fields.char('Name', size='128'),
        'partner_id' : fields.many2one('res.partner', 'Customer'),       
        'state': fields.selection(AVAILABLE_STATES, 'Order Status', readonly=True),
        'state_id': fields.function(_get_state, type='many2one', relation='sps.state', string='State', store=True),
        'nbr': fields.integer('Number of Records', readonly=True),
        }
    

    _group_by_full={
        'state_id': _read_group_stage_ids,
                    
        }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'sps_dashboard')
        cr.execute("""
            create or replace view sps_dashboard as (
            Select 1 as nbr, 1 as state_id, p.id+l.id+cs.id as id, l.name as name, p.id as partner_id, cs.name as state from crm_lead l 
inner join crm_case_stage cs on l.stage_id = cs.id 
inner join res_partner p on l.partner_id = p.id 
where l.state not in ('cancel','done')

union

Select 1 as nbr, 1 as state_id, p.id+s.id as id, s.name as name, p.id as partner_id, s.state as state from sale_order s 
inner join res_partner p on s.partner_id = p.id where state not in ('confirmed','done')

union

Select 1 as nbr, 1 as state_id, p.id+aa.id+tt.id as id, aa.name as name, p.id as partner_id, tt.name as state from account_analytic_account aa 
inner join res_partner p on aa.partner_id = p.id 
inner join project_project pr ON aa.id = pr.analytic_account_id
inner join project_task_type tt on pr.project_task_stage = tt.id

union

Select 1 as nbr, 1 as state_id, p.id+i.id as id, i.name as name, p.id as partner_id, i.state as state from account_invoice i 
inner join res_partner p on i.partner_id = p.id where state not in ('proforma','proforma2','paid','cancel')
)""")
        
sps_dashboard()