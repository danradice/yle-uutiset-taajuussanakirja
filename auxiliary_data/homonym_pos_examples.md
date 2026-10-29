Example sentences for lemma-POS combinations needing review
Source: YLENEWS_FI VRT 2011-2024. Target token marked «like this».
==============================================================================

Claude's analysis

Reading through them, most of these buckets look like **tagger/lemmatiser errors rather than genuine word classes**:

| Pair | count | What the examples actually are |
|---|---|---|
| `kuti` A | 40 | **Lemmatisation error.** All are verb forms of *kutista/kutiaa* ("itch") or *kutistaa* ("shrink") wrongly lemmatised to `kuti` — plus a surname *Kutilainen*. No genuine `kuti` adjective. |
| `kuti` Adv | 12 | **The noun sense.** All are sports slang *kuti* = "shot" (*torjua kuti*, *kutikin lähtee*). These belong with `kuti` N. |
| `läpi` N | 20,620 | All adverbial/adpositional (*pääsi läpi*, *käydään läpi*, *läpi karanneen*). None is the noun sense. |
| `lähin` Adv | 1,029 | All attributive superlative adjectives (*lähin vertailukohta*, *lähin partio*). |
| `lähin` N | 7,577 | Mostly attributive adjective (*lähimmälle poliisiasemalle*, *lähimpään klinikkaan*); #2 is the fixed adverbial idiom *tästä lähin* ("from now on"). |
| `kiltti` N | 1,024 | All adjective "kind/nice" (*olen kiltti*, *kiltti vanhus*). The actual noun sense (a kilt) doesn't appear. |
| `iso` N | 6,517 | Substantivised/predicative adjective (*olivat isot*, *isoille ja pienille*) and one proper name (*Ison Poron*). |

Note this cuts both ways against the `expected` flag: `iso`/`kiltti`/`läpi` N were marked `expected=yes` (the sanalista does list a noun sense) yet the corpus tokens aren't that noun — so a `yes` flag doesn't vindicate a bucket. Conversely `kuti` Adv was `no` but is recoverable, since it's cleanly the noun sense.

### iso  /  N   (5 examples)

1. Ne olivat «isot» enemmän korvien välissä ja pelissä kuin kolme pistettä.
   [http://yle.fi/urheilu/3-5303221]

2. Mittauspisteitä on tulossa lisää Säynätsalon, Kinkomaan ja «Ison» Poron alueille.
   [http://yle.fi/uutiset/jaat_heikenneet_nenainniemen_lahella/5304563]

3. Otetaanko joskus uudestaan?Kuuntele ja lue lisää Perheen ajassa: Luisteluvinkit ammatilaiselta «isoille» ja pienilleja Lapset liikkeelle ja pihaleikit kunniaan
   [https://yle.fi/aihe/artikkeli/2011/01/14/pihapeleja-luistinradalla]

4. \- Välillisetkin vaikutukset olisivat olleet «isot», Haapaniemi miettii.
   [http://yle.fi/uutiset/upm_ei_rakenna_biojalostamoa_kuusankoskelle/5307499]

5. Piste-erot ovat jo sen verran «isot», että jumbokolmikosta kahden kesäloma alkaa aikaisin.
   [http://yle.fi/urheilu/3-5310136]


### kiltti  /  N   (5 examples)

1. Jos olen heille «kiltti», niin toivon heidänkin olevan minulle «kilttejä», kertoo nuorimies.
   [http://yle.fi/uutiset/22-vuotias_veikko_pulli_johtaa_hattulan_kirkkovaltuustoa_hymyillen/5313151]

2. Urheilijoiden kohussa on jäänyt vähälle huomiolle, että normaalisti bakteeri on hyvin vaaraton. – Pääsääntöisesti se aiheuttaa niin «kiltin» hengitystieinfektion, ettei siitä tarvitse olla kovin huolissaan jos sitä lähiympäristössä on. – Yhtä keuhkokuumetta kohti esiintyy 10–20 kertaa enemmän ihan tavallisia hengitystietulehduksia, jotka rauhoittuvat ilman antibioottihoitoja, Syrjälä sanoo.
   [https://yle.fi/aihe/artikkeli/2011/02/08/urheilijoiden-mykoplasmainfektiot-epailyttavat]

3. Erityisesti «kiltti» ja yönsä nukkuva, mutta yksinäiseksi itsensä tunteva vanhus hyötyy perhehoidosta.
   [https://yle.fi/aihe/artikkeli/2011/02/22/vanhusten-perhehoito-tulee-jaksavatko-hoitajat]

4. Tätä arvokeskustelua kaivataan koteihin ja kouluihin pinnallisuuden vastapainoksi, Cacciatore penää.******Vahva itsetunto suojaa «kiltin» tytön syndroomalta ** - Vahva itsetunto suojaa «kiltin» tytön syndroomalta.
   [https://yle.fi/aihe/artikkeli/2011/03/01/mista-pienet-tytot-tehty]

5. Opettaja, rajaa työsi äläkä ole liian «kiltti»
   [http://yle.fi/uutiset/opettaja_rajaa_tyosi_alaka_ole_liian_kiltti/5091904]


### kuti  /  A   (5 examples)

1. Aina syödessäni maitotaloustuotteita korvani alkavat kamalasti «kutista» ja niistä tulee kellertävää vaikkua, muita oireita ei tule.
   [http://yle.fi/uutiset/moni_parjaa_allergian_kanssa_kotikonstein/5370479]

2. Ja on olemassa psyykkistäkin kutinaa – jos oikein jännittää, niin saattaa alkaa «kutista».
   [https://yle.fi/aihe/artikkeli/2011/10/04/miksi-ihminen-kutiaa]

3. Olenkin joskus nätisti sanonut, että ei se musta t-paita «kutista» kantajaansa kokoon 34, vaan saattaa pahimmillaan rajata, neuvoo Vaintola.
   [http://yle.fi/uutiset/musta_ei_kutista_kokoon_34/6216592]

4. Jos koiran terveydessä tapahtuu muutoksia, esimerkiksi jos silmät alkavat rähmiä tai anturat «kutista», on hyvä jutella eläinlääkärin tai eläinkauppiaan kanssa mahdollisista syistä.
   [http://yle.fi/uutiset/yksi_koirankakka_kertoo_enemman_kuin_tuhat_sanaa/6327728]

5. Pikku hiljaa vuosi vuodelta lukua on tarkoitus kasvattaa uuden tarjonnan myötä, arvioi Kaisa «Kutilainen».
   [http://yle.fi/uutiset/verstas-hanke_elavoittaisi_kylamakea/6420777]


### kuti  /  Adv   (5 examples)

1. Tästäkin huolimatta Mezinin olisi pitänyt torjua «kuti».
   [http://yle.fi/urheilu/3-6091098]

2. Ronaldo eteni heti perään uudestaan laukaisuetäisyydelle, mutta tällä kertaa «kuti» suuntautui suoraan päin maalivahtia.
   [http://yle.fi/urheilu/3-6572202]

3. Aleksilla on jäänyt hieman «kuti» piippuun, mutta hän pystyy takuuvarmasti parempaan, Korkeakunnas sanoo.
   [http://yle.fi/urheilu/3-7629644]

4. Tehot alkavat löytyä – " Kun onnistuu, niin «kutikin» lähtee herkemmin "
   [http://yle.fi/urheilu/3-7656818]

5. «Kutikin» lähti suurinpiirtein sinne minne yritin, sanoi Ville Hämäläinen.
   [http://yle.fi/urheilu/3-7749926]


### lähin  /  N   (5 examples)

1. Niemiseen liittyvistä katoamisen jälkeisistä havainnoista pyydetään ilmoittamaan yleiseen hätänumeroon 112 tai virka-aikana «lähimmälle» poliisiasemalle.
   [http://yle.fi/uutiset/viranomaistiedote/5300957]

2. Kaupunki vakuuttaa, että asiakkaat pääsevät tästä «lähin» lääkärille hoitotakuun mukaisesti.
   [http://yle.fi/uutiset/lieksa_laakaripalvelut_ovat_kunnossa/5302573]

3. Ylitalot veivät koiran aluksi «lähimpään» klinikkaan, mutta siellä ei ollut sopivaa vasta-ainemyrkkyä, sanoo Marja-Liisa Ylitalo.
   [http://yle.fi/uutiset/kyy_puri_koiraa_-_hoitolasku_1_500_euroa/5303522]

4. Nyt rakennettava Innova 2 tulee «lähimmäksi» Innovatornia.
   [http://yle.fi/uutiset/lutakkoon_nousee_innova_2/5305147]

5. Hänen «lähin» uhkaajansa, Ruotsin Helena Ekholm sijoittui Ruhpoldingin takaa-ajossa kuudenneksi.
   [http://yle.fi/urheilu/3-5306868]


### lähin  /  Adv   (5 examples)

1. Pilottialueilla on koettu hyväksi toiminta, jossa esimerkiksi äkillisesti sairastuneen luo lähetetään «lähin» mahdollinen viranomaispartio vastaamaan hätäensiavusta.
   [http://yle.fi/uutiset/yhteispartiointi_halutaan_pysyvaksi_toiminnaksi/5082273]

2. «Lähin» vertailukohta leffalle saattaisivat olla ruotsalaiset Viiru ja Pesonen -elokuvat, joiden ilmiasu tuo eittämättä mieleen Eetun ja Konnan.
   [http://yle.fi/uutiset/tahtihetki_perjantaina_182/5083020]

3. Rakennuksessa on kaksi kuumaöljykattilaa, ja «lähin» polttoainevarasto sijaitsee palaneesta rakennuksesta vain noin 50 metrin päässä.
   [http://yle.fi/uutiset/kotkan_kemikaalisatamassa_syttyi_uhkaava_palo/5087940]

4. Rakennuksessa on kaksi kuumaöljykattilaa ja «lähin» polttoainevarasto sijaitsee palaneesta rakennuksesta vain noin 50:n metrin päässä.
   [http://yle.fi/uutiset/kotkan_mussalossa_uhkaava_palo_sunnuntaina/5088551]

5. Jos tapahtuu jotain kiireellistä, kuten vaikkapa ryöstö tai tappelu, niin pitää hälyttää «lähin» partio muualta.
   [http://yle.fi/uutiset/juoppokuljetuksiin_kaytetty_aika_kasvaa/5323947]


### läpi  /  N   (5 examples)

1. Kotiyleisö vaati äänekkäästi rangaistuspotkua, kun punapaitojen konkaripuolustaja Gary Neville näytti kaatavan «läpi» karanneen Graham Dorransin.
   [http://yle.fi/urheilu/3-5299995]

2. \- Mutta se että joku lyö itsensä «läpi» muualla, on vain pelkästään positiivinen asia meidän junioritoiminnallemme, HIFK:n junioreiden puheenjohtaja Tom Nybondas tuumi.
   [http://yle.fi/urheilu/3-5300007]

3. Seuraavasta hyökkäyksestä Julius Junttila pääsi puolittain yksin «läpi» ja nosti kiekon upeasti Venäjän maalin takayläkulmaan.
   [http://yle.fi/urheilu/3-5300270]

4. Myös erilaisten laitosten lupa-asioita käydään «läpi».
   [http://yle.fi/uutiset/biokaasu_kiinnostaa_maanviljelijoita/5300739]

5. Jesper Fasth pääsi yksin «läpi», mutta alle vuorokauden Suomi-voittonsa jälkeen huilanneen Venäjän maalivahti Dimitri Shikin venyi hyvään torjuntaan.
   [http://yle.fi/urheilu/3-5300939]




==============================================================================
## 2.0.0 review

A sample of 2015, 2020 and January–February 2023 (about a fifth of the corpus).
Alt texts are excluded; repeats are not. For each bucket the table gives its
size in the sample, its ten commonest word forms, and five of ten random
examples. The decisions drawn from this are in `homonym_processing_notes.md`.

### aika  /  Adv   (sample n=17296)

Forms: aika:17256, aikakin:35, aikahan:5

1. Se onkin mielenkiintoista «aika» mysteerijuttu
2. Yleensä kaikki «aika» käytetään tämmöisissä hankkeissa
3. Kyllä mä pelasin «aika» aggressiivisesti
4. Opettajat ovat «aika» kovilla
5. Ikävä kyllä tätä näkee «aika» ajoin ainakin yleisurheilun parissa

### aika  /  N   (sample n=184393)

Forms: aikana:64740, ajan:31014, aikaa:23842, aikaan:20940, aika:10721, aikoina:5325, aikojen:4550, ajaksi:3420, ajassa:2497, aikanaan:2459

1. 538 184 koronatartuntaa on todettu Etelä-Afrikassa jossa todettiin torstain «aikana» yli 8 000 uutta tartuntaa
2. Laura Mikkola urakoi «aikamme» säveltaiteen parissa ja tekee sen hyvin
3. illalla Suomeen saapuu lännestä sadealue joka kulkee yön «aikana» kohti itää
4. Miten «aikaa» mitattiin ennen almanakkaa
5. On kiva katsella iloisia ilmeitä ja juttuja koko «ajan»

### iso  /  A   (sample n=39604)

Forms: iso:13543, isoja:4149, ison:2857, isot:2763, isoa:1596, isompi:1343, isossa:1143, isojen:1122, isompia:811, isoin:791

1. yleisiä haukkumasanoja ei saa käyttää vaikka olisit kuinka «ison» valtamedian toimittaja
2. Runsaan lumentulon takia «isoja» lumikasoja on muodostunut kaupunki- ja haja-asutusalueille
3. Jammeh on «iso» tekijä niin harjoituskentällä pukukopissa kuin pelikentälläkin
4. Siinä liikkuvat myös «isot» rahat
5. Palkansaajapuolella «isot» lomautukset näkyvät monen tilillä

### iso  /  Adv   (sample n=127)

Forms: isommin:123, isommasti:2, isomminkin:1, isommastikin:1

1. tehdä uusia työpaikkoja mutta en usko että niitä «isommin» tulee Salonen toteaa
2. Ei heidän tekemisistään ole «isommin» huudeltu
3. Cheekin kanssa mutta toki Cheek on kasvanut vähän «isommin» Kallonen sanoo
4. oli hyvin hereillä heti alusta eikä jännitystä ollut «isommin» nähtävillä kertoi tyytyväinen Åhman
5. Tämä alkoi «isommin» torstaina 12 päivä ja jo perjantaina syöjämäärät laskivat

### iso  /  N   (sample n=1123)

Forms: ison:317, isot:123, isojen:75, iso:60, isosta:57, isossa:50, isoista:49, isoon:39, isokin:39, isoja:38

1. Henrik Dettmann valottaa «isoa» uhkaa jos liikuntatiloja viedään lapsilta ja nuorilta poikkeusaikana
2. Edellinen ei tiedä mitä hänestä tulee «isona» ja väittää olevansa tyytyväinen tähän asiaintilaan vaikka naamasta
3. Jättipotista riittäisi «isojenkin» haaveiden toteuttamiseen sillä tavallisella elämällä nyt jaossa olevaa
4. Lauantaina puolestaan Espoossa kauppakeskus «Isossa» Omenassa nainen kuoli vartijoiden kiinniottotilanteen yhteydessä
5. Kalajoella suunnitelmissa oli useita «isoja» jopa kymmenien tuhansien osallistujien tapahtumia jotka nyt joudutaan

### juuri  /  A   (sample n=38)

Forms: juurinen:26, juurisen:8, juuriselta:2, juuriselle:1, juurinenkin:1

1. Jämsekin kehittämispäällikkö Jämsän kaupunginjohtajan tehtävää väliaikaisesti hoitanut Anna-Liisa «Juurinen» sekä Jämsekin toimitusjohtaja Ulla Haggrén
2. Huhtikuussa 1996 Helinä «Juurinen» oli junassa isänsä ja koiransa kanssa kun matka
3. Lahden yhteiskoulun lukion abi Jenni «Juurinen» tähtää lukion jälkeen Turun tai Tampereen yliopistoon
4. «Juurinenkin» lataa tottuneesti kahvinkeittimen ja tuo leivonnaiset pöytään
5. Aapo ja Jani kyselivät kalmasiivooja Simo «Juuriselta» mitä jäbä oikein duunaa

### juuri  /  Adv   (sample n=24790)

Forms: juuri:22631, juurikaan:2069, juurikin:87, juurihan:3

1. Nykyään toki ymmärrän että «juuri» niin runot eivät synny
2. Itse työvaiheessa taidokkaan leikkaajan katse ei «juuri» saksiin tai omiin käsiin eksy
3. Tampan ykkösketjun vuoksi Islandersille on vaikea antaa sarjassa «juurikaan» toivoa
4. Esimerkiksi «juuri» Lake Worth on ollut niin suosittu asuinpaikka että
5. «Juuri» nyt työvoimaa tarvitaan kauden aloitustöihin puutarhoissa kasvihuoneilla ja

### juuri  /  N   (sample n=2298)

Forms: juuret:743, juurensa:277, juurella:161, juurille:144, juuria:133, juurilleen:86, juurta:66, juurista:66, juuriaan:53, juurelle:52

1. Ylen asiantuntijan mukaan huippujalkapallossa nähtiin paluu «juurille» Bundesliiga on tietynlainen koelaboratorio
2. Jeren kohdalla taloudellisen väkivallan «juuret» ulottuvat 1990-luvulle
3. arvio on että salama löi puuhun tai sen «juuriin» ja sytytti sitä kautta vajan tuleen
4. mutta toiveet ja haaveet pitkäaikaisesta pysyvästä skeittipaikasta juontavat «juurensa» paljon kauemmas
5. räppää naisen roolista ja ammentaa voimaa mytologiasta ihmisyytemme «juurista»

### kohta  /  Adv   (sample n=1696)

Forms: kohta:1685, kohtahan:9, kohtapa:1, kohtaisesti:1

1. «Kohta» nelikymppinen kajaanilainen Jonna on käyttänyt huumeita vuosikymmeniä ja
2. Varpu täyttää «kohta» kolme vuotta
3. Kumpare metsässä voi kätkeä yllätyksen metsien kulttuuriperintö «kohta» kartoitettu
4. Vierailurajoitukset pitkäaikaishoidossa ovat oleet voimassa «kohta» kaksi kuukautta
5. Meillä on «kohta» levyllinen täynnä biisejä ja kohta lähdemme keikkailemaan

### kohta  /  N   (sample n=14758)

Forms: kohdalla:6671, kohtaa:1636, kohta:1100, kohdalle:706, kohdallaan:651, kohtaan:487, kohdassa:433, kohdalta:364, kohtia:330, kohdan:327

1. alusta kantava Lappeenranta uskoo omiin vahvuuksiin EU:n elvytyspaketin «kohdalla»
2. Joukkueesta on kuitenkin aistittavissa sen että latinki on «kohdallaan»
3. Helsingissä näitä toiminnallisiksi häiriöiksi kutsuttavia oireita on hoidettu «kohta» vuoden päivät Laakson alueella toimivalla toiminnallisten häiriöiden poliklinikalla
4. mitään suurempaa ukkosilmiötä tai se on jossakin tietyssä «kohdassa»
5. Tästä «kohtaa» käynnistyi kuitenkin Suomen alle 16-vuotiaiden nousu

### koko  /  Adv   (sample n=2)

Forms: kokokin:1, koosti:1

1. Piirakan väri ja pinta ja tietysti «kokokin» saattoivat antaa vääriä ennakko-odotuksia mausta ja koostumuksesta
2. Otsonkoulun 6A-luokka kirjoitti karhujen ruokinta-aamun kokemukset tarinaksi ja «koosti» kuvaamastaan videomateriaalista nettivideon luokanopettajansa Jarmo Määtän avustamana

### koko  /  N   (sample n=3836)

Forms: kokoon:574, koolle:559, kokoa:489, koossa:423, koon:404, kooltaan:391, koosta:257, koko:184, koolla:112, kokonsa:76

1. Taigakirvinen on sekä «kooltaan» että ääneltään hyvin samankaltainen kuin metsäkirvinen mutta pieniä
2. Varkaudessa akuuttityöryhmän «kokoa» kasvatettiin kun osasto suljettiin toistaiseksi
3. Tavoitteena on kerätä «koolle» tavallisia torniolaisia ja haaparantalaisia joille avoin raja on
4. Havainnekuva megawatin sähkövaraston «koosta» Helsingin Energian Hanasaaren voimala-alueella
5. Samana päivänä «KOKO» Lahti tiedotti Emilia Mäen irtisanoutuneen toimitusjohtajan tehtävistä ja

### koko  /  Pron   (sample n=55418)

Forms: koko:55415, kokokin:2, kokokaan:1

1. Lonka innostaa opettajia ilmiölähtöisiin projekteihin Ei projekteja tarvitse «koko» ajan keksiä
2. «Koko» maassa Terveyden ja Hyvinvoinnin laitos on varannut rokotetta
3. Katso «koko» Laukkasen haastattelu klikkaamalla jutun kuvaa
4. Laskuja joutuu «koko» ajan sumplimaan sopimaan ja sovittelemaan
5. voinut käsittää miten asia voi yhtäkkiä ollakin este «koko» uralleni vaikka se ei vaikuta nyrkkeilyyni millään tavalla

### kuusi  /  N   (sample n=2026)

Forms: kuusi:1067, kuusen:412, kuuset:119, kuusia:104, kuuseen:46, kuusesta:45, kuusten:39, kuusien:29, kuusessa:27, kuusta:22

1. Niistä seitsemän on jäljitetty ulkomaille ja «kuusi» on todettu paikallisesti Shandongin provinssissa jossa Qingdao sijaitsee
2. Esimerkiksi sivulla «kuusi» puhutaan päätöksenteosta muttei tekijöistä päätöksenteon takana
3. Tiistaina ohjelmassa oli vaatimukset täyttävän «kuusen» kaataminen Savilahdessa
4. Pihapuut pääsevät vähemmällä kun aaseille tarjoillaan myös «kuusia» kertoo hevostilan emäntä Marianne Jaakkola
5. «Kuusen» taimia kasvatetaan tehokkaissa taimitarhoissa

### kuusi  /  Num   (sample n=16995)

Forms: kuusi:9321, kuuden:4065, kuuteen:771, kuudesta:741, kuudessa:609, kuudella:568, kuutta:408, kuudeksi:168, kuudelle:163, kuutena:72

1. Uusi hakukierros tuotti tyydyttävän tuloksen ja nyt «kuusi» hakijaa on kutsuttu haastatteluun
2. laidalla sijaitsevassa murskaamossa syötettiin perjantaina koneen kitaan yli «kuusi» sataa kiloa norsunluuta
3. «Kuutta» ilmoitusta ei käsitelty viiden asian selvittely on edelleen
4. Hän pelasi Loimaalla «kuusi» kautta
5. on ollut että meillä on ollut tänä vuonna «kuusi» loppuunmyytyä ottelua

### kymmenes  /  N   (sample n=391)

Forms: kymmenes:304, kymmenestä:59, kymmeneksellä:15, kymmeneksen:13

1. Jos joka «kymmenes» tarvitsisi sairaalahoitoa olisivat kustannukset merkittäviä koko yhteiskunnan kannalta
2. Ylinopeuksissa hurjat erot kameratolpittain Siuntiossa joka «kymmenes» hurjastelee Raumalla Suomen rauhallisimmat kuskit
3. Alepa-ketjun henkilökunnasta enemmän kuin joka «kymmenes» on Leväsen mukaan maahanmuuttajia
4. otetaan 65 eli vain hieman useampi kuin joka «kymmenes»
5. Kyselyyn vastanneista esimerkiksi joka «kymmenes» oli ottanut kuvia onnettomuuspaikoilta

### kymmenes  /  Num   (sample n=1248)

Forms: kymmenes:581, kymmenenneksi:171, kymmenennen:133, kymmenentenä:119, kymmenennellä:63, kymmenettä:60, kymmenennessä:37, kymmenenteen:23, kymmenenneltä:20, kymmenennelle:14

1. kovaa taistoa tallien välillä kun autot porhaltavat kauden «kymmenenteen» kilpailuun
2. Kotkaniemen kauden «kymmenes» osuma oli historian neljänneksi nopein ulkoilmaottelussa
3. «Kymmenennellä» minuutilla Markus Kankaanperä otti yhteen Mikael Ahlenin kanssa
4. NST:n miesten kausi päättyi «kymmenenteen» sijaan
5. Nyt jopa olympiamenestys olisi realismia Riossa hän sijoittui «kymmenenneksi» tuloksella 192 kiloa

### live  /  Adv   (sample n=306)

Forms: live:306

1. Also I think it’s crazy Riku needs to «live» with 500 euros
2. Maaliskuun aikana Yle «Live» Stigin ja Kullankaivajien Erinin Scandivanian Music Groupin ja
3. Uunituore dokumentti Cheekistä ja Yle «Live» -taltiointi Blockfestistä Kakkosella sunnuntaina 8.11
4. Lippuja myytiin «Live» Nationin Finlandin järjestämään tilaisuuteen yhteensä 55 000 kappaletta
5. Yle Teema klo 19.10 alkaen Rocky Horrow Show «Live» Kulttishown tuore live-taltiointi Lontoon West Endistä

### live  /  N   (sample n=744)

Forms: live:737, live-:5, -live:2

1. hyväntekeväisyyteen levytyksillä ja konserteilla muun muassa vuoden 1985 «Live» Aid -konsertteilla
2. Lähteet «Live» Nation
3. Marja Hintikka «Live»
4. Net-tuki «Live» chat-päivystys www.tukinet.net Ma-to klo 15.00-19.00
5. Reprise FRANS KEDES Probably Nothing LACKLUSTER «Live» at Sähkökirjasto 2015 osa SATOI Live at Sähkökirjasto

### panna  /  A   (sample n=1)

Forms: pannaton:1

1. «Pannaton» poistetaan päiviltä

### panna  /  N   (sample n=387)

Forms: panna:95, pannan:64, pannassa:55, pannaan:55, pannaa:27, pannasta:23, paneminen:13, panemisesta:11, panemista:8, pannat:8

1. pelaajaa koska seuraava tälli tietää koko kauden mittaista «pannaa»
2. HIFK-kapteenille kahden pelin «panna» kurinpitäjä armahti Ilves-hyökkääjän
3. Tervaportin mukaan «panna» jätti rangaistun kirkon sakramenttien ulkopuolelle eivätkä sakramentit muutenkaan
4. asuu yhdessä Melanien kanssa mutta suhde on pelkkää «panemista» eikä se tyydytä Yannia henkisesti
5. katsomoon veljensä avuksi sai sakkoa ja neljän pelin «pannan»

### panna  /  V   (sample n=4056)

Forms: panna:646, pannaan:510, pani:424, pantiin:419, pantu:360, panee:322, pannut:255, pane:157, panemaan:115, pantava:115

1. lakkautusuhan alla olevien neljän lähikoulun aktiiviset vanhemmat ovat «panneet» tuulemaan
2. Ajattelin että «pannaan» nyt jotain vähän toisella tavalla kansiin
3. Energialaitosten käyttämät puupolttoaineet pitäisi «panna» verolle ehdottaa Suomen ilmastopaneelin puheenjohtaja Markku Ollikainen
4. laukomaan pallon maaliin hankalastakin paikasta mutta entäpä jos «pannaan» ensin pää pyörälle ja käsketään laukoa sen jälkeen
5. Hänkin on «pannut» merkille kasvaneet uimarimäärät

### päästä  /  Adp   (sample n=4824)

Forms: päästä:4803, päästäkin:16, päästäkään:3, päästähän:2

1. lupailivat että Niemi pystyy kävelemään viikon tai parin «päästä»
2. jo jotakin tästä outoudesta haltuun ja kolmen viikon «päästä» olemme jo aikamoisia etätyön ja uudenlaisen arjen hallitsemisen
3. Tuossa muutaman vuoden «päästä» olisi vähän kuin koti EM-kisat Saksassa lähellä Beerbaumeja
4. Ikääntyneiden palveluihin puolestaan tarvitaan vuosikymmenen «päästä» lähes 600 hoitajaa nykyistä enemmän
5. Jos uusia tapauksia ei ilmene ei ehkä hoitokeinoja «päästä» selvittämäänkään

### päästä  /  Adv   (sample n=9)

Forms: päästä:9

1. «Päästä» vähän treenaamaan ja palata Wislaan takaisin maailmancupin kuvioihin
2. «Päästä» lapsi paussille
3. «Päästä» itsesi irti ja ulos
4. «Päästä» vasen käsi irti alakulmasta ota kiinni vapaana olleesta
5. «Päästä» luovuutesi valloilleen ja tee kumppareistasi persoonalliset

### päästä  /  N   (sample n=788)

Forms: pääseminen:404, pääsemiseksi:94, pääsemistä:92, pääsemiseen:63, pääsemisen:51, pääsemisestä:49, pääsemiselle:7, pääsemisessä:7, pääsijät:6, pääsemisellä:3

1. Joukkueeseen «pääseminen» toi paljon itseluottamusta
2. Jäiden lähtiessä riemu vesille «pääsemisestä» on niin suuri että tuskin maltan jättää katiskaa
3. sama huone kuin se jossa nukun on ammattirooliin «pääsemiseksi» pidettävä yllä joitakin rutiineja
4. Etsiminen on hienoa ja perille «pääseminen» tylsää
5. Poliisin toimintavalmius eli aika joka poliisipartiolta kuluu tapahtumapaikalle «pääsemiseen» piteni 0,9 minuuttia

### päästä  /  V   (sample n=64363)

Forms: pääsee:11404, pääsi:8246, päästä:8208, päässyt:6106, pääse:4594, pääsevät:4316, päästään:3115, pääsivät:2274, päässeet:2174, päästy:1646

1. Jotta turvavälejä pystytään noudattamaan kirjastoautoon «pääsee» kerrallaan vain viisi ihmistä tai yksi perhekunta
2. Kuopion seudun lähikirjastoihin «pääsee» taas maanantaista lähtien myös silloin kun paikalla ei
3. Voide kannattaa sekoittaa kumihanskat kädessä ettei chiliä «pääse» silmille tai limakalvoille
4. Turun ammattikorkeakoulussa ei luennoille enää «pääse» ilman maskia
5. Ja kun talvi on sellainen että «pääsemme» hiihtämään niin me hiihdämme kertoo rehtori Matti Kompuinen

### rikki  /  A   (sample n=20)

Forms: rikkinen:14, rikkisen:4, rikkistä:1, rikitöntä:1

1. Minna «Rikkinen» on mukana kirkkohallituksen pian päättyvässä tasa-arvo- ja yhdenvertaisuusprojektissa
2. Jukka «Rikkinen» kertoo että esimerkiksi nosturia saavat käyttää vain määrätyt
3. ja sitoo kirkkoa ja seurakuntia sanoo asiantuntija Minna «Rikkinen»
4. Suomessa on tällä hetkellä myynnissä ainoastaan «rikitöntä» kevyttä polttoöljyä mikä mahdollistaa kondenssikattiloiden käytön ilman mitään
5. Julkisessa taiteessa alkaa olla enemmän inhimillisyyttä «Rikkinen» sanoo

### rikki  /  Adv   (sample n=1025)

Forms: rikki:1025

1. koronaviruksesta Ulkomaanmatkailun palautumisessa tasolleen mennee pari vuotta tartuntarajapyykkejä «rikki» Brasiliassa Iranissa ja Ukrainassa
2. Palo tuhosi kerrostaloasunnon Kuopiossa Ikkunat menivät «rikki» liekit löivät ulos
3. iskulauseissa toistellaan politiikan korjaamista kun se on ollut «rikki»
4. Jos moottoritiellä tapahtuu onnettomuus tai auto menee «rikki» pysy rauhallisena
5. Tourin ennakkosuosikille sataa kritiikkiä Hänellä on jotain «rikki» pään sisällä

### rikki  /  N   (sample n=198)

Forms: rikki:155, rikin:18, rikkiä:10, rikki-:5, rikistä:4, rikkeinä:3, rikkiin:2, rikiltä:1

1. syntyvät biotuoteehtaan prosesseissa joiden vaikuttavia kemikaaleja natrium ja «rikki» ovat
2. Jos yksikin moottorien tiivisteistä kuluu «rikki» voi öljyn tai voiteluaineiden höyry päästä myös matkustamoon
3. Kaakkois-rannikolla tuoksuu levä ja välillä «rikin» tapainen tuoksu
4. Puhelimesta julkaistulla mainosvideolla esitetään miten puhelimen «rikki» menneen näytön voi tarvittaessa vaihtaa itse melkein sekunnissa
5. menetelmän soveltamista puunjalostusteollisuuden jätevesiin ja niissä hajua aiheuttavaan «rikkiin»

### riski  /  A   (sample n=730)

Forms: riski:511, riskinsä:83, riskinä:38, riskiä:25, riskeistä:24, riskit:13, riskillä:13, riskejä:8, riskissä:3, riskeinä:2

1. 880 000 latausta vähentää jo «riskiä» tautitartunnoista arvioi Yrttiaho tämän hetkistä tilannetta Ylen aamussa
2. Yleinen rutiinien ja turvallisuudentunteen hajoaminen on myös «riski» mielenterveydelle
3. vaara leviämiselle on silti Pitempi oleskelu Ruotsissa on «riski»
4. pitkään investointitaantumaan on EK:n pääekonomistin Penna Urrilan mielestä «riski» vientiriippuvaiselle Suomelle
5. Siitä on lyhyt askel ajatella että he ovat «riskiä» muille

### riski  /  N   (sample n=9104)

Forms: riski:3196, riskiä:1444, riskejä:1334, riskin:849, riskit:848, riskinä:324, riskien:214, riskeistä:209, riskillä:176, riskiin:86

1. ja potilastietojärjestelmään ei liitytä sen taloudellisten ja toiminnallisten «riskien» takia
2. Renkaan puhkeaminen on niin sanottu välitön «riski»
3. Koronakuoleman «riski» todettiin Englannissa ja Walesissa kolminkertaiseksi verrattuna kuolemaan johtaneeseen
4. Yli 35 vuoden ikä ei sinänsä ollut synnytyksissä «riski» vaan riskit kasvoivat kun ikään liittyi muu riskitekijä
5. Meidän näkemyksemme mukaan tässä on «riski» sekä potilasturvallisuudelle että henkilöstön turvallisuudelle

### taata  /  N   (sample n=343)

Forms: takaamiseksi:220, takaaminen:52, takaamiseen:19, takaamista:15, takaamisessa:11, takaamisen:7, takaamisesta:7, takaamisella:4, taatan:2, takaamisensa:1

1. Se on tarkoitettu sekä matkailijoiden että asukkaiden turvallisuuden «takaamiseksi» kansalaisuudesta riippumatta
2. Juncker sanoi ja viittasi muun muassa rahoitukseen kaasutoimitusten «takaamiseksi» talvella
3. Modernin «Taatan» joulutarinoita
4. esiin esimerkiksi ajatus että Barr määräisi vaalien riippumattomuuden «takaamiseksi» osan vaaliuurnista liittovaltion viranomaisten haltuun tai pyrkisi joko
5. kysymyksiä ja vastauksia työvelvollisuudesta poissaolon perusteista ja työvoiman «takaamisesta» silloin kun seuraavan työvuoron kaikki työntekijät olisivatkin sairaana

### taata  /  V   (sample n=3354)

Forms: takaa:803, taata:741, takaamaan:265, takasi:204, taataan:193, takaisin:149, takaavat:139, taattu:121, takaisi:102, taannut:90

1. keskeyttivät harjoittelun Shanghaissa koronaviruksen vuoksi sairaala ei voinut «taata» turvallisuutta
2. Nykykenkien laatu «takaa» suutareille koko ajan lisää työtä
3. mukaan jo varhaisessa vaiheessa sillä näin he pystyivät «takaamaan» SM-hiihtoihin hyvän tykkilumiladun
4. työpaikat ja asunnot sekä paikkakuntaan sidotun asumisoikeuden mikä «takasi» julkisen koulutuksen ja sosiaaliedut
5. Ei meidän tarvitse geenimuuntelusta luopua kunhan «taataan» luomun mukana olo siinä rinnalla

### vasta  /  Adv   (sample n=20474)

Forms: vasta:20414, vastakin:25, vastahankaan:20, vastahan:14, vastasti:1

1. kasvavat jo pienistä alkoholimääristä miehillä alkoholin syöpävaikutukset ilmaantuvat «vasta» suuremmilla annoksilla
2. «Vasta» viime kevään mestaruus avasi mahdollisuuden hakea liigapaikkaa
3. Miksi potkut annettiin «vasta» kun mahdollisuudet lopputurnaukseen olivat käytännössä jo menneet
4. 160 000 turvapaikanhakijasta on onnistuttu siirtämään «vasta» vajaat 200
5. riittäisi yli 1 100 yksinyrittäjille mutta tukea on hakenut «vasta» vajaat 450 yritystä

### vasta  /  N   (sample n=8033)

Forms: vastaan:6685, vastassa:1050, vastoin:82, vastaansa:59, vastassaan:42, vastan:36, vastaa:12, vastassamme:9, vastoja:7, vastat:7

1. mahdollista että lämpenee mutta syksy tulee jo pian «vastaan»
2. Seuraava akilleen kantapää tulee «vastaan» kotona jos kukan on saanut hengissä sinne asti
3. olen aika väsynyt McKinney naurahtaa ja halaa lentoasemalla «vastassa» olevaa vaimoaan ja tytärtään
4. Hän tuli «vastaan» kisakylässä ja toivotti onnea koko Suomen joukkueelle Barcelonassa
5. Tässä «vastassa» Haka heinäkuussa 2014

### voi  /  A   (sample n=4)

Forms: voiton:3, voiton-:1

1. Ässien «Voiton» kivi odottaa kohtaloaan Isomäen remontissa
2. Ässien «Voiton» kivi odottaa kohtaloaan Isomäen remontissa
3. ravintoa omaisuutta tms kiihkeästi haluava perso ahnas rahan- «voiton-» tms himoinen
4. «Voiton» kalkki voisi maistua karvaalta

### voi  /  Adv   (sample n=324)

Forms: voikin:246, voihan:47, voiko:20, voikaan:6, voipa:4, voipahan:1

1. Kyllä siinä on havaittavissa tiettyä jännitystä «voihan» se vähän väkinäistä alussa olla
2. Osuvampi kuvaus «voikin» löytyä amerikkalaisen psykologin Lisa Diamondin esittelemästä naisen seksuaalisuuden
3. Jos niiden nauttiminen auttaa niin «voihan» niitä ottaa
4. Hallitus pähkäilee turvapaikanhakijoiden jalkapantoja rajunkuuloinen keino «voikin» helpottaa palautusta odottavien asemaa
5. Katsaus aikaisempien vuosien kättelyihin «voikin» tänä vuonna olla paikallaan sillä koronan vuoksi on

### voi  /  Interj   (sample n=507)

Forms: voi:507

1. Kyllä todellakin «voi»
2. Niitä vaan ei tuota kukaan eikä kääriä «voi» mukaan
3. «Voi» kunpa tämä yö jatkuisi aina vaan kotini ei
4. «Voi» jonkun verran vaikuttaa mutta en usko että tämä
5. Enhän minä «voi» sitä edellyttää että kaikki menee minun tahtoni mukaan

### voi  /  N   (sample n=1027)

Forms: voi:349, voit:273, voita:148, voin:86, voinko:30, voissa:28, voitko:18, voilla:9, voihan:8, voihin:8

1. voi kerätä jo keväällä kun routa sulaa niin «voi» kaivaa
2. Toivomme avointa keskustelua ja «voisihan» tämän tiimoilta järjestää vaikka suunnittelukilpailun nuorille jolloin saisimme
3. «Voi» auttaa joko ruualla rahalla tai rukoilemalla Leila jatkaa
4. On ihan sama «voitammeko» 2–1 vai 3–2 pääasia on että voitamme Khudobin
5. Miten valtaa pitävä «voi» välittää viestinsä vallan rakenteista jotka eivät välttämättä näe

### vuoksi  /  A   (sample n=1)

Forms: vuoksisen:1

1. Varikonniemen merkityksen «vuoksisen» viereen kaavoitettavan asuinalueen arkeologinen tutkimus oli välttämätöntä

### vuoksi  /  Adp   (sample n=32244)

Forms: vuoksi:32239, vuoksikin:4, vuoksihan:1

1. kukaan ulkopuolinen ei tällä hetkellä pääse vesitorniin minkä «vuoksi» tapahtumapalvelut joutuivat etsimään iltasoitolle uuden paikan kertoo Lappeenrannan
2. opiskelija Laura Kulmala kertoi tulleensa syrjityksi työnhaussa sukupuolensa «vuoksi»
3. Klaus Iohannis kehotti perjantaina Pontaa eroamaan virastaan korruptiosyytösten «vuoksi»
4. Kerrostaloasujien arki muuttuu koronan «vuoksi» saunavuorot on peruttu kosketuspintoja jynssätään ankarasti ja naapurisopu
5. jonka takia kone oli menettänyt ohjattavuutensa ja tämän «vuoksi» ohjaaja oli joutunut tekemään pakkolaskun

### vuoksi  /  N   (sample n=127)

Forms: vuoksen:47, vuokseen:32, vuoksella:12, vuoksessa:12, vuoksesta:9, vuoksenne:5, vuoksi-:4, vuoksi:2, vuokselta:1, vuoksikin:1

1. Vielä viime vuonna ravustusaika «Vuoksella» oli vain kaksi viikkoa
2. «Vuoksen» rannoilla on asutusta jo ennestään nyt suunnitteilla on
3. Kolme pilkkijää putosi jäihin «Vuoksessa» Imatralla Varpasaaren edustalla
4. «Vuoksen» pinnan alta löytyy runsaasti rapujen tekemiä koloja eli
5. Sanna Marin SDP:n puheenjohtajaksi Teidän ansiosta ja teidän «vuoksenne» Valtapelit yritetään purkaa keskusteluilla Yle seuraa kokousta
