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


{
    'name': 'Bundle product',
    'version': '1.0',
    'category': 'Sales Management',
    'description': """
    This allow you to create bundle product, which is a product containing other products.

    Example:
    "Drinks Set"
      - 1 Apple Juice
      - 1 Orange Juice
      - 1 Grape Juice

    On the Sale Order will appear "Drinks Set", and on the Packing list will appear the detail of the Bundle.
    You can replace one of the item in the Bundle in the Delivery Order, eg: replace 1 Orange Juice by 1 Mandarin Orange Juice.
    """,
    'author': 'Elico Corp, ECOSOFT',
    'website': 'http://www.elico-corp.com, http://www.ecosoft.co.th',
    'depends': ['sale_stock'],
    'init_xml': [],
    'update_xml': [
           'product_view.xml',
    ],
    'demo_xml': [],
    'installable': True,
    'active': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
