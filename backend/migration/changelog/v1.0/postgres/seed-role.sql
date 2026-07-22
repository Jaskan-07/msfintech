--liquibase formatted sql

--changeset economic-dashboard:004-enable-pgcrypto splitStatements:false
CREATE EXTENSION IF NOT EXISTS pgcrypto;

--changeset economic-dashboard:004-seed-role splitStatements:false
DO $$
DECLARE
    existing_role_id VARCHAR(36);
BEGIN
    SELECT id INTO existing_role_id FROM ms_role WHERE name = 'admin';
    IF existing_role_id IS NULL THEN
        INSERT INTO ms_role (id, name, description)
        VALUES (gen_random_uuid()::varchar(36), 'admin', 'Full access to ms_user and APIs');
    END IF;


    SELECT id INTO existing_role_id FROM ms_role WHERE name = 'analyst';
    IF existing_role_id IS NULL THEN
        INSERT INTO ms_role (id, name, description)
        VALUES (gen_random_uuid()::varchar(36), 'analyst', 'Can view and work with dashboard data');
    END IF;


    SELECT id INTO existing_role_id FROM ms_role WHERE name = 'inactive';
    IF existing_role_id IS NULL THEN
        INSERT INTO ms_role (id, name, description)
        VALUES (gen_random_uuid()::varchar(36), 'inactive', 'No active access');
    END IF;

END $$;
