# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2009 Gábor Dukai
#    Modified by Almacom (Thailand) Ltd.
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
{
    "name" : "MH Addons Installation",
    "version" : "1.0",
    "author" : "kittiu",
    "website" : "http://ecosoft.co.th",
    "description": """
Install all requried modules
""",
    "depends" : [
                 'sale','purchase','stock','account','account_voucher','account_accountant','procurement',
                 'mrp','base_import','base_report_designer','account_anglo_saxon',
                 'doc_nodelete','account_billing',#'purchase_product_uos',
                 'product_uom_bycategory','payment_register','hr_expense_extension','correct_deliver_bymistake',
                 'account_invoice_merge','invoice_cancel_ex','confirm_document_batch',
                 'product_code_extension','sale_delivery_date','customer_supplier_voucher','picking_invoice_rel',
                 'product_price_limit','product_flexible_search',
                 
                 'jasper_reports','ac_report_font_thai','rml_reports',
                 'ext_base','ext_product','ext_sale','vat_novat',
                 'ext_account','ext_account_voucher','ext_procurement','ext_purchase',
                 'ext_stock','advance_and_additional_discount','partner_shipper','jrxml_reports',
                 'product_so_uom','security_enhanced','auto_backup','fix_account_validate'
                 #'ext_stock','ext_sale',
                 #'product_attributes','product_variant_multi'
                 ],
                 
    "auto_install": False,
    "application": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

