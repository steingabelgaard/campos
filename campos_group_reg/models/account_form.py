# -*- coding: utf-8 -*-
# Copyright 2018 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models

class AccountForm(models.AbstractModel):
    """Partner account form."""

    _inherit = 'cms.form.my.account'
    _form_model = 'res.partner'
    _form_model_fields = (
        'name',
        'street',
        'street2',
        'zip',
        'city',
        'country_id',
        'mobile',
        'email',
    )
    _form_fields_order = _form_model_fields
    _form_required_fields = (
        "name", "street", "zip", "city",
        "country_id", "mobile", "email"
    )
