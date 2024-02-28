from odoo import _, api, fields, models

class ProductProduct(models.Model):
  _inherit = 'product.product'
  _description = 'Product Product'
  
  code = fields.Char("Code", tracking=True, related="product_class_ids.code")
  categ_code = fields.Char('Category Code', related="categ_id.code")
  product_class_ids = fields.Many2one(
    "product.class", string="Product Class",
    tracking=True,
  )