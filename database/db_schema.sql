-- DROP SCHEMA public;

-- CREATE SCHEMA public AUTHORIZATION pg_database_owner;

-- DROP SEQUENCE public.dataset_id_seq;

CREATE SEQUENCE public.dataset_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.file_id_seq;

CREATE SEQUENCE public.file_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.file_profile_id_seq;

CREATE SEQUENCE public.file_profile_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.projeto_id_seq;

CREATE SEQUENCE public.projeto_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.user_id_seq;

CREATE SEQUENCE public.user_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.version_id_seq;

CREATE SEQUENCE public.version_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.version_profile_id_seq;

CREATE SEQUENCE public.version_profile_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;-- public.dataset definição

-- Drop table

-- DROP TABLE public.dataset;

CREATE TABLE public.dataset (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	description text NULL,
	CONSTRAINT datasets_pk PRIMARY KEY (id)
);


-- public.projeto definição

-- Drop table

-- DROP TABLE public.projeto;

CREATE TABLE public.projeto (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NOT NULL,
	description text NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT projeto_pk PRIMARY KEY (id)
);


-- public."user" definição

-- Drop table

-- DROP TABLE public."user";

CREATE TABLE public."user" (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT user_pk PRIMARY KEY (id)
);


-- public."version" definição

-- Drop table

-- DROP TABLE public."version";

CREATE TABLE public."version" (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	dataset_id int8 NOT NULL,
	version_number int4 NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT version_pk PRIMARY KEY (id),
	CONSTRAINT version_dataset_fk FOREIGN KEY (dataset_id) REFERENCES public.dataset(id)
);


-- public.version_profile definição

-- Drop table

-- DROP TABLE public.version_profile;

CREATE TABLE public.version_profile (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	version_id int8 NOT NULL,
	created_at timestamp NOT NULL,
	n_files int8 NOT NULL,
	CONSTRAINT version_profile_pk PRIMARY KEY (id),
	CONSTRAINT version_profile_version_fk FOREIGN KEY (version_id) REFERENCES public."version"(id)
);


-- public.version_to_projeto definição

-- Drop table

-- DROP TABLE public.version_to_projeto;

CREATE TABLE public.version_to_projeto (
	version_id int8 NOT NULL,
	projeto_id int8 NOT NULL,
	CONSTRAINT version_to_projeto_pk PRIMARY KEY (version_id, projeto_id),
	CONSTRAINT version_to_projeto_projeto_fk FOREIGN KEY (projeto_id) REFERENCES public.projeto(id),
	CONSTRAINT version_to_projeto_version_fk FOREIGN KEY (version_id) REFERENCES public."version"(id)
);


-- public.version_to_user definição

-- Drop table

-- DROP TABLE public.version_to_user;

CREATE TABLE public.version_to_user (
	user_id int8 NOT NULL,
	"role" varchar NULL,
	version_id int8 NOT NULL,
	CONSTRAINT version_to_user_pk PRIMARY KEY (user_id, version_id),
	CONSTRAINT version_to_user_user_fk FOREIGN KEY (user_id) REFERENCES public."user"(id),
	CONSTRAINT version_to_user_version_fk FOREIGN KEY (version_id) REFERENCES public."version"(id)
);


-- public.file definição

-- Drop table

-- DROP TABLE public.file;

CREATE TABLE public.file (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	version_id int8 NOT NULL,
	storage_path varchar NOT NULL,
	file_type varchar NOT NULL,
	hash varchar NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT file_pk PRIMARY KEY (id),
	CONSTRAINT file_version_fk FOREIGN KEY (version_id) REFERENCES public."version"(id)
);


-- public.file_profile definição

-- Drop table

-- DROP TABLE public.file_profile;

CREATE TABLE public.file_profile (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	file_id int8 NOT NULL,
	n_columns int4 NULL,
	n_rows int4 NULL,
	CONSTRAINT file_profile_pk PRIMARY KEY (id),
	CONSTRAINT file_profile_file_fk FOREIGN KEY (file_id) REFERENCES public.file(id)
);