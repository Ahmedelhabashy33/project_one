from  odoo import models,fields

class AccountMove(models.Model):
   _inherit = 'account.move'

   print(">>> account_move.py loaded")

   def action_do_somthing(self):
        print("inside action_do_somthing method")