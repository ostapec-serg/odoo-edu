{
    'name': 'Hospital',
    'version': '16.0.1.0.0',
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
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/disease_views.xml',
        'views/patient_visit_views.xml',
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
