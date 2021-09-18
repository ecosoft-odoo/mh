# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class sale_order_line(osv.osv):

    _inherit = 'sale.order.line'
    _columns = {
        'promo_code': fields.many2one(
            'promo.code', 'Promo Code',
            domain="[('product_id', '=', product_id)]"),
    }

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        context = context or {}
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
            uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
        res.get('value').update({'promo_code': False})
        return res

    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        res = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line, account_id=account_id, context=context)
        res['promo_code'] = line and line.promo_code and line.promo_code.id or False
        return res

sale_order_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
