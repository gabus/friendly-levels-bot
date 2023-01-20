CREATE OR REPLACE FUNCTION public.update_duration_time()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    NEW.duration_time = EXTRACT(EPOCH FROM (now() - new.created_at));
  RETURN NEW;
END; $function$
;

-- public.channels definition

-- Drop table

-- DROP TABLE public.channels;

CREATE TABLE public.channels (
	id int8 NOT NULL,
	"name" varchar NOT NULL,
	guild_id int8 NOT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	CONSTRAINT channels_un UNIQUE (id)
);


-- public.guilds definition

-- Drop table

-- DROP TABLE public.guilds;

CREATE TABLE public.guilds (
	id int8 NOT NULL,
	"name" varchar NOT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	CONSTRAINT guilds_un UNIQUE (id)
);


-- public.members definition

-- Drop table

-- DROP TABLE public.members;

CREATE TABLE public.members (
	id int8 NOT NULL,
	"name" varchar NOT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	CONSTRAINT members_un UNIQUE (id)
);


-- public.messages definition

-- Drop table

-- DROP TABLE public.messages;

CREATE TABLE public.messages (
	message varchar NULL,
	member_id int8 NOT NULL,
	channel_id int8 NOT NULL,
	created_at timestamp NOT NULL DEFAULT now()
);


-- public.reactions definition

-- Drop table

-- DROP TABLE public.reactions;

CREATE TABLE public.reactions (
	emoji varchar NULL,
	member_id int8 NOT NULL,
	channel_id int8 NOT NULL,
	created_at timestamp NOT NULL DEFAULT now()
);


-- public.voip definition

-- Drop table

-- DROP TABLE public.voip;

CREATE TABLE public.voip (
	member_id int8 NOT NULL,
	voip_channel_id int8 NOT NULL,
	is_open bool NOT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	duration_time int4 NULL,
	guild_id int8 NOT NULL
);


-- public.level_weights definition

-- Drop table

-- DROP TABLE public.level_weights;

CREATE TABLE public.level_weights (
	guild_id int8 NOT NULL,
	message_weight float4 NOT NULL DEFAULT 1,
	reaction_weight float4 NOT NULL DEFAULT 2,
	voip_weight float4 NOT NULL DEFAULT 0.2,
	playing_weight float4 NOT NULL DEFAULT 0,
	CONSTRAINT level_weights_un UNIQUE (guild_id)
);


-- public.games definition

-- Drop table

-- DROP TABLE public.games;

CREATE TABLE public.games (
	id int8 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT games_un UNIQUE (id)
);


-- public.member_playing definition

-- Drop table

-- DROP TABLE public.member_playing;

CREATE TABLE public.member_playing (
	member_id int8 NOT NULL,
	game_id int8 NOT NULL,
	is_playing bool NOT NULL DEFAULT false,
	duration_time int4 NULL,
	created_at timestamp NOT NULL DEFAULT now()
);


-- Table Triggers

create trigger update_duration_time_on_update_for_voip before
update
    on
    public.voip for each row execute function update_duration_time();
