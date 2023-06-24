from odoo import fields, models, _
from .hr_hospital import constants as const


class HrPerson(models.AbstractModel):
    _name = 'hr.person.mixin'
    _description = _('HrPerson mixin')

    name = fields.Char(required=True)
    phone = fields.Char()
    email = fields.Char()
    img = fields.Image()
    sex = fields.Selection(
        selection=const.SEX_LIST, required=True
    )
