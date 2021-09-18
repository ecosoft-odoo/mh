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
import math
from openerp.tools.translate import _

# class account_cash_statement(osv.osv):
#
#     _inherit = 'account.bank.statement'
#
#     def _auto_fill_cash_box(self, cr, uid, ids, context=None):
#         cash_line_obj = self.pool.get('account.cashbox.line')
#         for st in self.browse(cr, uid, ids, context=context):
#             cr.execute('select id, pieces from account_cashbox_line where bank_statement_id = %s order by pieces desc', (st.id,))
#             cash_lines = cr.fetchall()
#             bal = st.balance_end
#             for line in cash_lines:
#                 pieces = line[1]
#                 if not pieces:
#                     continue
#                 qty = int(math.floor(bal/pieces))
#                 bal = math.fmod(bal, pieces)
#                 cash_line_obj.write(cr, uid, [line[0]], {'number_closing': qty})
#             if bal > 10 **-4:
#                 raise osv.except_osv(_('Warning!'),
#                     _('After attempt to fill in the cash box line, there are still remain amount of (%.2f).') % (bal,))
#         self._update_balances(cr, uid, ids, context)
#         return True
#
#     def button_confirm_cash_auto(self, cr, uid, ids, context=None):
#         # Auto fill in cash box
#         self._auto_fill_cash_box(cr, uid, ids, context=context)
#         return super(account_cash_statement, self).button_confirm_cash(cr, uid, ids, context=context)
#
# account_cash_statement()


class account_bank_statement_line(osv.osv):

    _inherit = 'account.bank.statement.line'
    _columns = {
        'product_id': fields.many2one('product.product', 'Product', required=False),
        'payto': fields.char('Pay to', required=False),
    }

    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        if context is None:
            context = {}
        if not product_id:
            return False
        product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
        if product:
            account_id = product.property_account_expense.id
            return {'value': {'account_id': account_id}}
        return False

account_bank_statement_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
