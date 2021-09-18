# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
import jasper_reports
from osv import osv,fields 
import pooler
import datetime

def mh_daily_customer_payment_parser( cr, uid, ids, data, context ):
    return {
        'parameters': {	
            'date': data['form']['date'],
            'user_id': data['form']['user_id'],
            'prepared_by': data['form']['prepared_by'],
        },
   }

jasper_reports.report_jasper(
    'report.mh_daily_customer_payment',
    'account.voucher',
    parser=mh_daily_customer_payment_parser
)
