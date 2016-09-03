

-----QUERY START HERE ----
-- Table: public.adhoc_hazard_summary
DROP TABLE public.adhoc_predef_hazard_summary;

CREATE TABLE public.adhoc_predef_hazard_summary
(
  id serial primary key,
  id_event integer,
  id_unit bigint,
  kota character varying(50),
  kecamatan character varying(50),
  kelurahan character varying(50),
  rt character varying(3),
  rw character varying(50),
  kelas character varying(2)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.adhoc_predef_hazard_summary
  OWNER TO jaksafe;

-- Table: public.adhoc_predef_dala_result

-- DROP TABLE public.adhoc_predef_dala_result;

CREATE TABLE public.adhoc_predef_dala_result
(
  id serial primary key,
  id_event integer,
  sector character varying(200),
  subsector character varying(200),
  asset character varying(200),
  rw character varying(50),
  kelurahan character varying(100),
  kecamatan character varying(100),
  kota character varying(100),
  kelas character varying(50),
  damage numeric(17,2),
  loss numeric(17,2)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.adhoc_predef_dala_result
  OWNER TO jaksafe;

-- Table: public.adhoc_predef_kota_terdampak

-- DROP TABLE public.adhoc_predef_kota_terdampak;

CREATE TABLE public.adhoc_predef_kota_terdampak
(
  id serial primary key,
  id_event integer,
  provinsi character varying(100),
  kota character varying(100),
  luas_terdampak double precision
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.adhoc_predef_kota_terdampak
  OWNER TO jaksafe;

-- Table: public.adhoc_predef_luas_banjir

-- DROP TABLE public.adhoc_predef_luas_banjir;

CREATE TABLE public.adhoc_predef_luas_banjir
(
  id serial primary key,
  id_event integer,
  luas_banjir double precision,
  jumlah_rw_banjir integer
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.adhoc_predef_luas_banjir
  OWNER TO jaksafe;

-- Table: public.adhoc_predef_dal_asumsi_temp

-- DROP TABLE public.adhoc_predef_dal_asumsi_temp;

CREATE TABLE public.adhoc_predef_dal_asumsi_temp
(
  id serial primary key,
  id_event integer,
  sector character varying(100),
  subsector character varying(100),
  asset character varying(100),
  kelurahan character varying(100),
  kecamatan character varying(100),
  kota character varying(100),
  damage double precision,
  loss double precision
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.adhoc_predef_dal_asumsi_temp
  OWNER TO jaksafe;

 -- Table: public.adhoc_predef_kerusakan_kendaraan

-- DROP TABLE public.adhoc_predef_kerusakan_kendaraan;

CREATE TABLE public.adhoc_predef_kerusakan_kendaraan
(
  id serial,
  id_event integer,
  kerusakan_kendaraan numeric
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.adhoc_predef_kerusakan_kendaraan
  OWNER TO jaksafe;
