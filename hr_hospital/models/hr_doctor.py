from odoo import fields, models, api, _


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.person.mixin'
    _description = _('Doctors')
    _parent_name = "parent_id"
    _order = "create_date"

    specialty = fields.Char()
    parent_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        domain="[('is_mentor', '=', True)]",
        string="Doctor"
    )
    child_ids = fields.One2many(
        comodel_name="hr.hospital.doctor",
        inverse_name="parent_id",
        string="Interns"
    )
    schedule = fields.One2many(
        comodel_name="hr.hospital.doctor.schedule",
        inverse_name="day_week"
    )
    is_intern = fields.Boolean()
    is_mentor = fields.Boolean()

    @api.onchange('is_intern')
    def onchange_is_intern(self):
        if not self.is_intern:
            self.parent_id = False
