from odoo import models, fields, _


class cmsParticipantForm(models.AbstractModel):
    """A test model form."""

    _name = 'cms.form.campos.participant'
    _inherit = 'cms.form'
    _form_model = 'campos.participant'
    _form_model_fields = ('name', 'street', 'street2', 'zip', 'city',
                           'country_id',
                           'gender', 'birthdate_date',
                           'arrival_date_id',
                           'depature_date_id',
                           )
    _form_required_fields = ('name', 'gender', 'birthdate_date',
                          'arrival_date_id',
                          'depature_date_id',)
    _form_fields_order = ('name', 'street', 'street2', 'zip', 'city',
                          'country_id', 'gender', 'birthdate_date',
                          'arrival_date_id',
                          'depature_date_id',
                          )
    
    participan_state = fields.Selection([('confirmed', 'Participate'),
                                          ('cancelled', 'Cancelled')], string="State", default='confirmed')

    def form_after_create_or_update(self, values, extra_values):
        if extra_values.get('notify_partner'):
            values['state'] = extra_values.get('notify_partner') 
    
    def form_load_defaults(self, main_object=None, request_values=None):
        defaults = super(cmsParticipantForm, self).form_load_defaults(
            main_object=main_object, request_values=request_values
        )
        defaults['birthdate_date'] = False
        return defaults
    
    @property
    def form_msg_success_updated(self):
        return _('Participant updated.')
    
    @property
    def form_msg_success_created(self):
        # TODO: include form model name if any
        msg = _('Participant added.')
        return msg

    def form_next_url(self, main_object=None):
        if self.request.args.get('redirect'):
            # redirect overridden
            return self.request.args.get('redirect')
        return '/participants'
    

class cmsParticipantSearchForm(models.AbstractModel):
    """A test model form."""

    _name = 'cms.search.campos.participant'
    _inherit = 'cms.form.search'
    _form_model = 'campos.participant'
    
    _form_model_fields = ('name')
    
    
    form_buttons_template = 'campos_group_reg.participant_search_form_buttons'
    form_search_results_template = 'campos_group_reg.participant_search_results'
    
    