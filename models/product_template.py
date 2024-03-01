from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "mail.thread", "mail.activity.mixin"]

    category_code = fields.Char("Category Code", related="categ_id.code", tracking=True)
    product_class_id = fields.Many2one(
        "product.class",
        string="Product Class",
        tracking=True,
    )
    product_class_code = fields.Char(
        "Product CLass Code",
        related="product_class_id.code",
        tracking=True,
    )

    product_brand_ids = fields.One2many(
        "product.brand", "product_template_id", string="Product Brand"
    )
    product_material_ids = fields.One2many(
        "product.material", "product_template_id", string="Product Material"
    )
