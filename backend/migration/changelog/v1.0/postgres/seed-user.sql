--liquibase formatted sql

--changeset economic-dashboard:005-seed-user splitStatements:false
DO $$
DECLARE
    admin_role_id INT;
    admin_username VARCHAR(50) := 'msadmin';
    admin_email VARCHAR(100) := 'msadmin@economic-dashboard.com';
    admin_password VARCHAR(255) := 'all4one';
    admin_full_name VARCHAR(100) := 'MS Admin';
BEGIN
    SELECT id
    INTO admin_role_id
    FROM ms_role
    WHERE name = 'admin';

    INSERT INTO ms_user (username, email, hashed_password, full_name, is_active, role_id)
    VALUES (
        admin_username,
        admin_email,
        admin_password,
        admin_full_name,
        true,
        admin_role_id
    );
END $$;

--rollback DELETE FROM ms_user WHERE username = 'msadmin';