INSERT INTO `auth_group` (id, name) VALUES (1, 'Validation Afrique Centrale');
INSERT INTO `auth_group` (id, name) VALUES (2, 'Validation Afrique de l''ouest');
INSERT INTO `auth_group` (id, name) VALUES (3, 'Validation Asie-Pacifique');
INSERT INTO `auth_group` (id, name) VALUES (4, 'Validation Caraïbe');
INSERT INTO `auth_group` (id, name) VALUES (5, 'Validation Europe centrale et orientale');
INSERT INTO `auth_group` (id, name) VALUES (6, 'Validation Europe de l''Ouest et Maghreb');
INSERT INTO `auth_group` (id, name) VALUES (7, 'Validation Moyen-Orient');
INSERT INTO `auth_group` (id, name) VALUES (8, 'Validation Océan indien');
INSERT INTO `auth_group` (id, name) VALUES (9, 'Validation Services centraux');
INSERT INTO `auth_group` (id, name) VALUES (10, 'Validation Amerique');

INSERT INTO `auth_group` (id, name) VALUES (11, 'Saisie Afrique Centrale');
INSERT INTO `auth_group` (id, name) VALUES (12, 'Saisie Afrique de l''ouest');
INSERT INTO `auth_group` (id, name) VALUES (13, 'Saisie Asie-Pacifique');
INSERT INTO `auth_group` (id, name) VALUES (14, 'Saisie Caraïbe');
INSERT INTO `auth_group` (id, name) VALUES (15, 'Saisie Europe centrale et orientale');
INSERT INTO `auth_group` (id, name) VALUES (16, 'Saisie Europe de l''Ouest et Maghreb');
INSERT INTO `auth_group` (id, name) VALUES (17, 'Saisie Moyen-Orient');
INSERT INTO `auth_group` (id, name) VALUES (18, 'Saisie Océan indien');
INSERT INTO `auth_group` (id, name) VALUES (19, 'Saisie Services centraux');
INSERT INTO `auth_group` (id, name) VALUES (20, 'Saisie Amerique');

INSERT INTO `auth_group` (id, name) VALUES (21, 'Responsable Régional Afrique Centrale');
INSERT INTO `auth_group` (id, name) VALUES (22, 'Responsable Régional Afrique de l''ouest');
INSERT INTO `auth_group` (id, name) VALUES (23, 'Responsable Régional Asie-Pacifique');
INSERT INTO `auth_group` (id, name) VALUES (24, 'Responsable Régional Caraïbe');
INSERT INTO `auth_group` (id, name) VALUES (25, 'Responsable Régional Europe centrale et orientale');
INSERT INTO `auth_group` (id, name) VALUES (26, 'Responsable Régional Europe de l''Ouest et Maghreb');
INSERT INTO `auth_group` (id, name) VALUES (27, 'Responsable Régional Moyen-Orient');
INSERT INTO `auth_group` (id, name) VALUES (28, 'Responsable Régional Océan indien');
INSERT INTO `auth_group` (id, name) VALUES (29, 'Responsable Régional Services centraux');
INSERT INTO `auth_group` (id, name) VALUES (30, 'Responsable Régional Amerique');

-- Validation
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 1, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 2, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 3, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 4, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 5, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 6, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 7, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 8, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 9, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 10, id FROM auth_permission WHERE codename = 'can_select_candidature';

INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 1, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 2, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 3, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 4, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 5, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 6, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 7, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 8, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 9, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 10, id FROM auth_permission WHERE codename = 'can_classe_candidature';

-- Saisie
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 11, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 12, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 13, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 14, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 15, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 16, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 17, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 18, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 19, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 20, id FROM auth_permission WHERE codename = 'add_candidature';

INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 11, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 12, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 13, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 14, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 15, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 16, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 17, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 18, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 19, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 20, id FROM auth_permission WHERE codename = 'change_candidature';

-- Responsable regional
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 21, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 22, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 23, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 24, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 25, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 26, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 27, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 28, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 29, id FROM auth_permission WHERE codename = 'add_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 30, id FROM auth_permission WHERE codename = 'add_candidature';

INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 21, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 22, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 23, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 24, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 25, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 26, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 27, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 28, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 29, id FROM auth_permission WHERE codename = 'change_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 30, id FROM auth_permission WHERE codename = 'change_candidature';

INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 21, id FROM auth_permission WHERE codename = 'add_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 22, id FROM auth_permission WHERE codename = 'add_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 23, id FROM auth_permission WHERE codename = 'add_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 24, id FROM auth_permission WHERE codename = 'add_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 25, id FROM auth_permission WHERE codename = 'add_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 26, id FROM auth_permission WHERE codename = 'add_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 27, id FROM auth_permission WHERE codename = 'add_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 28, id FROM auth_permission WHERE codename = 'add_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 29, id FROM auth_permission WHERE codename = 'add_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 30, id FROM auth_permission WHERE codename = 'add_appel';

INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 21, id FROM auth_permission WHERE codename = 'change_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 22, id FROM auth_permission WHERE codename = 'change_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 23, id FROM auth_permission WHERE codename = 'change_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 24, id FROM auth_permission WHERE codename = 'change_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 25, id FROM auth_permission WHERE codename = 'change_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 26, id FROM auth_permission WHERE codename = 'change_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 27, id FROM auth_permission WHERE codename = 'change_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 28, id FROM auth_permission WHERE codename = 'change_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 29, id FROM auth_permission WHERE codename = 'change_appel';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 30, id FROM auth_permission WHERE codename = 'change_appel';

INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 21, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 22, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 23, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 24, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 25, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 26, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 27, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 28, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 29, id FROM auth_permission WHERE codename = 'can_select_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 30, id FROM auth_permission WHERE codename = 'can_select_candidature';

INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 21, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 22, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 23, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 24, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 25, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 26, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 27, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 28, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 29, id FROM auth_permission WHERE codename = 'can_classe_candidature';
INSERT INTO auth_group_permissions(group_id, permission_id) SELECT 30, id FROM auth_permission WHERE codename = 'can_classe_candidature';

INSERT INTO `www_regionalgroup` VALUES (1, 1);
INSERT INTO `www_regionalgroup` VALUES (2, 2);
INSERT INTO `www_regionalgroup` VALUES (3, 3);
INSERT INTO `www_regionalgroup` VALUES (4, 4);
INSERT INTO `www_regionalgroup` VALUES (5, 5);
INSERT INTO `www_regionalgroup` VALUES (6, 6);
INSERT INTO `www_regionalgroup` VALUES (7, 7);
INSERT INTO `www_regionalgroup` VALUES (8, 8);
INSERT INTO `www_regionalgroup` VALUES (9, 9);
INSERT INTO `www_regionalgroup` VALUES (10, 10);

INSERT INTO `www_regionalgroup` VALUES (11, 1);
INSERT INTO `www_regionalgroup` VALUES (12, 2);
INSERT INTO `www_regionalgroup` VALUES (13, 3);
INSERT INTO `www_regionalgroup` VALUES (14, 4);
INSERT INTO `www_regionalgroup` VALUES (15, 5);
INSERT INTO `www_regionalgroup` VALUES (16, 6);
INSERT INTO `www_regionalgroup` VALUES (17, 7);
INSERT INTO `www_regionalgroup` VALUES (18, 8);
INSERT INTO `www_regionalgroup` VALUES (19, 9);
INSERT INTO `www_regionalgroup` VALUES (20, 10);

INSERT INTO `www_regionalgroup` VALUES (21, 1);
INSERT INTO `www_regionalgroup` VALUES (22, 2);
INSERT INTO `www_regionalgroup` VALUES (23, 3);
INSERT INTO `www_regionalgroup` VALUES (24, 4);
INSERT INTO `www_regionalgroup` VALUES (25, 5);
INSERT INTO `www_regionalgroup` VALUES (26, 6);
INSERT INTO `www_regionalgroup` VALUES (27, 7);
INSERT INTO `www_regionalgroup` VALUES (28, 8);
INSERT INTO `www_regionalgroup` VALUES (29, 9);
INSERT INTO `www_regionalgroup` VALUES (30, 10);
