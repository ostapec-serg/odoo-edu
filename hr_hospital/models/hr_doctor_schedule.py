from datetime import datetime, time

from odoo import fields, models, api


class HrHospitalDoctorSchedule(models.Model):
    _name = 'hr.hospital.doctor.schedule'
    _description = 'Doctor Schedule'
    _order = "visit_date"

    visit_date = fields.Date(
        required=True,
        string="Work day"
    )
    day_week = fields.Char(
        string="Day of the week",
        compute="_compute_day_week",
    )
    start_time = fields.Datetime()
    doctor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        ondelete="cascade"
    )

    @api.onchange('visit_date', 'start_time')
    @api.depends('visit_date', 'start_time')
    def _compute_day_week(self):
        # TODO re-write method
        """
        """
        if self.visit_date:
            day_week = self.visit_date.strftime('%A')
            self.day_week = day_week
            if not self.start_time:
                start_time = datetime.combine(
                    self.visit_date, time(0, 0)
                )
                self.start_time = start_time
            elif self.start_time:
                self.start_time = datetime.combine(
                    self.visit_date, self.start_time.time()
                )
        else:
            self.day_week = None
