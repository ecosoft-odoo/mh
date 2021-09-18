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
import time
from openerp.osv import fields, osv

class stock_invoice_onshipping(osv.osv_memory):

    _inherit = "stock.invoice.onshipping"

    def _is_date_over(self, cr, uid, context):
        if not context.get('invoice_date', False):
            context.update({'invoice_date': time.strftime('%Y-%m-%d')}) 
        cr.execute("select max(date_invoice) from account_invoice where state in ('open','paid')")
        max_invoice_date = cr.fetchone()[0]
        if context.get('invoice_date') < max_invoice_date:
            return True
        return False
    
    _columns = {
        'is_date_over': fields.boolean('Date Over?', readonly=True)
    }

    _defaults = {
        'invoice_date': lambda *a: time.strftime('%Y-%m-%d'),
        'is_date_over': _is_date_over
    }
    
    def onchange_invoice_date(self, cr, uid, ids, invoice_date=False, context=None):
        res = {}
        context.update({'invoice_date': invoice_date})
        res['value'] = {'is_date_over': self._is_date_over(cr, uid, context)}
        return res
    
stock_invoice_onshipping()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
