# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2013 Elico Corp. All Rights Reserved.
#    Author: Yannick Gouin <yannick.gouin@elico-corp.com>
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
from openerp import netsvc
from openerp.tools.translate import _


class sale_order(osv.osv):

    _inherit = 'sale.order'
    _name = 'sale.order'

    def _prepare_order_picking(self, cr, uid, order, context=None):
        pick_name = self.pool.get('ir.sequence').get(cr, uid, 'stock.picking.out')
        return {
            'name': pick_name,
            'origin': order.name,
            'date': order.date_order,
            'type': 'out',
            'state': 'auto',
            'move_type': order.picking_policy,
            'sale_id': order.id,
            'partner_id': order.partner_shipping_id.id,
            'note': order.note,
            'invoice_state': (order.order_policy == 'picking' and '2binvoiced') or 'none',
            'company_id': order.company_id.id,
        }

    def _create_pickings_and_procurements(self, cr, uid, order, order_lines, picking_id=False, context=None):
        """Create the required procurements to supply sales order lines, also connecting
        the procurements to appropriate stock moves in order to bring the goods to the
        sales order's requested location.

        If ``picking_id`` is provided, the stock moves will be added to it, otherwise
        a standard outgoing picking will be created to wrap the stock moves, as returned
        by :meth:`~._prepare_order_picking`.

        Modules that wish to customize the procurements or partition the stock moves over
        multiple stock pickings may override this method and call ``super()`` with
        different subsets of ``order_lines`` and/or preset ``picking_id`` values.

        :param browse_record order: sales order to which the order lines belong
        :param list(browse_record) order_lines: sales order line records to procure
        :param int picking_id: optional ID of a stock picking to which the created stock moves
                               will be added. A new picking will be created if ommitted.
        :return: True
        """
        move_obj = self.pool.get('stock.move')
        picking_obj = self.pool.get('stock.picking')
        procurement_obj = self.pool.get('procurement.order')
        proc_ids = []

        location_id = order.shop_id.warehouse_id.lot_stock_id.id
        output_id = order.shop_id.warehouse_id.lot_output_id.id

        for line in order_lines:
            if line.state == 'done':
                continue

            date_planned = self._get_date_planned(cr, uid, order, line, order.date_order, context=context)

            fake_line_ids = []
            is_bundle = False

            if line.product_id:
                if line.product_id.supply_method == 'bundle':
                    fake_line_ids = filter(None, map(lambda x: x, line.product_id.item_ids))
                    is_bundle = True
                else:
                    fake_line_ids.append(line)

                for fake_line in fake_line_ids:
                    line_vals = {}
                    line_vals.update({
                        'location_id': location_id,
                        'company_id': order.company_id.id,
                        #move
                        'location_dest_id': output_id,
                        'date': date_planned,
                        'date_expected': date_planned,
                        'partner_id': line.address_allotment_id.id or order.partner_shipping_id.id,
                        'sale_line_id': line.id,
                        'origin': order.name,
                        'tracking_id': False,
                        'state': 'draft',
                    })

                    if is_bundle:
                        line_vals.update({
                            'product_id': fake_line.item_id.id,
                            'product_qty': fake_line.qty_uom,
                            'product_uom': fake_line.uom_id.id,
                            'product_uos_qty': fake_line.qty_uom,
                            'product_uos': fake_line.uom_id.id,
                            'procure_method': fake_line.item_id.procure_method,
                            'price_unit': fake_line.item_id.standard_price or 0.0,
                            'name': fake_line.item_id.name,
                            'note': fake_line.item_id.name + ' (' + line.name + ')',
                        })
                        product_id = fake_line.item_id
                    else:
                        line_vals.update({
                            'name': line.name,
                            'note': line.name,
                            'product_id': line.product_id.id,
                            'product_qty': line.product_uom_qty,
                            'product_uom': line.product_uom.id,
                            'product_uos_qty': (line.product_uos and line.product_uos_qty) or line.product_uom_qty,
                            'product_uos': (line.product_uos and line.product_uos.id) or line.product_uom.id,
                            'procure_method': line.type,
                            'product_packaging': line.product_packaging,
                            'price_unit': line.product_id.standard_price or 0.0,
                        })
                        product_id = line.product_id

                    if product_id.type in ('product', 'consu'):
                        if not picking_id:
                            picking_id = picking_obj.create(cr, uid, self._prepare_order_picking(cr, uid, order, context=context))
                        line_vals.update({'picking_id': picking_id})
                        move_id = move_obj.create(cr, uid, line_vals)
                    else:
                        # a service has no stock move
                        move_id = False

                    if 'picking_id' in line_vals:
                        del line_vals['picking_id']
                    del line_vals['location_dest_id']
                    del line_vals['date']
                    del line_vals['date_expected']
                    del line_vals['partner_id']
                    del line_vals['sale_line_id']
                    del line_vals['tracking_id']
                    del line_vals['state']
                    line_vals.update({
                        'move_id': move_id,
                        'date_planned': date_planned,
                    })
                    proc_id = procurement_obj.create(cr, uid, line_vals)
                    proc_ids.append(proc_id)
                    line.write({'procurement_id': proc_id})
                    self.ship_recreate(cr, uid, order, line, move_id, proc_id)

        wf_service = netsvc.LocalService("workflow")
        if picking_id:
            wf_service.trg_validate(uid, 'stock.picking', picking_id, 'button_confirm', cr)
        for proc_id in proc_ids:
            wf_service.trg_validate(uid, 'procurement.order', proc_id, 'button_confirm', cr)

        val = {}
        if order.state == 'shipping_except':
            val['state'] = 'progress'
            val['shipped'] = False

            if (order.order_policy == 'manual'):
                for line in order.order_line:
                    if (not line.invoiced) and (line.state not in ('cancel', 'draft')):
                        val['state'] = 'manual'
                        break
        order.write(val)
        return True

    def action_ship_create(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self._create_pickings_and_procurements(cr, uid, order, order.order_line, None, context=context)
        return True

    def _validate_product_bundle(self, cr, uid, order_id, context=None):
        is_bundle_list = []
        order = self.browse(cr, uid, order_id, context)
        if not order:
            return
        for line in order.order_line:
            if line.product_id:
                is_bundle_list += [line.product_id.supply_method == 'bundle' or False]
            else:
                is_bundle_list += [False]
        is_bundle_list = list(set(is_bundle_list))
        if len(is_bundle_list) > 1 and False in is_bundle_list:  # [True, False]
            raise osv.except_osv(_('Product bundle exception!'),
                _('If there is a product bundle, all lines must be product bundle!'))
        elif is_bundle_list == [True] and order.order_policy != 'manual':  # If product bundle, also use invoice = On Demand
            self.write(cr, uid, [order_id], {'order_policy': 'manual'}, context)

    def create(self, cr, uid, vals, context=None):
        res_id = super(sale_order, self).create(cr, uid, vals, context=context)
        self._validate_product_bundle(cr, uid, res_id, context)
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        res = super(sale_order, self).write(cr, uid, ids, vals, context=context)
        for res_id in ids:
            self._validate_product_bundle(cr, uid, res_id, context)
        return res

sale_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
