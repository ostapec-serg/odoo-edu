from odoo import fields, models, api, _


class HrPatientVisit(models.Model):
    _name = 'hr.hospital.patient.visit'
    _description = _("Patients visits")

    patient_id = fields.Many2one(
        comodel_name="hr.hospital.patient",
        string="Patient", required=True
    )
    doctor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        string="Doctor",
        compute="_compute_doctor_id",
        readonly=True, store=True
    )
    disease_id = fields.Many2one(
        comodel_name="hr.hospital.disease",
        string="Disease"
    )
    visit_date = fields.Datetime(string="Visit date", required=True)

    @api.depends('patient_id')
    def _compute_doctor_id(self):
        for rec in self:
            rec.doctor_id = rec.patient_id.doctor_id

    def name_get(self):
        result = []
        name = self._rec_name
        if name in self._fields:
            convert = self._fields[name].convert_to_display_name
            for record in self:
                result.append((record.id, convert(record[name], record) or ""))
        else:
            for record in self:
                result.append((
                    record.id, f"[{record.visit_date}, "
                               f"{record.patient_id.name}]"
                ))
        return result
