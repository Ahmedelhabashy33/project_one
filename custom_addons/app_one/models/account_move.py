from  odoo import models,fields

class AccountMove(models.Model):
   _inherit = 'account.move'


   def action_do_somthing(self):
       for move in self:
           move.message_post(body="Someone clicked the button on this invoice.")