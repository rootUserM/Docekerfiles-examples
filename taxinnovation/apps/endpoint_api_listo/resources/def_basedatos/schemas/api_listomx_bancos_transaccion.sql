CREATE TABLE api_listomx_bancos_transaccion(
  schema_version INTEGER NOT NULL,
  id INTEGER NOT NULL,
  dt TIMESTAMP NOT NULL,
  dt_month TIMESTAMP NOT NULL,
  reference INTEGER NOT NULL,
  description TEXT NOT NULL,
  comments TEXT,
  transaction_type TEXT,
  rfc_id INTEGER NOT NULL,
  account_id INTEGER NOT NULL,
  statement_id INTEGER NOT NULL,
  is_open_date BOOLEAN NOT NULL,
  currency TEXT NOT NULL,
  customer_id INTEGER NOT NULL,
  original_counterparty TEXT,
  display_counterparty TEXT,
  detected_counterparty_rfc TEXT,
  detected_counterparty_name TEXT,
  detected_counterparty_name_ngrams TEXT,
  account_display_name TEXT NOT NULL,
  total_reconciled MONEY NOT NULL,
  total_reconciled_mxn MONEY NOT NULL,
  reconciliation_state TEXT NOT NULL,
  amount MONEY NOT NULL,
  balance MONEY NOT NULL,
  amount_mxn MONEY NOT NULL,
  balance_mxn MONEY NOT NULL,
  timestamp INTEGER NOT NULL,
  type TEXT NOT NULL,
  score TEXT,
  transaction_type_attrs JSON,
  extra_data JSON,
  PRIMARY KEY(id),
  CONSTRAINT fk_transaccion_rfc FOREIGN KEY(rfc_id) REFERENCES api_listomx_rfc(id),
  CONSTRAINT fk_transaccion_cuenta FOREIGN KEY(account_id) REFERENCES api_listomx_bancos_cuenta(value),
  CONSTRAINT fk_transaccion_statement FOREIGN KEY(statement_id) REFERENCES api_listomx_declaraciones_declaracion(id),
  CONSTRAINT fk_factura_cliente FOREIGN KEY(customer_id) REFERENCES api_listomx_clientes_rfc(id)
);