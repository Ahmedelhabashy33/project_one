from  odoo import models,fields

class Owner(models.Model):
    _name = 'owner'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    line_ids = fields.One2many('owner.line', 'owner_id')
    name = fields.Char()
    phone= fields.Char(tracking=True)
    address = fields.Char()
    property_ids=fields.One2many('property','owner_id')


class OwnerLine(models.Model):
    _name = 'owner.line'

    owner_id = fields.Many2one('owner')
    age = fields.Integer()
    street = fields.Char()