--liquibase formatted sql

--changeset economic-dashboard:005-seed-user splitStatements:false
DO $$
DECLARE
    ms_role_id INT;
BEGIN
    -- 1. Seed Admin User
    SELECT id INTO ms_role_id FROM ms_role WHERE name = 'admin';
    IF NOT EXISTS (SELECT 1 FROM ms_user WHERE id = 1) THEN
        INSERT INTO ms_user (id, username, email, hashed_password, full_name, is_active, role_id)
        VALUES (1, 'msadmin', 'msadmin@economic-dashboard.com', 'all4one', 'MS Admin', true, ms_role_id);
    END IF;

    -- 2. Seed Analyst User
    SELECT id INTO ms_role_id FROM ms_role WHERE name = 'analyst';
    IF NOT EXISTS (SELECT 1 FROM ms_user WHERE id = 2) THEN
        INSERT INTO ms_user (id, username, email, hashed_password, full_name, is_active, role_id)
        VALUES (2, 'msanalyst', 'analyst@economic-dashboard.com', 'analystpass', 'Data Analyst', true, ms_role_id);
    END IF;

    -- 3. Seed Inactive User
    SELECT id INTO ms_role_id FROM ms_role WHERE name = 'inactive';
    IF NOT EXISTS (SELECT 1 FROM ms_user WHERE id = 3) THEN
        INSERT INTO ms_user (id, username, email, hashed_password, full_name, is_active, role_id)
        VALUES (3, 'inactiveuser', 'inactiveuser@economic-dashboard.com', 'lockedout1', 'Ex Employee', false, ms_role_id);
    END IF;
END $$;
