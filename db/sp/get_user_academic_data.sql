DELIMITER //

CREATE PROCEDURE get_user_academic_data(IN p_email_unal VARCHAR(255))
BEGIN
    SELECT 
        u.email_unal,
        u.full_name AS user_name,
        uu.cod_unit,
        uu.name AS unit_name,
        s.cod_school,
        s.name AS school_name,
        h.cod_headquarters,
        h.name AS headquarters_name,
        p.cod_period,
        tua.type_user_name,
        tu.description AS type_user_description
    FROM user_unal u
    INNER JOIN user_unit_associate uua 
        ON u.email_unal = uua.email_unal
    INNER JOIN unit_unal uu 
        ON uua.cod_unit = uu.cod_unit
    INNER JOIN unit_school_associate usa 
        ON uu.cod_unit = usa.cod_unit
    INNER JOIN school s 
        ON usa.cod_school = s.cod_school
    INNER JOIN school_headquarters_associate sha 
        ON s.cod_school = sha.cod_school
    INNER JOIN headquarters h 
        ON sha.cod_headquarters = h.cod_headquarters
    INNER JOIN period p 
        ON uua.cod_period = p.cod_period
        AND usa.cod_period = p.cod_period
        AND sha.cod_period = p.cod_period
    LEFT JOIN type_user_association tua
        ON u.email_unal = tua.email_unal
        AND uua.cod_period = tua.cod_period
    LEFT JOIN type_user tu
        ON tua.type_user_name = tu.name
    WHERE u.email_unal = p_email_unal

    UNION ALL

    SELECT 
        u.email_unal,
        u.full_name AS user_name,
        NULL AS cod_unit,
        NULL AS unit_name,
        NULL AS cod_school,
        NULL AS school_name,
        NULL AS cod_headquarters,
        NULL AS headquarters_name,
        tua.cod_period,
        tua.type_user_name,
        tu.description AS type_user_description
    FROM user_unal u
    INNER JOIN type_user_association tua
        ON u.email_unal = tua.email_unal
    LEFT JOIN type_user tu
        ON tua.type_user_name = tu.name
    WHERE u.email_unal = p_email_unal
        AND NOT EXISTS (
            SELECT 1
            FROM user_unit_associate uua
            WHERE uua.email_unal = u.email_unal
                AND uua.cod_period = tua.cod_period
        );
END //

DELIMITER ;
