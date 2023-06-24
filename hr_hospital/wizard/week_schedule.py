from datetime import timedelta

from odoo import fields, models


class HrHospitalWeekScheduleWizard(models.TransientModel):
    _name = 'hr.hospital.week.schedule.wizard'
    _description = 'Create Week Schedule'

    week_start_date = fields.Date(required=True)
    work_day_start = fields.Datetime(required=True)
    doctor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        required=True,
        ondelete="cascade"
    )
    is_even_or_odd = fields.Selection(
        selection=[("even", "Even"), ("odd", "Odd")],
        string="Even or Odd",
        help="For even or odd days"
    )

    def add_schedule(self):
        self.ensure_one()
        week_start_date = fields.Date.to_date(self.week_start_date)
        delta = timedelta(days=1)
        if self.is_even_or_odd == 'even':
            for _ in range(0, 7):
                if week_start_date.day % 2 == 0:
                    params = {
                        "visit_date": week_start_date,
                        "day_week": week_start_date.strftime('%A'),
                        "start_time": self.work_day_start,
                        "doctor_id": self.doctor_id.id,
                    }
                    self._create_schedule(params)
                week_start_date = week_start_date + delta
        elif self.is_even_or_odd == 'odd':
            for _ in range(0, 7):
                if week_start_date.day % 2 != 0:
                    params = {
                        "visit_date": week_start_date,
                        "day_week": week_start_date.strftime('%A'),
                        "start_time": self.work_day_start,
                        "doctor_id": self.doctor_id.id,
                    }
                    self._create_schedule(params)
                week_start_date = week_start_date + delta
        else:
            for _ in range(0, 7):
                params = {
                    "visit_date": week_start_date,
                    "day_week": week_start_date.strftime('%A'),
                    "start_time": self.work_day_start,
                    "doctor_id": self.doctor_id.id,
                }
                self._create_schedule(params)
                week_start_date = week_start_date + delta
        raise

    def _create_schedule(self, params: dict):
        self.env['hr.hospital.doctor.schedule'].create({
            "visit_date": params["visit_date"],
            "day_week": params["day_week"],
            "start_time": params['start_time'],
            "doctor_id": params['doctor_id'],
        })

    # TODO Add doctor schedule checking
    # TODO Add auto fill date to field 'work_day_start'
