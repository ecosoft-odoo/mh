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

import time

from report import report_sxw

class receipt_voucher(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(receipt_voucher, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_total': self.get_total,
            'get_reconcile_name': self.get_reconcile_name,
            'get_reconcile_amount': self.get_reconcile_amount,
            'get_net_amount': self.get_net_amount,
            'get_payreg_check': self.get_payreg_check,
            'get_payreg_cash': self.get_payreg_cash,
            'get_payreg_transfer': self.get_payreg_transfer,
            'get_payreg_total': self.get_payreg_total
    })
        
    def get_total(self, receipt_voucher):
        if not receipt_voucher:
            return False
        else:
            total_amt = 0.0
            for line in receipt_voucher.line_ids:
                total_amt += line.amount or 0.0
            return total_amt
        
    def get_reconcile_name(self, receipt_voucher):
        if not receipt_voucher:
            return False
        else:
            if receipt_voucher.payment_option == 'with_writeoff':
                return receipt_voucher.writeoff_acc_id.name
            else:
                return 'ส่วนลดจ่าย'
            
    def get_reconcile_amount(self, receipt_voucher):
        if not receipt_voucher:
            return False
        else:
            if receipt_voucher.payment_option == 'with_writeoff':
                return receipt_voucher.writeoff_amount
            else:
                return 0.0
            
    def get_net_amount(self, receipt_voucher):
        if not receipt_voucher:
            return False
        else:
            total_amt = self.get_total(receipt_voucher)
            reconcile_amt = self.get_reconcile_amount(receipt_voucher)
            net_amt = total_amt + reconcile_amt    
            return net_amt
        
        
        
        
        
    def get_payreg_check(self, receipt_voucher):
        if not receipt_voucher:
            return 0.0
        else:
            amt = 0.0
            for line in receipt_voucher.payment_details:
                amt += line.type == 'check' and line.amount or 0.0
            return amt
        
    def get_payreg_cash(self, receipt_voucher):
        if not receipt_voucher:
            return 0.0
        else:
            amt = 0.0
            for line in receipt_voucher.payment_details:
                amt += line.type == 'cash' and line.amount or 0.0
            return amt
        
    def get_payreg_transfer(self, receipt_voucher):
        if not receipt_voucher:
            return 0.0
        else:
            amt = 0.0
            for line in receipt_voucher.payment_details:
                amt += line.type == 'transfer' and line.amount or 0.0
            return amt
        
    def get_payreg_total(self, receipt_voucher):
        if not receipt_voucher:
            return 0.0
        else:
            amt = 0.0
            for line in receipt_voucher.payment_details:
                amt += line.amount or 0.0
            return amt
        
            
report_sxw.report_sxw('report.account.receipt.voucher.mh', 'account.voucher', '', parser=receipt_voucher, header="internal")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

