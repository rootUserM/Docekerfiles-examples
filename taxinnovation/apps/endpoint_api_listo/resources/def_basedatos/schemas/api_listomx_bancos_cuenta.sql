CREATE TABLE api_listomx_bancos_cuenta(
  value INTEGER,
  rfc_id INTEGER NOT NULL,
  bank TEXT NOT NULL,
  total_balance MONEY,
  available_balance MONEY,
  currency TEXT NOT NULL,
  PRIMARY KEY(value),
  CONSTRAINT fk_conciliacion_transaccion FOREIGN KEY(rfc_id) REFERENCES api_listomx_rfc(id)
);