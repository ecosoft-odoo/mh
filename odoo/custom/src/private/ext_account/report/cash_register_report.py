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

from openerp import tools
from openerp.osv import fields, osv


class cash_register_report(osv.osv):
    _name = "cash.register.report"
    _description = "Cash Register Report"
    _auto = False
    _rec_name = 'date'
    _columns = {
        'name': fields.char('Document', readonly=True),
        'state': fields.selection([
            ('draft', 'New'),
            ('open', 'Open'),
            ('confirm', 'Closed'),
        ], 'Order Status', readonly=True),
        'user_id': fields.many2one('res.users', 'Responsible', readonly=True),
        'journal_id': fields.many2one('account.journal', 'Journal', readonly=True),
        'date': fields.date('Date', readonly=True),
        'year': fields.char('Year', size=4, readonly=True),
        'month': fields.selection([('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
                                   ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'),
                                   ('10', 'October'), ('11', 'November'), ('12', 'December')], 'Month', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'description': fields.char('Description', readonly=True),
        'day': fields.char('Day', size=128, readonly=True),
        'ref': fields.char('Reference', readonly=True),
        'payto': fields.char('Pay to', readonly=True),
        'account_id': fields.many2one('account.account', 'Account', readonly=True),
        'amount': fields.float('Amount', readonly=True),
    }
    _order = 'id'

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'cash_register_report')
        cr.execute("""
            create or replace view cash_register_report as (
                select absl.id,
                    abs.name,
                    abs.state,
                    abs.user_id,
                    abs.journal_id,
                    abs.date,
                    to_char(abs.date, 'YYYY') as year,
                    to_char(abs.date, 'MM') as month,
                    to_char(abs.date, 'YYYY-MM-DD') as day,
                    product_id,
                    absl.name description,
                    ref,
                    payto,
                    account_id,
                    amount
                from account_bank_statement abs
                join account_bank_statement_line absl on abs.id = absl.statement_id
                order by abs.id, absl.id
            )
        """)
cash_register_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
