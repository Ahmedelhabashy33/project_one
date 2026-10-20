from odoo import fields, models , _
from odoo.exceptions import UserError


class changestate(models.TransientModel):
    _name = 'change.state'

    property_id = fields.Many2one('property')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'pending'),
    ],default='draft')

    reason = fields.Char()


    def action_confirm(self):
        if self.property_id.state != 'closed':
            raise UserError(_("You can only change the state of a closed property."))

        self.property_id.state = self.state
        self.property_id.create_history_record('closed', self.state, self.reason)
