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
    'name' : 'VAT / No-VAT',
    'version' : '1.0',
    'author' : 'Kitti U.',
    'summary': 'VAT / No-VAT',
    'description': """
Based on MH requirement, which need to separate VAT / No-VAT document (running number) during invoicing process.
This module will add 2 new fields VAT and No-VAT in Sales Order and Customer Invoice.

Starting from SO, user will have 3 options
1) No checking -- this will follow the standard procedure
2) Check VAT -- this ensure that more discount 7/107 = 6.54% will be added to even out with the Tax. This is quite special case for MH.
3) Check No-VAT -- no discount and no Tax (even when it set to have Tax). This is also special for MH.

The checked flag will be transfered to Customer Invoice, either created from SO or DO.
And in Customer Invoice, if No-VAT is checked, in addition to the existing Invoice Number, a new Running Number series will be created for it (to be used in the No-VAT Form).
    
    """,
    'category': 'Sales Management',
    'website' : 'http://www.ecosoft.co.th',
    'images' : [],
    'depends' : ['sale','sale_stock','account_billing','advance_and_additional_discount','account_debitnote'],
    'demo' : [],
    'data' : [
              'data/billing_novat_sequence.xml',
              'data/billing_vat_sequence.xml',              
              'data/invoice_novat_sequence.xml',
              'data/invoice_vat_sequence.xml',
              'data/debitnote_novat_sequence.xml',
              'data/debitnote_vat_sequence.xml',              
              'data/refund_novat_sequence.xml',
              'data/refund_vat_sequence.xml',
              'sale_view.xml',
              'account_invoice_view.xml',
              'account_billing_view.xml',
              ],
    'test' : [],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
