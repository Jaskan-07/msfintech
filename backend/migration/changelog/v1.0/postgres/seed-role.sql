--liquibase formatted sql

--changeset economic-dashboard:004-seed-role splitStatements:false
DO $$
DECLARE
    admin_role_name VARCHAR(50) := 'admin';
    analyst_role_name VARCHAR(50) := 'analyst';
    inactive_role_name VARCHAR(50) := 'inactive';
BEGIN
    INSERT INTO ms_role (name, description)
    VALUES
        (admin_role_name, 'Full access to ms_user and APIs'),
        (analyst_role_name, 'Can view and work with dashboard data'),
        (inactive_role_name, 'No active access');
END $$;

