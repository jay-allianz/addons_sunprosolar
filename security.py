# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

import openerp.exceptions
from openerp import SUPERUSER_ID
import openerp.pooler as pooler
import openerp.tools as tools
from ast import literal_eval

#.apidoc title: Authentication helpers

def signup(db, values):
    pool = pooler.get_pool(db)
    user_obj = pool.get('res.users')
    cr = pooler.get_db(db).cursor()
    user_id = False
    values.update({"active":True})
    if values and values.get("signup_token"):
        cr.execute("select signup_token, id from res_partner where signup_token = %s", (values.get("signup_token"),))
        data = cr.fetchone()
        partner_id = data[1]
        if partner_id:
            ir_config_parameter = pool.get('ir.config_parameter')
            template_user_id = literal_eval(ir_config_parameter.get_param(cr, 1, 'auth_signup.template_user_id', 'False'))
            values.update({'partner_id':partner_id})
            user_id = user_obj.copy(cr, 1, template_user_id, values, context={})
            cr.commit()
    else:
            ir_config_parameter = pool.get('ir.config_parameter')
            template_user_id = literal_eval(ir_config_parameter.get_param(cr, 1, 'auth_signup.template_user_id', 'False'))
            user_id = user_obj.copy(cr, 1, template_user_id, values, context={})
            cr.commit()
    cr.close()
    return user_id
    

def login(db, login, password):
    pool = pooler.get_pool(db)
    user_obj = pool.get('res.users')
    return user_obj.login(db, login, password)

def check_super(passwd):
    if passwd == tools.config['admin_passwd']:
        return True
    else:
        raise openerp.exceptions.AccessDenied()

def check(db, uid, passwd):
    pool = pooler.get_pool(db)
    user_obj = pool.get('res.users')
    return user_obj.check(db, uid, passwd)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
