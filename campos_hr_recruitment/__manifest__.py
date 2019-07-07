# -*- coding: utf-8 -*-
# Copyright 2018 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Campos Hr Recruitment',
    'description': """
        CampOS HR Recruitment modifications""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Stein & Gabelgaard ApS',
    'website': 'www.steingabelgaard.dk',
    'depends': [
        'website_hr_recruitment',
        'campos_group_reg',
        ],
    'data': [
        #'views/res_company.xml',
        'views/hr_employee.xml',
        'templates/recruitment_template.xml',
        'report/hr_employee_badge.xml'
        ],
    'demo': [],
}
