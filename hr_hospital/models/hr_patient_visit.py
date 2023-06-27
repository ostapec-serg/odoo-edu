import logging

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

# Is this good practice?
from odoo.addons.hr_hospital import constants as const

_logger = logging.getLogger()


class HrPatientVisit(models.Model):
    _name = 'hr.hospital.patient.visit'
    _description = _("Patients visits")

    state = fields.Selection(
        selection=const.STATE_LIST,
        default="draft",
        string="Status"
    )
    patient_id = fields.Many2one(
        comodel_name="hr.hospital.patient",
        string="Patient", required=True
    )
    doctor_id = fields.Many2one(
        related='patient_id.doctor_id',
        store=True
    )
    is_intern = fields.Boolean(compute="_compute_is_intern")
    diagnosis_id = fields.Many2one(
        comodel_name="hr.hospital.diagnosis",
        readonly=True
    )
    visit_date = fields.Datetime(string="Visit date and time")
    is_done = fields.Boolean()
    active = fields.Boolean(default=True)
    visit_end_time = fields.Datetime(
        string="Visit end time",
        compute='_compute_visit_end_time'
    )
    # For easier searching. Maybe wrong way
    visit_date_date = fields.Date(
        compute='_compute_visit_date_date',
        store=True, index=True
    )
    schedule_id = fields.Many2one(
        comodel_name="hr.hospital.doctor.schedule",
        ondelete="cascade",
    )

    @api.model
    def create(self, vals_list: dict) -> dict:
        self.is_valid_fields(vals_list)
        self.is_available_time(vals_list)
        vals_list['state'] = "created"
        vals_list['visit_date_date'] = vals_list.get('visit_date', "")
        vals_list['schedule_id'] = self._get_schedule_id(vals_list)
        if vals_list.get("is_done", "") and vals_list["diagnosis_id"]:
            vals_list['state'] = 'done'
        return super().create(vals_list)

    def unlink(self) -> bool:
        for rec in self:
            if rec.is_done:
                raise ValidationError(
                    _("You can't delete visits that already done!")
                )
        return super().unlink()

    def write(self, vals: dict) -> bool:
        is_done = vals.get('is_done', "")
        for rec in self:
            if vals.get('visit_date', ""):
                vals['patient_id'] = rec.id
                self.is_available_time(vals)
            if is_done:
                diagnosis = vals.get('diagnosis_id', "") or rec.diagnosis_id
                if not diagnosis:
                    _logger.error("Visit cant be done with out diagnosis")
                    raise ValidationError(_("Visit cant be done with out diagnosis"))
                vals['state'] = 'done'

            elif is_done and rec.active:
                _logger.error("You can't arch visits that already done!")
                raise ValidationError(_("You can't arch visits that already done!"))
        return super().write(vals)

    @api.onchange('visit_date')
    @api.depends('visit_date')
    def _compute_visit_date_date(self) -> None:
        for rec in self:
            if rec.visit_date:
                rec.visit_date_date = rec.visit_date.date()
            else:
                rec.visit_date_date = False

    @api.depends('doctor_id')
    def _compute_is_intern(self) -> None:
        for rec in self:
            rec.is_intern = rec.doctor_id.is_intern

    @api.onchange('visit_date')
    @api.depends('visit_date')
    def _compute_visit_end_time(self):
        for rec in self:
            if rec.visit_date:
                duration = const.VISIT_DURATION
                end = rec.visit_date + duration
                rec.visit_end_time = end
            else:
                rec.visit_end_time = None

    def name_get(self) -> list:
        return [
            (visit.id, f"[{visit.visit_date}, "
                       f"{visit.patient_id.name}]") for visit in self
        ]

    def add_diagnosis(self) -> dict:
        for rec in self:
            return {
                "type": "ir.actions.act_window",
                "name": _("Add Diagnosis"),
                "res_model": "hr.hospital.add.diagnosis.wizard",
                "target": "new",
                "views": [[False, "form"]],
                "view_mode": "form",
                'context': {
                    'default_doctor_id': rec.doctor_id.id,
                    'default_patient_id': rec.patient_id.id,
                    'default_is_intern': rec.is_intern,
                    'default_visit_id': rec.id,
                }
            }

    def is_available_time(self, vals_list: dict) -> bool:
        delta = const.delta
        visit_date = fields.Datetime.to_datetime(
            vals_list.get("visit_date"))
        doctor_id = self.get_patient_doctor_id(vals_list.get("patient_id"))
        schedules = self.env[
            'hr.hospital.doctor.schedule'
        ].search([
            ('doctor_id', '=', doctor_id),
            ('visit_date', '=', visit_date)
        ])
        if schedules:
            for schedule in schedules:
                work_start = schedule.start_time
                work_end = schedule.shift_end_time
                start = visit_date
                end = start + const.VISIT_DURATION
                if not work_start < (start or end) < work_end:
                    _logger.warning(_("Specified time out of schedule"))
                    raise ValidationError(
                        _(f"Specified time out "
                          f"of schedule. Choose another time!"
                          )
                    )
            visits = self.env[
                'hr.hospital.patient.visit'
            ].search([
                ('doctor_id', '=', doctor_id),
                ('visit_date_date', '=', visit_date)])
            if visits:
                for visit in visits:
                    visit_start = visit.visit_date
                    visit_end = const.VISIT_DURATION
                    start = visit_date + delta
                    end = start + const.VISIT_DURATION - delta
                    if start < (visit_start or visit_end) < end:
                        _logger.warning(_("Specified time out of schedule"))
                        raise ValidationError(
                            _("Specified time is busy!"
                              " Choose another time!"
                              )
                        )
            return True
        raise ValidationError(_("No schedule found!"))

    def change_visit_action(self) -> dict:
        record = {"type": "ir.actions.act_window",
                  "name": _("Change Visit Time"),
                  "res_model": "hr.hospital.change.visit.time.wizard",
                  "target": "new",
                  "views": [[False, "form"]],
                  "view_mode": "form",
                  'context': {
                      'default_old_time': self.visit_date
                  }}
        return record

    def _get_schedule_id(self, vals_list: dict) -> int:
        delta = const.delta
        visit_date = vals_list.get('visit_date')
        visit_time = fields.Datetime.to_datetime(visit_date) - delta
        doctor_id = self.get_patient_doctor_id(vals_list.get("patient_id"))
        schedules = self.env[
            'hr.hospital.doctor.schedule'
        ].search([
            ('doctor_id', '=', doctor_id),
            ('visit_date', '=', vals_list['visit_date_date']),
        ])
        for schedule in schedules:
            start = schedule.start_time
            end = schedule.shift_end_time.time()
            if start.time() <= visit_time.time() < end:
                return schedule.id
        raise ValidationError(
            _("No schedule found!")
        )

    def get_patient_doctor_id(self, patient_id: int) -> int:
        doctor_id = self.env[
            'hr.hospital.patient'
        ].browse(patient_id).doctor_id
        return doctor_id.id

    def is_valid_fields(self, vals_list: dict) -> bool:
        is_done = vals_list.get("is_done", "")
        diagnosis_id = vals_list.get("diagnosis_id", "")
        if is_done and not diagnosis_id:
            _logger.warning("Visit cant be done with out diagnosis")
            raise ValidationError(_("Visit cant be done with out diagnosis"))
        return True
