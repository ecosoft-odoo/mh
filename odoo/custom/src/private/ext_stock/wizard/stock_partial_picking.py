# -*- coding: utf-8 -*-

#################################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from tools.translate import _
import openerp.addons.decimal_precision as dp


class stock_partial_picking_line(osv.TransientModel):
        
    _inherit = 'stock.partial.picking.line'
    
    _columns = {
                'init_qty':fields.float("Init Qty", digits_compute=dp.get_precision('Product Unit of Measure'), required=True)
    }
    
    def onchange_quantity(self, cr, uid, ids, quantity, init_qty, context=None):
        
        # We decide not to use this feature at MH
#         if not quantity or not init_qty:
#             return {'value':{}}
#         
#         if quantity > init_qty:
#             warning = {
#                 'title': _('Quantity Warning!'),
#                 'message' : _('Delivery Quantity more than Initial Quantity is not allowed!')
#                 }
#             value = {'quantity':init_qty}
#             return {'warning': warning, 'value': value}
#         else:
#             return {'value':{}}
    
        return {'value':{}}
        
stock_partial_picking_line()

class stock_partial_picking(osv.osv_memory):
    
    _inherit = "stock.partial.picking"
    
    def _partial_move_for(self, cr, uid, move):
        
        partial_move = super(stock_partial_picking, self)._partial_move_for(cr, uid, move)
        partial_move.update({
                             'init_qty': move.product_qty if move.state in ('assigned','draft','confirmed') else 0
                        })

        return partial_move  
      
stock_partial_picking()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
