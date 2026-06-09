DROP PROCEDURE IF EXISTS get_email_list_of_unit;
DELIMITER //
CREATE PROCEDURE get_email_list_of_unit (
    IN p_cod_unit   VARCHAR(50),
    IN p_cod_period VARCHAR(50)
)
BEGIN
    SET p_cod_unit   := TRIM(LOWER(p_cod_unit));
    SET p_cod_period := TRIM(LOWER(p_cod_period));

    -- Miembros: Usuarios asociados a la unidad en el periodo
    SELECT DISTINCT
        TRIM(LOWER(esu.sender_id)) AS email,  -- Correo del propietario
        'OWNER' AS tipo                     -- Tipo: Propietario
    FROM email_sender_unit esu
    WHERE TRIM(LOWER(esu.cod_unit)) = p_cod_unit  -- Relación por código de unidad
    AND esu.sender_id IS NOT NULL
    AND esu.sender_id <> ''  -- Asegura que no sea un correo vacío

    UNION ALL

    -- Miembros: Usuarios asociados a la unidad en el periodo
    SELECT DISTINCT
        TRIM(LOWER(uu.email_unal)) AS email,  -- Correo de los miembros
        'MEMBER' AS tipo                -- Tipo: Miembro
    FROM user_unal uu
    INNER JOIN user_unit_associate uua
        ON TRIM(LOWER(uua.email_unal)) = TRIM(LOWER(uu.email_unal))  -- Relación por email
       AND TRIM(LOWER(uua.cod_unit))   = p_cod_unit                   -- Relación por unidad
       AND TRIM(LOWER(uua.cod_period)) = p_cod_period                 -- Relación por periodo
    WHERE uu.email_unal IS NOT NULL AND uu.email_unal <> ''

    ORDER BY tipo DESC;  -- 'OWNER' primero y 'MEMBER' después
END //
DELIMITER ;
