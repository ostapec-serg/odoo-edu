from odoo import fields, models, _


class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = _('Diseases')

    name = fields.Char(string="Disease name")
