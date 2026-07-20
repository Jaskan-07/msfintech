--liquibase formatted sql

--changeset economic-dashboard:004-seed-role splitStatements:false
DO $$
DECLARE
    existing_role_id INT;
BEGIN
    SELECT id INTO existing_role_id
    FROM ms_role
    WHERE name = 'admin';

    IF existing_role_id IS NULL THEN
        INSERT INTO ms_role (name, description)
        VALUES ('admin', 'Full access to ms_user and APIs');
    END IF;

    SELECT id INTO existing_role_id
    FROM ms_role
    WHERE name = 'analyst';

    IF existing_role_id IS NULL THEN
        INSERT INTO ms_role (name, description)
        VALUES ('analyst', 'Can view and work with dashboard data');
    END IF;

    SELECT id INTO existing_role_id
    FROM ms_role
    WHERE name = 'inactive';

    IF existing_role_id IS NULL THEN
        INSERT INTO ms_role (name, description)
        VALUES ('inactive', 'No active access');
    END IF;
END $$;
