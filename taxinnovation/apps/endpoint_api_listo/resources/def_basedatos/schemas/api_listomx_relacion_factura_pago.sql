DROP TABLE IF EXISTS "api_listomx_relacion_factura_pago" CASCADE;
CREATE TABLE IF NOT EXISTS "api_listomx_relacion_factura_pago"(
  id SERIAL,
  invoice NUMERIC NOT NULL,
  cfdi_pago INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(invoice) REFERENCES api_listomx_cfdis_factura(id),
  FOREIGN KEY(cfdi_pago) REFERENCES api_listomx_cfdis_pago(id)
);