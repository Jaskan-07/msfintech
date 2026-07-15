INSERT INTO ms_roles (role_id, role_name, modified_by) VALUES
(1, 'Admin', 'system_init'),
(2, 'Analyst', 'system_init'),
(3, 'Viewer', 'system_init')
ON CONFLICT (role_id) DO UPDATE
SET role_name = EXCLUDED.role_name,
    modified_at = CURRENT_TIMESTAMP,
    modified_by = EXCLUDED.modified_by;

SELECT setval(pg_get_serial_sequence('ms_roles', 'role_id'), COALESCE(MAX(role_id), 1)) FROM ms_roles;
