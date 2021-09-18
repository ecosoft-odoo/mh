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

{
    'name' : 'Product Extension for MH',
    'version' : '1.0',
    'author' : 'Kitti U.',
    'summary': 'Product Extensions for MH',
    'description': """
    
Feature Includes,

* New product attributes added in information tab. Each has its own window -- Paper Size, Grams, Number of pages, Binding method
* Add field "Partner Barcode" in Product.
* Add field "Code" in Product Category.
* Add Product Brand master data. Brand will also belong to Product Category

    """,
    'category': 'Sales',
    'sequence': 7,
    'website' : 'http://www.ecosoft.co.th',
    'images' : [],
    'depends' : ['product'],
    'demo' : [],
    'data' : [
        'product_view.xml',
    ],
    'test' : [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
