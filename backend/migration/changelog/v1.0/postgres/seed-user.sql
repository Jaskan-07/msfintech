<<<<<<< HEAD
-- Purge seed users to avoid unique username/email collision checks
DELETE FROM users WHERE username IN ('msadmin', 'janalyst', 'rviewer');

-- Insert mapped records pointing to Admin (1), Analyst (2), and Viewer (3) roles
INSERT INTO users (username, email, hashed_password, full_name, is_active, role_id) VALUES
(
    'msadmin',
    'msadmin@economic-dashboard.com',
    'all4one',
    'MS Admin',
    true,
    1
),
(
    'janalyst', 
    'analyst@economic-dashboard.com', 
    'all4one', -- Stored in plain text here to match your framework templates default fallback 
    'Jane Data Analyst', 
    true,
    2
),
(
    'rviewer', 
    'viewer@economic-dashboard.com', 
    'all4one', 
    'Robert Viewer', 
    true,
    3
);
=======
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
>>>>>>> other-repo/main
