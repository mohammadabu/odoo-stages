# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions
from odoo.tools.translate import _
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
# from odoo.exceptions import UserError, AccessError
# from odoo .exceptions import ValidationError
class NewModule(models.Model):
    _inherit = 'crm.lead'
    opportunity_name = fields.Text(string="Opportunity Name")
    materials_supply = fields.Selection(
        [
            ('yes','yes'),
            ('no','no')
        ],
        string="Materials Supply",
        track_visibility=1
    )
    materials_supply_text = fields.Text(string='materials supply text',track_visibility=1)
    services_supply = fields.Selection(
        [
            ('yes','yes'),
            ('no','no')
        ],
        string="3rd party Services Supply",
        track_visibility=1
    )
    services_supply_text = fields.Text(string='services_supply text',track_visibility=1)
    house_required = fields.Selection(
        [
            ('yes','yes'),
            ('no','no')
        ],
        string="In House PS Required",
        track_visibility=1
    )
    house_required_text = fields.Text(string='house required text',track_visibility=1)
    outsourcing_required = fields.Selection(
        [
            ('yes','yes'),
            ('no','no')
        ],
        string="Outsourcing Required",
        track_visibility=1
    )
    outsourcing_required_text = fields.Text(string='outsourcing required text',track_visibility=1)
    ms_sla_required = fields.Selection(
        [
            ('yes','yes'),
            ('no','no')
        ],
        string="MS/SLA Required",
        track_visibility=1
    )
    ms_sla_required_text = fields.Text(string='ms_sla_required text',track_visibility=1)
    driven_by = fields.Many2one(
        'res.users',
        'Driven by',
        track_visibility=1
    )
    account_manager = fields.Many2one(
        'res.users',
        'Account manager',
        track_visibility=1
    )
    status = fields.Selection(
        [
            ('open','open'),
            ('won','won'),
            ('lost','lost'),
            ('on_hold','on hold')
        ],
        string="Status",
        default='open',
        track_visibility=1
    )
    # on_hold_status  = fields.Many2one(
    #     'crm.onhold.reason',
    #     'On Hold Reason',
    #     track_visibility=1
    # )
    on_hold_status = fields.Text(string='On Hold Reason',track_visibility=1)
    # lost_reason = fields.Many2one(
    #     'crm.lost.reason',
    #     'Lost Reason',
    #     track_visibility=1
    # )
    lost_reason_new = fields.Text(string='Lost Reason',track_visibility=1)

    folder_link = fields.Char(string='folder link',track_visibility=1)
    scope_work = fields.Char(string='Scope of Work - High level SoW',track_visibility=1)
    user_name = fields.Many2many('res.users','name')
    stage_name = fields.Char(string='Stage Name',compute="set_stage_name")
    activity = fields.Text(string='activity')
    opportunity_esc_date = fields.Datetime(string='opportunity_esc_date',default=datetime.now())
    opportunity_esc_send_email = fields.Boolean()
    users_email = fields.Char(string='User Email')
    # all_user_is_presalse_eng = fields.Text(string='all_user_is_presalse_eng')

    @api.model
    def _getUserGroupId(self):
        all_emails = []
        all_ispresales_eng_position = self.env['hr.job'].search([('is_presales_eng','=',True)])
        for default_ispre in all_ispresales_eng_position:
            all_employee_pre = self.env['hr.employee'].search([('job_id','=',default_ispre.id)])
            for employee_pre in all_employee_pre:
                if employee_pre.user_id != False:
                    user_email_pre = self.env['res.users'].search([('id','=',employee_pre.user_id.id)])
                    if user_email_pre.login != False:
                        all_emails.append(user_email_pre.id)
        return [('id', 'in', all_emails)]
    username_ids = fields.Many2many('res.users','id',track_visibility=1,domain=_getUserGroupId)
    # @api.onchange('user_name')
    # def onchange_user_name_value(self):
    #     self.partner_id.message_post(body="Create Users",subject="ssss")
    
    @api.model
    def custom_default_group(self):
        all_emails_default_pos = ""
        all_emails_pre_sales_eng = ""
        all_stages = self.env['crm.stage'].search([])
        #get default position
        all_default_position = self.env['hr.job'].search([('default_groub_crm','=',True)])
        for default_position in all_default_position:
            all_employee = self.env['hr.employee'].search([('job_id','=',default_position.id)])
            for employee in all_employee:
                if employee.user_id != False:
                    user_email = self.env['res.users'].search([('id','=',employee.user_id.id)])
                    if user_email.login != False:
                        if all_emails_default_pos != False:
                            if ("#"+str(user_email.id)+"#") not in all_emails_default_pos:
                                all_emails_default_pos = all_emails_default_pos + ("#"+str(user_email.id)+"#")
                        else:
                            all_emails_default_pos = ("#"+str(user_email.id)+"#")
        #get default presales eng
        # all_ispresales_eng_position = self.env['hr.job'].search([('is_presales_eng','=',True)])
        # for default_ispre in all_ispresales_eng_position:
        #     all_employee_pre = self.env['hr.employee'].search([('job_id','=',default_ispre.id)])
        #     for employee_pre in all_employee_pre:
        #         if employee_pre.user_id != False:
        #             user_email_pre = self.env['res.users'].search([('id','=',employee_pre.user_id.id)])
        #             if user_email_pre.login != False:
        #                 if all_emails_pre_sales_eng != False and all_emails_pre_sales_eng != "":
        #                     if (user_email_pre.login not in all_emails_pre_sales_eng):
        #                         all_emails_pre_sales_eng = all_emails_pre_sales_eng +","+ user_email_pre.login
        #                 else:
        #                     all_emails_pre_sales_eng = user_email_pre.login 
                                    
        for stage in all_stages:
            all_emails_default_stage = False
            all_emails_default_opp = False
            all_emails_default_presales_eng = False
            #get default pos stage 
            all_access_group = stage.access_group
            for access_group in all_access_group:    
                all_employee_stage = self.env['hr.employee'].search([('job_id','=',access_group.id)])
                for employee_stage in all_employee_stage:
                    if employee_stage.user_id != False:
                        user_email_stage = self.env['res.users'].search([('id','=',employee_stage.user_id.id)])
                        if user_email_stage.login != False:
                            if all_emails_default_stage != False:
                                if ("#"+str(employee_stage.user_id.id)+"#") not in all_emails_default_stage:
                                    all_emails_default_stage =  all_emails_default_stage+"#"+str(employee_stage.user_id.id)+"#"
                            else:
                                all_emails_default_stage = "#"+str(employee_stage.user_id.id)+"#"
            
            #get owner and owner manager
            all_opportunity = self.env['crm.lead'].search([('stage_id','=',stage.id)])
            # print(stage.name)
            # print(all_opportunity)
            for opportunity in all_opportunity:
                if opportunity.user_id != False:
                    user_owner_email = self.env['res.users'].search([('id','=',opportunity.user_id.id)])      
                    user_owner_manager_info = self.env['hr.employee'].search([('user_id','=',opportunity.user_id.id)])
                    # get owner
                    if user_owner_email.login != False:
                        if all_emails_default_opp != False:
                            if ("#"+str(user_owner_email.id)+"#") not in all_emails_default_opp:
                                all_emails_default_opp = all_emails_default_opp + "#"+str(user_owner_email.id)+"#"
                        else:
                            all_emails_default_opp = "#"+str(user_owner_email.id)+"#"
                    # get owner manager
                    if user_owner_manager_info.parent_id != False:
                        employee_manager = self.env['hr.employee'].search([('id','=',user_owner_manager_info.parent_id.id)])
                        if employee_manager.user_id != False:
                            user_owner_manager_email = self.env['res.users'].search([('id','=',employee_manager.user_id.id)])
                            if user_owner_manager_email.login != False:
                                if all_emails_default_opp != False:
                                    if ("#"+str(user_owner_manager_email.id)+"#") not in all_emails_default_opp:
                                        all_emails_default_opp = all_emails_default_opp + "#"+str(user_owner_manager_email.id)+"#"
                                else:
                                    all_emails_default_opp = "#"+str(user_owner_manager_email.id)+"#"
                opportunity.all_user_is_presalse_eng = all_emails_pre_sales_eng
            
            # get presales eng if stage = presales
            if stage.name == "Presales":
                all_opportunity = self.env['crm.lead'].search([('stage_id','=',stage.id)])
                for opportunity in all_opportunity:
                    presales_eng = opportunity.username_ids
                    for pre_eng in presales_eng:
                        user_presales_email = self.env['res.users'].search([('id','=',pre_eng.id)])        
                        if user_presales_email.login != False:
                            if all_emails_default_presales_eng != False:
                                if ("#"+str(user_presales_email.id)+"#") not in all_emails_default_presales_eng:
                                    all_emails_default_presales_eng = all_emails_default_presales_eng + ("#"+str(user_presales_email.id)+"#")
                            else:
                                all_emails_default_presales_eng = ("#"+str(user_presales_email.id)+"#")   

            
            stage.all_user_emails_from_stage = all_emails_default_stage
            stage.all_user_emails = all_emails_default_pos                    
            stage.all_user_emails_from_opper = all_emails_default_opp
            stage.all_user_emails_from_presales = all_emails_default_presales_eng
            stage.all_user_is_presalse_eng = all_emails_pre_sales_eng
    @api.model
    def escalation_opportunity(self):
        job_positions = self.env['hr.job'].search([('default_esc_crm','=',True)])
        opportunity = self.env['crm.lead'].search([])
        for opp in opportunity:
            if opp.opportunity_esc_send_email != True:
                date_now = datetime.today()
                opp_stage = opp.stage_name
                arrivalـtime = opp.opportunity_esc_date
                stage_info = self.env['crm.stage'].search([('name','=',opp_stage)])
                # all_esc_groub = stage_info.escalation_group
                # print('----------------------')
                # print(stage_info.name)
                # print(all_esc_groub)
                escalation_after = stage_info.escalation_after
                if escalation_after > 0:
                    arrivalـtime = arrivalـtime + timedelta(minutes=escalation_after)
                    if date_now >= arrivalـtime :
                        # get all default esc
                        all_user_emails = False
                        for pos in job_positions:
                            employee = self.env['hr.employee'].search([('job_id','=',pos.id)])
                            for emp in employee:
                                if emp.user_id != False:
                                    user_email = self.env['res.users'].search([('id','=',emp.user_id.id)])
                                    if user_email.login != False:
                                        if all_user_emails != False:
                                            if user_email.login not in all_user_emails:
                                                all_user_emails = all_user_emails + "," + user_email.login
                                        else:
                                            all_user_emails = user_email.login
                        # get all position esc      
                        all_esc_groub = stage_info.escalation_group
                        for esc_groub in all_esc_groub:
                            employee_esc = self.env['hr.employee'].search([('job_id','=',esc_groub.id)])               
                            for emp_esc in employee_esc:
                                if emp_esc.user_id != False:
                                    user_email = self.env['res.users'].search([('id','=',emp_esc.user_id.id)])
                                    if user_email.login != False:
                                        if all_user_emails != False:
                                            if user_email.login not in all_user_emails:
                                                all_user_emails = all_user_emails + "," + user_email.login
                                        else:
                                            all_user_emails = user_email.login
                                # get manager for this employee
                                if emp_esc.parent_id != False:
                                    employee_manager = self.env['hr.employee'].search([('id','=',emp_esc.parent_id.id)])
                                    if employee_manager.user_id != False:
                                        user_manager_email = self.env['res.users'].search([('id','=',employee_manager.user_id.id)])      
                                        if user_manager_email.login != False:
                                            if all_user_emails != False:
                                                if user_manager_email.login not in all_user_emails:
                                                    all_user_emails = all_user_emails + "," + user_manager_email.login
                                            else:
                                                all_user_emails = user_manager_email.login
                                # if emp_esc.parent_id != False:
                                #     user_manager_email = self.env['res.users'].search([('id','=',emp_esc.parent_id.user_id.id)])      
                                #     if user_manager_email.login != False:
                                #         if all_user_emails != False:
                                #             if user_manager_email.login not in all_user_emails:
                                #                 all_user_emails = all_user_emails + "," + user_manager_email.login
                                #         else:
                                #             all_user_emails = user_manager_email.login
                        #check if stage =  presales
                        if stage_info.name == "Presales":
                            presales_eng = opp.username_ids
                            for pre_eng in presales_eng:
                                user_presales_email = self.env['res.users'].search([('id','=',pre_eng.id)])        
                                if user_presales_email.login != False:
                                    if all_user_emails != False:
                                        if user_presales_email.login not in all_user_emails:
                                            all_user_emails = all_user_emails + "," + user_presales_email.login
                                    else:
                                        all_user_emails = user_manager_email.login   
                        opp.users_email = all_user_emails
                        template_id = self.env.ref('custom_crm.opportunities_email_tempalte').id
                        self.env['mail.template'].browse(template_id).send_mail(opp.id,force_send=True)
                        opp.opportunity_esc_send_email = True
    @api.one
    def set_stage_name(self):
        current_stage =  self.stage_id.name
        self.stage_name = current_stage
    @api.onchange('stage_id')
    def onchange_value(self):
        # self.ensure_one()
        current_stage =  self._origin.stage_id.name
        current_field = self._origin
        for rec in self:
            found_activity = 1
            if current_field.activity == False:
                found_activity = 0
            else:
                if (rec.stage_id.name not in current_field.activity):
                    found_activity = 0

            if current_stage == 'Qualification':
                if rec.stage_id.name != "Presales Manager Review 1":
                    if found_activity == 0 or (rec.stage_id.name == "Presales" and found_activity == 0):
                        raise exceptions.ValidationError("move the opportunity just to Presales Manager Review 1")
            
            if current_stage == 'Presales Manager Review 1':
                if rec.stage_id.name != "Presales" and rec.stage_id.name != "Qualification":
                    if found_activity == 0:
                        raise exceptions.ValidationError("move the opportunity forward to presales or backward if there is missing information or if the opportunity is not valid")    
            
            if current_stage == 'Presales':
                if rec.stage_id.name != "Qualification" and rec.stage_id.name != "Presales Manager Review 1" and rec.stage_id.name != "Presales Manager Review 2":
                    raise exceptions.ValidationError("move the opportunity forward to Presales Manager Review 2 or backward as needed")
            
            if current_stage == 'Presales Manager Review 2':
                if current_field.outsourcing_required == 'yes' or current_field.ms_sla_required == 'yes':
                    if rec.stage_id.name == "Professional Services Review" or rec.stage_id.name == "Sales Proposal" or rec.stage_id.name == "Submitted" or rec.stage_id.name == "On Hold" or rec.stage_id.name == "Sales Order Review" or rec.stage_id.name == "Won" or rec.stage_id.name == "Closed and Collected":
                        raise exceptions.ValidationError("move the opportunity forward to Managed Services Review or backward as needed")
                elif current_field.house_required == 'yes':
                    if rec.stage_id.name == "Managed Services Review" or rec.stage_id.name == "Sales Proposal" or rec.stage_id.name == "Submitted" or rec.stage_id.name == "On Hold" or rec.stage_id.name == "Sales Order Review" or rec.stage_id.name == "Won" or rec.stage_id.name == "Closed and Collected":
                        raise exceptions.ValidationError("move the opportunity forward to Professional Services Review or backward as needed")
                else:
                    if rec.stage_id.name == "Managed Services Review" or rec.stage_id.name == "Professional Services Review" or rec.stage_id.name == "Submitted" or rec.stage_id.name == "On Hold" or rec.stage_id.name == "Sales Order Review" or rec.stage_id.name == "Won" or rec.stage_id.name == "Closed and Collected":
                        if found_activity == 0:
                            raise exceptions.ValidationError("move the opportunity forward to Sales Proposal or backward as needed")
            
            if current_stage == 'Managed Services Review':
                if current_field.house_required == 'yes':
                    if rec.stage_id.name == "Sales Proposal" or rec.stage_id.name == "Submitted" or rec.stage_id.name == "On Hold" or rec.stage_id.name == "Sales Order Review" or rec.stage_id.name == "Won" or rec.stage_id.name == "Closed and Collected":
                        raise exceptions.ValidationError("move the opportunity forward to Professional Services Review or backward as needed")
                else:
                    if rec.stage_id.name == "Professional Services Review" or rec.stage_id.name == "Submitted" or rec.stage_id.name == "On Hold" or rec.stage_id.name == "Sales Order Review" or rec.stage_id.name == "Won" or rec.stage_id.name == "Closed and Collected":
                        if found_activity == 0:
                            raise exceptions.ValidationError("move the opportunity forward to Sales Proposal or backward as needed")                            

            if rec.stage_id.name != "Qualification":
                if current_field.materials_supply != 'yes' and current_field.services_supply != 'yes' and current_field.house_required != 'yes' and current_field.outsourcing_required != 'yes' and current_field.ms_sla_required != 'yes':
                    raise exceptions.UserError("At least one of the previous 5 points should be set to Yes Or take it back to a stage Qualification.")
            
            if rec.stage_id.name == "Presales":
                if len(current_field.username_ids) <= 0:
                    raise exceptions.ValidationError('Minimum required fields to move it to the Presales stage (Presales engineer(s))')   
                if current_field.stage_id.name != 'Presales Manager Review 1':
                    raise exceptions.ValidationError('You can only moved to this stage through Presales Manager Review 1')
                    
            if rec.stage_id.name == "Qualification" or rec.stage_id.name == "Presales Manager Review 1" or rec.stage_id.name == "Presales" or rec.stage_id.name == "Presales Manager Review 2" or rec.stage_id.name == "Managed Services Review" or rec.stage_id.name == "Professional Services Review" or rec.stage_id.name == "Sales Proposal" or rec.stage_id.name == "Submitted" or rec.stage_id.name == "Sales Order Review":        
               if current_field.status != 'open':
                    raise exceptions.ValidationError('Please change the status to open.')     

            if rec.stage_id.name == "On Hold":
               if current_field.status != 'on_hold':
                    raise exceptions.ValidationError('Please change the status to on hold and fill in the reason.')

            if rec.stage_id.name == "Won":
                if current_field.stage_id.name != 'Sales Order Review':
                    raise exceptions.ValidationError('You can only moved to this stage through Sales Order Review')
                if current_field.status != 'won':
                    raise exceptions.ValidationError('Please change the status to won.')                     
            if rec.stage_id.name == "Managed Services Review":
                if current_field.outsourcing_required != 'yes' and current_field.ms_sla_required != 'yes' and found_activity == 0:
                    raise exceptions.ValidationError('The opportunity cannot be moved to a Managed Services Review => (Outsourcing Required	or MS/SLA Required not equal yes)')

            if rec.stage_id.name == "Professional Services Review":
                if current_field.house_required != 'yes' and found_activity == 0:
                    raise exceptions.ValidationError("The opportunity cannot be moved to a sales proposal => (In House PS Required not equal yes) ")        


            if rec.stage_id.name == "Sales Proposal":
                if current_field.materials_supply != 'yes' and current_field.services_supply != 'yes' and found_activity == 0:
                    raise exceptions.ValidationError('The opportunity cannot be moved to a Sales Proposal => (Materials Supply or 3rd party Services Supply not equal yes)')           

            stage_name_active = rec.stage_id.name
            if stage_name_active == 'Presales':
                stage_name_active = 'Presales_active'    
            act = current_field.activity
            if act == False:
                act = current_field.stage_id.name
            if act.find(stage_name_active) == -1:
                act += "," 
                act = act + stage_name_active
            if current_field.activity != False:    
                if (current_field.stage_id.name not in current_field.activity):
                    act = current_field.stage_id.name+","+act
            rec.activity = act  
                    
            rec.opportunity_esc_date = datetime.today()    
            self.opportunity_esc_send_email = False      
    @api.multi
    def action_set_lost(self):
        """ Lost semantic: probability = 0, active = False """
        if self.status == "lost" and self.lost_reason != "":
            return self.write({'probability': 0, 'active': False})
        else:
            raise exceptions.ValidationError('123')
    def toggle_active(self):
        """ When re-activating leads and opportunities set their probability
        to the default stage one. """
        if self.stage_name == "Won" and self.status != "won":
            raise exceptions.ValidationError('Please change the status to won')
        elif self.stage_name == "On Hold" and self.status != "on_hold":
          raise exceptions.ValidationError('Please change the status to on hold')
        elif (self.stage_name != "won" and self.stage_name != "On Hold") and self.status != "open":
            raise exceptions.ValidationError('Please change the status to open')
        else:
            res = super(NewModule, self).toggle_active()
            for lead in self.filtered(lambda lead: lead.active and lead.stage_id.probability):
                lead.probability = lead.stage_id.probability
            return res        
    @api.multi
    def _stage_find(self, team_id=False, domain=None, order='sequence'):
        """ Determine the stage of the current lead with its teams, the given domain and the given team_id
            :param team_id
            :param domain : base search domain for stage
            :returns crm.stage recordset
        """
        # collect all team_ids by adding given one, and the ones related to the current leads
        team_ids = set()
        if team_id:
            team_ids.add(team_id)
        for lead in self:
            if lead.team_id:
                team_ids.add(lead.team_id.id)
        # generate the domain
        if team_ids:
            search_domain = ['|', ('team_id', '=', False), ('team_id', 'in', list(team_ids))]
        else:
            search_domain = [('team_id', '=', False)]
        # AND with the domain in parameter
        if domain:
            search_domain += list(domain)
        # perform search, return the first found
        return self.env['crm.stage'].sudo().search(search_domain, order=order, limit=1)
    def mark_on_hold(self):
        if self.status != 'on_hold':
            raise exceptions.ValidationError('Please change the status to on hold and fill in the reason.')           
        stage_id = self._stage_find(domain=[('name', '=', 'On Hold'), ('on_change', '=', True)])
        self.sudo().stage_id = stage_id.id    
    @api.multi
    def action_set_won_rainbowman(self):
        if self.status != 'won':
            raise exceptions.ValidationError('Please change the status to won.')
        self.ensure_one()
        self.action_set_won()
        if self.user_id and self.team_id and self.planned_revenue:
            query = """
                SELECT
                    SUM(CASE WHEN user_id = %(user_id)s THEN 1 ELSE 0 END) as total_won,
                    MAX(CASE WHEN date_closed >= CURRENT_DATE - INTERVAL '30 days' AND user_id = %(user_id)s THEN planned_revenue ELSE 0 END) as max_user_30,
                    MAX(CASE WHEN date_closed >= CURRENT_DATE - INTERVAL '7 days' AND user_id = %(user_id)s THEN planned_revenue ELSE 0 END) as max_user_7,
                    MAX(CASE WHEN date_closed >= CURRENT_DATE - INTERVAL '30 days' AND team_id = %(team_id)s THEN planned_revenue ELSE 0 END) as max_team_30,
                    MAX(CASE WHEN date_closed >= CURRENT_DATE - INTERVAL '7 days' AND team_id = %(team_id)s THEN planned_revenue ELSE 0 END) as max_team_7
                FROM crm_lead
                WHERE
                    type = 'opportunity'
                AND
                    active = True
                AND
                    probability = 100
                AND
                    DATE_TRUNC('year', date_closed) = DATE_TRUNC('year', CURRENT_DATE)
                AND
                    (user_id = %(user_id)s OR team_id = %(team_id)s)
            """
            self.env.cr.execute(query, {'user_id': self.user_id.id,
                                        'team_id': self.team_id.id})
            query_result = self.env.cr.dictfetchone()

            message = False
            if query_result['total_won'] == 1:
                message = _('Go, go, go! Congrats for your first deal.')
            elif query_result['max_team_30'] == self.planned_revenue:
                message = _('Boom! Team record for the past 30 days.')
            elif query_result['max_team_7'] == self.planned_revenue:
                message = _('Yeah! Deal of the last 7 days for the team.')
            elif query_result['max_user_30'] == self.planned_revenue:
                message = _('You just beat your personal record for the past 30 days.')
            elif query_result['max_user_7'] == self.planned_revenue:
                message = _('You just beat your personal record for the past 7 days.')

            if message:
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': message,
                        'img_url': '/web/image/%s/%s/image' % (self.team_id.user_id._name, self.team_id.user_id.id) if self.team_id.user_id.image else '/web/static/src/img/smile.svg',
                        'type': 'rainbow_man',
                    }
                }
        return True


    @api.multi
    def write(self,values):
        before_edit_user = self.user_id.id
        befory_edit_presales = self.username_ids
        befory_edit_stage = self.stage_id.name
        rtn = super(NewModule,self).write(values)
        after_edit_user = self.user_id.id
        after_edit_presales = self.username_ids
        after_edit_stage = self.stage_id.name
        can_edit = False
        if len(befory_edit_presales) != len(after_edit_presales):
            can_edit = True
        else:
            result =  all(elem in befory_edit_presales  for elem in after_edit_presales)
            if not result:
                can_edit = True    
        if(before_edit_user != after_edit_user or can_edit == True or befory_edit_stage != after_edit_stage):
            self.pool.get("crm.lead").custom_default_group(self)
        return rtn
    @api.multi
    def unlink(self):
        rtn = super(NewModule, self).unlink()
        self.pool.get("crm.lead").custom_default_group(self)
        return rtn    
 
