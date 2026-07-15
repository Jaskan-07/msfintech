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
