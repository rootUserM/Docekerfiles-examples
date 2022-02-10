DROP TABLE IF EXISTS "api_listomx_declaraciones_diot" CASCADE;

CREATE TABLE IF NOT EXISTS "api_listomx_declaraciones_diot" (
"id" NUMERIC NULL,
"rfc" TEXT NULL,
"model_version" TEXT NULL,
"folder" NUMERIC NULL,
"type" TEXT NULL,
"filed_on" TIMESTAMP NULL,
"accountant" TEXT NULL,
"receipt" NUMERIC NULL,
"filing_period" NUMERIC NULL,
PRIMARY KEY(id),
FOREIGN KEY(filing_period) REFERENCES api_listomx_declaraciones_periodo(id)
);
