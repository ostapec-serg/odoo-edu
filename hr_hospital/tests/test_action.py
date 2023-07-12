from odoo.addons.hr_hospital.tests.common import HospitalCommon
from odoo.tests import tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install', 'library')
class TestAccessRights(HospitalCommon):

    def test_action_take_in(self):
        self.patient.write({'doctor_id': self.hospital_user.doctor_id.id})

        # A library user can't return a book himself
        with self.assertRaises(UserError):
            self.book_demo.with_user(self.library_user).action_take_in()

        # A library admin can return a book
        self.book_demo.with_user(self.library_admin).action_take_in()
        self.assertFalse(self.book_demo.reader_id)
