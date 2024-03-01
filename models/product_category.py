from odoo import _, api, fields, models


class ProductCategory(models.Model):
    _name = "product.category"
    _inherit = ["product.category", "mail.thread", "mail.activity.mixin"]
    _description = "Product Category"

    code = fields.Char("Code", tracking=True)
    product_class_ids = fields.One2many(
        "product.class", "product_category_id", string="Product Class", tracking=True
    )
