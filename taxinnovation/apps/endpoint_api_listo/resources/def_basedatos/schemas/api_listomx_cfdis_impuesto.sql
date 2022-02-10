DROP TABLE IF EXISTS "api_listomx_cfdis_impuesto" CASCADE;

CREATE TABLE IF NOT EXISTS "api_listomx_cfdis_impuesto" (
"id" SERIAL NOT NULL,
"tax_type" TEXT NULL,
"tax_rate" DECIMAL NULL,
"amount" DECIMAL NULL,
"amount_mxn" DECIMAL NULL,
"treatment" TEXT NULL,
"lineitem" NUMERIC NULL,
PRIMARY KEY(id),
FOREIGN KEY(lineitem) REFERENCES api_listomx_cfdis_articulo(id)
);
