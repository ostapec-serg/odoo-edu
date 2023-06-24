from odoo import fields, models


class HrDiseaseCategory(models.Model):
    _name = 'hr.hospital.disease.category'
    _description = 'Disease Category'

    name = fields.Char()
    desc = fields.Text(string="Description")
    disease_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id'
    )
