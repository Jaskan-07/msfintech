--liquibase formatted sql

--changeset economic-dashboard:005-seed-user splitStatements:false
DO $$
DECLARE
    admin_role_id INT;
    existing_user_id INT;
BEGIN
    SELECT id INTO admin_role_id
    FROM ms_role
    WHERE name = 'admin';

    SELECT id INTO existing_user_id
    FROM ms_user
    WHERE username = 'msadmin';

    IF existing_user_id IS NULL THEN
        INSERT INTO ms_user (username, email, hashed_password, full_name, is_active, role_id)
        VALUES (
            'msadmin',
            'msadmin@economic-dashboard.com',
            'all4one',
            'MS Admin',
            true,
            admin_role_id
        );
    END IF;
END $$;
