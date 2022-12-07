CREATE SCHEMA models;

CREATE TABLE IF NOT EXISTS models.model
(
    id_model uuid NOT NULL,
    description character varying COLLATE pg_catalog."default",
    configuration json,
    model_serialized bytea,
    CONSTRAINT model_pkey PRIMARY KEY (id_model)
)

CREATE TABLE IF NOT EXISTS models.model_status
(
    id_status uuid NOT NULL,
    id_model uuid,
    status character varying COLLATE pg_catalog."default",
    message character varying COLLATE pg_catalog."default",
    last_updated timestamp without time zone,
    CONSTRAINT model_status_pkey PRIMARY KEY (id_status),
    CONSTRAINT id_models_fkey FOREIGN KEY (id_model)
        REFERENCES models.model (id_model) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
