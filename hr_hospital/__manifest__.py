{
    'name': 'Hospital',
    'version': '16.0.2.0.0',
    'category': 'Customization',
    'summary': 'Maintaining records of doctors and patients',

    'author': 'Ostapets Sergii',
    'website': 'https://t.me/ostapec_serg',

    'depends': [
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/disease_data.xml',
        'views/hr_hospital_menus.xml',
        'wizard/create_appointment.xml',
        'wizard/add_diagnosis.xml',
        'wizard/change_doctor.xml',
        'wizard/change_visit_time.xml',
        'wizard/hospital_report.xml',
        'wizard/week_schedule.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/disease_views.xml',
        'views/disease_category_views.xml',
        'views/patient_visit_views.xml',
        'views/contact_person_views.xml',
        'views/diagnosis_views.xml',
        'views/doctor_schedule_views.xml',
        'views/hr_history_changing_doctor.xml',
    ],

    'demo': [
        'data/hr_hospital_demo.xml',
    ],

    'images': [
        'static/description/icon.png',
    ],

    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
