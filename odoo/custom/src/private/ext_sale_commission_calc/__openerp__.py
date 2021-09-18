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
    'name': "Sales Commission Calculations Extension for MH",
    'author': 'Ecosoft',
    'summary': '',
    'description': """

* Added new type of Last Yay Due Date = Invoice's Period + 3 months, and use the last day of that month.
* Separate Calculation Worksheet with MH VAT and MH No-VAT

""",
    'category': 'Sales',
    'sequence': 20,
    'website': 'http://www.ecosoft.co.th',
    'images': [],
    'depends': ['sale', 'sale_commission_calc'],
    'demo': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'commission_calc_view.xml',
        'account_invoice_view.xml',
        'invoice_info_view.xml',
        'commission_rule_view.xml',
        'sale_view.xml',
    ],
    'test': [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
