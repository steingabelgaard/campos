from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.tools import consteq
import datetime

import logging
_logger = logging.getLogger(__name__)


class PortalGroupReg(CustomerPortal):

    def _group_reg_check_access(self, ckr_id, access_token=None):
        ckr = request.env['partner.ckr.check'].browse([ckr_id])
        ckr_sudo = ckr.sudo()
        try:
            ckr.check_access_rights('read')
            ckr.check_access_rule('read')
        except AccessError:
            if not access_token or not consteq(ckr_sudo.access_token, access_token):
                raise
        return ckr_sudo
    
    
    @http.route(['/group-reg/add1'], type='http', auth="public", website=True)
    def portal_group_reg_add_1(self, **post):
        
        _logger.info("ADD1 %s", request.httprequest.method)

        countries = request.env['res.country'].search([])
        country_da_id = request.env.ref('base.dk').id
        values = {'group': {'country_id': country_da_id},
                  'contact': {},
                  'error': {},
                  'countries': countries,    
                  }
        
        error = {}        
        if request.httprequest.method == 'POST':
            for field_name in ["group_name", "group_country_id", "contact_name", "contact_email"]:
                if not post.get(field_name):
                    error[field_name] = 'Missing %s' % field_name
            email = post.get('contact_email', False)
            partner_sudo = request.env['res.partner'].sudo()
            if email and '@' in email:
                if partner_sudo.search([('email', '=ilike', email)]):
                    return request.render("campos_group_reg.group_add_email_exist", {'email': email})
            
            group_reg = None
            country_id = False
            lang = 'da_DK'
            if not error:    
                if post.get('group_country_id', False):
                    country_id =  int(post.get('group_country_id', False))
                    if country_id != country_da_id:
                        lang = 'en_US'
                contact = partner_sudo.create({'name': post.get('contact_name'),
                                               'email': post.get('contact_email'),
                                               'country_id': country_id,
                                               'lang': lang,
                                               'type': 'other',
                                               })
                
                group = partner_sudo.create({'name': post.get('group_name'),
                                             'scoutgroup': True,
                                             'country_id': country_id,
                                             'is_company': True,
                                             'lang': lang,
                                             })
                group_reg = request.env['campos.group.reg'].sudo().create({'partner_id': group.id,
                                                                           'contact_partner_id': contact.id})
                _logger.info('GROUP REG: %s', group_reg)

                scout_org_domain = []    
                if country_id == country_da_id:
                    scout_org_domain = [('country_id', '=', country_da_id)]
                else:
                    scout_org_domain = [('country_id', '!=', country_da_id)] 
                values = {'group': group,
                          'contact': contact,
                          'scout_orgs': request.env['campos.scout.org'].sudo().search(scout_org_domain),
                          'error': error,
                          'countries': countries,
                          'group_reg': group_reg,
                          }
    
            if group_reg:
                return request.render("campos_group_reg.group_add_2", values)
        
        
        
        return request.render("campos_group_reg.group_add_1", values)
    
    @http.route(['/group-reg/add2'], type='http', auth="public", website=True)
    def portal_group_reg_add_2(self, **post):
        
        _logger.info("ADD2")
        countries = request.env['res.country'].search([])
        country_da_id = request.env.ref('base.dk').id
        values = {'group': {'country_id': country_da_id},
                  'contact': {},
                  'error': {},
                  'countries': countries,    
                  }
        error = {}        
        if request.httprequest.method == 'POST':
            group_reg_id = post.get('group_reg_id')
            if group_reg_id:
                group_reg = request.env['campos.group.reg'].sudo().search([('id', '=', group_reg_id)])
                if group_reg:
                    group = {}
                    for f in ['street', 'street2', 'zip', 'city']:
                        if post.get('group_' + f):
                            group[f] = post.get('group_' + f)
                    if group:
                        group_reg.partner_id.write(group)
                        values['group'] = group_reg.partner_id
                    contact = {}
                    for f in ['street', 'street2', 'zip', 'city', 'country_id', 'mobile']:
                        if post.get('contact_' + f):
                            contact[f] = post.get('contact_' + f)
                    if contact:
                        contact['parent_id'] = group_reg.partner_id.id
                        group_reg.contact_partner_id.write(contact)
                        values['contact'] = group_reg.contact_partner_id
                    if post.get('group_scout_org_id', False):
                        group_reg.scout_org_id = post.get('group_scout_org_id', False) 
                    
                    if post.get('same_as_contact', False) == 'reuse':
                        group_reg.treasurer_partner_id = group_reg.contact_partner_id
                    else:    
                        treasurer = {}
                        tres_vals = {}
                        for f in ['name', 'street', 'street2', 'zip', 'city', 'country_id', 'email', 'mobile']:
                            if post.get('treasurer_' + f):
                                treasurer[f] = post.get('treasurer_' + f)
                                tres_vals[f] = treasurer[f] 
                        if treasurer:
                            if not group_reg.treasurer_partner_id:
                                lang = 'da_DK'
                                if treasurer['country_id'] != country_da_id:
                                    lang = 'en_US'
                                treasurer['lang'] = lang
                                treasurer['type'] = 'invoice'
                                treasurer['parent_id'] = group_reg.partner_id.id
                                group_reg.treasurer_partner_id = request.env['res.partner'].sudo().create(treasurer)
                            else:
                                group_reg.treasurer_partner_id.write(treasurer)
                            for f in ['name', 'street', 'zip', 'city', 'country_id', 'email', 'mobile']:
                                if not post.get('treasurer_' + f):
                                    request.website.add_status_message(_('Missing required field: %s') % f, type_='danger')
                                    values['treasurer'] = tres_vals
                                    values['group_reg'] = group_reg
                                    return request.render("campos_group_reg.group_add_3", values)
                                    
                                    
                                
                    if post.get('group_scout_org_id', False):
                        group_reg.scout_org_id = post.get('group_scout_org_id', False)     
                    values['group_reg'] = group_reg
                    
                    if not group_reg.treasurer_partner_id:
                        values['treasurer'] = {'country_id': group_reg.country_id.id}
                        return request.render("campos_group_reg.group_add_3", values)
                    
                    group_reg.action_registrered()
                    group_reg.write({'prereg_ids': group_reg._default_prereg_ids()})    
                    values['group_reg'] = group_reg
                    
                    periods = request.env['campos.camp.period'].sudo().search([])
                    agegroups = request.env['campos.age.group'].sudo().search([])
                    cell = {}
                    for ag in agegroups:
                        cell[ag.id] = {}
                        for p in periods:
                            cell[ag.id][p.id] = 0
                    for c in group_reg.prereg_ids:
                        cell[c.age_group_id.id][c.period_id.id] = c.value
                    
                    
                    
                    values['periods'] = periods
                    values['agegroups'] = agegroups
                    values['cell'] = cell
                    
                    return request.render("campos_group_reg.group_pre_reg", values)
        
        return request.render("campos_group_reg.group_add_1", values)
    
    @http.route(['/group-reg/pre-reg'], type='http', auth="public", website=True)
    
    def portal_group_reg_pre_reg(self, **post):
        _logger.info("pre-reg")
        
        if request.httprequest.method == 'POST':
            group_reg_id = post.get('group_reg_id')
            if group_reg_id:
                group_reg = request.env['campos.group.reg'].sudo().search([('id', '=', group_reg_id)])
                if group_reg:
                    for c in group_reg.prereg_ids:
                        c.value = post.get('cell_%s_%s' % (c.age_group_id.id, c.period_id.id), False)
                    group_reg.action_pre_reg()
                                           
        return request.render("campos_group_reg.thank_you", {})                  
    
    @http.route(['/my/pre_reg'], type='http', auth="user", website=True)
    def portal_my_pre_reg(self, **post):
        _logger.info('MY Prereg')
        partner = request.env.user.partner_id
        _logger.info('My Partner: %s', partner)
        if partner.parent_id.scoutgroup:
            if request.httprequest.method == 'POST':
                group_reg_id = post.get('group_reg_id')
                if group_reg_id:
                    group_reg = request.env['campos.group.reg'].sudo().search([('id', '=', group_reg_id)])
                    if group_reg:
                        for c in group_reg.prereg_ids:
                            c.value = post.get('cell_%s_%s' % (c.age_group_id.id, c.period_id.id), False)
                if request.website:
                    request.website.add_status_message(_('Pre registration figures has been updated.'))
                return request.redirect('/my')
            
            group_reg = request.env['campos.group.reg'].sudo().search([('partner_id', '=', partner.parent_id.id)])
            _logger.info('My group: %s', group_reg)
            values = {}
            values['group_reg'] = group_reg
                    
            periods = request.env['campos.camp.period'].sudo().search([])
            agegroups = request.env['campos.age.group'].sudo().search([])
            cell = {}
            for ag in agegroups:
                cell[ag.id] = {}
                for p in periods:
                    cell[ag.id][p.id] = 0
            for c in group_reg.prereg_ids:
                cell[c.age_group_id.id][c.period_id.id] = c.value
            
            
            
            values['periods'] = periods
            values['agegroups'] = agegroups
            values['cell'] = cell
            
            return request.render("campos_group_reg.group_pre_reg_edit", values)
        return request.redirect('/my')
    
    @http.route(['/my/group_reg'], type='http', auth="user", website=True)
    def portal_my_group_reg(self):
        partner = request.env.user.partner_id
        if partner.parent_id.scoutgroup:
            group_reg = request.env['campos.group.reg'].sudo().search([('partner_id', '=', partner.parent_id.id)])
            return request.redirect('/group_reg/%d/edit' % (group_reg.id))
        return request.redirect('/my')    

        
                         
                              
    @http.route(['/my/ckr/submit/<int:ckr_id>/<access_token>/'], type='http', auth="public", methods=['POST'], website=True)
    def portal_my_ckr_submit(self, ckr_id, access_token, **kw):
        _logger.info('SUBMIT')
        try:
            ckr_sudo = self._ckr_check_access(ckr_id, access_token)
        except AccessError:
            return request.redirect('/my')

        error = {}        
        if request.httprequest.method == 'POST':
            # Validate post vars
            birthdate = request.params.get('birthdate')
            try:
                datetime.datetime.strptime(birthdate, '%Y-%m-%d')
            except ValueError:
                error['birthdate'] = _('Invalid birth date')
            cpr = request.params.get('cpr')
            try:
                int(cpr)
                if len(cpr) != 4:
                    raise ValueError
            except ValueError:
                error['cpr'] = _('CPR must be 4 digits')

            if not error:
        
                ckr_sudo.write({'cpr': cpr,
                                'birthdate': birthdate})
                ckr_sudo.action_confirm()
                values = {}
                _logger.info('THANK YOU')
                return request.render("partner_ckr.thank_you", values)
            
        values = {'ckr': ckr_sudo,
                  'error': {},
                  'access_token': access_token}
        
        return request.render("partner_ckr.cpr_fetch", values)
        
        