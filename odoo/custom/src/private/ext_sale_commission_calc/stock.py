# -*- coding: utf-8 -*-

from openerp.osv import osv


class stock_picking(osv.osv):
    _inherit = "stock.picking"

    def _prepare_invoice_line(self, cr, uid, group, picking, move_line, invoice_id, invoice_vals, context=None):
        res = super(stock_picking, self)._prepare_invoice_line(cr, uid, group, picking, move_line, invoice_id, invoice_vals, context=context)
        res['promo_code'] = (move_line
                             and move_line.sale_line_id
                             and move_line.sale_line_id.promo_code
                             and move_line.sale_line_id.promo_code.id or False)
        return res
