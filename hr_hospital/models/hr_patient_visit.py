import logging

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

# Is this good practice?
from .hr_hospital import constants as const


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
    )
    is_intern = fields.Boolean(compute="_compute_is_intern")
    diagnosis_id = fields.Many2one(
        comodel_name="hr.hospital.diagnosis",
        readonly=True
    )
    visit_date = fields.Datetime(string="Visit date and time")
    is_done = fields.Boolean()
    active = fields.Boolean(default=True)

    # For easier searching. Maybe wrong way
    visit_date_date = fields.Date(
        compute='_compute_visit_date_date',
        store=True, index=True
    )

    @api.model
    def create(self, vals_list: dict) -> dict:
        is_done = vals_list.get("is_done", "")
        diagnosis_id = vals_list.get("diagnosis_id", "")
        vals_list['visit_date_date'] = vals_list.get('visit_date', "")
        if is_done and diagnosis_id:
            vals_list['state'] = const.STATE_LIST['2'][1]
        elif is_done and not diagnosis_id:
            _logger.warning("Visit cant be done with out diagnosis")
            raise UserError(_("Visit cant be done with out diagnosis"))
        self.is_available_time(vals_list)
        return super().create(vals_list)

    def unlink(self) -> bool:
        for rec in self:
            if rec.is_done:
                raise UserError(
                    _("You can't delete visits that already done!")
                )
        return super().unlink()

    def write(self, vals: dict) -> bool:
        is_done = vals.get('is_done', "")
        for rec in self:
            if vals.get('visit_date', ""):
                vals['patient_id'] = rec.id
                self.is_available_time(vals)

            #  need to remove
            if not rec.visit_date_date:
                vals['visit_date_date'] = rec.visit_date.date()

            if is_done:
                diagnosis = vals.get('diagnosis_id', "") or rec.diagnosis_id
                if not diagnosis:
                    _logger.error("Visit cant be done with out diagnosis")
                    raise UserError(_("Visit cant be done with out diagnosis"))
                vals['state'] = 'done'

            elif is_done and rec.active:
                _logger.error("You can't arch visits that already done!")
                raise UserError(_("You can't arch visits that already done!"))
        return super().write(vals)

    def _compute_is_intern(self) -> None:
        for rec in self:
            rec.is_intern = rec.doctor_id.is_intern

    def name_get(self) -> list:
        return [
            (visit.id, f"[{visit.visit_date}, "
                       f"{visit.patient_id.name}]") for visit in self
        ]

    def add_diagnosis(self) -> dict:
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Add Diagnosis"),
            "res_model": "hr.hospital.add.diagnosis.wizard",
            "target": "new",
            "views": [[False, "form"]],
            "view_mode": "form",
            'context': {
                'default_doctor_id': self.doctor_id.id,
                'default_patient_id': self.patient_id.id,
                'default_is_intern':  self.is_intern,
                'default_visit_id':  self.id,
            }
        }

    def is_available_time(self, vals_list: dict) -> bool:
        delta = const.delta
        visit_date = fields.Datetime.to_datetime(
            vals_list.get("visit_date"))

        doctor_id = self.env[
            'hr.hospital.patient'
        ].browse(vals_list.get("patient_id")).doctor_id
        schedules = self.env[
            'hr.hospital.doctor.schedule'
        ].search([
            ('doctor_id', '=', doctor_id.id),
            ('visit_date', '=', visit_date)
        ])
        if schedules:
            for schedule in schedules:
                work_start = schedule.start_time
                work_end = work_start + const.WORK_DAY_DURATION
                start = visit_date
                end = start + const.VISIT_DURATION
                if not work_start < (start or end) < work_end:
                    _logger.warning(_("Specified time out of schedule"))
                    raise ValidationError(
                        _(f"Specified time out "
                          f"of schedule of doctor {doctor_id.name} "
                          f" Choose another time!"
                          )
                    )
            visits = self.env[
                'hr.hospital.patient.visit'
                ].search([
                    ('doctor_id', '=', doctor_id.id),
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
        raise ValidationError(
            _(f"Doctor {doctor_id.name} dont work on {visit_date.date()}"
              f" Choose another day!"
              )
        )

    @api.onchange('visit_date')
    @api.depends('visit_date')
    def _compute_visit_date_date(self):
        for rec in self:
            if rec.visit_date:
                rec.visit_date_date = rec.visit_date.date()
            else:
                rec.visit_date_date = False

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
