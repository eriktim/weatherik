--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Name: source_knmi_id_seq; Type: SEQUENCE; Schema: public; Owner: weatherik_user
--

CREATE SEQUENCE source_knmi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE source_knmi_id_seq OWNER TO weatherik_user;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: source_knmi; Type: TABLE; Schema: public; Owner: weatherik_user; Tablespace: 
--

CREATE TABLE source_knmi (
    id integer DEFAULT nextval('source_knmi_id_seq'::regclass) NOT NULL,
    url character varying(128) NOT NULL,
    date date NOT NULL,
    url_timestamp timestamp without time zone NOT NULL,
    day smallint NOT NULL,
    temperature_average real,
    temperature_maximum real,
    temperature_minimum real,
    rain_amount real,
    rain_duration real,
    sunshine_duration real,
    sunshine_relative smallint,
    sky_coverage smallint,
    sky_visibiliy real,
    wind_speed_average real,
    wind_speed_maximum_average real,
    wind_speed_maximum real,
    wind_direction smallint,
    atmosphere_humidity smallint,
    atmosphere_pressure real
);


ALTER TABLE source_knmi OWNER TO weatherik_user;

--
-- Name: source_weeronline_id_seq; Type: SEQUENCE; Schema: public; Owner: weatherik_user
--

CREATE SEQUENCE source_weeronline_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE source_weeronline_id_seq OWNER TO weatherik_user;

--
-- Name: source_weeronline; Type: TABLE; Schema: public; Owner: weatherik_user; Tablespace: 
--

CREATE TABLE source_weeronline (
    id integer DEFAULT nextval('source_weeronline_id_seq'::regclass) NOT NULL,
    url character varying(128) NOT NULL,
    date date NOT NULL,
    url_timestamp timestamp without time zone NOT NULL,
    day smallint NOT NULL,
    temperature_minimum smallint,
    temperature_maximum smallint,
    wind_force smallint,
    wind_direction character varying(2),
    rain_percentage smallint,
    rain_amount real,
    rating smallint,
    icon_1 character varying(64),
    icon_2 character varying(64),
    icon_3 character varying(64)
);


ALTER TABLE source_weeronline OWNER TO weatherik_user;

--
-- Name: source_yr_id_seq; Type: SEQUENCE; Schema: public; Owner: weatherik_user
--

CREATE SEQUENCE source_yr_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE source_yr_id_seq OWNER TO weatherik_user;

--
-- Name: source_yr; Type: TABLE; Schema: public; Owner: weatherik_user; Tablespace: 
--

CREATE TABLE source_yr (
    id integer DEFAULT nextval('source_yr_id_seq'::regclass) NOT NULL,
    url character varying(128) NOT NULL,
    date date NOT NULL,
    url_timestamp timestamp without time zone NOT NULL,
    day smallint NOT NULL,
    temperature_average_1 smallint,
    temperature_average_2 smallint,
    temperature_average_3 smallint,
    temperature_average_4 smallint,
    rain_amount_1 real,
    rain_amount_2 real,
    rain_amount_3 real,
    rain_amount_4 real,
    wind_speed_1 smallint,
    wind_speed_2 smallint,
    wind_speed_3 smallint,
    wind_speed_4 smallint,
    wind_direction_1 character varying(32),
    wind_direction_2 character varying(32),
    wind_direction_3 character varying(32),
    wind_direction_4 character varying(32),
    icon_1 character varying(64),
    icon_2 character varying(64),
    icon_3 character varying(64),
    icon_4 character varying(64)
);


ALTER TABLE source_yr OWNER TO weatherik_user;

--
-- Data for Name: source_knmi; Type: TABLE DATA; Schema: public; Owner: weatherik_user
--

COPY source_knmi (id, url, date, url_timestamp, day, temperature_average, temperature_maximum, temperature_minimum, rain_amount, rain_duration, sunshine_duration, sunshine_relative, sky_coverage, sky_visibiliy, wind_speed_average, wind_speed_maximum_average, wind_speed_maximum, wind_direction, atmosphere_humidity, atmosphere_pressure) FROM stdin;
\.


--
-- Name: source_knmi_id_seq; Type: SEQUENCE SET; Schema: public; Owner: weatherik_user
--

SELECT pg_catalog.setval('source_knmi_id_seq', 1, false);


--
-- Data for Name: source_weeronline; Type: TABLE DATA; Schema: public; Owner: weatherik_user
--

COPY source_weeronline (id, url, date, url_timestamp, day, temperature_minimum, temperature_maximum, wind_force, wind_direction, rain_percentage, rain_amount, rating, icon_1, icon_2, icon_3) FROM stdin;
\.


--
-- Name: source_weeronline_id_seq; Type: SEQUENCE SET; Schema: public; Owner: weatherik_user
--

SELECT pg_catalog.setval('source_weeronline_id_seq', 1, false);


--
-- Data for Name: source_yr; Type: TABLE DATA; Schema: public; Owner: weatherik_user
--

COPY source_yr (id, url, date, url_timestamp, day, temperature_average_1, temperature_average_2, temperature_average_3, temperature_average_4, rain_amount_1, rain_amount_2, rain_amount_3, rain_amount_4, wind_speed_1, wind_speed_2, wind_speed_3, wind_speed_4, wind_direction_1, wind_direction_2, wind_direction_3, wind_direction_4, icon_1, icon_2, icon_3, icon_4) FROM stdin;
\.


--
-- Name: source_yr_id_seq; Type: SEQUENCE SET; Schema: public; Owner: weatherik_user
--

SELECT pg_catalog.setval('source_yr_id_seq', 1, false);


--
-- Name: source_knmi_pkey; Type: CONSTRAINT; Schema: public; Owner: weatherik_user; Tablespace: 
--

ALTER TABLE ONLY source_knmi
    ADD CONSTRAINT source_knmi_pkey PRIMARY KEY (id);


--
-- Name: source_weeronline_pkey; Type: CONSTRAINT; Schema: public; Owner: weatherik_user; Tablespace: 
--

ALTER TABLE ONLY source_weeronline
    ADD CONSTRAINT source_weeronline_pkey PRIMARY KEY (id);


--
-- Name: source_yr_pkey; Type: CONSTRAINT; Schema: public; Owner: weatherik_user; Tablespace: 
--

ALTER TABLE ONLY source_yr
    ADD CONSTRAINT source_yr_pkey PRIMARY KEY (id);


--
-- Name: source_knmi_day; Type: INDEX; Schema: public; Owner: weatherik_user; Tablespace: 
--

CREATE INDEX source_knmi_day ON source_knmi USING btree (day);


--
-- Name: source_weeronline_day; Type: INDEX; Schema: public; Owner: weatherik_user; Tablespace: 
--

CREATE INDEX source_weeronline_day ON source_weeronline USING btree (day);


--
-- Name: source_yr_day; Type: INDEX; Schema: public; Owner: weatherik_user; Tablespace: 
--

CREATE INDEX source_yr_day ON source_yr USING btree (day);


--
-- PostgreSQL database dump complete
--

