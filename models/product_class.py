from odoo import _, api, fields, models


class ProductClass(models.Model):
    _name = "product.class"
    _description = "Product Class"

    name = fields.Char("Name")
    code = fields.Char("Code")
    product_category_id = fields.Many2one("product.category", string="Product Category")
