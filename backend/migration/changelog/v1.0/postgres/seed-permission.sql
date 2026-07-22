--liquibase formatted sql

--changeset economic-dashboard:006-seed-permission splitStatements:false
DO $$
DECLARE
    existing_permission_id VARCHAR(36);
BEGIN
    -- 1. Seed view_dashboard
    SELECT id INTO existing_permission_id FROM ms_permission WHERE name = 'view_dashboard';
    IF existing_permission_id IS NULL THEN
        INSERT INTO ms_permission (id, name, description)
        VALUES (gen_random_uuid()::varchar(36), 'view_dashboard', 'Permission to view the dashboard');
    END IF;

    -- 2. Seed edit_dashboard
    SELECT id INTO existing_permission_id FROM ms_permission WHERE name = 'edit_dashboard';
    IF existing_permission_id IS NULL THEN
        INSERT INTO ms_permission (id, name, description)
        VALUES (gen_random_uuid()::varchar(36), 'edit_dashboard', 'Permission to edit the dashboard');
    END IF;

    -- 3. Seed manage_users
    SELECT id INTO existing_permission_id FROM ms_permission WHERE name = 'manage_users';
    IF existing_permission_id IS NULL THEN
        INSERT INTO ms_permission (id, name, description)
        VALUES (gen_random_uuid()::varchar(36), 'manage_users', 'Permission to manage users');
    END IF;

END $$;
