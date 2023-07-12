from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import Form
from odoo.addons.hr_hospital.tests.common import HospitalCommon


@tagged('post_install', '-at_install', 'library')
class TestForm(HospitalCommon):

    def test_book_taken_date(self):
        patient_form = Form(self.patient)

        patient_form.doctor_id = self.hospital_user.doctor_id
        self.assertEqual(patient_form.taken_date, fields.Date.today())

        patient_form.doctor_id = self.hospital_user.doctor_id
        self.assertEqual(patient_form.taken_date, fields.Date.today())
