from  odoo import models, fields, api

from odoo.exceptions import ValidationError


class property(models.Model):
    _name = 'property'

    name = fields.Char(required=1)
    description = fields.Text()
    postcode = fields.Char(required=1)
    date_available = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage=fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West'),
    ])

    _sql_constraints = [
        ('unique_name','unique(name)','This name already exists.')
    ]

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for record in self:
            if record.bedrooms == 0:
                raise ValidationError('Bedrooms cannot be Equal 0')