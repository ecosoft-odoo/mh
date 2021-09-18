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
from openerp.osv import fields,osv


class account_invoice_report(osv.osv):
    _inherit = "account.invoice.report"

    _columns = {
        'line_discount': fields.float('Line Discount', readonly=True),
    }

    def _select(self):
        return  super(account_invoice_report, self)._select() + ", sub.line_discount / cr.rate as line_discount"

    def _sub_select(self):
        select_str = """
            SELECT min(ail.id) AS id,
                    ai.date_invoice AS date,
                    to_char(ai.date_invoice::timestamp with time zone, 'YYYY'::text) AS year,
                    to_char(ai.date_invoice::timestamp with time zone, 'MM'::text) AS month,
                    to_char(ai.date_invoice::timestamp with time zone, 'YYYY-MM-DD'::text) AS day,
                    ail.product_id, ai.partner_id, ai.payment_term, ai.period_id,
                    CASE
                     WHEN u.uom_type::text <> 'reference'::text
                        THEN ( SELECT product_uom.name
                               FROM product_uom
                               WHERE product_uom.uom_type::text = 'reference'::text
                                AND product_uom.active
                                AND product_uom.category_id = u.category_id LIMIT 1)
                        ELSE u.name
                    END AS uom_name,
                    ai.currency_id, ai.journal_id, ai.fiscal_position, ai.user_id, ai.company_id,
                    count(ail.*) AS nbr,
                    ai.type, ai.state, pt.categ_id, ai.date_due, ai.account_id, ail.account_id AS account_line_id,
                    ai.partner_bank_id,
                    SUM(CASE
                         WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                            THEN (- ail.quantity) / u.factor
                            ELSE ail.quantity / u.factor
                        END) AS product_qty,
                    SUM(CASE
                         WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                            THEN - (ail.discount/100 * ail.quantity * ail.price_unit) -- kittiu
                            ELSE (ail.discount/100 * ail.quantity * ail.price_unit) -- kittiu
                        END) AS line_discount,
                    SUM(CASE
                         WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                            THEN - (ail.price_subtotal - (ai.add_disc/100 * ail.price_subtotal)) -- kittiu
                            ELSE (ail.price_subtotal - (ai.add_disc/100 * ail.price_subtotal)) -- kittiu
                        END) AS price_total,
                    CASE
                     WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                        THEN SUM(- (ail.price_subtotal - (ai.add_disc/100 * ail.price_subtotal))) -- kittiu
                        ELSE SUM((ail.price_subtotal - (ai.add_disc/100 * ail.price_subtotal))) -- kittiu
                    END / CASE
                           WHEN SUM(ail.quantity / u.factor) <> 0::numeric
                               THEN CASE
                                     WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                                        THEN SUM((- ail.quantity) / u.factor)
                                        ELSE SUM(ail.quantity / u.factor)
                                    END
                               ELSE 1::numeric
                          END AS price_average,
                    CASE
                     WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                        THEN - ai.residual
                        ELSE ai.residual
                    END / CASE
                           WHEN (( SELECT count(l.id) AS count
                                   FROM account_invoice_line l
                                   LEFT JOIN account_invoice a ON a.id = l.invoice_id
                                   WHERE a.id = ai.id)) <> 0
                               THEN ( SELECT count(l.id) AS count
                                      FROM account_invoice_line l
                                      LEFT JOIN account_invoice a ON a.id = l.invoice_id
                                      WHERE a.id = ai.id)
                               ELSE 1::bigint
                          END::numeric AS residual
        """
        return select_str

    def init(self, cr):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM (
                %s %s %s
            ) AS sub
            JOIN res_currency_rate cr ON (cr.currency_id = sub.currency_id)
            WHERE
                cr.id IN (SELECT id
                          FROM res_currency_rate cr2
                          WHERE (cr2.currency_id = sub.currency_id)
                              AND ((sub.date IS NOT NULL AND cr2.name <= sub.date)
                                    OR (sub.date IS NULL AND cr2.name <= NOW()))
                          ORDER BY name DESC LIMIT 1)
        )""" % (
                    self._table, 
                    self._select(), self._sub_select(), self._from(), self._group_by()))

account_invoice_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
