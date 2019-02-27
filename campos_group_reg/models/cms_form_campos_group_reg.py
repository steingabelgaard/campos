from odoo import models, _


class cmsGroupRegForm(models.AbstractModel):
    """A test model form."""

    _name = 'cms.form.campos.group.reg'
    _inherit = 'cms.form'
    _form_model = 'campos.group.reg'
    _form_model_fields = ('name', 'street', 'street2', 'zip', 'city',
                          'country_id',
                          'contact_name', 'contact_street',
                          'contact_street2', 'contact_zip',
                          'contact_city',
                          'contact_country_id', 'contact_mobile',
                          'contact_email',
                          'security_partner_id',
                          'security_mobile',
                          'security_email',
                          'treasurer_name',
                          'treasurer_street',
                          'treasurer_street2',
                          'treasurer_zip',
                          'treasurer_city',
                          'treasurer_country_id',
                          'treasurer_mobile',
                          'treasurer_email',
                          'cars','busses','trailers','large_tents','large_constructions','ckr_ok',
                          'arrival_date1_id', 'arrival_time1', 'arrival_date2_id', 'arrival_time2', 'arrival_date3_id', 'arrival_time3', 
                          'departure_date1_id', 'departure_time1', 'departure_date2_id', 'departure_time2', 'departure_date3_id', 'departure_time3', 
                          'transport_form')
    _form_required_fields = ( 'name', #'arrival_date', 'departure_date', 
                             #'transport_form',
                             #'cars','busses','trailers'
                             )
    _form_fields_order = ('name', 'street', 'street2', 'zip', 'city',
                          'country_id',
                          'contact_name', 'contact_street',
                          'contact_street2', 'contact_zip',
                          'contact_city', 'contact_country_id',
                          'contact_mobile', 'contact_email',
                          'security_partner_id',
                          'security_mobile',
                          'security_email',
                          'treasurer_name', 'treasurer_street',
                          'treasurer_street2', 'treasurer_zip',
                          'treasurer_city', 'treasurer_country_id',
                          'treasurer_mobile', 'treasurer_email',
                          'cars','busses','trailers','large_tents','large_constructions','ckr_ok',
                          'arrival_date1_id', 'arrival_time1', 'arrival_date2_id', 'arrival_time2', 'arrival_date3_id', 'arrival_time3', 
                          'departure_date1_id', 'departure_time1', 'departure_date2_id', 'departure_time2', 'departure_date3_id', 'departure_time3', 
                          'transport_form'
                          )


    @property
    def _form_fieldsets(self):
        return [
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
                    'security_partner_id',
                    'security_mobile',
                    'security_email',
                ],
            },
            {
                'id': 'treasurer',
                'title': _('Treasurer'),
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
            {
                'id': 'final_reg',
                'title': _('Final Registration'),
                'fields': [
                    'cars','busses','trailers','large_tents','large_constructions','ckr_ok'
                ],
            },
            {
                'id': 'transport',
                'title': _('Arrival / Departure'),
                'fields': [
                    'arrival_date1_id', 'arrival_time1', 'arrival_date2_id', 'arrival_time2', 'arrival_date3_id', 'arrival_time3', 
                    'departure_date1_id', 'departure_time1', 'departure_date2_id', 'departure_time2', 'departure_date3_id', 'departure_time3', 
                    'transport_form',
                ],
            },
        ]

    _form_fieldsets_display = 'tabs'
        
        
    @property
    def form_msg_success_updated(self):
        return _('Scout Troop updated.')

    def form_next_url(self, main_object=None):
        if self.request.args.get('redirect'):
            # redirect overridden
            return self.request.args.get('redirect')
        return '/my/home'
