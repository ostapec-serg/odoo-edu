from odoo import fields, models, _


class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = _('Diseases')
    _parent_name = "parent_id"

    parent_id = fields.Many2one(
        comodel_name="hr.hospital.disease.category",
        string="Disease category"
    )
    name = fields.Char(string="Disease name")
