# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
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

from osv import osv, fields
import base64
import tempfile
import xlrd
from tools.translate import _
import datetime
from tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from xlrd import open_workbook,xldate_as_tuple
from dateutil.relativedelta import relativedelta
import tools


class import_utility_company(osv.osv_memory):
    _name = 'import.utility.company'

    def import_company(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        partner_obj = self.pool.get('res.partner')
        product_pricelist_obj = self.pool.get('product.pricelist')
        product_pricelist_version_obj = self.pool.get('product.pricelist.version')
        product_pricelist_item_obj = self.pool.get('product.pricelist.item')
        temp_path = tempfile.gettempdir()
        wiz_rec = self.browse(cr, uid, ids[0], context=context)
        csv_data = base64.decodestring(wiz_rec.file)
        fp = open(temp_path + '/utility_company.xls', 'wb+')
        fp.write(csv_data)
        fp.close()
        wb = xlrd.open_workbook(temp_path + '/utility_company.xls')
        current_year = datetime.date.today().year
        year_start_date = '01/01/%s' % current_year
        year_end_date = '%s-12-31' % current_year
        year_end_date = datetime.datetime.strptime(year_end_date , DEFAULT_SERVER_DATE_FORMAT).strftime(DEFAULT_SERVER_DATE_FORMAT)
        for sheet in wb.sheets():
            for rownum in range(sheet.nrows):
                if rownum == 0:
                    headers = sheet.row_values(rownum)
                    no_index = headers.index('No.')
                    company_name_index = headers.index('Company Name')
                    state_index = headers.index('State')
                    features_index = headers.index('Features')
                    season_name_index = headers.index('Season Name')
                    season_date_from_index = headers.index('Season Date from')
                    season_date_to_index = headers.index('Season Date to')
                    daily_minimum_charges_index = headers.index('daily miniumum charges')
                    monthly_minimum_charges_index = headers.index('monthly minimum charges')
                    daily_meter_charges_index = headers.index('Daily meter charges')
                    monthly_meter_charges_index = headers.index('monthly meter charges')
                    tier1_index = headers.index('tier 1')
                    off_peaktier2_index = headers.index('Off-Peak/tier 2')
                    part_peak_tier3_index = headers.index('Part-Peak/tier 3')
                    peak_tier4_index = headers.index('Peak/tier 4')
                    state_chages_index = headers.index('state chages')
                    rate_stablization_index = headers.index('Rate Stablization')
                    surcharge3_index = headers.index('Surcharge 3')
                    surcharge4_index = headers.index('Surcharge 4')
                    surcharge5_index = headers.index('Surcharge 5')
                    surcharge6_index = headers.index('Surcharge 6')
                    pinno_index = headers.index('daily miniumum charges')
                    summer_winter_qty_index = headers.index('Baseline Qty per Day Summer/Winter')
                else:
                    date_from = date_to = False
                    if sheet.row_values(rownum)[season_date_from_index]:
                        date_from = xldate_as_tuple(sheet.row_values(rownum)[season_date_from_index],wb.datemode)
                        date_from = datetime.datetime.strftime(datetime.datetime(*date_from), DEFAULT_SERVER_DATE_FORMAT)
                    if sheet.row_values(rownum)[season_date_to_index]:
                        date_to = xldate_as_tuple(sheet.row_values(rownum)[season_date_to_index],wb.datemode)
                        date_to = datetime.datetime.strftime(datetime.datetime(*date_to), DEFAULT_SERVER_DATE_FORMAT)
                    data = sheet.row_values(rownum)[summer_winter_qty_index].split('/')
                    summer_data = winter_data = 0.00
                    if data and data[0] and data[1]:
                        summer_data = data[0]
                        winter_data = data[1]
                    pricelist_id = product_pricelist_obj.create(cr, uid, {
                                                        'name': str(sheet.row_values(rownum)[company_name_index]) + ' ' + str(sheet.row_values(rownum)[season_name_index]),
                                                        'type': 'sale'
                                                })
                    price_version_ids = []
                    price_version_ids.append(product_pricelist_version_obj.create(cr, uid, {
                                                                'name': str(sheet.row_values(rownum)[company_name_index]) + ' ' + str(sheet.row_values(rownum)[season_name_index]),
                                                                'date_start': year_start_date or False,
                                                                'date_end': date_from or False,
                                                                'pricelist_id': pricelist_id
                                                        }))
                    date_from = (datetime.datetime.strptime(date_from , DEFAULT_SERVER_DATE_FORMAT) + relativedelta(days=1)).strftime(DEFAULT_SERVER_DATE_FORMAT)
                    price_version_ids.append(product_pricelist_version_obj.create(cr, uid, {
                                                                'name': str(sheet.row_values(rownum)[company_name_index]) + ' ' + str(sheet.row_values(rownum)[season_name_index]),
                                                                'date_start': date_from or False,
                                                                'date_end': date_to or False,
                                                                'pricelist_id': pricelist_id
                                                        }))
                    date_to = (datetime.datetime.strptime(date_to , DEFAULT_SERVER_DATE_FORMAT) + relativedelta(days=1)).strftime(DEFAULT_SERVER_DATE_FORMAT)
                    price_version_ids.append(product_pricelist_version_obj.create(cr, uid, {
                                                                'name': str(sheet.row_values(rownum)[company_name_index]) + ' ' + str(sheet.row_values(rownum)[season_name_index]),
                                                                'date_start': date_to or False,
                                                                'date_end': year_end_date or False,
                                                                'pricelist_id': pricelist_id
                                                        }))
                    for price_version in price_version_ids:
                        price_list_id = product_pricelist_item_obj.create(cr, uid, {
                                                                'daily_minimum_charges': sheet.row_values(rownum)[daily_minimum_charges_index] or 0.00,
                                                                'monthly_minimum_charges': sheet.row_values(rownum)[monthly_minimum_charges_index] or 0.00,
                                                                'daily_meter_charges': sheet.row_values(rownum)[daily_meter_charges_index] or 0.00,
                                                                'monthly_meter_charges': sheet.row_values(rownum)[monthly_minimum_charges_index] or 0.00,
                                                                'tier1': sheet.row_values(rownum)[tier1_index] or 0.00,
                                                                'off_peak_tier2': sheet.row_values(rownum)[off_peaktier2_index] or 0.00,
                                                                'part_peak_tier3': sheet.row_values(rownum)[part_peak_tier3_index] or 0.00,
                                                                'peak_tier4': sheet.row_values(rownum)[peak_tier4_index] or 0.00,
                                                                'stage_changes': sheet.row_values(rownum)[state_chages_index] or 0.00,
                                                                'rate_stablization': sheet.row_values(rownum)[rate_stablization_index] or 0.00,
                                                                'surcharge_3': sheet.row_values(rownum)[surcharge3_index] or 0.00,
                                                                'surcharge_4': sheet.row_values(rownum)[surcharge4_index] or 0.00,
                                                                'surcharge_5': sheet.row_values(rownum)[surcharge5_index] or 0.00,
                                                                'surcharge_6': sheet.row_values(rownum)[surcharge6_index] or 0.00,
                                                                'summer_qty': summer_data or 0.00,
                                                                'winter_qty': winter_data or 0.00,
                                                                'name': sheet.row_values(rownum)[season_name_index] or '',
                                                                'price_version_id': price_version
                                                        })
                    partner_obj.create(cr, uid, {
                                            'name': str(sheet.row_values(rownum)[company_name_index]) + ' ' + str(sheet.row_values(rownum)[features_index]),
                                            'is_utility_company': True,
                                            'is_company': True,
                                            'property_product_pricelist': pricelist_id,
                                            'customer': False
                                    })
        return {}

    _columns = {
            'file': fields.binary("Input File", required=True, filters='*.xlsx'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: