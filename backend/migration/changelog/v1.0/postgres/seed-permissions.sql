INSERT INTO ms_permissions (permission_id, permission_name, permission_description, modified_by, created_by) VALUES
(1, 'user:write', 'Create, update, and remove backend platform users', 'system_init', 'system_init'),
(2, 'indicator:write', 'Ingest and overwrite macroeconomic indicators data', 'system_init', 'system_init'),
(3, 'dashboard:read', 'View charts, metrics, and report summaries', 'system_init', 'system_init')
ON CONFLICT (permission_id) DO UPDATE
SET permission_name = EXCLUDED.permission_name,
    permission_description = EXCLUDED.permission_description,
    modified_at = CURRENT_TIMESTAMP,
    modified_by = EXCLUDED.modified_by,
    created_by = EXCLUDED.created_by;

SELECT setval(pg_get_serial_sequence('ms_permissions', 'permission_id'), COALESCE(MAX(permission_id), 1)) FROM ms_permissions;
