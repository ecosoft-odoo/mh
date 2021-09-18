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
from openerp.tools.translate import _
from openerp import netsvc


class account_invoice_refund(osv.osv_memory):

    _inherit = "account.invoice.refund"

    def onchange_filter_refund(self, cr, uid, ids, filter_refund, context=None):
        if context is None:
            context = {}
        active_id = context.get('active_id', False)
        if active_id:
            invoice_ids = self.pool.get('account.invoice').search(cr, uid, [('type', '=', 'out_refund'),
                                                                            ('invoice_id_ref', '=', active_id),
                                                                            ('state', 'in', ('open', 'paid'))], context=context)
            invoices = self.pool.get('account.invoice').read(cr, uid, invoice_ids, ['amount_untaxed'], context=context)
            refunded_amount = 0.0
            for i in invoices:
                refunded_amount += i['amount_untaxed'] or 0.0
            if refunded_amount:
                warning = {
                    'title': _('Warning!'),
                    'message': _('Refunded Amount = %.2f') % (refunded_amount,)
                }
                return {'warning': warning}
        return True

account_invoice_refund()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
