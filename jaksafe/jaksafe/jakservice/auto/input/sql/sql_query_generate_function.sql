-- GET AFFECTED RW
CREATE OR REPLACE FUNCTION get_auto_rw_affected(event_id int, kelurahan_name text) RETURNS text AS $$
DECLARE
    rws text;
    rw_serial text;
BEGIN
    FOR rws IN SELECT distinct(rw) FROM auto_dala_result a WHERE a.id_event = event_id and a.kelurahan = kelurahan_name order by rw
    LOOP
        rw_serial = concat_ws(', ',rw_serial,rws);
    END LOOP;

    RETURN rw_serial;
END;
$$ LANGUAGE plpgsql;

--SELECT * FROM get_auto_rw_affected(5,'PETOGOGAN');


-- GET DAMAGE PER SECTOR
CREATE OR REPLACE FUNCTION get_auto_damage_sector(event_id int, kelurahan_name text, sector_name text) RETURNS numeric AS $$
DECLARE
    dala numeric;
    damage_return numeric;
BEGIN
    For dala in 
    SELECT sum(a.damage) damage FROM auto_dala_result a WHERE a.id_event = event_id and a.kelurahan = kelurahan_name and a.sector = sector_name
    group by a.sector
    Loop 
      damage_return = dala;
    end loop;  
    return damage_return;
END;
$$ LANGUAGE plpgsql;

-- GET LOSS PER SECTOR
CREATE OR REPLACE FUNCTION get_auto_loss_sector(event_id int, kelurahan_name text, sector_name text) RETURNS numeric AS $$
DECLARE
    dala numeric;
    loss_return numeric;
BEGIN
    For dala in 
    SELECT sum(a.loss) loss FROM auto_dala_result a WHERE a.id_event = event_id and a.kelurahan = kelurahan_name and a.sector = sector_name
    group by a.sector
    Loop 
      loss_return = dala;
    end loop;  
    return loss_return;
END;
$$ LANGUAGE plpgsql;

--GET LOSS
CREATE OR REPLACE FUNCTION get_auto_loss(event_id int, kelurahan_name text) RETURNS numeric AS $$
DECLARE
    dala numeric;
    loss_return numeric;
BEGIN
    For dala in 
    SELECT sum(a.loss) loss FROM auto_dala_result a WHERE a.id_event = event_id and a.kelurahan = kelurahan_name
    group by a.kelurahan
    Loop 
      loss_return = dala;
    end loop;  
    return loss_return;
END;
$$ LANGUAGE plpgsql;

---GET DAMAGE
CREATE OR REPLACE FUNCTION get_auto_damage(event_id int, kelurahan_name text) RETURNS numeric AS $$
DECLARE
    dala numeric;
    damage_return numeric;
BEGIN
    For dala in 
    SELECT sum(a.damage) damage FROM auto_dala_result a WHERE a.id_event = event_id and a.kelurahan = kelurahan_name 
    group by a.kelurahan
    Loop 
      damage_return = dala;
    end loop;  
    return damage_return;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION auto_dala_json(event_id int, event_date timestamp with time zone);
CREATE OR REPLACE FUNCTION auto_dala_json(event_id int, event_date timestamp with time zone)
  RETURNS TABLE (
	id text,
	kelurahan_id text,
	kota varchar(100),
	kecamatan varchar(100),
	kelurahan varchar(100),
	rw text,
	tanggal text,
	damage_infrastruktur numeric,
	loss_infrastruktur numeric,
	damage_lintas_sektor numeric,
	loss_lintas_sektor numeric,
	damage_produktif numeric,
	loss_produktif numeric,
	damage_sosial_perumahan numeric,
	loss_sosial_perumahan numeric,
	damage_total numeric,
	loss_total numeric,
	sumber text) AS
$func$
BEGIN
   RETURN QUERY
   SELECT 
        substr(to_char(id_unit,'9999999999999999'),2,10) id,
	substr(to_char(id_unit,'9999999999999999'),2,10) kelurahan_id, 
	a.kota,
	a.kecamatan,
	a.kelurahan,
	get_auto_rw_affected(a.id_event,a.kelurahan) rw,
	to_char(event_date, 'yyyy-mm-dd hh24:mi:ss') tanggal,
	get_auto_damage_sector(a.id_event,a.kelurahan,'INFRASTRUKTUR') damage_infrastruktur,
	get_auto_loss_sector(a.id_event,a.kelurahan,'INFRASTRUKTUR') loss_infrastruktur,
	get_auto_damage_sector(a.id_event,a.kelurahan,'LINTAS SEKTOR') damage_lintas_sektor,
	get_auto_loss_sector(a.id_event,a.kelurahan,'LINTAS SEKTOR') loss_lintas_sektor,
	get_auto_damage_sector(a.id_event,a.kelurahan,'PRODUKTIF') damage_produktif,
	get_auto_loss_sector(a.id_event,a.kelurahan,'PRODUKTIF') loss_produktif,
	get_auto_damage_sector(a.id_event,a.kelurahan,'SOSIAL DAN PERUMAHAN') damage_sosial_perumahan,
	get_auto_loss_sector(a.id_event,a.kelurahan,'SOSIAL DAN PERUMAHAN') loss_sosial_perumahan,
	get_auto_damage(a.id_event,a.kelurahan) damage_total,
	get_auto_loss(a.id_event,a.kelurahan) loss_total,
	'http://jaksafe.bpbd.jakarta.go.id/report/auto_report/'||a.id_event||'/' sumber
    FROM auto_dala_result a 
	JOIN auto_hazard_summary b 
	ON(a.kelurahan=b.kelurahan) 
    WHERE a.id_event = event_id
    GROUP BY a.id_event, a.kelurahan, a.kecamatan, a.kota, kelurahan_id
    ORDER BY kelurahan_id;
END
$func$  LANGUAGE plpgsql;

DROP FUNCTION auto_dala_json(event_id int, event_date timestamp without time zone);
CREATE OR REPLACE FUNCTION auto_dala_json(event_id int, event_date timestamp without time zone)
  RETURNS TABLE (
	id text,
	kelurahan_id text,
	kota varchar(100),
	kecamatan varchar(100),
	kelurahan varchar(100),
	rw text,
	tanggal text,
	damage_infrastruktur numeric,
	loss_infrastruktur numeric,
	damage_lintas_sektor numeric,
	loss_lintas_sektor numeric,
	damage_produktif numeric,
	loss_produktif numeric,
	damage_sosial_perumahan numeric,
	loss_sosial_perumahan numeric,
	damage_total numeric,
	loss_total numeric,
	sumber text) AS
$func$
BEGIN
   RETURN QUERY
   SELECT 
        substr(to_char(id_unit,'9999999999999999'),2,10) id,
	substr(to_char(id_unit,'9999999999999999'),2,10) kelurahan_id, 
	a.kota,
	a.kecamatan,
	a.kelurahan,
	get_auto_rw_affected(a.id_event,a.kelurahan) rw,
	to_char(event_date, 'yyyy-mm-dd hh24:mi:ss') tanggal,
	get_auto_damage_sector(a.id_event,a.kelurahan,'INFRASTRUKTUR') damage_infrastruktur,
	get_auto_loss_sector(a.id_event,a.kelurahan,'INFRASTRUKTUR') loss_infrastruktur,
	get_auto_damage_sector(a.id_event,a.kelurahan,'LINTAS SEKTOR') damage_lintas_sektor,
	get_auto_loss_sector(a.id_event,a.kelurahan,'LINTAS SEKTOR') loss_lintas_sektor,
	get_auto_damage_sector(a.id_event,a.kelurahan,'PRODUKTIF') damage_produktif,
	get_auto_loss_sector(a.id_event,a.kelurahan,'PRODUKTIF') loss_produktif,
	get_auto_damage_sector(a.id_event,a.kelurahan,'SOSIAL DAN PERUMAHAN') damage_sosial_perumahan,
	get_auto_loss_sector(a.id_event,a.kelurahan,'SOSIAL DAN PERUMAHAN') loss_sosial_perumahan,
	get_auto_damage(a.id_event,a.kelurahan) damage_total,
	get_auto_loss(a.id_event,a.kelurahan) loss_total,
	'http://jaksafe.bpbd.jakarta.go.id/report/auto_report/'||a.id_event||'/' sumber
    FROM auto_dala_result a 
	JOIN auto_hazard_summary b 
	ON(a.kelurahan=b.kelurahan) 
    WHERE a.id_event = event_id
    GROUP BY a.id_event, a.kelurahan, a.kecamatan, a.kota, kelurahan_id
    ORDER BY kelurahan_id;
END
$func$  LANGUAGE plpgsql;


--SELECT * FROM auto_dala_json(174, '2014-11-25T23:15:00+00:00')