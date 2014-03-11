from openerp.osv import fields, orm

class db_config(orm.Model):
    
    _name = 'db.config'
    
    _columns = {
        'name' : fields.char('DB Host', size=36),
        'port' : fields.integer('DB Port'),
        'db_name' : fields.char('DB Name', size=36),
        'user' : fields.char('DB User', size=36),
        'password' : fields.char('DB Password', size=36),
    }
    
    _defaults = {
        'port' : 5432,
        'user' : 'admin',
    } 