--liquibase formatted sql

--changeset economic-dashboard:007-seed-role-permission splitStatements:false
DO $$
DECLARE
    admin_role_id INT;
    analyst_role_id INT;

    view_dashboard_permission_id INT;
    edit_dashboard_permission_id INT;
    manage_users_permission_id INT;
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

    INSERT INTO ms_role_permission (role_id, permission_id)
    VALUES
        (admin_role_id, view_dashboard_permission_id),
        (admin_role_id, edit_dashboard_permission_id),
        (admin_role_id, manage_users_permission_id),
        (analyst_role_id, view_dashboard_permission_id);
END $$;

--rollback DELETE FROM ms_role_permission WHERE role_id IN (SELECT id FROM ms_role WHERE name IN ('admin', 'analyst')) AND permission_id IN (SELECT id FROM ms_permission WHERE name IN ('view_dashboard', 'edit_dashboard', 'manage_users'));