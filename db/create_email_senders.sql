-- =====================================
-- CARGA GLOBAL (aplica a todas las sedes/organizaciones)
-- priority = 10
-- =====================================
INSERT INTO email_sender (email, name, org_type, role, priority)
VALUES
('boletin_un@unal.edu.co',               NULL, 'GLOBAL', 'OWNER', 10),
('comdninfoa_nal@unal.edu.co',           NULL, 'GLOBAL', 'OWNER', 10),
('enviosvri_nal@unal.edu.co',            NULL, 'GLOBAL', 'OWNER', 10),
('rectorinforma@unal.edu.co',            NULL, 'GLOBAL', 'OWNER', 10),
('comunicado_csu_bog@unal.edu.co',       NULL, 'GLOBAL', 'OWNER', 10),
('reconsejobu_nal@unal.edu.co',          NULL, 'GLOBAL', 'OWNER', 10),
('dninfoacad_nal@unal.edu.co',           NULL, 'GLOBAL', 'OWNER', 10),
('dgt_dned@unal.edu.co',                 NULL, 'GLOBAL', 'OWNER', 10),
('gruposeguridad_nal@unal.edu.co',       NULL, 'GLOBAL', 'OWNER', 10),
('sisii_nal@unal.edu.co',                NULL, 'GLOBAL', 'OWNER', 10),
('postmaster_unal@unal.edu.co',          NULL, 'GLOBAL', 'OWNER', 10),
('postmasterdnia_nal@unal.edu.co',       NULL, 'GLOBAL', 'OWNER', 10),
('protecdatos_na@unal.edu.co',           NULL, 'GLOBAL', 'OWNER', 10),
('infraestructurati_dned@unal.edu.co',   NULL, 'GLOBAL', 'OWNER', 10),
('dre@unal.edu.co',                      NULL, 'GLOBAL', 'OWNER', 10),
('dned@unal.edu.co',                     NULL, 'GLOBAL', 'OWNER', 10),
('estudiantilcsu@unal.edu.co',           NULL, 'GLOBAL', 'OWNER', 10),
('estudiantilca@unal.edu.co',            NULL, 'GLOBAL', 'OWNER', 10)
ON DUPLICATE KEY UPDATE
  name=VALUES(name),
  org_type=VALUES(org_type),
  org_code=NULL,
  sede_code=NULL,
  level='ANY',
  role=VALUES(role),
  priority=VALUES(priority),
  is_active=TRUE;

-- =====================================
-- SEDE MEDELLÍN
-- priority = 20
-- =====================================
INSERT INTO email_sender (email, name, org_type, sede_code, role, priority)
VALUES
('alertas_med@unal.edu.co',                              NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_biblioteca@unal.edu.co',                       NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_comunicaciones@unal.edu.co',                   NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_direccion_administrativa@unal.edu.co',         NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_direccion_laboratorios@unal.edu.co',           NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_fac_ciencias_humanas_y_economicas@unal.edu.co',NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_juridica@unal.edu.co',                         NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('inf_aplicaciones_med@unal.edu.co',                     NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_vicerrectoria@unal.edu.co',                    NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_bienestar_universitario@unal.edu.co',          NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('infservcomp_med@unal.edu.co',                          NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('inflogistica_med@unal.edu.co',                         NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_fac_ciencias@unal.edu.co',                     NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_fac_minas@unal.edu.co',                        NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_fac_ciencias_agrarias@unal.edu.co',            NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('info_aplica_med@unal.edu.co',                          NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_secretaria_sede@unal.edu.co',                  NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('innovaacad_med@unal.edu.co',                           NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('unalternativac_nal@unal.edu.co',                       NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('pcm@unal.edu.co',                                      NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('postmaster_med@unal.edu.co',                           NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('infeducontinua@unal.edu.co',                           NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_direccion_academica@unal.edu.co',              NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_direccion_de_investigacion_y_extension@unal.edu.co', NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_direccion_ordenamiento_y_desarrollo_fisico@unal.edu.co', NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_fac_arquitectura@unal.edu.co',                 NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_registro_y_matricula@unal.edu.co',             NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('informa_unimedios@unal.edu.co',                        NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('infpersonal_med@unal.edu.co',                          NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20),
('reestudia_med@unal.edu.co',                            NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER', 20)
ON DUPLICATE KEY UPDATE
  name=COALESCE(VALUES(name), email_sender.name),
  org_type='HEADQUARTERS',
  org_code=NULL,
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  priority=VALUES(priority),
  is_active=TRUE;

-- =====================================
-- SEDE MANIZALES
-- priority = 20
-- =====================================
INSERT INTO email_sender (email, name, org_type, sede_code, role, priority)
VALUES
('ventanilla_man@unal.edu.co',   NULL, 'HEADQUARTERS', 'SEDE MANIZALES ESTUDIANTE', 'OWNER', 20),
('bienestar_man@unal.edu.co',    NULL, 'HEADQUARTERS', 'SEDE MANIZALES ESTUDIANTE', 'OWNER', 20),
('planea_man@unal.edu.co',       NULL, 'HEADQUARTERS', 'SEDE MANIZALES ESTUDIANTE', 'OWNER', 20),
('postmaster_man@unal.edu.co',   NULL, 'HEADQUARTERS', 'SEDE MANIZALES ESTUDIANTE', 'OWNER', 20),
('vicsede_man@unal.edu.co',      NULL, 'HEADQUARTERS', 'SEDE MANIZALES ESTUDIANTE', 'OWNER', 20),
('estudiantilcs_man@unal.edu.co',NULL, 'HEADQUARTERS', 'SEDE MANIZALES ESTUDIANTE', 'OWNER', 20)
ON DUPLICATE KEY UPDATE
  name=COALESCE(VALUES(name), email_sender.name),
  org_type='HEADQUARTERS',
  org_code=NULL,
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  priority=VALUES(priority),
  is_active=TRUE;

-- =====================================
-- SEDE PALMIRA
-- priority = 20
-- =====================================
INSERT INTO email_sender (email, name, org_type, sede_code, role, priority)
VALUES
('unnoticias_pal@unal.edu.co',   NULL, 'HEADQUARTERS', 'SEDE PALMIRA ESTUDIANTE', 'OWNER', 20),
('postmaster_pal@unal.edu.co',   NULL, 'HEADQUARTERS', 'SEDE PALMIRA ESTUDIANTE', 'OWNER', 20),
('estudiantilcs_pal@unal.edu.co',NULL, 'HEADQUARTERS', 'SEDE PALMIRA ESTUDIANTE', 'OWNER', 20)
ON DUPLICATE KEY UPDATE
  name=COALESCE(VALUES(name), email_sender.name),
  org_type='HEADQUARTERS',
  org_code=NULL,
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  priority=VALUES(priority),
  is_active=TRUE;

-- =====================================
-- SEDE ORINOQUÍA
-- priority = 20
-- =====================================
INSERT INTO email_sender (email, name, org_type, sede_code, role, priority)
VALUES
('divcultural_ori@unal.edu.co',  NULL, 'HEADQUARTERS', 'SEDE ORINOQUÍA ESTUDIANTE', 'OWNER', 20)
ON DUPLICATE KEY UPDATE
  name=COALESCE(VALUES(name), email_sender.name),
  org_type='HEADQUARTERS',
  org_code=NULL,
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  priority=VALUES(priority),
  is_active=TRUE;

-- =====================================
-- SEDE DE LA PAZ
-- priority = 20
-- =====================================
INSERT INTO email_sender (email, name, org_type, sede_code, role, priority)
VALUES
('secsedelapaz@unal.edu.co',     NULL, 'HEADQUARTERS', 'SEDE DE LA PAZ ESTUDIANTE', 'OWNER', 20),
('sedelapaz@unal.edu.co',        NULL, 'HEADQUARTERS', 'SEDE DE LA PAZ ESTUDIANTE', 'OWNER', 20),
('tics_paz@unal.edu.co',         NULL, 'HEADQUARTERS', 'SEDE DE LA PAZ ESTUDIANTE', 'OWNER', 20),
('vicesedelapaz@unal.edu.co',    NULL, 'HEADQUARTERS', 'SEDE DE LA PAZ ESTUDIANTE', 'OWNER', 20)
ON DUPLICATE KEY UPDATE
  name=COALESCE(VALUES(name), email_sender.name),
  org_type='HEADQUARTERS',
  org_code=NULL,
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  priority=VALUES(priority),
  is_active=TRUE;

-- =====================================
-- SEDE BOGOTÁ
-- priority = 20
-- =====================================
INSERT INTO email_sender (email, name, org_type, sede_code, role, priority)
VALUES
('divulgaciondrm_bog@unal.edu.co', NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 20),
('reprecarrera_bog@unal.edu.co',   NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 20),
('comunicaciones_bog@unal.edu.co', NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 20),
('diracasede_bog@unal.edu.co',     NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 20),
('dircultural_bog@unal.edu.co',    NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 20),
('notificass_bog@unal.edu.co',     NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 20),
('postmaster_bog@unal.edu.co',     NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 20)
ON DUPLICATE KEY UPDATE
  name=COALESCE(VALUES(name), email_sender.name),
  org_type='HEADQUARTERS',
  org_code=NULL,
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  priority=VALUES(priority),
  is_active=TRUE;

-- =====================================
-- FACULTADES (SCHOOL) - BOGOTÁ
-- priority = 30
-- org_code = Nombre Facultad (según tu diccionario)
-- =====================================
INSERT INTO email_sender (email, name, org_type, org_code, sede_code, role, priority)
VALUES
('correo_fchbog@unal.edu.co', 'Facultad de Ciencias Humanas - Bogotá', 'SCHOOL', 'FACULTAD DE CIENCIAS HUMANAS ESTUDIANTE', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 30),
('correo_fibog@unal.edu.co',  'Facultad de Ingeniería - Bogotá',       'SCHOOL', 'FACULTAD DE INGENIERÍA ESTUDIANTE',       'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 30),
('correo_fcbog@unal.edu.co',  'Facultad de Ciencias - Bogotá',         'SCHOOL', 'FACULTAD DE CIENCIAS ESTUDIANTE',          'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 30),
('correo_farbog@unal.edu.co', 'Facultad de Artes - Bogotá',            'SCHOOL', 'FACULTAD DE ARTES ESTUDIANTE',             'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 30),
('correo_fcebog@unal.edu.co', 'Facultad de Ciencias Económicas - Bogotá','SCHOOL','FACULTAD DE CIENCIAS ECONÓMICAS ESTUDIANTE','SEDE BOGOTÁ ESTUDIANTE','OWNER',30),
('correo_fmbog@unal.edu.co',  'Facultad de Medicina - Bogotá',         'SCHOOL', 'FACULTAD DE MEDICINA ESTUDIANTE',          'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 30),
('correo_fdbog@unal.edu.co',  'Facultad de Derecho, Ciencias Políticas y Sociales - Bogotá','SCHOOL','FACULTAD DE DERECHO, CIENCIAS POLÍTICAS Y SOCIALES','SEDE BOGOTÁ ESTUDIANTE','OWNER',30),
('correo_fmvbog@unal.edu.co', 'Facultad de Medicina Veterinaria y de Zootecnia - Bogotá','SCHOOL','FACULTAD DE MEDICINA VETERINARIA Y DE ZOOTECNIA','SEDE BOGOTÁ ESTUDIANTE','OWNER',30),
('correo_fcabog@unal.edu.co', 'Facultad de Ciencias Agrarias - Bogotá','SCHOOL', 'FACULTAD DE CIENCIAS AGRARIAS ESTUDIANTE', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 30),
('correo_febog@unal.edu.co',  'Facultad de Enfermería - Bogotá',       'SCHOOL', 'FACULTAD DE ENFERMERÍA ESTUDIANTE',        'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 30),
('correo_fobog@unal.edu.co',  'Facultad de Odontología - Bogotá',      'SCHOOL', 'FACULTAD DE ODONTOLOGÍA ESTUDIANTE',       'SEDE BOGOTÁ ESTUDIANTE', 'OWNER', 30)
ON DUPLICATE KEY UPDATE
  name=VALUES(name),
  org_type='SCHOOL',
  org_code=VALUES(org_code),
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  priority=VALUES(priority),
  is_active=TRUE;

