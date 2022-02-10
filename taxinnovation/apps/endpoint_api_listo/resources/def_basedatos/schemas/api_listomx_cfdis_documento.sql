
DROP TABLE IF EXISTS "api_listomx_cfdis_documento" CASCADE;

CREATE TABLE IF NOT EXISTS "api_listomx_cfdis_documento" (
"id" NUMERIC NULL,
"invoice_id" NUMERIC NULL,
"status" TEXT NULL,
"watch_active" BOOL NULL,
"watch_for" JSON NULL,
"has_xml" BOOL NULL,
"thumbnail_url" TEXT NULL,
"received_at" TEXT NULL,
"modified_on" TIMESTAMP NULL,
"document_type" TEXT NULL,
"rfc_id" NUMERIC NULL,
"period_year" TEXT NULL,
"period_month" TEXT NULL,
"invoice" NUMERIC NULL,
PRIMARY KEY(id),
FOREIGN KEY(rfc_id) REFERENCES api_listomx_rfc(id),
FOREIGN KEY(invoice) REFERENCES api_listomx_cfdis_factura(id)
);