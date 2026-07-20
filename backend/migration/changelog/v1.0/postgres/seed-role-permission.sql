--liquibase formatted sql

--changeset economic-dashboard:007-seed-role-permission splitStatements:false
DO $$
DECLARE
    admin_role_id INT;
    analyst_role_id INT;

    view_dashboard_permission_id INT;
    edit_dashboard_permission_id INT;
    manage_users_permission_id INT;
    existing_role_permission_id INT;
BEGIN
    SELECT id INTO admin_role_id
    FROM ms_role
    WHERE name = 'admin';

    SELECT id INTO analyst_role_id
    FROM ms_role
    WHERE name = 'analyst';
    SELECT id INTO view_dashboard_permission_id
    FROM ms_permission
    WHERE name = 'view_dashboard';

    SELECT id INTO edit_dashboard_permission_id
    FROM ms_permission
    WHERE name = 'edit_dashboard';

    SELECT id INTO manage_users_permission_id
    FROM ms_permission
    WHERE name = 'manage_users';

    SELECT id INTO existing_role_permission_id
    FROM ms_role_permission
    WHERE role_id = admin_role_id
      AND permission_id = view_dashboard_permission_id;

    IF existing_role_permission_id IS NULL THEN
        INSERT INTO ms_role_permission (role_id, permission_id)
        VALUES (admin_role_id, view_dashboard_permission_id);
    END IF;

    SELECT id INTO existing_role_permission_id
    FROM ms_role_permission
    WHERE role_id = admin_role_id
      AND permission_id = edit_dashboard_permission_id;

    IF existing_role_permission_id IS NULL THEN
        INSERT INTO ms_role_permission (role_id, permission_id)
        VALUES (admin_role_id, edit_dashboard_permission_id);
    END IF;

    SELECT id INTO existing_role_permission_id
    FROM ms_role_permission
    WHERE role_id = admin_role_id
      AND permission_id = manage_users_permission_id;

    IF existing_role_permission_id IS NULL THEN
        INSERT INTO ms_role_permission (role_id, permission_id)
        VALUES (admin_role_id, manage_users_permission_id);
    END IF;

    SELECT id INTO existing_role_permission_id
    FROM ms_role_permission
    WHERE role_id = analyst_role_id
      AND permission_id = view_dashboard_permission_id;

    IF existing_role_permission_id IS NULL THEN
        INSERT INTO ms_role_permission (role_id, permission_id)
        VALUES (analyst_role_id, view_dashboard_permission_id);
    END IF;
END $$;
