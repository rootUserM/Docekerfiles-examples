DROP TABLE IF EXISTS "api_listomx_declaraciones_balanzacredito" CASCADE;

CREATE TABLE IF NOT EXISTS "api_listomx_declaraciones_balanzacredito" (
"id" NUMERIC NULL,
"tax" TEXT NULL,
"credit_balance_type" TEXT NULL,
"reduction_tax" TEXT NULL,
"current" BOOL NULL,
"filing" NUMERIC NULL,
"due" DECIMAL NULL,
"origination_id" NUMERIC NULL,
"origination_credit_balance_type" TEXT NULL,
"remainder_due" DECIMAL NULL,
"initial_due" DECIMAL NULL,
"after_reduction_due" DECIMAL NULL,
PRIMARY KEY(id),
FOREIGN KEY(filing) REFERENCES api_listomx_declaraciones_declaracion(id)
);