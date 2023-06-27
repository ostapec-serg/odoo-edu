from odoo import fields, models, api, _
from odoo.addons.hr_hospital import constants as const
from odoo.exceptions import ValidationError


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.person.mixin'
    _description = _('Doctors')
    _parent_name = "parent_id"
    _order = "create_date"

    state = fields.Selection(
        selection=const.DOCTOR_STATE_LIST,
        default="draft",
        string="Status"
    )
    specialty = fields.Char(required=True)
    parent_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        domain="[('is_mentor', '=', True)]",
        string="Mentor"
    )
    child_ids = fields.One2many(
        comodel_name="hr.hospital.doctor",
        inverse_name="parent_id",
        string="Interns"
    )
    schedule = fields.One2many(
        comodel_name="hr.hospital.doctor.schedule",
        inverse_name="doctor_id"
    )
    is_intern = fields.Boolean()
    is_mentor = fields.Boolean()
    active = fields.Boolean(default=True)

    @api.model
    def create(self, vals_list):
        vals_list['state'] = "active"
        return super().create(vals_list)

    def write(self, vals):
        active = vals.get('active', "")
        for rec in self:
            if active is False:
                rec.state = "arch"
        return super().write(vals)

    @api.onchange('is_intern')
    def onchange_is_intern(self):
        if not self.is_intern:
            self.parent_id = False

    @api.constrains('parent_id')
    def _check_mentor_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create intern recursive.'))
