from openerp.osv import fields, orm
from openerp.service.web_services import db
import openerp.sql_db as sql_db
import openerp.tools as tools
import os
import openerp
import base64
import datetime

class db_sync(orm.TransientModel):
    
    _name = 'db.sync'
    
    _columns = {
        'host' : fields.many2one('db.config' ,'Host'),
    }
    
    def _create_empty_database(self, name):
        db = sql_db.db_connect('postgres')
        cr = db.cursor()
        chosen_template = tools.config['db_template']
        cr.execute("""SELECT datname 
                              FROM pg_database
                              WHERE datname = %s """,
                           (name,))
        if cr.fetchall():
            raise openerp.exceptions.Warning(" %s database already exists!" % name )
        try:
            cr.autocommit(True) # avoid transaction block
            cr.execute("""CREATE DATABASE "%s" ENCODING 'unicode' TEMPLATE "%s" """ % (name, chosen_template))
        finally:
            cr.close()
    
    
    def import_database(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids, context=context):
            curr_datetime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M-%S')
            new_db_name = rec.host.db_name + '_' + curr_datetime
            self._create_empty_database(new_db_name)
            file_name = '/tmp/'+new_db_name +'.sql'
            command = 'export PGPASSWORD=' +rec.host.password +'\npg_dump ' +rec.host.db_name +' -U ' +rec.host.user +' --file=' +file_name +' -h '+ rec.host.name
            os.system(command)
            db_port = tools.config['db_port'] or 5432
            db_user = tools.config['db_user']
            db_host = tools.config['db_host'] or 'localhost'
            st = 'psql -p ' +str(db_port) +' -U '+db_user +' -h ' + db_host +' -f '+file_name +' ' +new_db_name
            os.system(st)
            os.remove(file_name)
        return True
    