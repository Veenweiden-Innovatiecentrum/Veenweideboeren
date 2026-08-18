/* Hoofdstuk C als magazine — VOLLEDIGE, LETTERLIJKE tekst uit het brondocument.
   Geen woord weggelaten, niets herschreven. Het verschil met de documentvorm
   zit volledig in de opmaak: full-bleed opener, lead met drop cap, editoriale
   callouts, een marge-pull-quote (verbatim herhaling ter nadruk), een triptiek
   die de drie-diensten-alinea in drie kaarten zet, en een afsluitende band.
   De leesvolgorde is exact gelijk aan het document. */

function MagC({ foto }) {
  return (
    <div className="magc" data-screen-label="Visie magazine — hoofdstuk C (proef)">

      {/* 1. full-bleed opener — alleen de hoofdstuktitel */}
      <header className="magc-opener">
        <img src={foto} alt="" className="magc-opener-img" />
        <div className="magc-opener-veil"></div>
        <div className="magc-opener-tekst">
          <span className="magc-kicker magc-kicker--licht">Hoofdstuk C · de omslag</span>
          <h1 className="magc-titel">Van klempositie<br />naar motorblok</h1>
        </div>
      </header>

      {/* 2. lead — eerste zin groot, rest van alinea 1 met drop cap (volledig) */}
      <section className="magc-lead-wrap">
        <p className="magc-lead">De boer is niet het probleem,<br /><span className="magc-lead-accent">de boer is de motor.</span></p>
        <div className="magc-lead-body">
          <p className="magc-dropcap">Waterkwaliteit, biodiversiteit, broeikasgasreductie: ze worden pas bereikbaar als de boer er een verdienmodel in ziet. Verdienmodel betekent hier méér dan geld: het gaat om toekomstperspectief — werken aan de opgaves moet de overlevingskans van het bedrijf vergroten in plaats van bedreigen. Dat veel jonge boeren het vandaag als bedreiging ervaren, is precies de omkering die deze visie wil maken. Niet ondanks ondernemerschap, maar dankzij. Mits de overheid de juiste condities schept.</p>
        </div>
      </section>

      {/* 3. callout — Ondernemerschap als motor (verbatim) */}
      <aside className="magc-callout magc-callout--groen">
        <span className="magc-callout-label">Ondernemerschap als motor</span>
        <p>Waarom zouden veenweideboeren betaald worden uit publieke middelen? Niet omdat ze het moeilijk hebben. Maar <strong>omdat ze een publieke dienst leveren.</strong> Schoon water, vastgehouden koolstof, weidevogels, landschapskwaliteit, dat zijn diensten waar de samenleving dagelijks gebruik van maakt en die ze nergens anders vandaan krijgt. Dat is geen steun. Dat is een zakelijke transactie tussen een leverancier en de samenleving die een dienst afneemt. Dat is geen radicale koerswijziging maar een aanvulling op bestaand overheidsdenken: landbouw is beleidsmatig altijd al deels nutsfunctie geweest — de samenleving voorzien van betaalbaar, gezond en veilig voedsel — en deels economische activiteit. Nieuw is alleen dat de nutsfunctie breder wordt: naast voedsel ook water, koolstof en landschap.</p>
      </aside>

      {/* 4. body (verbatim) */}
      <div className="magc-body">
        <p>Bij dat publieke-dienstargument komt een tweede argument dat in beleidsgesprekken zelden expliciet wordt gemaakt: in een Nederland waar de ruimtedruk historisch hoog is, vormt het veenweidegebied een uitzondering. De recent gepubliceerde Ontwerp-Nota Ruimte schetst een land waarin wonen, defensie, datacenters, energie-infrastructuur, voedselproductie in nieuwe vormen, bouwmaterialen, infrastructuur en handelsroutes allemaal aanspraak maken op dezelfde vierkante meters. In dat licht is het veenweidegebied — honderdduizenden hectares die vandaag monofunctioneel als gras voor melk worden gebruikt — een zeldzame ruimtelijke reserve. Wie zwijgt over wat er met die ruimte gebeurt, is de eerste die overruled wordt door wie luider claimt.</p>
      </div>

      {/* 5. callout — Drager van een schaarse hulpbron (verbatim) */}
      <aside className="magc-callout magc-callout--blauw">
        <span className="magc-callout-label">Drager van een schaarse hulpbron</span>
        <p>De veenweideboer is niet alleen leverancier van publieke diensten — óók de drager van een schaarse hulpbron: ruimte zelf, die de samenleving niet elders kan ophalen. Daarmee wordt zijn positie dubbel onderbouwd. Een datacenter doet één ding. Een woonwijk doet één ding. Een defensieterrein doet één ding. De veenweideboer in akte III doet zes of zeven dingen tegelijk op dezelfde hectare. In een land waar elke vierkante meter strategisch wordt afgewogen, is dat geen marginale positie maar een hoofdrolpositie. Verdwijnt deze drager, dan wordt diezelfde ruimte herverdeeld onder de claimantenrij — zonder garantie dat die nieuwe gebruikers de maatschappelijke opgaves invullen.</p>
      </aside>

      {/* 6. rebuttal — volledige alinea + marge-pull-quote (verbatim herhaling) */}
      <section className="magc-rebut">
        <p className="magc-rebut-q">“Maar maak er dan<br />helemaal natuur van.”</p>
        <div className="magc-rebut-body">
          <p>"Maar maak er dan helemaal natuur van", die tegenwerping is logisch en moet expliciet weerlegd worden. Pure natuur zou betekenen: voedselproductie verplaatsen naar elders, met alle import-, transport- en klimaatkosten van dien. De veenweideboer levert juist meerdere producten op één plek: voedsel én water én koolstofopslag én biodiversiteit én landschap. Dat is geen tweederangs natuur en geen tweederangs landbouw, het is een combinatie die nergens anders zo efficiënt kan. Strategisch is voedselproductie in eigen gebied een waarde op zich, zeker in een wereld waarin geopolitiek voedsel weer een schaarste-issue wordt. En wie er natuur van maakt, is niet goedkoper uit: natuurbeheer kost óók publiek geld — maar dan zonder voedsel, zonder ondernemerschap en zonder beheerder met eigen belang bij het resultaat. Het meerproducten-frame is daarmee niet een compromis tussen natuur en landbouw, maar een meerwaarde die beide overstijgt.</p>
        </div>
      </section>

      {/* 7. body (verbatim) */}
      <div className="magc-body">
        <p>Akte I lijkt te werken omdat er nog niks is gebeurd. Het is geen stabiele toestand, het is een kwetsbaarheidspositie die zich pas openbaart bij de volgende schok — in soja, kunstmest, melkprijs, klimaat of regelgeving. Akte III is in die zin niet een morele maar een ontwerpkeuze: een antifragiel systeem dat van variatie profiteert in plaats van eraan onderdoor te gaan.</p>
      </div>

      {/* 8. sectie-breuk */}
      <section className="magc-sectiebreuk">
        <span className="magc-kicker">Buitengericht</span>
        <h2 className="magc-h2">Het veenweidegebied als oplossingsleverancier</h2>
      </section>

      {/* 9. body (verbatim) */}
      <div className="magc-body">
        <p>De waarde-argumenten tot dusver gaan over wat er <em>in</em> het veenweidegebied gebeurt: klimaat, water, natuur, kringloop, voedselzekerheid, cultuur en wonen. Allemaal opgaves binnen het gebied zelf. Maar het verhaal kan een stap groter. Het veenweidegebied is niet alleen een gebied dat hulp behoeft, het is ook een gebied dat <em>oplossingen levert</em> aan andere sectoren en regio's.</p>
        <p className="magc-triptiek-intro">Drie concrete voorbeelden maken dat tastbaar.</p>
      </div>

      {/* 10. triptiek — de drie-diensten-alinea, opgesplitst in kaarten (verbatim) */}
      <div className="magc-triptiek">
        <article className="magc-dienst">
          <span className="magc-dienst-num">01</span>
          <h3>CO₂-compensatie voor de akkerbouw.</h3>
          <p>Akkerbouwgebieden produceren voedsel met aanzienlijke CO₂-uitstoot en zoeken compensatieroutes om aan klimaatdoelen te voldoen. In plaats van het planten van bos op een polder of het inrichten van compensatieprojecten elders, kan een aanzienlijk deel van die compensatie veel efficiënter plaatsvinden in het veenweidegebied. De CO₂-voorraad in het veen is enorm; het remmen van veenoxidatie en het stimuleren van paludicultuur leveren per geïnvesteerde euro mogelijk meer CO₂-reductie op dan bosaanplant op zandgrond.</p>
        </article>
        <article className="magc-dienst">
          <span className="magc-dienst-num">02</span>
          <h3>Organische mest voor de akkerbouw.</h3>
          <p>Veenweidebedrijven produceren mest in een hoeveelheid en kwaliteit die akkerbouwgebieden juist missen, zeker in een context van kunstmestbeperking en bodemverbetering. Wat in de huidige logica nog regelmatig als mestoverschotprobleem wordt geframed, wordt in deze logica een gebiedsoverstijgende dienstenstroom: van veengebied naar akkerbouwgebied, met economische en bodembiologische winst aan beide kanten. De strakkere mestnormen van na de derogatie maken deze stroom voorwaardelijker — minder ruimte per hectare, preciezere balans van stikstof en fosfaat — maar de complementariteit zelf blijft: veen heeft de organische stof die de akkerbouw mist.</p>
        </article>
        <article className="magc-dienst">
          <span className="magc-dienst-num">03</span>
          <h3>Waterbuffer voor de akkerbouw.</h3>
          <p>Wat in akte III op het veenweidebedrijf gebeurt — wateropslag op het eigen land, dynamisch peilbeheer, sloten en greppels als opslag- en infiltratiesysteem — is ruimtelijk veel meer dan een bedrijfsbouwsteen. Het maakt het gebied tot een buffer voor de omliggende regio: in natte winters vangt het veenweidegebied piekafvoer op die anders akkerland onder water zet, in droge zomers levert het water terug aan een akkerbouw die steeds vaker droogtestress kent. Dat is een dienst aan andere voedselproducenten die de akkerbouw zelf niet kan organiseren — en die in een klimaat met grotere extremen alleen maar belangrijker wordt. En dat is geen hypothetische rol: I&amp;W stuurt sinds 2026 op waterzelfvoorzienendheid van veenweidegebieden, met aanzienlijke ruimteclaims voor waterberging als logisch gevolg.</p>
        </article>
      </div>

      {/* 11. body (verbatim) */}
      <div className="magc-body">
        <p>Deze kanteling verandert ook wie er aan tafel komt. Naast LVVN voor de veenweideboer worden ook andere agrarische sectoren (akkerbouw), de industrie, waterschappen en partijen die elders compensatieoplossingen zoeken relevante gesprekspartners. Het maatschappelijke debat over veenweide verschuift van een binnen-gebied probleem naar een gebiedsoverstijgende strategische bron. Institutioneel vraagt dit wel het nodige: bestaande markten zijn er nog niet voor — een akkerbouwer kan niet zomaar CO₂ compenseren door geld naar een Friese veenweideboer over te maken, een organische-mest-marktplaats die kwaliteit en hoeveelheid borgt bestaat niet kant-en-klaar, en betalingsarrangementen voor regionale waterdiensten zijn nog nauwelijks ontwikkeld. Een veenweide-zuivelketen, een organische-mest-platform, een CO₂-certificatensysteem op veen en een waterdienst-vergoeding tussen veen- en akkerbouwgebieden vragen alle vier eigen institutionele inrichting. Precies het type vraagstukken waar het VIC een rol in kan spelen.</p>
        <p className="magc-brug">Dat roept de volgende vraag op: hoe ziet zo'n veenweideboer er dan uit?</p>
      </div>

      {/* 12. afsluitende band — Het frame kantelt (verbatim) */}
      <section className="magc-band">
        <span className="magc-kicker magc-kicker--licht">Het frame kantelt</span>
        <p className="magc-band-tekst">In de huidige Europese context worden investeringen in water, natuur en landschap 'niet-productieve investeringen' genoemd, ze dienen niet de voedselproductie. Maar als maatschappelijke diensten zelf het product worden waarvoor de boer betaald wordt, kantelt dat hele frame. Dan is schoon slootwater geen bijproduct meer maar <em>het product</em>, en het helofytenfilter de productie-installatie. Dan is een natte teelt geen verlies van landbouwgrond maar een nieuwe productielocatie. Voedsel is niet langer het enige product dat van het bedrijf komt. Dat is de fundamentele verschuiving waar dit verhaal over gaat.</p>
      </section>

      <p className="magc-voetnoot">Ontwerpproef: dezelfde, volledige tekst als in de documentvorm — geen woord weggelaten, niets herschreven — alleen redactioneel opgemaakt. Wissel bovenaan tussen <em>document</em> en <em>magazine</em>.</p>
    </div>
  );
}

window.MagC = MagC;
