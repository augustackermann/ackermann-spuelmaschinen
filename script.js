// Customer-story slider: one frame, images cross-fade, caption updates
(function () {
  const story = document.querySelector('.story');
  if (!story) return;
  const photos = Array.from(story.querySelectorAll('.story-photo'));
  const dots = Array.from(story.querySelectorAll('.story-dot'));
  const quote = story.querySelector('#story-quote');
  const person = story.querySelector('#story-person');
  const firm = story.querySelector('#story-firm');
  const link = story.querySelector('#story-link');
  if (photos.length < 2) return;
  let i = 0, timer;

  function show(n) {
    i = (n + photos.length) % photos.length;
    photos.forEach((p, k) => p.classList.toggle('is-active', k === i));
    dots.forEach((d, k) => d.classList.toggle('is-active', k === i));
    const p = photos[i].dataset;
    if (quote) quote.textContent = '„' + p.quote + '“';
    if (person) person.textContent = p.person;
    if (firm) firm.textContent = p.firm;
    if (link) link.href = p.url;
  }
  function next() { show(i + 1); }
  function prev() { show(i - 1); }
  function start() { stop(); timer = setInterval(next, 5000); }
  function stop() { if (timer) clearInterval(timer); }

  story.querySelector('.story-arrow--next').addEventListener('click', () => { next(); start(); });
  story.querySelector('.story-arrow--prev').addEventListener('click', () => { prev(); start(); });
  dots.forEach((d) => d.addEventListener('click', () => { show(+d.dataset.go); start(); }));
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stop();
    else start();
  });
  start();
})();

// Mobile navigation toggle
const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.nav');

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// Maschinenfinder: transparent rule-based preselection for machine + system.
(function () {
  const root = document.querySelector('#maschinenfinder');
  if (!root) return;

  const stylesheetHref = document.querySelector('link[href$="/styles.css"]')?.getAttribute('href') || '/styles.css';
  const siteBase = stylesheetHref.replace(/\/styles\.css$/, '');
  const sitePath = (path) => `${siteBase}${path}`;

  const machines = {
    'u-430-2': { name: 'U 430-2', series: 'Kompakte Untertischspülmaschine · 40 Körbe/h', image: '/assets/img/machines/U-430-2.png', url: '/produkte/spuelmaschinen/u-430-2/', max: 40, basket: '400 × 400 mm', power: '230 V' },
    'u-440': { name: 'U 440', series: 'Gläser- und Bistrospülmaschine · 40 Körbe/h', image: '/assets/img/machines/U-440.png', url: '/produkte/spuelmaschinen/u-440/', max: 40, basket: '400 × 400 mm', power: '230 V' },
    'u-540-bistro': { name: 'U 540 Bistro', series: 'Breite Gläser- und Bistrospülmaschine · 40 Körbe/h', image: '/assets/img/machines/U-540-Bistro.png', url: '/produkte/spuelmaschinen/u-540-bistro/', max: 40, basket: '500 × 500 mm', power: '230/400 V' },
    'u-530-2': { name: 'U 530-2 / U 530-2E', series: 'Untertischspülmaschine · 40 Körbe/h', image: '/assets/img/machines/U-530-2.png', url: '/produkte/spuelmaschinen/u-530-2/', max: 40, basket: '500 × 500 mm', power: '230/400 V', hasE: true },
    'u-540e': { name: 'U 540 / U 540E', series: 'Untertisch-Geschirrspülmaschine · 40 Körbe/h', image: '/assets/img/machines/U-540E.png', url: '/produkte/spuelmaschinen/u-540e/', max: 40, basket: '500 × 500 mm', power: '400 V', hasE: true },
    'u-640e': { name: 'U 640 / U 640E', series: 'Untertisch für Geschirr, Tabletts und Gerätschaften · 48 Körbe/h', image: '/assets/img/machines/U-640E.png', url: '/produkte/spuelmaschinen/u-640e/', max: 48, basket: '500 × 500 mm / EN 4', power: '400 V', hasE: true },
    'h-530-2': { name: 'H 530-2 / H 530-2E', series: 'Kompakte Haubenspülmaschine · 40 Körbe/h', image: '/assets/img/machines/H-530-2.png', url: '/produkte/spuelmaschinen/h-530-2/', max: 40, basket: '500 × 500 mm', power: '400 V', hasE: true, hood: true },
    'h-540e': { name: 'H 540 / H 540E', series: 'Haubenspülmaschine · 60 Körbe/h', image: '/assets/img/machines/H-540E.png', url: '/produkte/spuelmaschinen/h-540e/', max: 60, basket: '500 × 500 mm', power: '400 V', hasE: true, hood: true },
    'h-540e-klima-plus': { name: 'H 540 Klima+ / H 540E Klima+', series: 'Haubenspülmaschine mit Wärmerückgewinnung · 60 Körbe/h', image: '/assets/img/machines/H-540E-Klima-Plus.png', url: '/produkte/spuelmaschinen/h-540e-klima-plus/', max: 60, basket: '500 × 500 mm', power: '400 V', hasE: true, hood: true, climate: true },
    'h-640': { name: 'H 640', series: 'Haubenspülmaschine für gemischtes Spülgut · 60 Körbe/h', image: '/assets/img/machines/H-640.png', url: '/produkte/spuelmaschinen/h-640/', max: 60, basket: '500 × 500 mm / EN 4', power: '400 V', hood: true },
    'h-640-klima-plus': { name: 'H 640 Klima+', series: 'Große Haubenspülmaschine mit Wärmerückgewinnung · 60 Körbe/h', image: '/assets/img/machines/H-640-Klima-Plus.png', url: '/produkte/spuelmaschinen/h-640-klima-plus/', max: 60, basket: '500 × 500 mm / EN 4', power: '400 V', hood: true, climate: true },
    'f-720': { name: 'F 720', series: 'Gerätespülmaschine · Spülgut bis 800 × 600 mm', image: '/assets/img/machines/F-720.png', url: '/produkte/spuelmaschinen/f-720/', max: 30, basket: 'Gerätegrundkorb 700 × 700 mm', power: '400 V', utensil: true },
    'f-920': { name: 'F 920', series: 'Gerätespülmaschine XL · Spülgut bis 1.200 × 600 mm', image: '/assets/img/machines/F-920.png', url: '/produkte/spuelmaschinen/f-920/', max: 30, basket: 'XL-Gerätekorb', power: '400 V', utensil: true },
    'kt-1': { name: 'KT-1', series: 'Korbtransportspülmaschine · 80–160 Körbe/h', image: '/assets/img/machines/KT1.png', url: '/produkte/spuelmaschinen/kt-1/', max: 160, basket: '500 × 500 mm', power: '400 V', conveyor: true },
    'kt-1-plus': { name: 'KT-1 Plus', series: 'Effiziente Korbtransportspülmaschine · 100–200 Körbe/h', image: '/assets/img/machines/KT1-Plus.png', url: '/produkte/spuelmaschinen/kt-1-plus/', max: 200, basket: '500 × 500 mm', power: '400 V', conveyor: true },
    'kt-2': { name: 'KT-2', series: 'Korbtransportspülmaschine mit Vorspülzone · 130–270 Körbe/h', image: '/assets/img/machines/KT2.png', url: '/produkte/spuelmaschinen/kt-2/', max: 270, basket: '500 × 500 mm', power: '400 V', conveyor: true },
    'kt-2-plus': { name: 'KT-2 Plus', series: 'Korbtransport-Flaggschiff · 135–270 Körbe/h', image: '/assets/img/machines/KT2-Plus.png', url: '/produkte/spuelmaschinen/kt-2-plus/', max: 270, basket: '500 × 500 mm', power: '400 V', conveyor: true }
  };

  const form = root.querySelector('#finder-form');
  const steps = Array.from(root.querySelectorAll('.finder-step'));
  const result = root.querySelector('#finder-result');
  const next = root.querySelector('#finder-next');
  const back = root.querySelector('#finder-back');
  const restart = root.querySelector('#finder-restart');
  const error = root.querySelector('#finder-error');
  const stepLabel = root.querySelector('#finder-step-label');
  const progressValue = root.querySelector('#finder-progress-value');
  const progressBar = root.querySelector('#finder-progress-bar');
  let step = 0;

  function selected(name) {
    const control = form.querySelector(`[name="${name}"]:checked`);
    return control ? control.value : '';
  }

  function showStep(index) {
    step = index;
    steps.forEach((item, i) => {
      item.classList.toggle('is-active', i === step);
      item.hidden = i !== step;
    });
    const percent = Math.round(((step + 1) / steps.length) * 100);
    stepLabel.textContent = `Schritt ${step + 1} von ${steps.length}`;
    progressValue.textContent = `${percent} %`;
    progressBar.style.width = `${percent}%`;
    back.hidden = step === 0;
    next.textContent = step === steps.length - 1 ? 'Empfehlung anzeigen →' : 'Weiter →';
    error.hidden = true;
    steps[step].querySelector('legend').focus?.();
  }

  function transportModel(capacity) {
    if (capacity <= 160) return 'kt-1';
    if (capacity <= 200) return 'kt-1-plus';
    return 'kt-2-plus';
  }

  function chooseMachine(answers) {
    const capacity = Number(answers.capacity);
    if (answers.washware === 'utensil1200') return 'f-920';
    if (answers.washware === 'utensil800') return 'f-720';

    if (capacity > 60 || answers.setup === 'conveyor') return transportModel(capacity);

    if (answers.washware === 'tray600') {
      if (answers.setup === 'hood' || capacity > 48) {
        return answers.climate ? 'h-640-klima-plus' : 'h-640';
      }
      return 'u-640e';
    }

    if (answers.setup === 'hood' || capacity > 48) {
      if (capacity <= 40 && !answers.climate) return 'h-530-2';
      return answers.climate ? 'h-540e-klima-plus' : 'h-540e';
    }

    if (answers.washware === 'glasses') {
      if (answers.setup === 'compact400' || answers.power === '230') return 'u-440';
      return 'u-540-bistro';
    }
    if (answers.power === '230') return 'u-530-2';
    if (answers.washware === 'mixed' && capacity > 40) return 'u-640e';
    return 'u-540e';
  }

  function washwareReason(value) {
    const labels = {
      glasses: 'auf Gläser und Tassen abgestimmtes Korbformat',
      dishes: 'passend für Geschirr und Besteck im Tagesgeschäft',
      mixed: 'flexibel für gemischtes Spülgut',
      tray600: 'geeignet für Tabletts und Behälter bis 600 × 400 mm',
      utensil800: '850 mm Einfahrhöhe für Bleche, Töpfe und Gerätschaften',
      utensil1200: 'für sehr großes Spülgut bis 1.200 × 600 mm ausgelegt'
    };
    return labels[value];
  }

  function setupReason(machine) {
    if (machine.conveyor) return 'automatischer Korbtransport für kontinuierlichen Durchsatz';
    if (machine.utensil) return 'spezialisierte Gerätebauform für sperriges Spülgut';
    if (machine.hood) return 'ergonomisches Durchschubprinzip für schnelle Korbwechsel';
    return `${machine.basket} Korbmaß bei kompakter Untertisch-Aufstellung`;
  }

  function waterRecommendation(machine, answers) {
    const parts = [];
    if (answers.hardness === 'unknown') {
      parts.push('Wasseranalyse vor der Bestellung: Härte und Salzgehalt sind noch unbekannt.');
    } else if (answers.hardness === 'soft') {
      parts.push('Bei bestätigten maximal 5 °dH ist für den Kalkschutz in der Regel keine zusätzliche Enthärtung nötig.');
    } else if (machine.hasE) {
      parts.push(`Die E-Ausführung mit eingebautem Enthärter und Regeneriersalz 2/6 wählen; Härtebereich bei Inbetriebnahme einstellen.`);
    } else if (machine.conveyor) {
      parts.push('Externes, auf den maximalen Stundenverbrauch dimensioniertes Enthärtungssystem vorsehen; Auslegung durch Ackermann erforderlich.');
    } else if (machine.hood || machine.utensil) {
      parts.push('Duomat S oder eine passend dimensionierte externe Enthärtungsanlage für kontinuierliches Weichwasser vorsehen.');
    } else {
      parts.push('Monomat Simplex als kompakte externe Enthärtung einplanen; bei unterbrechungsfreiem Bedarf Duomat S prüfen.');
    }

    if (answers.finish === 'shine') {
      parts.push(Number(answers.capacity) <= 60
        ? 'Für glänzende, fleckenarme Ergebnisse zusätzlich eine Teilentsalzungspatrone TE 15 S bzw. TE 20 S nach Wasseranalyse prüfen.'
        : 'Für fleckenarme Ergebnisse eine auf den Durchsatz ausgelegte Teil- oder Vollentsalzung prüfen.');
    }
    if (answers.finish === 'polishfree') {
      parts.push(machine.conveyor
        ? 'Für polierfreie Ergebnisse ist eine individuell dimensionierte Umkehrosmose oder Vollentsalzung erforderlich.'
        : 'KPRO Compact (160 l/h) als Umkehrosmose-Vorschaltgerät prüfen; Vorfilter und eventuelle Vorenthärtung richten sich nach der Wasseranalyse.');
    }
    return parts.join(' ');
  }

  function accessoriesFor(machine, answers) {
    const items = [];
    if (answers.washware === 'glasses') {
      items.push(`Gläserkorb mit Schrägstellung in ${machine.basket.startsWith('400') ? '400 × 400 mm' : '500 × 500 mm'}`, 'Besteckköcher für Kleinteile');
    } else if (answers.washware === 'dishes') {
      items.push('Tellerkorb 18/12', 'Universal- oder Besteckkorb mit passenden Köchern');
    } else if (answers.washware === 'mixed') {
      items.push('Tellerkorb 18/12', 'Universalkorb mit wechselbaren Einsätzen', 'Besteckköcher');
    } else if (answers.washware === 'tray600') {
      items.push('Tablettkorb GN 500 × 500 mm', 'Einlegegitter für Euronorm-Kisten bzw. passende Behältereinsätze');
    } else if (answers.washware === 'utensil800') {
      items.push('Gerätegrundkorb 700 × 700 mm', 'Blecheinsatz und Kleinteilekorb nach Spülgut');
    } else {
      items.push('XL-Gerätekorb passend zur F 920', 'Blecheinsatz bzw. Sonderanfertigung nach Spülgut');
    }
    if (machine.hood || machine.conveyor) items.push('Zu- und Ablauftisch sowie Schlauchpendelbrause für Vorsortierung und Vorspülen');
    if (answers.hardness !== 'soft') items.push('Regeneriersalz 2/6 bei Enthärtung');
    return items;
  }

  function chemistryFor(answers) {
    if (answers.washware === 'glasses') return 'F 440 Bistro oder F 450 green plus KLAR GG sauer. Dosierung auf Wasseranalyse und Gläser abstimmen.';
    if (answers.washware === 'utensil800' || answers.washware === 'utensil1200' || answers.washware === 'tray600') return 'F 600 GR für Geschirr und Gerätschaften plus KLAR GS; bei starker Belastung Anwendung vor Ort abstimmen.';
    return 'F 500 GS als Geschirrreiniger plus KLAR GS. Bei starker Fett- oder Stärkebelastung F 540 Power prüfen.';
  }

  function notices(machine, answers) {
    const notes = ['Vorauswahl: Vor Bestellung sind Wasseranalyse, reale Spitzenlast, Einfahrhöhe, Strom, Wasser, Abfluss und Aufstellmaße fachlich zu bestätigen.'];
    const capacity = Number(answers.capacity);
    if (answers.power === '230' && machine.power === '400 V') notes.unshift(`Wichtig: ${machine.name} benötigt 400 V. Wenn kein Drehstromanschluss hergestellt werden kann, muss Leistung oder Bauform neu geplant werden.`);
    if (answers.power === 'unknown') notes.unshift('Stromanschluss vor Bestellung prüfen; die Empfehlung kann 400 V voraussetzen.');
    if (machine.utensil && capacity > machine.max) notes.unshift(`Die F-Serie ist auf großes Spülgut ausgelegt und erreicht theoretisch 30 Körbe/h. Für die gewählte Spitzenmenge sind Prozessplanung, eventuell mehrere Maschinen oder eine Sonderlösung nötig.`);
    if (answers.setup === 'compact400' && !['u-430-2', 'u-440'].includes(Object.keys(machines).find(key => machines[key] === machine))) notes.unshift('Das gewählte Spülgut passt nicht sinnvoll in eine 400-×-400-mm-Kompaktmaschine; die Empfehlung benötigt mehr Stellfläche.');
    if (answers.climate && !machine.climate) notes.unshift('Klima+ ist nur bei passenden Haubenmodellen verfügbar; für diese Bauform muss die Lüftungs- und Energielösung separat geplant werden.');
    return notes.join(' ');
  }

  function renderResult() {
    const answers = {
      washware: selected('washware'),
      capacity: selected('capacity'),
      setup: selected('setup'),
      power: selected('power'),
      hardness: selected('hardness'),
      finish: selected('finish'),
      climate: Boolean(form.querySelector('[name="climate"]:checked'))
    };
    const key = chooseMachine(answers);
    const machine = machines[key];
    const reasons = [washwareReason(answers.washware), `Leistungsbereich bis ${machine.max} Körbe/h`, setupReason(machine)];
    if (machine.climate) reasons.push('Klima+ nutzt Wärmerückgewinnung und reduziert Wrasen');

    root.querySelector('#finder-result-name').textContent = machine.name;
    root.querySelector('#finder-result-series').textContent = machine.series;
    root.querySelector('#finder-result-image').src = sitePath(machine.image);
    root.querySelector('#finder-result-image').alt = machine.name;
    root.querySelector('#finder-result-link').href = sitePath(machine.url);
    root.querySelector('#finder-result-reasons').innerHTML = reasons.map(item => `<li>${item}</li>`).join('');
    root.querySelector('#finder-water').textContent = waterRecommendation(machine, answers);
    root.querySelector('#finder-accessories').innerHTML = accessoriesFor(machine, answers).map(item => `<li>${item}</li>`).join('');
    root.querySelector('#finder-chemistry').textContent = chemistryFor(answers);
    root.querySelector('#finder-notice').textContent = notices(machine, answers);

    form.hidden = true;
    root.querySelector('.finder__progress').hidden = true;
    result.hidden = false;
    result.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  next.addEventListener('click', () => {
    const requiredName = ['washware', 'capacity', 'setup', 'power', 'hardness', 'finish'][step];
    if (!selected(requiredName)) {
      error.hidden = false;
      return;
    }
    if (step === steps.length - 1) renderResult();
    else showStep(step + 1);
  });

  back.addEventListener('click', () => showStep(Math.max(0, step - 1)));
  form.addEventListener('change', () => { error.hidden = true; });
  restart.addEventListener('click', () => {
    form.reset();
    result.hidden = true;
    form.hidden = false;
    root.querySelector('.finder__progress').hidden = false;
    showStep(0);
    root.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  showStep(0);
})();
