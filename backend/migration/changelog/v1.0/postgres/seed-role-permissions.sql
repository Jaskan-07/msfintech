DELETE FROM ms_role_permissions
WHERE (role_id, permission_id) IN ((1, 1), (2, 2), (3, 3));

INSERT INTO ms_role_permissions (role_id, permission_id) VALUES
(1, 1),
(2, 2),
(3, 3);
