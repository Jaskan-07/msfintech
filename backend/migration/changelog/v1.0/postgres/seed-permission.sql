--liquibase formatted sql

--changeset economic-dashboard:006-seed-permission splitStatements:false
DO $$
DECLARE
    existing_permission_id INT;
BEGIN
    -- 1. Seed view_dashboard
    SELECT id INTO existing_permission_id FROM ms_permission WHERE id = 1;
    IF existing_permission_id IS NULL THEN
        INSERT INTO ms_permission (id, name, description)
        VALUES (1, 'view_dashboard', 'Permission to view the dashboard');
    END IF;

    -- 2. Seed edit_dashboard
    SELECT id INTO existing_permission_id FROM ms_permission WHERE id = 2;
    IF existing_permission_id IS NULL THEN
        INSERT INTO ms_permission (id, name, description)
        VALUES (2, 'edit_dashboard', 'Permission to edit the dashboard');
    END IF;

    -- 3. Seed manage_users
    SELECT id INTO existing_permission_id FROM ms_permission WHERE id = 3;
    IF existing_permission_id IS NULL THEN
        INSERT INTO ms_permission (id, name, description)
        VALUES (3, 'manage_users', 'Permission to manage users');
    END IF;



END $$;
