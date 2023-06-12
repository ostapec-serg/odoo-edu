from odoo import fields, models, _


class HrHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = _('Diseases')

    name = fields.Char()
    doctor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        string="Attending doctor", required=True
    )
