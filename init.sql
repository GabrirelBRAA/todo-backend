--
-- PostgreSQL database dump
--

-- Dumped from database version 17.6 (Debian 17.6-1.pgdg13+1)
-- Dumped by pg_dump version 17.5

-- Started on 2025-09-23 15:24:08 -03

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 16402)
-- Name: item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item (
    id character varying(36) NOT NULL,
    title character varying NOT NULL,
    description character varying NOT NULL,
    user_id character varying(36) NOT NULL
);


ALTER TABLE public.item OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16408)
-- Name: itemtag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itemtag (
    item_id character varying(36) NOT NULL,
    tag_id character varying(36) NOT NULL
);


ALTER TABLE public.itemtag OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16405)
-- Name: tag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tag (
    id character varying(36) NOT NULL
);


ALTER TABLE public.tag OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16388)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    firstname character varying NOT NULL,
    lastname character varying NOT NULL,
    role integer DEFAULT 0 NOT NULL,
    hash character varying NOT NULL,
    id character varying(36) NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- TOC entry 3293 (class 2606 OID 16436)
-- Name: item item_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_pk PRIMARY KEY (id);


--
-- TOC entry 3297 (class 2606 OID 16460)
-- Name: itemtag itemtag_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itemtag
    ADD CONSTRAINT itemtag_pk PRIMARY KEY (item_id, tag_id);


--
-- TOC entry 3295 (class 2606 OID 16471)
-- Name: tag tag_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_pk PRIMARY KEY (id);


--
-- TOC entry 3287 (class 2606 OID 16482)
-- Name: user user_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pk PRIMARY KEY (id);


--
-- TOC entry 3289 (class 2606 OID 16497)
-- Name: user user_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_unique UNIQUE (username);


--
-- TOC entry 3291 (class 2606 OID 16499)
-- Name: user user_unique_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_unique_email UNIQUE (email);


--
-- TOC entry 3298 (class 2606 OID 16491)
-- Name: item item_user_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_user_fk FOREIGN KEY (user_id) REFERENCES public."user"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3299 (class 2606 OID 16448)
-- Name: itemtag itemtag_item_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itemtag
    ADD CONSTRAINT itemtag_item_fk FOREIGN KEY (item_id) REFERENCES public.item(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3300 (class 2606 OID 16472)
-- Name: itemtag itemtag_tag_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itemtag
    ADD CONSTRAINT itemtag_tag_fk FOREIGN KEY (tag_id) REFERENCES public.tag(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2025-09-23 15:24:09 -03

--
-- PostgreSQL database dump complete
--

