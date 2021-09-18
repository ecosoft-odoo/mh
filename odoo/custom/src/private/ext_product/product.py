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

import netsvc
from osv import osv, fields
from tools.translate import _

import openerp.addons.decimal_precision as dp

class product_template(osv.osv):
    
    _inherit = "product.template"
    _columns = {
        # Do not translate
        'name': fields.char('Name', size=128, required=True, translate=False, select=True),
    }    
    
product_template()

class product_category(osv.osv):

    _inherit = "product.category"
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=False, select=True),
        'code': fields.char('Code', size=3, required=False),
    }
    
product_category()

class product_product(osv.osv):

    _inherit = "product.product"
    _columns = {
        # Sales
        'partner_barcode': fields.char('Partner Barcode', size=128, required=False),
        'paper_size_id': fields.many2one('product.paper.size', 'Paper Size'),
        'paper_grams_id': fields.many2one('product.paper.grams', 'Grams'),
        'paper_nums_id': fields.many2one('product.paper.nums', 'Number of pages'),
        'paper_binding_id': fields.many2one('product.paper.binding', 'Binding method'),
        'cover_unit_price': fields.float('Cover price (1 PCE)', digits_compute=dp.get_precision('Product Price')),
        'brand_id': fields.many2one('product.brand', 'Brand'),
        'product_pack_id': fields.many2one('product.pack', 'Product Pack'),
        # Purchase
        'pieces_per_uom': fields.float('Pieces / UOM'),
    }
    
    def onchange_product_categ(self, cr, uid, ids, categ_id=False):
        if not categ_id:
            return {'value': {'product_main_code': False}}
        results = self.pool.get('product.category').read(cr, uid, [categ_id], ['code'])
        return {'value': {'product_main_code': results[0]['code']}}


product_product()

class product_paper_size(osv.osv):
    _name = 'product.paper.size'
    _description = 'Size of paper'
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
    }

product_paper_size()

class product_paper_grams(osv.osv):
    _name = 'product.paper.grams'
    _description = 'Grams of paper'
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
    }
    
product_paper_grams()

class product_paper_nums(osv.osv):
    _name = 'product.paper.nums'
    _description = 'Number of pages'
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
    }
    
product_paper_nums()

class product_paper_binding(osv.osv):
    _name = 'product.paper.binding'
    _description = 'Binding methods'
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
    }
    
product_paper_binding()
    
class product_brand(osv.osv):
    _name = "product.brand"
    _description = "Product Brand"
    _columns = {
        'name': fields.char('Brand Name', size=64, required=True),
    }
    
product_brand()

class product_pack(osv.osv):
    _name = "product.pack"
    _description = "Product Pack"
    _columns = {
        'name': fields.char('Product Pack', size=64, required=True),
    }
    
product_brand()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
