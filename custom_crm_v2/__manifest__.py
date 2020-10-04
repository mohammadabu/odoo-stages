# -*- coding: utf-8 -*-
{
    'name': "custom-crm-v2",
    'author': "Mohammad abusubhia",
    'version': '1.2',
    'depends': ['base','crm','mail','hr'],
    # always loaded
    'data': [
        'views/custom_lead_views.xml',
        'data/cron.xml',
        'data/mail_template.xml',
        'security/security.xml',
    ],
}