# -*- coding: utf-8 -*-
{
    'name': "custom-pipeline-v1",
    'author': "Mohammad abusubhia",
    'version': '0.2',
    'depends': ['base','crm','mail'],
    # always loaded
    'data': [
        'views/custom_pipeline_view.xml',
        'security/security.xml',
    ],
}