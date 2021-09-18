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

from openerp.tools.translate import _
from openerp.osv import osv
from openerp import tools


def rounding(f, r):
    # TODO for trunk: log deprecation warning
    # _logger.warning("Deprecated rounding method, please use tools.float_round to round floats.")
    return tools.float_round(f, precision_rounding=r)


class product_uom(osv.osv):

    _inherit = 'product.uom'

    # Override method
    def _compute_qty_obj(self, cr, uid, from_unit, qty, to_unit, context=None):
        if context is None:
            context = {}
        if from_unit.category_id.id != to_unit.category_id.id:
            if context.get('raise-exception', True):
                raise osv.except_osv(_('Error!'), _('Conversion from Product UoM %s to Default UoM %s is not possible as they both belong to different Category!.') % (from_unit.name, to_unit.name,))
            else:
                return qty
        amount = qty / from_unit.factor
        if to_unit:
            # kittiu: Change from celiing to rounding
            amount = rounding(amount * to_unit.factor, to_unit.rounding)
        return amount

product_uom()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
