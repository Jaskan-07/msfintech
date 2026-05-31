-- Seed default admin user
-- Username: msadmin
-- Password: all4one (plain text - encryption to be added later)

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM users WHERE username = 'msadmin') THEN
        INSERT INTO users (username, email, hashed_password, full_name, is_active)
        VALUES (
            'msadmin',
            'msadmin@economic-dashboard.com',
            'all4one',
            'MS Admin',
            true
        );
    END IF;
END $$;
