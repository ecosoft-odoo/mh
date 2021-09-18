# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class promo_code(osv.osv):

    _name = "promo.code"
    _rec_name = "promo_code"
    _columns = {
        'product_id': fields.many2one(
            'product.product',
            'Product',
            ondelete='cascade',
            select=True,
            required=True),
        'promo_code': fields.char(
            'Promo Code',
            size=64,
            required=True),
        'percent_commission': fields.float(
            'Commission (%)',
            digits=(16, 2),
            required=True),
        'promo_description': fields.char(
            'Description',
            size=128,
            required=True),
    }
    _order = 'product_id'

promo_code()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
