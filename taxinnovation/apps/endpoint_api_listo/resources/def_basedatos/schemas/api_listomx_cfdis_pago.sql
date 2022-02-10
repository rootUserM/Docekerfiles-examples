DROP TABLE IF EXISTS "api_listomx_cfdis_pago" CASCADE;

CREATE TABLE IF NOT EXISTS "api_listomx_cfdis_pago" (
"id" NUMERIC NULL,
"currency" TEXT NULL,
"counterparty_name" TEXT NULL,
"counterparty_rfc" TEXT NULL,
"effective_on" TIMESTAMP NULL,
"issued_on" TIMESTAMP NULL,
"amount" DECIMAL NULL,
"amount_mxn" DECIMAL NULL,
"is_income" BOOL NULL,
"receipt_uuid" TEXT NULL,
"receipt_id" NUMERIC NULL,
"payment_method_display" TEXT NULL,
"source_rfc" TEXT NULL,
"source_foreign_name" TEXT NULL,
"source_account_num" TEXT NULL,
"destination_rfc" TEXT NULL,
"destination_account_num" NUMERIC NULL,
"operation_num" TEXT NULL,
"data_warnings" JSON NULL,
PRIMARY KEY(id)
);