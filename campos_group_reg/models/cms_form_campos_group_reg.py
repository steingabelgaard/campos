from odoo import models


class cmsGroupRegForm(models.AbstractModel):
        """A test model form."""

        _name = 'cms.form.campos.group.reg'
        _inherit = 'cms.form'
        _form_model = 'campos.group.reg.wiz'
        _form_model_fields = ('name', 'street', 'street2', 'zip', 'city',
                              'country_id',
                              'contact_name', 'contact_street',
                              'contact_street2', 'contact_zip',
                              'contact_city',
                              'contact_country_id', 'contact_mobile',
                              'contact_email',
                              'treasurer_name',
                              'treasurer_street',
                              'treasurer_street2',
                              'treasurer_zip',
                              'treasurer_city',
                              'treasurer_country_id',
                              'treasurer_mobile',
                              'treasurer_email')
        _form_required_fields = ('name',)
        _form_fields_order = ('name', 'street', 'street2', 'zip', 'city',
                              'country_id',
                              'contact_name', 'contact_street',
                              'contact_street2', 'contact_zip',
                              'contact_city', 'contact_country_id',
                              'contact_mobile', 'contact_email',
                              'treasurer_name', 'treasurer_street',
                              'treasurer_street2', 'treasurer_zip',
                              'treasurer_city', 'treasurer_country_id',
                              'treasurer_mobile', 'treasurer_email')

        _form_fieldsets = [
            {
                'id': 'group',
                'title': 'Group',
                'fields': [
                    'name',
                    'street',
                    'street2',
                    'zip',
                    'city',
                    'country_id',
                ],
            },
            {
                'id': 'contact',
                'title': 'Contact',
                'fields': [
                    'contact_name',
                    'contact_street',
                    'contact_street2',
                    'contact_zip',
                    'contact_city',
                    'contact_country_id',
                    'contact_mobile',
                    'contact_email',
                ],
            },
            {
                'id': 'treasurer',
                'title': 'Treasurer',
                'fields': [
                    'treasurer_name',
                    'treasurer_street',
                    'treasurer_street2',
                    'treasurer_zip',
                    'treasurer_city',
                    'treasurer_country_id',
                    'treasurer_mobile',
                    'treasurer_email',
                ],
            },
        ]

        _form_fieldsets_display = 'tabs'
