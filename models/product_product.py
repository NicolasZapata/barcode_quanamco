from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = "sequency"

    product_reference_id = fields.Many2one(
        "product.reference",
        string="Product Reference",
        tracking=True,
    )
    product_reference_code = fields.Char(
        "Product Reference Code", related="product_reference_id.code"
    )
    sequency = fields.Integer(
        "sequency",
        required=False,
    )

    barcode = fields.Char(
        "Barcode",
        # copy=False,
        compute="_auto_complete_barcode",
        readonly=False,
        # index="btree_not_null",
        help="International Article Number used for product identification.",
        store=True,
    )

    # TODO: Por defecto, dentro del código de barras la secuencia no aparece hasta que se guarde el formulario
    # La tarea será buscar una forma en que se pueda actualizar automáticamente la secuencia.
    @api.model
    def create(self, vals):
        """
        Al guardarse:
            . . . . .  secuencia
            00000000022-> 02 <-
            00000000022-> 03 <-
            00000000022-> 04 <-
            . . . . . . . . . .
            00000000022-> n1n2 <-
        """

    # Conformación del código de barras
    @api.depends(
        "categ_code",
        "product_class_code",
        "product_brand_code",
        "product_material_code",
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

        Auto-generates a barcode based on various fields.

        This method constructs a QR code by concatenating values from different fields
        (such as `categ_code`, `product_class_code`, etc.) and assigns the resulting
        barcode to the `barcode` field of the current record.

        :return: None
        """
        for record in self:
            qr_code = []

            # Add category code or default "00"
            if record.categ_code:
                qr_code.append(record.categ_code)
            elif not record.categ_code:
                qr_code.append("00")

            # Add product class code or default "00"
            if record.product_class_code:
                qr_code.append(record.product_class_code)
            elif not record.product_class_code:
                qr_code.append("")

            # Add product brand code or default "000"
            if record.product_brand_id:
                qr_code.append(record.product_brand_code)
            elif not record.product_brand_id.code:
                qr_code.append("000")

            # Add product material code or default "00"
            if record.product_material_id:
                qr_code.append(record.product_material_code)
            elif not record.product_material_id:
                qr_code.append("00")

            # Add product reference code or default "00"
            if record.product_reference_code:
                qr_code.append(record.product_reference_code)
            elif not record.product_reference_code:
                qr_code.append("00")

            # Add custom sequence (if available)
            if record.sequency:
                qr_code.append(record.sequency)
            else:
                qr_code.append(
                    self.env["ir.sequence"].next_by_code("product.product.sequence")
                )

            # Join all components to form the final barcode
            record.barcode = "".join(qr_code)
