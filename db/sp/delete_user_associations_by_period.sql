DELIMITER $$

CREATE PROCEDURE dned.delete_user_associations_by_period(
    IN p_email_unal VARCHAR(100),
    IN p_cod_period VARCHAR(50)
)
BEGIN
    DECLARE v_deleted_user_units INT DEFAULT 0;
    DECLARE v_deleted_type_users INT DEFAULT 0;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    DELETE FROM dned.user_unit_associate
    WHERE email_unal = p_email_unal
      AND cod_period = p_cod_period;

    SET v_deleted_user_units = ROW_COUNT();

    DELETE FROM dned.type_user_association
    WHERE email_unal = p_email_unal
      AND cod_period = p_cod_period;

    SET v_deleted_type_users = ROW_COUNT();

    COMMIT;

    SELECT 
        p_email_unal AS email_unal,
        p_cod_period AS cod_period,
        v_deleted_user_units AS user_unit_associations_deleted,
        v_deleted_type_users AS type_user_associations_deleted,
        v_deleted_user_units + v_deleted_type_users AS total_deleted;
END$$

DELIMITER ;