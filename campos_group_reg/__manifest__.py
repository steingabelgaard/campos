# -*- coding: utf-8 -*-
# Copyright 2018 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'CampOS Group Registration',
    'description': """
        Manage Scout Camps""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Stein & Gabelgaard ApS',
    'website': 'www.steingabelgaard.dk',
    'depends': [
        'mail',
        'portal',
        'partner_municipality',
        'web_widget_x2many_2d_matrix',
        'cms_form',
    ],
    'data': [
        
        #'views/res_partner.xml',
        #'wizards/campos_group_reg_wiz.xml',
        'security/campos_group_reg.xml',
        'views/campos_group_reg.xml',
        'security/campos_prereg_age_period.xml',
        'views/campos_prereg_age_period.xml',
        'security/campos_camp_period.xml',
        'views/campos_camp_period.xml',
        'security/campos_age_group.xml',
        'views/campos_age_group.xml',
        'security/campos_scout_org.xml',
        'views/campos_scout_org.xml',
        'data/campos.scout.org.csv',
        'templates/website_group_add.xml',

    ],
    'demo': [
        'demo/campos_prereg_age_period.xml',
        'demo/campos_camp_period.xml',
        'demo/campos_age_group.xml',
        'demo/campos_group_reg.xml',
    ],
}
