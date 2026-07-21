--liquibase formatted sql

--changeset economic-dashboard:005-seed-user splitStatements:false
DO $$
DECLARE
    admin_role_id INT;
    analyst_role_id INT;
    inactive_role_id INT;
    existing_user_id INT;
BEGIN
    SELECT id INTO admin_role_id FROM ms_role WHERE name = 'admin';
    SELECT id INTO analyst_role_id FROM ms_role WHERE name = 'analyst';
    SELECT id INTO inactive_role_id FROM ms_role WHERE name = 'inactive';

    SELECT id INTO existing_user_id FROM ms_user WHERE id = 1;
    IF existing_user_id IS NULL THEN
        INSERT INTO ms_user (id, username, email, hashed_password, full_name, is_active, role_id)
        VALUES (1, 'msadmin', 'msadmin@economic-dashboard.com', 'all4one', 'MS Admin', true, admin_role_id);
    END IF;

    SELECT id INTO existing_user_id FROM ms_user WHERE id = 2;
    IF existing_user_id IS NULL THEN
        INSERT INTO ms_user (id, username, email, hashed_password, full_name, is_active, role_id)
        VALUES (2, 'msanalyst', 'analyst@economic-dashboard.com', 'analystpass', 'Data Analyst', true, analyst_role_id);
    END IF;

    SELECT id INTO existing_user_id FROM ms_user WHERE id = 3;
    IF existing_user_id IS NULL THEN
        INSERT INTO ms_user (id, username, email, hashed_password, full_name, is_active, role_id)
        VALUES (3, 'msexpelled', 'disabled@economic-dashboard.com', 'lockedout1', 'Ex Employee', false, inactive_role_id);
    END IF;
    PERFORM setval(pg_get_serial_sequence('ms_user', 'id'), COALESCE(MAX(id), 1)) FROM ms_user;

END $$;
