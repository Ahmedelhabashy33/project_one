from  odoo import models, fields, api

from odoo.exceptions import ValidationError


class property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread' , 'mail.activity.mixin']

    name = fields.Char(required=1)
    description = fields.Text(tracking=True)
    postcode = fields.Char(required=1)
    date_available = fields.Date(tracking=True)
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff' ,store=True)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage=fields.Boolean()

    active=fields.Boolean(default=True)
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West'),
    ])
    owner_id=fields.Many2one('owner')
    owner_address = fields.Char(related='owner_id.address')
    owner_phone = fields.Char(related='owner_id.phone')
    tag_ids = fields.Many2many('tag')
    state=fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold','Sold')
    ])


    _sql_constraints = [
        ('unique_name','unique(name)','This name already exists.')
    ]

    Line_ids = fields.One2many('property.line','property_id')

    @api.depends('selling_price','expected_price')
    def _compute_diff(self):
        for record in self:
            print("record is diff")
            record.diff = record.selling_price - record.expected_price

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for record in self:
            print("record is diff")
            if record.expected_price < 0:
                return {
                    'warning' :{ 'title' : 'warning', 'message'  : 'Negative value' , 'type' : 'notification' },
                }

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


    class PropertyLine(models.Model):
        _name = 'property.line'

        property_id = fields.Many2one('property')
        area = fields.Float()
        description = fields.Char()