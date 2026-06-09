DELIMITER $$

CREATE PROCEDURE dned.delete_all_data_by_period(
    IN p_cod_period VARCHAR(50)
)
BEGIN
    DECLARE v_user_workspace_deleted INT DEFAULT 0;
    DECLARE v_user_unit_deleted INT DEFAULT 0;
    DECLARE v_unit_school_deleted INT DEFAULT 0;
    DECLARE v_school_headquarters_deleted INT DEFAULT 0;
    DECLARE v_type_user_deleted INT DEFAULT 0;
    DECLARE v_period_deleted INT DEFAULT 0;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    DELETE FROM dned.user_unit_associate
    WHERE cod_period = p_cod_period;

    SET v_user_unit_deleted = ROW_COUNT();

    DELETE FROM dned.type_user_association
    WHERE cod_period = p_cod_period;

    SET v_type_user_deleted = ROW_COUNT();

    DELETE FROM dned.unit_school_associate
    WHERE cod_period = p_cod_period;

    SET v_unit_school_deleted = ROW_COUNT();

    DELETE FROM dned.school_headquarters_associate
    WHERE cod_period = p_cod_period;

    SET v_school_headquarters_deleted = ROW_COUNT();

    DELETE FROM dned.user_workspace
    WHERE cod_period = p_cod_period;

    SET v_user_workspace_deleted = ROW_COUNT();

    DELETE FROM dned.period
    WHERE cod_period = p_cod_period;

    SET v_period_deleted = ROW_COUNT();

    COMMIT;

    SELECT
        p_cod_period AS cod_period,
        v_user_unit_deleted AS user_unit_associations_deleted,
        v_type_user_deleted AS type_user_associations_deleted,
        v_unit_school_deleted AS unit_school_associations_deleted,
        v_school_headquarters_deleted AS school_headquarters_associations_deleted,
        v_user_workspace_deleted AS user_workspace_deleted,
        v_period_deleted AS period_deleted;
END$$

DELIMITER ;