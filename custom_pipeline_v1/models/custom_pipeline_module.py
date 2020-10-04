# -*- coding: utf-8 -*-

from odoo import models, fields, api
class UserPipeline(models.Model):
    _inherit = 'crm.stage'
    access_group = fields.Many2many(
        'hr.job',
        'default_groub_crm',
        string='Access Group'
    )
    escalation_group = fields.Many2many(
        'hr.job',
        'default_esc_crm',
        string='Escalation Group'
    )
    escalation_after = fields.Integer(string='Escalation after (Business Days)')   
    all_user_emails = fields.Text(string='All User Emails')
    all_user_emails_from_stage = fields.Text(string='All User Emails From Stage')
    all_user_emails_from_opper = fields.Text(string='All User Emails From Opper')
    all_user_emails_from_presales = fields.Text(string='All User Emails From presales')
    all_user_esc = fields.Text(string='All User Esc')
     

    @api.multi
    def write(self,values):
        befory_edit_access_group = self.access_group
        rtn = super(UserPipeline,self).write(values)
        after_edit_access_group = self.access_group
        can_edit = False
        if len(befory_edit_access_group) != len(after_edit_access_group):
            can_edit = True
        else:
            result =  all(elem in befory_edit_access_group  for elem in after_edit_access_group)
            if not result:
                can_edit = True    
        if(can_edit == True):
            self.pool.get("crm.lead").custom_default_group(self)
        return rtn

    @api.multi
    def create(self,vals):
        all_emails_default_pos = ""
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
        vals['all_user_emails'] = all_emails_default_pos
        rtn = super(UserPipeline,self).create(vals)
        return rtn 