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
from openerp.tools.translate import _

class stock_fill_move_by_sale(osv.osv_memory):
    _name = "stock.fill.move.by.sale"
    _description = "Fill Move Lines"

    _columns = {
        'location_id': fields.many2one('stock.location', 'Source Location', required=True),
        'location_dest_id': fields.many2one('stock.location', 'Destination Location', required=True),
        'sale_id': fields.many2one('sale.order', "Sales Order"),
    }

    _defaults = {
        'location_id': lambda self,cr,uid,c: c.get('location_id', False),
        'location_dest_id': lambda self,cr,uid,c: c.get('location_dest_id', False),
    }

    def fill_move(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        picking_obj = self.pool.get('stock.picking.out')
        move_obj = self.pool.get('stock.move')
        sale_obj = self.pool.get('sale.order')
        picking_id = context.get('active_id', False)

        if not picking_id:
            return {'type': 'ir.actions.act_window_close'}

        if ids and len(ids):
            ids = ids[0]
        else:
            return {'type': 'ir.actions.act_window_close'}
        fill_move = self.browse(cr, uid, ids, context=context)
        # Find SO
        sale = sale_obj.browse(cr, uid, fill_move.sale_id.id)
        # Check for existing lines in this picking, remove them if exists.
        move_ids = move_obj.search(cr, uid, [('picking_id', '=', picking_id)])
        move_obj.unlink(cr, uid, move_ids)
        # Find the latest picking (confirmed, assigned)
        picking_ids = [x.id for x in sale.picking_ids]
        picking_ids = picking_obj.search(cr, uid, [('id', 'in', picking_ids),
                                                   ('state', 'in', ('confirmed', 'assigned'))],
                                         order='id desc', limit=1)
        move_ids = move_obj.search(cr, uid, [('picking_id', 'in', picking_ids)])
        for move in move_obj.browse(cr, uid, move_ids, context=context):
            res = {
                'picking_id': picking_id,
                'product_id': move.product_id.id,
                'name': '/',
                'product_uom': move.product_uom.id,
                'product_qty': move['product_qty'],
                'location_id': fill_move.location_id.id,
                'location_dest_id': fill_move.location_dest_id.id,
            }
            print res
            if res.get('product_qty') > 0:
                move_obj.create(cr, uid, res)

        return {'type': 'ir.actions.act_window_close'}

stock_fill_move_by_sale()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
