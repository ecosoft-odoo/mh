# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields, osv
import time


class mh_daily_customer_payment_wizard(osv.osv_memory):

    _name = 'mh.daily.customer.payment.wizard'

    _columns = {
        'date': fields.date('Date', required=True),
        'user_id': fields.many2one('res.users', 'By', required=False),
    }

    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def start_report(self, cr, uid, ids, data, context=None):
        for wiz_obj in self.read(cr, uid, ids):
            if 'form' not in data:
                data['form'] = {}
            data['form']['date'] = wiz_obj['date']
            user_id = wiz_obj['user_id'] and wiz_obj['user_id'][0] or 0
            data['form']['user_id'] = user_id
            data['form']['prepared_by'] = user_id and self.pool.get('res.users').browse(cr, uid, user_id).name or ""
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'mh_daily_customer_payment',
                    'datas': data}

mh_daily_customer_payment_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: