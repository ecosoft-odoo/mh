# -*- coding: utf-8 -*-
import csv
from openerp.modules import get_module_path
from openerp.osv import fields, osv


class res_partner(osv.osv):
    _inherit = 'res.partner'

    def _get_loc_info(self, cr, uid, ids, name, args, context=None):
        res = {}
        for partner in self.browse(cr, uid, ids, context=context):
            print partner
            if partner.location_code:
                loc_dict = self.\
                    _get_loc_dict_by_location_code(cr, uid,
                                                   partner.location_code)
                res[partner.id] = loc_dict
            else:
                if partner.zip:
                    loc_dict = self.\
                        _get_loc_dict_by_zip_code(cr, uid, partner.zip)
                    res[partner.id] = loc_dict
                else:
                    res[partner.id] = {'changwat': False,
                                       'amphur': False,
                                       'tambon': False,
                                       'zip_code': False}
        return res

    _columns = {
        'location_code': fields.char(
            string='รหัสที่ตั้ง', size=6),
        'amphur': fields.function(_get_loc_info, method=True, type='char', string='อำเภอ', store=True, multi='loc'),
        'tambon': fields.function(_get_loc_info, method=True, type='char', string='ตำบล', store=True, multi='loc'),
        'changwat': fields.function(_get_loc_info, method=True, type='char', string='จังหวัด', store=True, multi='loc'),
        'zip_code': fields.function(_get_loc_info, method=True, type='char', string='รหัสไปรษนีย์', store=True, multi='loc'),
    }

    def _get_loc_dict_by_location_code(self, cr, uid, location_code):
        module_path = get_module_path('location_code')
        file_path = module_path + '/data/location.csv'
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0] == location_code:
                    return {'changwat': row[1],
                            'amphur': row[2],
                            'tambon': row[3],
                            'zip_code': row[4]}
        return {'changwat': False,
                'amphur': False,
                'tambon': False,
                'zip_code': False}

    def _get_loc_dict_by_zip_code(self, cr, uid, zip):
        module_path = get_module_path('location_code')
        file_path = module_path + '/data/location.csv'
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[4] == zip:
                    return {'changwat': row[1],
                            'amphur': row[2],
                            'tambon': False,
                            'zip_code': row[4]}

        return {'changwat': False,
                'amphur': False,
                'tambon': False,
                'zip_code': False}
