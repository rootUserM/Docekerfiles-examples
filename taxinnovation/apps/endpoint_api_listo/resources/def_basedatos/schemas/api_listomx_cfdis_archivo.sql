DROP TABLE IF EXISTS "api_listomx_cfdis_archivo" CASCADE;

CREATE TABLE IF NOT EXISTS "api_listomx_cfdis_archivo" (
"id" NUMERIC NULL,
"file_type" TEXT NULL,
"file_name" TEXT NULL,
"data" TEXT NULL,
"is_invoice" BOOL NULL,
"thumbnail_url" TEXT NULL,
"is_image" BOOL NULL,
"is_cfdi_xml" BOOL NULL,
"num_pages" NUMERIC NULL,
"digest" TEXT NULL,
"url" TEXT NULL,
"document" NUMERIC NULL,
PRIMARY KEY(id),
FOREIGN KEY(document) REFERENCES api_listomx_cfdis_documento(id)
);