DROP PROCEDURE IF EXISTS get_email_list_of_school;
DELIMITER //
CREATE PROCEDURE get_email_list_of_school (
    IN p_cod_school VARCHAR(50),
    IN p_cod_period VARCHAR(50)
)
BEGIN
    -- Miembros: Usuarios asociados a la escuela
    SELECT DISTINCT u.email AS email, 'MEMBER' AS tipo
    FROM unit_unal u
    JOIN unit_school_associate usa
      ON usa.cod_unit   = u.cod_unit
     AND usa.cod_school = p_cod_school
     AND usa.cod_period = p_cod_period
    WHERE u.email IS NOT NULL AND u.email <> ''

    UNION ALL

    -- Propietarios: Emisores asociados a la escuela
    SELECT DISTINCT ess.sender_id AS email, 'OWNER' AS tipo
    FROM email_sender_school ess
    WHERE ess.cod_school = p_cod_school

    ORDER BY tipo DESC;  -- 'OWNER' primero y 'MEMBER' después
END //
DELIMITER ;
