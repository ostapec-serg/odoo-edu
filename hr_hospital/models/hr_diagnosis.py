from odoo import fields, models


class HrHospitalDiagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'HrHospitalDiagnosis'
    _order = "diagnosis_date"

    patient_id = fields.Many2one(
        comodel_name="hr.hospital.patient",
        required=True
    )
    doctor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
    )
    disease_id = fields.Many2one(
        comodel_name="hr.hospital.disease",
        string="Disease"
    )
    # visit_id = fields.One2many(
    #     comodel_name="hr.hospital.patient.visit",
    #     inverse_name="patient_id",
    #     domain=[("diagnosis_id", "=", "False")]
    # )
    diagnosis_date = fields.Date()
    treatment = fields.Text()
    mentor_comment = fields.Text()
    is_intern = fields.Boolean(compute="_compute_is_intern")

    def _compute_is_intern(self) -> None:
        for rec in self:
            rec.is_intern = rec.doctor_id.is_intern

    def name_get(self) -> list:
        return [
            (diagnosis.id, diagnosis.diagnosis_date) for diagnosis in self
        ]
