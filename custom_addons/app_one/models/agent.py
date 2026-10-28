from  odoo import models,fields

class Agent(models.Model):
    _name = 'agent'

    name = fields.Char()
    description = fields.Text()

    property_ids = fields.One2many(
        'property', 'agent_id',
        domain=[('state', '=', 'draft')]
    )