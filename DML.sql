INSERT INTO CAPA(url_imagem, alt)
VALUES
('https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/55/41/4a/55414a18-861a-79d1-e575-5bf8cf205dbe/886445056839_Cover.jpg/600x600bb.jpg', 'Strange Trails'),
('https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/9b/d8/9c/9bd89c9e-b44d-ad25-1516-b9b30f64fd2a/23UMGIM71510.rgb.jpg/600x600bb.jpg', 'GUTS'),
('https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/07/60/ba/0760ba0f-148c-b18f-d0ff-169ee96f3af5/634904078164.png/600x600bb.jpg', 'OK COMPUTER'),
('https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/a4/86/59/a486593a-53c9-1c2a-5122-8f25339f7359/24UMGIM44778.rgb.jpg/600x600bb.jpg','THE TORTURED POETS DEPARTMENT: THE ANTHOLOGY'),
('https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/3c/da/d2/3cdad2a3-82dc-0de1-aa34-68a30b87bf23/22UMGIM49870.rgb.jpg/600x600bb.jpg','Superache'),
('https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/c5/cb/89/c5cb8997-7735-e2dd-a815-649627340c66/199538462074.jpg/600x600bb.jpg','CARRANCA'),
('https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/c7/1e/c9/c71ec9f8-f6fd-5374-0e5c-3419539618f4/075679607942.jpg/600x600bb.jpg','Youll be alright, kid'),
('https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/07/41/6a/07416a78-38b9-2d47-7ce8-8a52a44c510f/196874010112.jpg/600x600bb.jpg','Kiss All The Time. Disco, Occasionally'),
('https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/9e/9f/62/9e9f624b-40fa-e806-05fc-4b0308ef5344/190295698201.jpg/600x600bb.jpg','Pop 2'),
('https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/f9/aa/69/f9aa6992-40ca-a756-85ca-b27c48f7c720/26UMGIM02802.rgb.jpg/600x600bb.jpg','The Great Divide'),
('https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/d1/c9/65/d1c965fe-57d0-8705-e3e0-4c7419cd079e/0044003159716_Cover.jpg/600x600bb.jpg','The Wild Youth EP'),
('https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/ea/6e/bf/ea6ebff3-a03a-d2d1-510a-262532379736/886446439082.jpg/600x600bb.jpg','Broken Machine (Deluxe)'),
('https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/26/8d/bb/268dbb59-4df1-36c3-525e-8d24c921ee25/23UMGIM04594.rgb.jpg/600x600bb.jpg', 'Messy'),
('https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/cc/f1/7f/ccf17ff9-c0cb-f4fe-06b5-a7ee44d52a95/0.jpg/600x600bb.jpg', 'Ã‰ disso que eu me alimento'),
('https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/d5/5f/28/d55f28f4-610c-ee81-dc16-a01cda46bbc4/886443546264.jpg/600x600bb.jpg', 'BAD'),
('https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/92/9f/69/929f69f1-9977-3a44-d674-11f70c852d1b/24UMGIM36186.rgb.jpg/600x600bb.jpg', 'HIT ME HARD AND SOFT'),
('https://a1.mzstatic.com/r40/Music116/v4/a6/85/b9/a685b9f8-dad3-2ed7-58b2-ab7f64304505/23UMGIM58157.rgb.jpg', 'Midnights');
INSERT INTO PLANO_ASSINATURA(nome, valor, descricao) VALUES
('Free',       0,  'Plano gratuito com anúncios e funcionalidades limitadas'),
('Premium',    20, 'Plano com todos os benefícios: sem anúncios, download offline e qualidade máxima'),
('Student',    10, 'Plano Premium com desconto para estudantes'),
('Duo',        27, 'Plano Premium para 2 contas no mesmo endereço'),
('Family',     35, 'Plano Premium para até 6 contas da mesma família'),
('Business',   50, 'Plano para uso empresarial com recursos adicionais'),
('Artist Pro', 30, 'Plano para artistas com ferramentas de análise e distribuição'),
('Kids',        5, 'Plano infantil com conteúdo curado para crianças'),
('Podcast+',   15, 'Plano com acesso premium a podcasts exclusivos'),
('HiFi',       25, 'Plano com qualidade de áudio lossless');


INSERT INTO USUARIO(nome, apelido, id_plano_assinatura) VALUES
('Rafael',       'rafanduba',        2),
('João Pedro',   'princesa',         2),
('Jader',        '*****_hedonista',  3),
('Samuel Silva', 'samuel_silva',     5),
('Alice',        'lili_gameplays',   1),
('Danniel',      'danni',            2),
('Samir',        'namorado',         2),
('Arthur',       'taylor',           4),
('William',      'swift',            1),
('Raulivan',     'prof_gente_boa',   4);



INSERT INTO GRAVADORA(nome) VALUES
('IAMSOUND Records'),   -- 1  Lord Huron
('Geffen Records'),     -- 2  Olivia Rodrigo
('Parlophone'),         -- 3  Radiohead
('Republic Records'),   -- 4  Taylor Swift / Conan Gray
('30PRAUM'),            -- 5  Urias / gravadora BR
('Sony Music'),         -- 6  genérica
('Universal Music'),    -- 7  genérica
('Columbia Records'),   -- 8  Nothing But Thieves
('Interscope Records'), -- 9  Charli XCX
('Warner Music'),       -- 10 genérica
('Mataderos Records');  -- 11 Urias (label original)


INSERT INTO ARTISTA(nome, ouvintes_mensais, descricao, ano_debut, id_gravadora) VALUES
('Lord Huron',          3200000,  'Banda americana de indie folk liderada por Ben Schneider, conhecida por suas letras cinematogrÃ¡ficas e atmosfera aventureira.', 2010, 1),
('Olivia Rodrigo',     42000000, 'Cantora e compositora americana, conhecida por seu debut aclamado SOUR e o Ã¡lbum GUTS, misturando pop com rock alternativo.', 2021, 2),
('Radiohead',          14000000, 'Banda britÃ¢nica de rock alternativo formada em Oxford em 1985, pioneira na fusÃ£o de rock, eletrÃ´nica e experimentalismo.', 1992, 3),
('Taylor Swift',      100000000, 'Cantora e compositora americana, uma das artistas mais vendidas de todos os tempos, com 11 Ã¡lbuns de estÃºdio.', 2006, 4),
('Conan Gray',          8500000, 'Cantor e compositor americano de pop indie, conhecido por suas letras emotivas e estÃ©tica vintage.', 2019, 4),
('Urias',               1200000, 'Cantora, compositora e danÃ§arina trans brasileira nascida em UberlÃ¢ndia, MG, conhecida por unir pop eletrÃ´nico e R&B com identidade afro-brasileira.', 2019, 11),
('Alex Warren',          800000, 'Cantor pop conhecido pelo hit "Ordinary"', 2023, 2),
('Harry Styles',        9000000, 'Cantor, compositor e produtor americano de pop, antigo integrante do grupo "One Direction".', 2015, 7),
('Charli XCX',         18000000, 'Cantora e compositora britÃ¢nica de pop experimental e hyperpop, conhecida por Ã¡lbuns como Brat e Pop 2.', 2012, 9),
('Noah Karran',         3000000, 'Cantor country, pop e folk.', 2019, 3),
('Wild Youth',          1500000, 'Banda irlandesa de indie pop formada em Dublin em 2015.', 2017, 7),
('Nothing But Thieves', 4700000, 'Banda britÃ¢nica de rock alternativo formada em Southend-on-Sea, Essex, em 2012.', 2014, 8),
('Olivia Dean',           90000, 'Cantora pop, R&B, ganhou grammy de artista revelaÃ§Ã£o 2026', 2023, 6),
('NandaTsunami',           5000, 'Artista de rap brasileira', 2020, 5),
('Michael Jackson',    90000000, 'Cantor famoso nos anos 80 - 2000, mundialmente conhecido atÃ© hoje', 1962, 2),
('Billie Eilish',      65000000, 'Cantora e compositora americana de pop alternativo, vencedora de mÃºltiplos Grammys.', 2016, 2);



INSERT INTO ALBUM(nome, data_lancamento, quantidade_faixas, id_artista, id_capa) VALUES
('Strange Trails',                                  '2015-04-08', 13, 1,  1),
('GUTS',                                            '2023-09-08', 12, 2,  2),
('OK Computer',                                     '1997-06-16', 12, 3,  3),
('THE TORTURED POETS DEPARTMENT: THE ANTHOLOGY',    '2024-04-19', 31, 4,  4),
('Superache',                                       '2022-06-24', 12, 5,  5),
('CARRANCA',                                        '2025-10-07', 14, 6,  6),
('You''ll Be Alright, Kid',                         '2022-09-23', 12, 7,  7),
('Kiss All the Time. Disco, Occasionally',          '2026-03-03', 10, 8,  8),
('Pop 2',                                           '2017-12-15', 10, 9,  9),
('The Great Divide',                                '2025-03-07', 14, 10, 10),
('The Wild Youth EP',                               '2018-04-13',  5, 11, 11),
('Broken Machine (Deluxe)',                         '2017-09-08', 15, 12, 12),
('Messy',                                           '2024-10-11', 11, 13, 13),
('É disso que eu me alimento',                      '2025-11-19', 12, 14, 14),
('BAD',                                             '1987-09-07', 11, 15, 15),
('Hit me Hard and Soft',                            '2024-05-07', 10, 16, 16),
('Midnights',                                       '2022-05-12', 22, 4, 17);



INSERT INTO MUSICA(nome, id_album) VALUES
-- Strange Trails
('Love Like Ghosts',      1),  -- id 1
('Until the Night Turns', 1),  -- id 2
('Dead Man''s Hand',      1),  -- id 3
('Hurricane (War)',       1),  -- id 4
-- GUTS
('all-american bitch',    2),  -- id 5
('bad idea right?',       2),  -- id 6
('lacy',                  2),  -- id 7
('get him back!',         2),  -- id 8
-- OK Computer
('Airbag',                3),  -- id 9
('Paranoid Android',      3),  -- id 10
('Karma Police',          3),  -- id 11
('Fitter Happier',        3),  -- id 12
-- TTPD: The Anthology
('Fortnight',             4),  -- id 13
('But Daddy I Love Him',  4),  -- id 14
('So Long, London',       4),  -- id 15
('Down Bad',              4),  -- id 16
-- Superache
('Movies',                5),  -- id 17
('Disaster',              5),  -- id 18
('Best Friend',           5),  -- id 19
('Astronomy',             5),  -- id 20
-- CARRANCA
('A Liberdade (Intro)',   6),  -- id 21
('Quando A Fonte Secar',  6),  -- id 22
('Vênus Noir',            6),  -- id 23
('Etiópia',               6),  -- id 24
-- You'll Be Alright, Kid
('Eternity',              7),  -- id 25
('Ordinary',              7),  -- id 26
('First Time on Earth',   7),  -- id 27
('Troubled Waters',       7),  -- id 28
-- Kiss All the Time...
('Aperture',              8),  -- id 29
('Pop',                   8),  -- id 30
('Taste Back',            8),  -- id 31
('Ready, Steady, Go',     8),  -- id 32
-- Pop 2
('tears',                 9),  -- id 33
('backseat',              9),  -- id 34
('I Got It',              9),  -- id 35
('Out of My Head',        9),  -- id 36
-- The Great Divide
('Porch Light',          10),  -- id 37
('The Great Divide',     10),  -- id 38
('Doors',                10),  -- id 39
-- The Wild Youth EP
('youth',                11),  -- id 40
('medicine',             11),  -- id 41
-- Broken Machine (Deluxe)
('Amsterdam',            12),  -- id 42
('Reset Me',             12),  -- id 43
('If I Get High',        12),  -- id 44
('Hell Yeah',            12),  -- id 45
-- Messy
('The Hardest Part',     13),  -- id 46
('Dangerously Easy',     13),  -- id 47
-- É disso que eu me alimento
('Pq Vc NÃ£o me liga?',   14),  -- id 48
('Oi Linda',             14),  -- id 49
-- BAD
('Dirty Diana',          15),  -- id 50
('Smooth Criminal',      15),  -- id 51
-- HIT ME HARD AND SOFT
('Blue',                 16),  -- id 52
('BITTERSUIT',           16);  -- id 53


INSERT INTO GENERO(nome) VALUES
('Indie Folk'),       -- 1
('Pop'),              -- 2
('Rock Alternativo'), -- 3
('Art Rock'),         -- 4
('Country Pop'),      -- 5
('Trap'),             -- 6
('R&B'),              -- 7
('Hyperpop'),         -- 8
('Indie Pop'),        -- 9
('Pop Experimental'), -- 10
('Folk'),             -- 11
('Pop Rock');         -- 12



INSERT INTO ARTISTA_GENERO(id_artista, id_genero) VALUES
(1,  1),  -- Lord Huron - Indie Folk
(1,  11), -- Lord Huron - Folk
(2,  2),  -- Olivia Rodrigo - Pop
(2,  12), -- Olivia Rodrigo - Pop Rock
(3,  3),  -- Radiohead - Rock Alternativo
(3,  4),  -- Radiohead - Art Rock
(4,  2),  -- Taylor Swift - Pop
(4,  5),  -- Taylor Swift - Country Pop
(5,  9),  -- Conan Gray - Indie Pop
(5,  2),  -- Conan Gray - Pop
(6,  7),  -- Urias - R&B
(6,  10), -- Urias - Pop Experimental
(7,  2),  -- Alex Warren - Pop
(8,  2),  -- Harry Styles - Pop
(8,  9),  -- Harry Styles - Indie Pop
(9,  8),  -- Charli XCX - Hyperpop
(9,  10), -- Charli XCX - Pop Experimental
(10, 5),  -- Noah Karran - Country Pop
(10, 11), -- Noah Karran - Folk
(11, 9),  -- Wild Youth - Indie Pop
(12, 3),  -- Nothing But Thieves - Rock Alternativo
(12, 12), -- Nothing But Thieves - Pop Rock
(13, 2),  -- Olivia Dean - Pop
(13, 7),  -- Olivia Dean - R&B
(14, 6),  -- NandaTsunami - Trap
(15, 2),  -- Michael Jackson - Pop
(16, 2),  -- Billie Eilish - Pop
(16, 3);  -- Billie Eilish - Rock Alternativo
INSERT INTO MEMBRO(nome, nascimento, nacionalidade, id_artista) VALUES

('Ben Schneider',       1989, 'Estadunidense', 1),
('Tom Renaud',          1988, 'Estadunidense', 1),
('Mark Barry',          1987, 'Estadunidense', 1),
('Miguel Briseno',      1989, 'Estadunidense', 1),

('Thom Yorke',          1968, 'Britânico',     3),
('Jonny Greenwood',     1971, 'Britânico',     3),
('Colin Greenwood',     1969, 'Britânico',     3),
('Ed O''Brien',         1968, 'Britânico',     3),
('Philip Selway',       1967, 'Britânico',     3),

('Conor Mason',         1993, 'Britânico',     12),
('Joe Langridge-Brown', 1992, 'Britânico',     12),
('Dominic Craik',       1992, 'Britânico',     12),
('Philip Blake',        1992, 'Britânico',     12);


INSERT INTO PLAYLIST(nome, id_usuario) VALUES
('Brasileiras',      1),
('Indie Vibes',      2),
('Rock Clássico',    3),
('Pop Hits',         4),
('Sad Hours',        5),
('Chill Sunday',     6),
('Workout Mix',      7),
('Late Night Drive', 8),
('Hyperpop Only',    9),
('Favoritas',        10),
('Melhores Charli xcx', 7);


INSERT INTO MUSICA_PLAYLIST(id_playlist, id_musica) VALUES
(1, 21),  -- Brasileiras - A Liberdade (Intro)
(1, 22),  -- Brasileiras - Quando A Fonte Secar
(2, 1),   -- Indie Vibes - Love Like Ghosts
(2, 2),   -- Indie Vibes - Until the Night Turns
(3, 9),   -- Rock Clássico - Airbag
(3, 10),  -- Rock Clássico - Paranoid Android
(4, 5),   -- Pop Hits - all-american bitch
(4, 6),   -- Pop Hits - bad idea right?
(5, 17),  -- Sad Hours - Movies
(5, 18),  -- Sad Hours - Disaster
(6, 13),  -- Chill Sunday - Fortnight
(6, 14),  -- Chill Sunday - But Daddy I Love Him
(7, 33),  -- Workout Mix - tears
(7, 34),  -- Workout Mix - backseat
(8, 37),  -- Late Night Drive - Porch Light
(8, 38),  -- Late Night Drive - The Great Divide
(9, 33),  -- Hyperpop Only - tears
(9, 34),  -- Hyperpop Only - backseat
(10, 5),  -- Favoritas - all-american bitch
(10, 21); -- Favoritas - A Liberdade (Intro)

INSERT INTO FAIXA(numero, id_album) VALUES
-- Strange Trails
(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
-- GUTS
(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
-- OK Computer
(1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
-- TTPD: The Anthology
(1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
-- Superache
(1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5),
-- CARRANCA
(1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6),
-- You'll Be Alright, Kid
(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
-- Messy
(1, 13), (2, 13), (3, 13), (4, 13), (5, 13),
-- É disso que eu me alimento
(1, 14), (2, 14), (3, 14), (4, 14), (5, 14),
-- BAD
(1, 15), (2, 15), (3, 15), (4, 15), (5, 15);



INSERT INTO SINGLE(nome, data_lancamento, id_faixa, id_capa) VALUES
('Vampire',           '2023-06-30',  9, 2),
('No Surprises',      '1997-01-06', 15, 3),
('Fortnight',         '2024-04-19', 19, 4),
('People Watching',   '2021-07-14', 28, 5),
('Deus',              '2025-08-01', 32, 6),
('The Hardest Part',  '2024-01-01', 43, 13),
('Von dutch',         '2024-06-11', 44, 13),
('Memories',          '2022-04-15', 27, 5),
('Porch Light',       '2025-03-07', 20, 10),
('medicine',          '2018-01-01', 41, 11);



INSERT INTO PREVIEW(url_audio, id_musica) VALUES
('', 1),
('', 2),
('', 3),
('', 4),
('', 5),
('', 6),
('', 7),
('', 8),
('', 9),
('', 10),
('', 11),
('', 12),
('', 13),
('', 14),
('', 15);



INSERT INTO LETRA(idioma, letra_original, traducao_BR, id_musica) VALUES
('EN', '', '', 1),  -- Love Like Ghosts
('EN', '', '', 2),  -- Until the Night Turns
('EN', '', '', 3),  -- Dead Man's Hand
('EN', '', '', 4),  -- Hurricane (War)
('EN', '', '', 5),  -- all-american bitch
('EN', '', '', 6),  -- bad idea right?
('EN', '', '', 7),  -- lacy
('EN', '', '', 8),  -- get him back!
('EN', '', '', 9),  -- Airbag
('EN', '', '', 10), -- Paranoid Android
('EN', '', '', 11), -- Karma Police
('EN', '', '', 12), -- Fitter Happier
('EN', '', '', 13), -- Fortnight
('EN', '', '', 14), -- But Daddy I Love Him
('EN', '', '', 15); -- So Long, London



INSERT INTO AVALIACAO(quantidade_estrelas, comentario, id_album, id_usuario) VALUES
(5,   'Állbum da minha vida',                                                 1,  1),
(4.5, 'Tem vampire, tem nota boa',                                            2,  2),
(3,   'Álbum estranho pra gente estranha',                                    3,  3),
(5,   'Branca básica',                                                        4,  4),
(4.5, 'Álbum mais maduro dele, é o único que não parece uma grande fanfic',   5,  5),
(5,   'CARRANCA é um marco da música brasileira, Vontade de Voar arrasa',     6,  6),
(3,   'Álbum lindo. Pena que desandou e só lança single ruim agora',          7,  7),
(4.5, 'Oi galerinha fiquei sabendo que vocês gostam de Tame Impala',          8,  8),
(2,   'Essa menina não sabe cantar e fica botando efeito na voz',             9,  9),
(5,   'Álbum imaculado. Doors é um tiro no peito',                            10, 10),
(3.5, 'EP promissor',                                                         11,  1),
(3, 'É. Tem gente que gosta. Capa bonita',                                    12,  2),
(2,   'Álbum mais ou menos. Capa horrorosa meu deus',                         13,  3),
(4,   'Aborda tópicos sensíveis, capa linda',                                 14,  4),
(4.5,   'Clássico do pop né, não tem muito o que dizer',                      15,  5);



INSERT INTO ARTISTA_MUSICA(id_artista, id_musica, tipo_participacao) VALUES
-- Lord Huron (id 1) músicas 1 e 2
(1,  1,  'Principal'),
(1,  2,  'Principal'),
-- Olivia Rodrigo (id 2) músicas 5 e 6
(2,  5,  'Principal'),
(2,  6,  'Principal'),
-- Radiohead (id 3) músicas 9 e 10
(3,  9,  'Principal'),
(3,  10, 'Principal'),
-- Taylor Swift (id 4) músicas 13 e 14
(4,  13, 'Principal'),
(4,  14, 'Principal'),
-- Conan Gray (id 5)  músicas 17 e 18
(5,  17, 'Principal'),
(5,  18, 'Principal'),
-- Urias (id 6)  músicas 21 e 22
(6,  21, 'Principal'),
(6,  22, 'Principal'),
-- Alex Warren (id 7)  músicas 25 e 26
(7,  25, 'Principal'),
(7,  26, 'Principal'),
-- Harry Styles (id 8)  músicas 29 e 30
(8,  29, 'Principal'),
(8,  30, 'Principal'),
-- Charli XCX (id 9)  músicas 33 e 34
(9,  33, 'Principal'),
(9,  34, 'Principal'),
-- Noah Karran (id 10)  músicas 37 e 38
(10, 37, 'Principal'),
(10, 38, 'Principal'),
-- Wild Youth (id 11)  músicas 40 e 41
(11, 40, 'Principal'),
(11, 41, 'Principal'),
-- Nothing But Thieves (id 12) músicas 42 e 43
(12, 42, 'Principal'),
(12, 43, 'Principal');
