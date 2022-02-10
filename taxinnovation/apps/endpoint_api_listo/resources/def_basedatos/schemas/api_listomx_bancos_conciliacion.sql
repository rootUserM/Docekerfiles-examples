CREATE TABLE api_listomx_bancos_conciliacion(
    id INTEGER,
    type TEXT NOT NULL,
    folio TEXT NOT NULL,
    transaction_id INTEGER NOT NULL,
    invoice_id INTEGER NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT fk_conciliacion_transaccion FOREIGN KEY(transaction_id) REFERENCES api_listomx_bancos_transaccion(id),
    CONSTRAINT fk_conciliacion_factura FOREIGN KEY(invoice_id) REFERENCES api_listomx_cfdis_factura(id)
);