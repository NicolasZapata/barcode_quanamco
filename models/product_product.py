from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = "barcode desc"

    product_reference_id = fields.Many2one(
        "product.reference",
        string="Product Reference",
        tracking=True,
    )
    product_reference_code = fields.Char('Product Reference Code', related='product_reference_id.code')
    sequency = fields.Char("Sequency", )
 
    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('product.product.sequence')
        vals['sequency'] = sequence
        return super(ProductProduct, self).create(vals)

    # Conformación del código de barras
    @api.depends(
        "categ_code",
        "product_class_code",
        "product_brand_id",
        "product_material_id",
        "product_reference_code",
        "sequency",
        "barcode",
    )
    def _auto_complete_barcode(self):
        """
        Categoria(2) + Clase(2) + material(2) + Marca(3) + Referencia de producto(2) + secuencia(2)

             99      +  99      +     99      +    999   +             99            +     99

        Ejemplo:
            45+02+02+123+01+01
            45+02+00+000+01+02
            45+02+01+045+00+03
            45+02+01+045+12+04
        """
        for record in self:
            qr_code = []
            if record.categ_code:
                qr_code.append(record.categ_code)
            elif not record.categ_code:
                qr_code.append("00")

            if record.product_class_code:
                qr_code.append(record.product_class_code)
            elif not record.product_class_code:
                qr_code.append("00")

            if record.product_brand_id:
                qr_code.append(record.product_brand_id.code)
            elif not record.product_brand_id.code:
                qr_code.append("000")

            if record.product_material_id:
                qr_code.append(record.product_material_id.code)
            elif not record.product_material_id:
                qr_code.append("00")

            if record.product_reference_code:
                qr_code.append(record.product_reference_code)
            elif not record.product_reference_code:
                qr_code.append("00")

            if record.sequency:
                qr_code.append(record.sequency)

            record.barcode = "".join(qr_code)
