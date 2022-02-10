DROP TABLE IF EXISTS "api_listomx_cfdis_articulo" CASCADE;

CREATE TABLE IF NOT EXISTS "api_listomx_cfdis_articulo" (
"id" NUMERIC NULL,
"quantity" DECIMAL NULL,
"units" TEXT NULL,
"description" TEXT NULL,
"unitary_amount" DECIMAL NULL,
"unitary_amount_mxn" DECIMAL NULL,
"customs" JSON NULL,
"product_code" NUMERIC NULL,
"product_code_display" TEXT NULL,
"units_code" TEXT NULL,
"units_code_display" TEXT NULL,
"id_num" TEXT NULL,
"discounts" DECIMAL NULL,
"discounts_mxn" DECIMAL NULL,
"invoice" NUMERIC NULL,
PRIMARY KEY(id),
FOREIGN KEY(invoice) REFERENCES api_listomx_cfdis_factura(id)
);