DROP TABLE IF EXISTS "api_listomx_cfdis_recibo" CASCADE;

CREATE TABLE IF NOT EXISTS "api_listomx_cfdis_recibo" (
"id" NUMERIC NULL,
"payment" NUMERIC NULL,
"uuid" TEXT NULL,
"issuer_rfc" TEXT NULL,
"receiver_rfc" TEXT NULL,
"issuer_name" TEXT NULL,
"receiver_name" TEXT NULL,
"created_on" TIMESTAMP NULL,
"issued_on" TIMESTAMP NULL,
"original_xml" TEXT NULL,
"is_income" BOOL NULL,
"counterparty_rfc" TEXT NULL,
"counterparty_name" TEXT NULL,
"validation_status.code" TEXT NULL,
"validation_status.message" TEXT NULL,
"warnings" JSON NULL,
"series" TEXT NULL,
"folio" NUMERIC NULL,
"generated_invoice_id" TEXT NULL,
"canceled_on" TIMESTAMP NULL,
"email_status" JSON NULL,
PRIMARY KEY(id),
FOREIGN KEY(payment) REFERENCES api_listomx_cfdis_pago(id)
);
