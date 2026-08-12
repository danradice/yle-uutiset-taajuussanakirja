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


