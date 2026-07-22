--liquibase formatted sql

--changeset economic-dashboard:005-seed-user splitStatements:false
DO $$
DECLARE
    ms_role_id VARCHAR(36);
BEGIN
    -- 1. Seed Admin User
    SELECT id INTO ms_role_id FROM ms_role WHERE name = 'admin';
    IF NOT EXISTS (SELECT 1 FROM ms_user WHERE username = 'msadmin') THEN
        INSERT INTO ms_user (id, username, email, hashed_password, full_name, is_active, role_id)
        VALUES (gen_random_uuid()::varchar(36), 'msadmin', 'msadmin@economic-dashboard.com', 'all4one', 'MS Admin', true, ms_role_id);
    END IF;

    -- 2. Seed Analyst User
    SELECT id INTO ms_role_id FROM ms_role WHERE name = 'analyst';
    IF NOT EXISTS (SELECT 1 FROM ms_user WHERE username = 'msanalyst') THEN
        INSERT INTO ms_user (id, username, email, hashed_password, full_name, is_active, role_id)
        VALUES (gen_random_uuid()::varchar(36), 'msanalyst', 'analyst@economic-dashboard.com', 'analystpass', 'Data Analyst', true, ms_role_id);
    END IF;

    -- 3. Seed Inactive User
    SELECT id INTO ms_role_id FROM ms_role WHERE name = 'inactive';
    IF NOT EXISTS (SELECT 1 FROM ms_user WHERE username = 'inactiveuser') THEN
        INSERT INTO ms_user (id, username, email, hashed_password, full_name, is_active, role_id)
        VALUES (gen_random_uuid()::varchar(36), 'inactiveuser', 'inactiveuser@economic-dashboard.com', 'lockedout1', 'Ex Employee', false, ms_role_id);
    END IF;
END $$;
