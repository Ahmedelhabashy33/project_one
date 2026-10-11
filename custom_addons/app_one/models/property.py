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
    owner_id=fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    state=fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold','Sold')
    ])


    _sql_constraints = [
        ('unique_name','unique(name)','This name already exists.')
    ]

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for record in self:
            if record.bedrooms == 0:
                raise ValidationError('Bedrooms cannot be Equal 0')


    def action_to_pending(self):
        for record in self:
            print("record is pendig")
            record.state = 'pending'

    def action_to_sold(self):
        for record in self:
            print("record is sold")
            record.state = 'sold'

    def action_to_draft(self):
        for record in self:
            print("record is draft")
            record.state = 'draft'


    # @api.model_create_multi
    # def create(self, vals):
    #     res=super(property,self).create(vals)
    #     print('creating property in terminal')
    #     return res
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super()._search(domain, offset=offset, limit=limit, order=order, access_rights_uid=access_rights_uid)
    #     print("searching property in terminal")
    #     return res
    #
    # def write(self, vals):
    #     res=super().write(vals)
    #     print("writing property in terminal")
    #     return res
    #
    # def unlink(self):
    #     res=super().unlink()
    #     print("unlinking property in terminal")
    #     return res