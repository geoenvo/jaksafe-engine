BEGIN
/* Get prev t0 */
SELECT t0 INTO @prev_t0 FROM auto_calc WHERE id=NEW.id-1;

/* Get days from time difference */
SELECT DATEDIFF(NEW.t1,NEW.t0) INTO @time_diff FROM auto_calc WHERE id=NEW.id;

/* Get the new id for auto_calc_daily table */
SELECT CONCAT(DATE_FORMAT(t0, '%y'),'',LPAD(MONTH(t0), 2, '0')) INTO @year_month FROM auto_calc WHERE id=NEW.id-1;

/* Get the previous id event from auto_calc table */
SELECT id_event INTO @prev_id_event FROM auto_calc WHERE id=NEW.id-1;

/* Get the latest id for updating auto_calc_daily table */
SELECT MAX(id) INTO @last_id FROM auto_calc_daily;

/* Check whether the auto_calc_daily table is empty */
SELECT COUNT(*) INTO @is_empty FROM auto_calc_daily;

/* Get the new id */
IF @is_empty > 0 THEN
	SET @l_loop = 0;
	loop_id: LOOP
		SET @l_loop = @l_loop + 1;
		SET @add = LPAD(@l_loop,3,'00');
		SET @new_id = CONCAT(@year_month,'',@add);
	
		IF @new_id = @last_id THEN
			SET @new_id = @new_id + 1;
			LEAVE loop_id;
		end IF;
	
		IF @l_loop > 32 THEN
			SET @new_id = CONCAT(@year_month,'','001');
			LEAVE loop_id;
		end IF;

	end LOOP loop_id;
ELSE
	SET @new_id = CONCAT(@year_month,'','001');
END IF;

/* Insert or update the auto_calc_daily table */
IF NEW.id_event IS NOT NULL THEN
	IF @prev_id_event IS NOT NULL THEN
		UPDATE auto_calc_daily
		SET id_event = NEW.id_event, to_date = NEW.t1, day = @time_diff, loss = NEW.loss
		WHERE id = @last_id;
	ELSE
		INSERT INTO auto_calc_daily (id,id_event,from_date,to_date,day,loss)
		VALUES (@new_id,NEW.id_event,NEW.t0, NEW.t1, @time_diff, NEW.loss);
	END IF;
END IF;
END