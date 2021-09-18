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


class account_voucher(osv.osv):

    def _net_amount(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for voucher in self.browse(cr, uid, ids, context=context):
            res[voucher.id] = voucher.amount - voucher.writeoff_amount
        return res

    _inherit = 'account.voucher'
    _columns = {
        'net_amount': fields.function(_net_amount, string='Net Total', type='float'),
        'note': fields.text('Note'),
        'saleperson_id': fields.related('partner_id', 'user_id', type='many2one', relation='res.users', string='Salesperson', store=True, readonly=True),
    }

account_voucher()


class account_voucher_line(osv.osv):

    def _supplier_invoice_number(self, cursor, user, ids, name, arg, context=None):
        res = {}
        cursor.execute('SELECT vl.id, i.supplier_invoice_number \
                        FROM account_voucher_line vl, account_move_line ml, account_invoice i \
                        WHERE vl.move_line_id = ml.id and ml.move_id = i.move_id \
                        AND vl.id IN %s',
                        (tuple(ids),))
        for line_id, supplier_invoice_number in cursor.fetchall():
            res[line_id] = supplier_invoice_number
        return res

    _inherit = 'account.voucher.line'
    _columns = {
        'supplier_invoice_number': fields.function(_supplier_invoice_number, string='Supplier Invoice Number', type='char'),
    }

account_voucher_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
