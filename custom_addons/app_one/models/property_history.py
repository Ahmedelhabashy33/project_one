from  odoo import models, fields, api

from odoo.exceptions import ValidationError


class propertyHistory(models.Model):
    _name = 'property.history'
    _description = 'Property'
    user_id=fields.Many2one('res.users')
    property_id=fields.Many2one('property')
    old_state=fields.Char()
    new_state=fields.Char()

    reason=fields.Char()