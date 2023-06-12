from odoo import fields, models, _


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = _('Doctors')

    name = fields.Char()
