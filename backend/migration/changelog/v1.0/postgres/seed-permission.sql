--liquibase formatted sql

--changeset economic-dashboard:006-seed-permission splitStatements:false
DO $$
DECLARE
    existing_permission_id INT;
BEGIN
    SELECT id INTO existing_permission_id
    FROM ms_permission
    WHERE name = 'view_dashboard';

    IF existing_permission_id IS NULL THEN
        INSERT INTO ms_permission (name, description)
        VALUES ('view_dashboard', 'Permission to view the dashboard');
    END IF;

    SELECT id INTO existing_permission_id
    FROM ms_permission
    WHERE name = 'edit_dashboard';

    IF existing_permission_id IS NULL THEN
        INSERT INTO ms_permission (name, description)
        VALUES ('edit_dashboard', 'Permission to edit the dashboard');
    END IF;

    SELECT id INTO existing_permission_id
    FROM ms_permission
    WHERE name = 'manage_users';

    IF existing_permission_id IS NULL THEN
        INSERT INTO ms_permission (name, description)
        VALUES ('manage_users', 'Permission to manage users');
    END IF;
END $$;
