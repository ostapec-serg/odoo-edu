from odoo.tests.common import TransactionCase


class HospitalCommon(TransactionCase):

    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        """
        super(HospitalCommon, self).setUp()
        self.group_hospital_user = self.env.ref(
            'hr_hospital.group_hospital_user')
        self.group_hospital_admin = self.env.ref(
            'hr_hospital.group_hospital_admin')
        self.library_user = self.env['res.users'].create({
            'name': 'Hospital User',
            'login': 'Hospital_user',
            'groups_id': [(4, self.env.ref('base.group_user').id),
                          (4, self.group_hospital_user.id)],
        })
        self.hospital_admin = self.env['res.users'].create({
            'name': 'Hospital Admin',
            'login': 'Hospital_admin',
            'groups_id': [(4, self.env.ref('base.group_user').id),
                          (4, self.group_hospital_admin.id)],
        })

        self.doctor = self.env['hr.hospital.doctor'].create(
            {
                'name': 'Demo Doctor'
            }
        )
        self.patient = self.env['hr.hospital.patient'].create(
            {
                'name': 'Demo Patient'
            }
        )

