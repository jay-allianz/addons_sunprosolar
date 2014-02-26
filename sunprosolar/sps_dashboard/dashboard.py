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
    ('Installation', 'Installation'),
    ('Final Inspection', 'Final Inspection'),
    ('Monitoring', 'Monitoring'),
    ('Invoicing', 'Invoicing'),
    ('Wrap Up', 'Wrap Up'),
    ('sent', 'Quotation Sent'),
    ('contract_generated', 'Contract Generated'),
    ('contract_signed', 'Contract Signed'),
    ('manual', 'Sale to Invoice'),
    ('financing_type','Financing Type'),
    ('site_inspection', 'Site Inspection'),
    ('progress', 'Sales Order'),
    ('assign_financing_incharge', 'Assign Financing Incharge'),
]

class sps_dashboard(osv.Model):
    _name = "sps.dashboard"
    _description = "Sunpro Solar Statistics"
    _auto = False
    _columns = {
        'name' : fields.char('Name', size='128'),
        'partner_id' : fields.many2one('res.partner', 'Customer'),       
        'state': fields.selection(AVAILABLE_STATES, 'Order Status', readonly=True),
        'nbr': fields.integer('Number of Records', readonly=True),
        }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'sps_dashboard')
        cr.execute("""
            create or replace view sps_dashboard as (
            Select 1 as nbr, p.id+l.id+cs.id as id, l.name as name, p.id as partner_id, cs.name as state from crm_lead l 
inner join crm_case_stage cs on l.stage_id = cs.id 
inner join res_partner p on l.partner_id = p.id 
where l.state not in ('cancel','done')

union

Select 1 as nbr, p.id+s.id as id, s.name as name, p.id as partner_id, s.state as state from sale_order s 
inner join res_partner p on s.partner_id = p.id where state not in ('confirmed','done')

union

Select 1 as nbr, p.id+aa.id+tt.id as id, aa.name as name, p.id as partner_id, tt.name as state from account_analytic_account aa 
inner join res_partner p on aa.partner_id = p.id 
inner join project_project pr ON aa.id = pr.analytic_account_id
inner join project_task_type tt on pr.project_task_stage = tt.id

union

Select 1 as nbr, p.id+i.id as id, i.name as name, p.id as partner_id, i.state as state from account_invoice i 
inner join res_partner p on i.partner_id = p.id where state not in ('proforma','proforma2','paid','cancel')
)""")
        
sps_dashboard()