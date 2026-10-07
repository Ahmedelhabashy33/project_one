from  odoo import models,fields

class Agent(models.Model):
    _name = 'agent'

    name = fields.Char()
    description = fields.Text()


