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
from datetime import datetime
from dateutil.relativedelta import relativedelta

LAST_PAY_DATE_RULE = [('invoice_duedate', 'Invoice Due Date (default)'),
                      ('invoice_period_plus_3_months', 'Invoice Period + 3 months'),
                      ('invoice_date_payterm_monthend', 'Invoice Date + Payment Term > Month End'),
                      ('invoice_date_monthpayterm_monthend', 'Invoice Date + Month Payment Term > Month End'),
                      ('invoice_date_plus_cust_payterm', 'Invoice Date + Customer Payment Term')]


class commission_worksheet(osv.osv):

    _inherit = "commission.worksheet"

    _columns = {
        'is_mh_novat': fields.boolean('No-VAT', required=False, readonly=True, states={'draft': [('readonly', False)]}),
    }
    _defaults = {
        'is_mh_novat': False
    }
    _sql_constraints = [
        ('unique_sale_team_period', 'unique(sale_team_id, period_id, is_mh_novat)', 'Duplicate Sale Team / Period / No-VAT'),
        ('unique_salesperson_period', 'unique(salesperson_id, period_id, is_mh_novat)', 'Duplicate Salesperson / Period / No-VAT')
    ]

    def _get_matched_invoices_by_period(self, cr, uid, salesperson_id, sale_team_id, period, context=None):
        """
        Override method, split between VAT and No-VAT
        """
        res_id = salesperson_id or sale_team_id
        condition = salesperson_id and 't.salesperson_id = %s' or 't.sale_team_id = %s'

        is_mh_novat = context.get('is_mh_novat')
        if is_mh_novat != None:
            condition += ' and ai.is_mh_novat = %s' % is_mh_novat
        cr.execute("select ai.id from account_invoice ai \
                            join account_invoice_team t on ai.id = t.invoice_id \
                            where ai.state in ('open','paid') \
                            and date_invoice >= %s and date_invoice <= %s \
                            and " + condition + " order by ai.id", (period.date_start, period.date_stop, res_id))
        invoice_ids = map(lambda x: x[0], cr.fetchall())
        return invoice_ids

    # overwrite percent commission with promo_code
    def _get_percent_product_category(self, cr, uid, line):
        if line.promo_code:
            return line.promo_code.percent_commission
        return super(commission_worksheet, self)._get_percent_product_category(cr, uid, line)

    def _get_percent_product(self, cr, uid, line):
        if line.promo_code:
            return line.promo_code.percent_commission
        return super(commission_worksheet, self)._get_percent_product(cr, uid, line)

    def _get_percent_product_step(self, cr, uid, line):
        if line.promo_code:
            return line.promo_code.percent_commission
        return super(commission_worksheet, self)._get_percent_product_step(cr, uid, line)

commission_worksheet()


class commission_worksheet_line(osv.osv):

    _inherit = "commission.worksheet.line"

    def _get_invoice_period_plus_3_months(self, cr, uid, invoice, context=None):
        future_date = datetime.strptime(invoice.date_invoice, '%Y-%m-%d') + relativedelta(months=4)
        last_pay_date = datetime.strptime(future_date.strftime("%Y") + '-' + future_date.strftime("%m") + '-01', '%Y-%m-%d') - relativedelta(days=1)
        return last_pay_date.strftime('%Y-%m-%d')

    def _get_invoice_date_payterm_monthend(self, cr, uid, invoice, context=None):
        date_due = self._get_date_maturity(cr, uid, invoice, invoice.date_invoice) or invoice.date_due
        future_date = datetime.strptime(date_due, '%Y-%m-%d') + relativedelta(months=1)
        last_pay_date = datetime.strptime(future_date.strftime("%Y") + '-' + future_date.strftime("%m") + '-01', '%Y-%m-%d') - relativedelta(days=1)
        return last_pay_date.strftime('%Y-%m-%d')

    def _get_invoice_date_monthpayterm_monthend(self, cr, uid, invoice, context=None):
        # If payment term are 30, 60, 90, 120 and 150, converted to 1, 2, 3, 4, 5 months respectively.
        map_payterms = {'30': 1, '60': 2, '90': 3, '120': 4, '150': 5}
        if invoice.partner_id.property_payment_term and (invoice.partner_id.property_payment_term.name in map_payterms):
            months = map_payterms[invoice.partner_id.property_payment_term.name] + 1
            future_date = datetime.strptime(invoice.date_invoice, '%Y-%m-%d') + relativedelta(months=months)
            last_pay_date = datetime.strptime(future_date.strftime("%Y") + '-' + future_date.strftime("%m") + '-01', '%Y-%m-%d') - relativedelta(days=1)
            return last_pay_date.strftime('%Y-%m-%d')
        else:  # Otherwise fall back to invoice_date_payterm_monthends
            return self._get_invoice_date_payterm_monthend(cr, uid, invoice, context=context)

    def _calculate_last_pay_date(self, cr, uid, rule, invoice, context=None):
        res = super(commission_worksheet_line, self)._calculate_last_pay_date(cr, uid, rule, invoice, context=context)
        if res:
            return res
        elif rule == 'invoice_period_plus_3_months':
            return self._get_invoice_period_plus_3_months(cr, uid, invoice, context=context)
        elif rule == 'invoice_date_payterm_monthend':
            return self._get_invoice_date_payterm_monthend(cr, uid, invoice, context=context)
        elif rule == 'invoice_date_monthpayterm_monthend':
            return self._get_invoice_date_monthpayterm_monthend(cr, uid, invoice, context=context)
        else:
            return None

commission_worksheet_line()


class res_users(osv.osv):

    _inherit = "res.users"
    _columns = {
        'last_pay_date_rule': fields.selection(LAST_PAY_DATE_RULE, 'Last Pay Date Rule')
    }
    _defaults = {
        'last_pay_date_rule': 'invoice_period_plus_3_months'
    }

res_users()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
