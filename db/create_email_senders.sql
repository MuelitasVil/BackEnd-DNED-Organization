-- =====================================
-- CARGA GLOBAL (aplica a todas las sedes/organizaciones)
-- =====================================
INSERT INTO email_sender (email, name, org_type, role)
VALUES
('boletin_un@unal.edu.co',               NULL, 'GLOBAL', 'OWNER'),
('comdninfoa_nal@unal.edu.co',           NULL, 'GLOBAL', 'OWNER'),
('enviosvri_nal@unal.edu.co',            NULL, 'GLOBAL', 'OWNER'),
('rectorinforma@unal.edu.co',            NULL, 'GLOBAL', 'OWNER'),
('comunicado_csu_bog@unal.edu.co',       NULL, 'GLOBAL', 'OWNER'),
('reconsejobu_nal@unal.edu.co',          NULL, 'GLOBAL', 'OWNER'),
('dninfoacad_nal@unal.edu.co',           NULL, 'GLOBAL', 'OWNER'),
('dgt_dned@unal.edu.co',                 NULL, 'GLOBAL', 'OWNER'),
('gruposeguridad_nal@unal.edu.co',       NULL, 'GLOBAL', 'OWNER'),
('sisii_nal@unal.edu.co',                NULL, 'GLOBAL', 'OWNER'),
('postmaster_unal@unal.edu.co',          NULL, 'GLOBAL', 'OWNER'),
('postmasterdnia_nal@unal.edu.co',       NULL, 'GLOBAL', 'OWNER'),
('protecdatos_na@unal.edu.co',           NULL, 'GLOBAL', 'OWNER'),
('infraestructurati_dned@unal.edu.co',   NULL, 'GLOBAL', 'OWNER'),
('dre@unal.edu.co',                      NULL, 'GLOBAL', 'OWNER'),
('dned@unal.edu.co',                     NULL, 'GLOBAL', 'OWNER'),
('estudiantilcsu@unal.edu.co',           NULL, 'GLOBAL', 'OWNER'),
('estudiantilca@unal.edu.co',            NULL, 'GLOBAL', 'OWNER')
ON DUPLICATE KEY UPDATE
  name=VALUES(name),
  org_type=VALUES(org_type),
  org_code=NULL,
  sede_code=NULL,
  level='ANY',
  role=VALUES(role),
  is_active=TRUE;

-- =====================================
-- SEDE MEDELLÍN
-- =====================================
INSERT INTO email_sender (email, name, org_type, sede_code, role)
VALUES
('alertas_med@unal.edu.co',                              NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_biblioteca@unal.edu.co',                       NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_comunicaciones@unal.edu.co',                   NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_direccion_administrativa@unal.edu.co',         NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_direccion_laboratorios@unal.edu.co',           NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_fac_ciencias_humanas_y_economicas@unal.edu.co',NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_juridica@unal.edu.co',                         NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('inf_aplicaciones_med@unal.edu.co',                     NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_vicerrectoria@unal.edu.co',                    NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_bienestar_universitario@unal.edu.co',          NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('infservcomp_med@unal.edu.co',                          NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('inflogistica_med@unal.edu.co',                         NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_fac_ciencias@unal.edu.co',                     NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_fac_minas@unal.edu.co',                        NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_fac_ciencias_agrarias@unal.edu.co',            NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('info_aplica_med@unal.edu.co',                          NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_secretaria_sede@unal.edu.co',                  NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('innovaacad_med@unal.edu.co',                           NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('unalternativac_nal@unal.edu.co',                       NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('pcm@unal.edu.co',                                      NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('postmaster_med@unal.edu.co',                           NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('infeducontinua@unal.edu.co',                           NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_direccion_academica@unal.edu.co',              NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_direccion_de_investigacion_y_extension@unal.edu.co', NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_direccion_ordenamiento_y_desarrollo_fisico@unal.edu.co', NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_fac_arquitectura@unal.edu.co',                 NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_registro_y_matricula@unal.edu.co',             NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('informa_unimedios@unal.edu.co',                        NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('infpersonal_med@unal.edu.co',                          NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER'),
('reestudia_med@unal.edu.co',                            NULL, 'HEADQUARTERS', 'SEDE MEDELLÍN ESTUDIANTE', 'OWNER')
ON DUPLICATE KEY UPDATE
  name=COALESCE(VALUES(name), email_sender.name),
  org_type='HEADQUARTERS',
  org_code=NULL,
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  is_active=TRUE;

-- =====================================
-- SEDE MANIZALES
-- =====================================
INSERT INTO email_sender (email, name, org_type, sede_code, role)
VALUES
('ventanilla_man@unal.edu.co',   NULL, 'HEADQUARTERS', 'SEDE MANIZALES ESTUDIANTE', 'OWNER'),
('bienestar_man@unal.edu.co',    NULL, 'HEADQUARTERS', 'SEDE MANIZALES ESTUDIANTE', 'OWNER'),
('planea_man@unal.edu.co',       NULL, 'HEADQUARTERS', 'SEDE MANIZALES ESTUDIANTE', 'OWNER'),
('postmaster_man@unal.edu.co',   NULL, 'HEADQUARTERS', 'SEDE MANIZALES ESTUDIANTE', 'OWNER'),
('vicsede_man@unal.edu.co',      NULL, 'HEADQUARTERS', 'SEDE MANIZALES ESTUDIANTE', 'OWNER'),
('estudiantilcs_man@unal.edu.co',NULL, 'HEADQUARTERS', 'SEDE MANIZALES ESTUDIANTE', 'OWNER')
ON DUPLICATE KEY UPDATE
  name=COALESCE(VALUES(name), email_sender.name),
  org_type='HEADQUARTERS',
  org_code=NULL,
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  is_active=TRUE;

-- =====================================
-- SEDE PALMIRA
-- =====================================
INSERT INTO email_sender (email, name, org_type, sede_code, role)
VALUES
('unnoticias_pal@unal.edu.co',   NULL, 'HEADQUARTERS', 'SEDE PALMIRA ESTUDIANTE', 'OWNER'),
('postmaster_pal@unal.edu.co',   NULL, 'HEADQUARTERS', 'SEDE PALMIRA ESTUDIANTE', 'OWNER'),
('estudiantilcs_pal@unal.edu.co',NULL, 'HEADQUARTERS', 'SEDE PALMIRA ESTUDIANTE', 'OWNER')
ON DUPLICATE KEY UPDATE
  name=COALESCE(VALUES(name), email_sender.name),
  org_type='HEADQUARTERS',
  org_code=NULL,
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  is_active=TRUE;

-- =====================================
-- SEDE ORINOQUÍA
-- =====================================
INSERT INTO email_sender (email, name, org_type, sede_code, role)
VALUES
('divcultural_ori@unal.edu.co',  NULL, 'HEADQUARTERS', 'SEDE ORINOQUÍA ESTUDIANTE', 'OWNER')
ON DUPLICATE KEY UPDATE
  name=COALESCE(VALUES(name), email_sender.name),
  org_type='HEADQUARTERS',
  org_code=NULL,
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  is_active=TRUE;

-- =====================================
-- SEDE DE LA PAZ
-- =====================================
INSERT INTO email_sender (email, name, org_type, sede_code, role)
VALUES
('secsedelapaz@unal.edu.co',     NULL, 'HEADQUARTERS', 'SEDE DE LA PAZ ESTUDIANTE', 'OWNER'),
('sedelapaz@unal.edu.co',        NULL, 'HEADQUARTERS', 'SEDE DE LA PAZ ESTUDIANTE', 'OWNER'),
('tics_paz@unal.edu.co',         NULL, 'HEADQUARTERS', 'SEDE DE LA PAZ ESTUDIANTE', 'OWNER'),
('vicesedelapaz@unal.edu.co',    NULL, 'HEADQUARTERS', 'SEDE DE LA PAZ ESTUDIANTE', 'OWNER')
ON DUPLICATE KEY UPDATE
  name=COALESCE(VALUES(name), email_sender.name),
  org_type='HEADQUARTERS',
  org_code=NULL,
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  is_active=TRUE;

-- =====================================
-- SEDE BOGOTÁ
-- =====================================
INSERT INTO email_sender (email, name, org_type, sede_code, role)
VALUES
('divulgaciondrm_bog@unal.edu.co', NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER'),
('reprecarrera_bog@unal.edu.co',   NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER'),
('comunicaciones_bog@unal.edu.co', NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER'),
('diracasede_bog@unal.edu.co',     NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER'),
('dircultural_bog@unal.edu.co',    NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER'),
('notificass_bog@unal.edu.co',     NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER'),
('postmaster_bog@unal.edu.co',     NULL, 'HEADQUARTERS', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER')
ON DUPLICATE KEY UPDATE
  name=COALESCE(VALUES(name), email_sender.name),
  org_type='HEADQUARTERS',
  org_code=NULL,
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  is_active=TRUE;

-- =====================================
-- FACULTADES (SCHOOL) - BOGOTÁ
-- org_code = Nombre Facultad (según tu diccionario)
-- =====================================
INSERT INTO email_sender (email, name, org_type, org_code, sede_code, role)
VALUES
('correo_fchbog@unal.edu.co', 'Facultad de Ciencias Humanas - Bogotá', 'SCHOOL', 'FACULTAD DE CIENCIAS HUMANAS ESTUDIANTE', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER'),
('correo_fibog@unal.edu.co',  'Facultad de Ingeniería - Bogotá',       'SCHOOL', 'FACULTAD DE INGENIERÍA ESTUDIANTE',       'SEDE BOGOTÁ ESTUDIANTE', 'OWNER'),
('correo_fcbog@unal.edu.co',  'Facultad de Ciencias - Bogotá',         'SCHOOL', 'FACULTAD DE CIENCIAS ESTUDIANTE',          'SEDE BOGOTÁ ESTUDIANTE', 'OWNER'),
('correo_farbog@unal.edu.co', 'Facultad de Artes - Bogotá',            'SCHOOL', 'FACULTAD DE ARTES ESTUDIANTE',             'SEDE BOGOTÁ ESTUDIANTE', 'OWNER'),
('correo_fcebog@unal.edu.co', 'Facultad de Ciencias Económicas - Bogotá','SCHOOL','FACULTAD DE CIENCIAS ECONÓMICAS ESTUDIANTE','SEDE BOGOTÁ ESTUDIANTE','OWNER'),
('correo_fmbog@unal.edu.co',  'Facultad de Medicina - Bogotá',         'SCHOOL', 'FACULTAD DE MEDICINA ESTUDIANTE',          'SEDE BOGOTÁ ESTUDIANTE', 'OWNER'),
('correo_fdbog@unal.edu.co',  'Facultad de Derecho, Ciencias Políticas y Sociales - Bogotá','SCHOOL','FACULTAD DE DERECHO, CIENCIAS POLÍTICAS Y SOCIALES','SEDE BOGOTÁ ESTUDIANTE','OWNER'),
('correo_fmvbog@unal.edu.co', 'Facultad de Medicina Veterinaria y de Zootecnia - Bogotá','SCHOOL','FACULTAD DE MEDICINA VETERINARIA Y DE ZOOTECNIA','SEDE BOGOTÁ ESTUDIANTE','OWNER'),
('correo_fcabog@unal.edu.co', 'Facultad de Ciencias Agrarias - Bogotá','SCHOOL', 'FACULTAD DE CIENCIAS AGRARIAS ESTUDIANTE', 'SEDE BOGOTÁ ESTUDIANTE', 'OWNER'),
('correo_febog@unal.edu.co',  'Facultad de Enfermería - Bogotá',       'SCHOOL', 'FACULTAD DE ENFERMERÍA ESTUDIANTE',        'SEDE BOGOTÁ ESTUDIANTE', 'OWNER'),
('correo_fobog@unal.edu.co',  'Facultad de Odontología - Bogotá',      'SCHOOL', 'FACULTAD DE ODONTOLOGÍA ESTUDIANTE',       'SEDE BOGOTÁ ESTUDIANTE', 'OWNER')
ON DUPLICATE KEY UPDATE
  name=VALUES(name),
  org_type='SCHOOL',
  org_code=VALUES(org_code),
  sede_code=VALUES(sede_code),
  level='ANY',
  role=VALUES(role),
  is_active=TRUE;

