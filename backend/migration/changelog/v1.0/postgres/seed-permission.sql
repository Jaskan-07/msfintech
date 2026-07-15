--liquibase formatted sql

--changeset economic-dashboard:006-seed-permission splitStatements:false
DO $$
DECLARE
    view_dashboard_permission VARCHAR(50) := 'view_dashboard';
    edit_dashboard_permission VARCHAR(50) := 'edit_dashboard';
    manage_users_permission VARCHAR(50) := 'manage_users';
BEGIN
    INSERT INTO ms_permission (name, description)
    VALUES
        (view_dashboard_permission, 'Permission to view the dashboard'),
        (edit_dashboard_permission, 'Permission to edit the dashboard'),
        (manage_users_permission, 'Permission to manage users');
END $$;

