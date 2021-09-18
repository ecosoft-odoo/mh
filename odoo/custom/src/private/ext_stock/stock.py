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

from osv import fields, osv

class stock_picking(osv.osv):

    def _is_bangkok_customer(self, cursor, user, ids, name, arg, context=None):
        res = {}
        cursor.execute("select pick.id, (case when bkk.id is not null then true else false end) is_bkk \
                        from stock_picking pick left outer join \
                        (select distinct p.id from res_partner p, res_partner_res_partner_category_rel r \
                        where r.partner_id = p.id and r.category_id in \
                        (select id from res_partner_category categ where name like %s or name ilike %s)) bkk \
                        on pick.partner_id = bkk.id \
                        where pick.id in %s", ('%กรุงเทพ%', '%bangkok%', tuple(ids),))
        rs = cursor.fetchall()
        for r in rs:
            res[r[0]] = r[1]
        return res

    _inherit = 'stock.picking'

    _columns = {
        'is_bangkok_customer': fields.function(_is_bangkok_customer, string='Is Bangkok?', type='boolean', store=True),
        'po_reference': fields.char('PO Reference', size=64, readonly=True, states={'draft': [('readonly', False)]}),
        'po_date': fields.date('PO Date', readonly=True, states={'draft': [('readonly', False)]}),
        'x_shipper': fields.char('Shipper Text'),
    }

stock_picking()

class stock_picking_out(osv.osv):

    def _is_bangkok_customer(self, cursor, user, ids, name, arg, context=None):
        return self.pool.get('stock.picking')._is_bangkok_customer(cursor, user, ids, name, arg, context=context)

    _inherit = 'stock.picking.out'

    _columns = {
        'is_bangkok_customer': fields.function(_is_bangkok_customer, string='Is Bangkok?', type='boolean', store=True),
        'po_reference': fields.char('PO Reference', size=64, readonly=True, states={'draft': [('readonly', False)]}),
        'po_date': fields.date('PO Date', readonly=True, states={'draft': [('readonly', False)]}),
    }

stock_picking_out()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
