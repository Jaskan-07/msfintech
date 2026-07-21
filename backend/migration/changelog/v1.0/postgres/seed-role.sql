--liquibase formatted sql

--changeset economic-dashboard:004-seed-role splitStatements:false
DO $$
DECLARE
    existing_role_id INT;
BEGIN
    SELECT id INTO existing_role_id FROM ms_role WHERE id = 1;
    IF existing_role_id IS NULL THEN
        INSERT INTO ms_role (id, name, description)
        VALUES (1, 'admin', 'Full access to ms_user and APIs');
    END IF;


    SELECT id INTO existing_role_id FROM ms_role WHERE id = 2;
    IF existing_role_id IS NULL THEN
        INSERT INTO ms_role (id, name, description)
        VALUES (2, 'analyst', 'Can view and work with dashboard data');
    END IF;


    SELECT id INTO existing_role_id FROM ms_role WHERE id = 3;
    IF existing_role_id IS NULL THEN
        INSERT INTO ms_role (id, name, description)
        VALUES (3, 'inactive', 'No active access');
    END IF;

   
    PERFORM setval(pg_get_serial_sequence('ms_role', 'id'), COALESCE(MAX(id), 1)) FROM ms_role;

END $$;
