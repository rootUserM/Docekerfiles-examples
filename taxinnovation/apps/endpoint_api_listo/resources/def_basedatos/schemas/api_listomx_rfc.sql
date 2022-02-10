DROP TABLE IF EXISTS "api_listomx_rfc" CASCADE;

CREATE TABLE IF NOT EXISTS "api_listomx_rfc" (
"id" NUMERIC NOT NULL,
"rfc" TEXT NULL,
"rfc_name" TEXT NULL,
"street" TEXT NULL,
"ext_num" TEXT NULL,
"int_num" TEXT NULL,
"colonia" TEXT NULL,
"locality" TEXT NULL,
"municipio" TEXT NULL,
"state" TEXT NULL,
"country" TEXT NULL,
"postal_code" TEXT NULL,
"mailbox_suffix" TEXT NULL,
"tax_regime" TEXT NULL,
"sat_sync_enabled" BOOL NULL,
"failed_login" NUMERIC NULL,
"last_sat_sync_on" TIMESTAMP NULL,
"active" BOOL NULL,
"download_status" JSON NULL,
"is_company" BOOL NULL,
"has_filings" BOOL NULL,
"last_filing_sync_on" TIMESTAMP NULL,
"last_annual_filing_sync_on" TIMESTAMP NULL,
"filing_sync_active" BOOL NULL,
PRIMARY KEY (id)
);