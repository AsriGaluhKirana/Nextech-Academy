PGDMP         7                {            courseonline    15.3    15.3      "           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            #           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            $           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            %           1262    16978    courseonline    DATABASE     �   CREATE DATABASE courseonline WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Indonesia.1252';
    DROP DATABASE courseonline;
                postgres    false            �            1259    18174    course    TABLE     �   CREATE TABLE public.course (
    id character varying NOT NULL,
    nama character varying NOT NULL,
    deskripsi character varying NOT NULL
);
    DROP TABLE public.course;
       public         heap    postgres    false            �            1259    18182 
   coursedata    TABLE     �   CREATE TABLE public.coursedata (
    id integer NOT NULL,
    user_id character varying,
    course_id character varying,
    status character varying NOT NULL
);
    DROP TABLE public.coursedata;
       public         heap    postgres    false            �            1259    18181    coursedata_id_seq    SEQUENCE     �   CREATE SEQUENCE public.coursedata_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.coursedata_id_seq;
       public          postgres    false    217            &           0    0    coursedata_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.coursedata_id_seq OWNED BY public.coursedata.id;
          public          postgres    false    216            �            1259    18167    pengguna    TABLE     �   CREATE TABLE public.pengguna (
    id character varying NOT NULL,
    nama character varying,
    password character varying NOT NULL,
    role character varying NOT NULL,
    username character varying,
    contact character varying
);
    DROP TABLE public.pengguna;
       public         heap    postgres    false            �            1259    18239    pengguna_id_seq    SEQUENCE     x   CREATE SEQUENCE public.pengguna_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.pengguna_id_seq;
       public          postgres    false            �            1259    18201 
   prequisite    TABLE     �   CREATE TABLE public.prequisite (
    id integer NOT NULL,
    course_id character varying,
    prequisite_id character varying
);
    DROP TABLE public.prequisite;
       public         heap    postgres    false            �            1259    18200    prequisite_id_seq    SEQUENCE     �   CREATE SEQUENCE public.prequisite_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.prequisite_id_seq;
       public          postgres    false    219            '           0    0    prequisite_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.prequisite_id_seq OWNED BY public.prequisite.id;
          public          postgres    false    218            �            1259    18231    viewtopcourse    VIEW     �   CREATE VIEW public.viewtopcourse AS
 SELECT count(a.nama) AS jumlah,
    a.nama
   FROM (public.course a
     LEFT JOIN public.coursedata b ON (((a.id)::text = (b.course_id)::text)))
  GROUP BY a.nama
  ORDER BY (count(a.nama)) DESC
 LIMIT 5;
     DROP VIEW public.viewtopcourse;
       public          postgres    false    215    215    217            �            1259    18235    viewtopstudent    VIEW     �   CREATE VIEW public.viewtopstudent AS
 SELECT count(a.nama) AS jumlah,
    a.nama
   FROM (public.pengguna a
     LEFT JOIN public.coursedata b ON (((a.id)::text = (b.user_id)::text)))
  GROUP BY a.nama
  ORDER BY (count(b.status)) DESC
 LIMIT 5;
 !   DROP VIEW public.viewtopstudent;
       public          postgres    false    217    214    214    217            {           2604    18185    coursedata id    DEFAULT     n   ALTER TABLE ONLY public.coursedata ALTER COLUMN id SET DEFAULT nextval('public.coursedata_id_seq'::regclass);
 <   ALTER TABLE public.coursedata ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    217    217            |           2604    18204    prequisite id    DEFAULT     n   ALTER TABLE ONLY public.prequisite ALTER COLUMN id SET DEFAULT nextval('public.prequisite_id_seq'::regclass);
 <   ALTER TABLE public.prequisite ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    218    219                      0    18174    course 
   TABLE DATA           5   COPY public.course (id, nama, deskripsi) FROM stdin;
    public          postgres    false    215   �$                 0    18182 
   coursedata 
   TABLE DATA           D   COPY public.coursedata (id, user_id, course_id, status) FROM stdin;
    public          postgres    false    217   )                 0    18167    pengguna 
   TABLE DATA           O   COPY public.pengguna (id, nama, password, role, username, contact) FROM stdin;
    public          postgres    false    214   E)                 0    18201 
   prequisite 
   TABLE DATA           B   COPY public.prequisite (id, course_id, prequisite_id) FROM stdin;
    public          postgres    false    219   �)       (           0    0    coursedata_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.coursedata_id_seq', 68, true);
          public          postgres    false    216            )           0    0    pengguna_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.pengguna_id_seq', 3, true);
          public          postgres    false    222            *           0    0    prequisite_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.prequisite_id_seq', 4, true);
          public          postgres    false    218            �           2606    18180    course course_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.course
    ADD CONSTRAINT course_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.course DROP CONSTRAINT course_pkey;
       public            postgres    false    215            �           2606    18189    coursedata coursedata_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.coursedata
    ADD CONSTRAINT coursedata_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.coursedata DROP CONSTRAINT coursedata_pkey;
       public            postgres    false    217            ~           2606    18173    pengguna pengguna_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.pengguna
    ADD CONSTRAINT pengguna_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.pengguna DROP CONSTRAINT pengguna_pkey;
       public            postgres    false    214            �           2606    18208    prequisite prequisite_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.prequisite
    ADD CONSTRAINT prequisite_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.prequisite DROP CONSTRAINT prequisite_pkey;
       public            postgres    false    219            �           2606    18195 $   coursedata coursedata_course_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.coursedata
    ADD CONSTRAINT coursedata_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.course(id);
 N   ALTER TABLE ONLY public.coursedata DROP CONSTRAINT coursedata_course_id_fkey;
       public          postgres    false    217    215    3200            �           2606    18190 "   coursedata coursedata_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.coursedata
    ADD CONSTRAINT coursedata_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.pengguna(id);
 L   ALTER TABLE ONLY public.coursedata DROP CONSTRAINT coursedata_user_id_fkey;
       public          postgres    false    3198    217    214            �           2606    18209 $   prequisite prequisite_course_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.prequisite
    ADD CONSTRAINT prequisite_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.course(id);
 N   ALTER TABLE ONLY public.prequisite DROP CONSTRAINT prequisite_course_id_fkey;
       public          postgres    false    219    215    3200            �           2606    18214 (   prequisite prequisite_prequisite_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.prequisite
    ADD CONSTRAINT prequisite_prequisite_id_fkey FOREIGN KEY (prequisite_id) REFERENCES public.course(id);
 R   ALTER TABLE ONLY public.prequisite DROP CONSTRAINT prequisite_prequisite_id_fkey;
       public          postgres    false    219    215    3200               %  x��UMS�6=�_�#T��w�d7�e��T��K��xɒK��f}�$�,�ra���~��������bcH�g/n(���.�S�˞vԳhȑ���~�"S�'���R�d�#�Yژ����8��,>��6���n4�,�4�t=He��/��ߩ�v(E5�S�FLS��⓭��xqr��� �J8������D�a��F��~�$��L��4�j�jړ�ժ��h¨������k�=�(�E��� ��*�V�,�� }�%��?���ŭ	Rk�i$:��D�"���7B���ęgp>D�A2���e_S&׶R���ؘ�D"��4PP)8Q���� ���4!>����tg���@��tO�j�W�j��PS�	E��A�;ϙ�8��_d-ޏZ�W��7̄,�����a��w�A/`s�(�ݱ;��& w���8۹���Y����E��â��������R�A�T5��PBv��x��b�-}w��f�W�ۚ�,�rCQIu�|�����ak]g�,gp�PY�nf�k)�l�Q,�oC����&�O�y��}q'�]>.ֻ5�:`��E	�A*���<�ծ<߹w��ņg��	l�f�ʚ'[B٨g �U���r���Owg)d���;�ϲ�A��dr�?�g�� �V<F�xqzk�V�����t{��n��,9����6H4���l2ʒ�K�ˮM{s�r^�oxQ��&~*��[qm�#��u�)k0{Ѥ�f>/�Pa��*�8�	5v[�����:+W��
��ڣ�u���*����1��O��C2�yΓ{�����m���:-��v�Ib"��s�7�Ҋ�Kq#��-�8,^;�M�A��8�|N	�^#�t�H�������w���ly�\��h��i[F]=�t�xl:��bq�R*��Kq�m��],� �>���E�1��֑�W"��E��ڛ'�J��M��C���ZٗQ�����0����?I��Q�n�%ro��[�b|,
q����4y���r�$;,l�J�0{hjoZ'��:��L��I�s���y�6޲.��i^�TNq�����ɿ�NSc         .   x�33�62600�t�700�t��-�I-IM�2�@�1D������ �J�         y   x�st100�tL����L���?�`#c���L�Ĝ��̢ļD�D����1gpIiJj^	��R�i`ahdaibblbh�o�U�����X�����YU����
*	�ilnhid����� �M.[            x������ � �     