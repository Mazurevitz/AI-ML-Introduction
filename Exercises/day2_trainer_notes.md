
# 🤖 Notatki trenera — Dzień 2: LLM, Context Engineering i Agenci AI

**Slajdy:** `RevealJS/day2/part1.html`, `part2.html`, `part3.html`
**Notebooki:** `combined_exercise.ipynb` (Części 4-5), `simple_python_agent.ipynb`, `langgraph_ticket_router.ipynb`
**Czas:** 09:00–16:45 (z przerwami)
**Charakter:** 75% praktyka, 25% teoria

---

## ✅ Checklist przed warsztatem

- [ ] Google Colab z GPU T4 — wszystkie 3 notebooki otwarte, runtime ustawiony
- [ ] `large_tickets.csv` wgrany do Colab
- [ ] Ollama zainstalowana na laptopie trenera (`ollama list` działa)
- [ ] Modele Ollama pobrane: `gemma3:4b`, `phi4-mini`
- [ ] LM Studio zainstalowane (opcja: do porównania z Ollama)
- [ ] Transformer Explainer otwarty: https://poloclub.github.io/transformer-explainer/
- [ ] Chatbot Arena otwarty: https://lmarena.ai
- [ ] Tokenizer OpenAI otwarty: https://platform.openai.com/tokenizer
- [ ] Plik `/tmp/ITBot` (Modelfile) przygotowany do demo
- [ ] Obrazy do demo Vision (jeśli będzie czas): error screenshot, whiteboard, chart
- [ ] Zoom font/zoom duży na projektorze
- [ ] Ten dokument na drugim ekranie

---

## ⏱️ Plan czasowy

| Czas | Blok | Ćwiczenie | Slajdy |
|------|------|-----------|--------|
| 09:00–09:10 | Powitanie + Agenda | — | part1 |
| 09:10–09:30 | LLM: tokeny, attention | Quiz tokenizacji (Zoom reactions) | part1 |
| 09:30–09:40 | Transformer | Demo: Transformer Explainer | part1 |
| 09:40–10:25 | LLM + RAG | combined_exercise.ipynb (Części 4-5) | part1 |
| 10:25–10:30 | Q&A + przejście | — | part1 |
| 10:30–10:45 | ☕ Przerwa | — | — |
| 10:45–11:15 | Context Engineering | Teoria + przykłady kodu | part2 |
| 11:15–11:30 | Model types + quiz | Quiz typów modeli (Zoom) | part2 |
| 11:30–11:40 | Chatbot Arena | lmarena.ai — blind test | part2 |
| 11:40–11:55 | Ollama Modelfile | Ćwiczenie: budowa ITBot | part2 |
| 11:55–12:15 | Popularne modele + LLM limits | Slajdy + dyskusja | part2 |
| 12:15–12:45 | Architektura agentów | Whiteboard: zaprojektuj agenta | part2 |
| 12:45–13:45 | 🍽️ Obiad | — | — |
| 13:45–14:45 | Python Agent | simple_python_agent.ipynb | part3 |
| 14:45–15:00 | ☕ Przerwa | — | — |
| 15:00–16:10 | LangGraph | langgraph_ticket_router.ipynb | part3 |
| 16:10–16:30 | Ryzyka AI | Hallucination hunt + jailbreak | part3 |
| 16:30–16:45 | Podsumowanie | Refleksja + Q&A | part3 |

---

## 🔹 Blok 1: Jak działają LLM-y (09:00–10:30)

### Powitanie i Agenda (~10 min)

#### Intro — co powiedzieć
„Wczoraj poznaliśmy fundamenty: supervised learning, unsupervised, klasyfikację zgłoszeń IT. Dziś idziemy dalej — zobaczymy, jak duże modele językowe działają pod spodem, jak nimi sterować, i jak budować z nich inteligentne systemy. 75% dzisiejszego dnia to praktyka — będziemy pisać kod."

#### Storytelling
„Wyobraźcie sobie, że wczoraj nauczyliśmy się prowadzić samochód. Dziś zajrzymy pod maskę — zobaczymy silnik, skrzynię biegów, układ hamulcowy. A potem zbudujemy własny pojazd."

#### Aktywizacja
- „Co pamiętacie z wczoraj? Jedno zdanie na czacie."
- „Kto z Was już dziś rano użył jakiegoś narzędzia AI?"

---

### Tokenizacja (~15 min)

#### Intro — co powiedzieć
„Zanim model cokolwiek wygeneruje, musi 'zobaczyć' tekst. Ale tekst dla niego to nie litery — to liczby. Pierwszy krok to tokenizacja — rozbicie tekstu na kawałki, które model rozumie."

#### Storytelling
„Tokeny to jak klocki LEGO. Całe zdanie to gotowa budowla, ale model widzi tylko pojedyncze klocki — i z nich próbuje odbudować sens. Czasem jeden klocek to całe słowo. Czasem to kawałek słowa. A emoji? To osobny, kolorowy klocek."

„Albo inaczej: wyobraźcie sobie, że dostajecie SMS-a, ale każde słowo jest osobną wiadomością. I musicie sami złożyć sens. Tak 'czyta' tekst model."

#### Aktywizacja — Quiz tokenizacji
- Otwórz quiz w slajdach (part1)
- Uczestnicy reagują emoji na Zoomie: 😲 = 1 token, 👍 = 2-3, 🎉 = 4+
- Po każdym pytaniu: 10 sekund na reakcje, potem ujawnij odpowiedź
- **Kluczowe momenty zaskoczenia:**
  - „Dziękuję!" = 5 tokenów (polskie znaki!)
  - „今日は" = 1 token (zaskoczenie!)

#### Wskazówki do moderowania
- **Jeśli ktoś pyta „dlaczego polskie słowa mają więcej tokenów?"**: tokenizer trenowany głównie na angielskim, polskie znaki diakrytyczne rozbijają na mniejsze jednostki
- **Tip**: otwórz tokenizer.openai.com na żywo i pozwól uczestnikom zgadywać

#### Przejście
„OK, teraz wiemy, jak model rozbija tekst na kawałki. Ale jak z tych kawałków wyciąga sens? Tu pojawia się mechanizm Attention."

---

### Attention i Transformer (~15 min)

#### Intro — co powiedzieć
„Attention to serce nowoczesnych modeli. To mechanizm, który pozwala modelowi skupić się na najważniejszych fragmentach tekstu — tak jak Wy skupiacie się na jednej rozmowie w hałaśliwym pomieszczeniu."

#### Storytelling
„Wyobraźcie sobie przyjęcie firmowe. 50 osób, muzyka, rozmowy. Nagle ktoś wypowiada Wasze imię — i natychmiast się odwracacie. Wasz mózg cały czas 'słyszał' wszystko, ale dopiero teraz skupił uwagę na jednym sygnale. Tak działa Attention w modelu — każdy token analizuje wszystkie inne i przypisuje im wagę."

„Inny przykład: 'Janek dał prezent Tomkowi, bo miał urodziny.' Kto miał urodziny — Janek czy Tomek? My wiemy intuicyjnie. Model uczy się tego przez Attention."

#### Demo: Transformer Explainer
- Otwórz https://poloclub.github.io/transformer-explainer/ na projektorze
- Wpisz proste zdanie: „The cat sat on the"
- Pokaż, jak model przetwarza je warstwa po warstwie
- Kliknij na attention heads — pokaż, że różne głowy patrzą na różne relacje
- Zmień zdanie i pokaż, jak zmienia się attention
- **Czas:** ~5 minut

#### Aktywizacja
- „Czy ten schemat bardziej przypomina sieć neuronową, czy fabrykę tekstu?"
- „Jakie inne zastosowania Transformerów znacie poza językiem?" (wizja komputerowa, muzyka, biologia)

#### Przejście
„Teraz wiemy, jak model działa od środka. Czas go uruchomić! Zobaczymy, jak LLM radzi sobie z klasyfikacją naszych zgłoszeń IT."

---

### Ćwiczenie: LLM + RAG — combined_exercise.ipynb Części 4-5 (~25 min)

#### Intro — co powiedzieć
„Pamiętacie wczorajsze ćwiczenie? Klasyfikowaliśmy zgłoszenia ręcznie (Część 1), z ML (Część 2), z KMeans (Część 3). Teraz porównamy te same 10 zgłoszeń z LLM (zero-shot) i z RAG (LLM + baza wiedzy)."

#### Storytelling
„To jak różnica między pytaniem kogoś z ulicy ('Jak sklasyfikować to zgłoszenie?') a pytaniem eksperta, który ma przed sobą dokumentację firmy. Obie osoby mogą być inteligentne, ale ta z dokumentacją da lepszą odpowiedź."

#### Jak poprowadzić krok po kroku
1. Otwórz `combined_exercise.ipynb` w Colab
2. Przejdź do **Części 4: LLM Zero-Shot**
3. Uruchom komórki — model klasyfikuje 10 zgłoszeń bez żadnego kontekstu
4. **Zwróć uwagę na „Drukarka sieciowa nie odpowiada"** — model prawdopodobnie powie Sprzęt
5. Przejdź do **Części 5: RAG**
6. Pokaż bazę wiedzy (knowledge_base) — 5 krótkich procedur
7. Uruchom — teraz model MA kontekst i powinien zmienić na Sieć
8. Pokaż podsumowanie — wykres porównawczy 5 podejść

#### Aktywizacja
- „Które podejście wygrało? Dlaczego?"
- „W waszej firmie — kto miałby czas przygotować bazę wiedzy dla RAG?"
- „Czy 85% accuracy wystarczy do produkcji? Co byście dodali?"

#### Wskazówki do moderowania
- **Jeśli GPU nie działa**: notebook ma `fallback_llm_results` i `fallback_rag_results` — użyj ich
- **Jeśli model się ładuje wolno** (~3 min): opowiedz w tym czasie o RAG w praktyce
- **Typowy wynik**: ML ~80-85%, LLM ~70-80%, RAG ~85-90%

#### Przejście do przerwy
„Zobaczyliśmy 5 podejść do tego samego problemu. Po przerwie pójdziemy dalej — od prostych promptów do Context Engineering, czyli nowoczesnego podejścia do sterowania modelami AI."

---

## 🔹 Blok 2: Context Engineering (10:45–12:15)

### Od Prompt Engineering do Context Engineering (~15 min)

#### Intro — co powiedzieć
„W 2023 cały świat mówił o prompt engineering — jak napisać lepszy prompt. W 2024 przeszliśmy do systemów promptów z rolami i szablonami. Teraz, w 2026, to za mało. Modele są na tyle dobre, że kluczowe nie jest JAK pytasz, ale CO im dajesz."

#### Storytelling
„Wyobraźcie sobie nowego pracownika. Opcja A: dajecie mu lepszą instrukcję — 'bądź dokładny, odpowiadaj po polsku'. Opcja B: dajecie mu dostęp do CRM-a, bazy wiedzy, systemu ticketowego, i mówicie: 'użyj tego, co potrzebujesz'. Która opcja daje lepsze wyniki? Oczywiście B. To jest Context Engineering."

„Inny przykład: lekarz. Czy lepszy prompt to 'bądź dokładny'? Nie. Lepszy kontekst to: wyniki badań, historia choroby, aktualne leki. To robi różnicę."

#### Wyjaśnienie — 4 warstwy kontekstu
1. **System Prompt** — kim jest model, jakie ma zasady
2. **Tools (Narzędzia)** — co model MOŻE zrobić: API, bazy danych, funkcje
3. **RAG / Wiedza** — dokumenty, procedury, baza wiedzy dopasowana do pytania
4. **Pamięć** — historia rozmowy, preferencje użytkownika

#### Aktywizacja
- „Gdybyście budowali chatbota dla waszej firmy — które z tych 4 warstw byłyby najważniejsze?"
- „Kto z Was pisał kiedykolwiek system prompt? Co w nim było?"

---

### Tool Calling i Structured Outputs (~10 min)

#### Intro — co powiedzieć
„Dwa kluczowe pojęcia nowoczesnego AI: Tool Calling — model SAM decyduje, które narzędzie użyć. I Structured Output — model zwraca dane w formacie, który od razu możemy przetworzyć."

#### Storytelling — Tool Calling
„Pamiętacie regex? Kto kiedyś parsował odpowiedź LLM-a, żeby wyciągnąć jedną wartość? W 2023 to było codziennością — model zwracał tekst, a Ty musiałeś go 'obierać' jak cebulę. W 2026 model zwraca czysty JSON — bo mu to zdefiniujemy jako narzędzie."

#### Storytelling — Structured Output
„To jak formularz urzędowy vs list. List możesz napisać jak chcesz — pięknie, ale trudno go automatycznie przetworzyć. Formularz ma pola: imię, data, kwota. Model, któremu damy structured output format, zachowuje się jak pracownik wypełniający formularz — dokładnie, w odpowiednich polach."

#### Wskazówki do moderowania
- Pokaż kod z slajdu (tool definition JSON)
- Porównaj stare vs nowe podejście (tekst vs JSON)
- Nie wchodź zbyt głęboko w implementację — zobaczymy to w praktyce w notebooku agenta

---

### Quiz typów modeli (~10 min)

#### Jak poprowadzić
- 4 pytania, reakcje Zoom: 👍 Foundation, 🎉 Fine-tuned, 😲 RAG
- Szybkie tempo — 15 sekund na reakcje, ujawnienie, krótki komentarz

#### Kluczowe analogie
- Foundation = encyklopedyczny student — wie dużo, ale ogólnie
- Fine-tuned = specjalista z wieloletnim doświadczeniem — wie konkretnie o swojej branży
- RAG = konsultant z dostępem do dokumentacji — sprawdza zanim odpowie

---

### Ćwiczenie: Chatbot Arena (~10 min)

#### Intro — co powiedzieć
„Zamiast mi wierzyć na słowo, że różne modele dają różne wyniki — sprawdźcie sami. W blind teście."

#### Jak poprowadzić
1. Otwórz https://lmarena.ai na projektorze
2. Pokaż jak działa: wpisujesz prompt → dostajesz 2 odpowiedzi (Model A vs B) → głosujesz → widzisz nazwy
3. Uczestnicy robią to samo na swoich komputerach
4. Sugerowany prompt: „Classify this IT ticket: Network printer is not responding. Respond with category and reasoning."
5. Po 5 minutach: „Które modele wygrywały? Zaskoczeni?"

#### Puenta
„Nie zawsze najdroższy model = najlepszy do waszego zadania. Testujcie!"

---

### Ćwiczenie: Ollama Modelfile (~15 min)

#### Intro — co powiedzieć
„Teraz zbudujemy własnego specjalistę IT. Z nazwą, osobowością, parametrami. W 30 sekund."

#### Jak poprowadzić krok po kroku
1. Pokaż slajd z Modelfile
2. Uruchom na projektorze:
   ```bash
   cat << 'EOF' > /tmp/ITBot
   FROM gemma3:4b
   PARAMETER temperature 0
   PARAMETER num_ctx 4096
   SYSTEM """You are ITBot, an internal IT helpdesk assistant.
   Rules:
   - Always respond in Polish
   - Classify tickets into: Sprzet, Siec, Oprogramowanie, Konto
   - Always explain reasoning in one sentence
   - Always suggest one next step
   - Be concise and professional"""
   EOF
   ollama create itbot -f /tmp/ITBot
   ```
3. Uruchom: `ollama run itbot`
4. Przetestuj na 3 zgłoszeniach:
   - „Drukarka sieciowa nie odpowiada po awarii prądu"
   - „Kolega nie może się zalogować po urlopie"
   - „Excel zawiesza się przy dużych plikach"

#### Storytelling
„Stworzyliście własnego specjalistę IT w 30 sekund. Ma ustawioną temperaturę na 0 (deterministyczny), zawsze odpowiada po polsku, zawsze klasyfikuje i sugeruje kolejny krok. W firmie można takich 'botów' mieć kilka — do HR, do IT, do finansów."

#### Aktywizacja
- „Co byście zmienili w system prompcie?"
- „Jakie inne narzędzia/boty byłyby przydatne w waszej firmie?"

#### Fallback
Jeśli uczestnicy nie mają Ollama — mogą zrobić Custom Instructions w ChatGPT z tym samym system promptem.

---

### Popularne modele + Co LLM umie/nie umie (~10 min)

#### Intro
Szybki przegląd rynku modeli 2026. Pokaż tabelę ze slajdu.

#### Storytelling
„Rynek modeli to jak rynek samochodów. GPT-4o i Claude to limuzyny — drogie, potężne, w chmurze. Gemma 3 i Phi-4 to miejskie auta — lekkie, szybkie, na Twoim laptopie. Wczoraj widzieliśmy je w Ollama."

#### Kluczowe punkty
- **Context window** rośnie: od 4K (GPT-3) do 2M (Gemini) — to zmienia grę
- **Modele lokalne** (Gemma, Phi, Llama) są coraz lepsze — wystarczą do większości zadań
- **Halucynacje** nadal istnieją — nawet w najlepszych modelach
- **RAG + Tools** rozwiązują większość ograniczeń

---

### Architektura agentów + Whiteboard exercise (~30 min)

#### Intro — co powiedzieć
„Do tej pory budowaliśmy chatboty — odpowiadały na pytania. Teraz budujemy agentów — wykonują zadania. LLM to silnik. Agent to cały samochód: silnik + kierownica + nawigacja + bagażnik na narzędzia."

#### Storytelling
„Chatbot to informacja. Agent to akcja. Chatbot mówi: 'Twoje zgłoszenie dotyczy sieci.' Agent mówi: 'Sprawdzam ping do drukarki... brak odpowiedzi... tworzę ticket w Jira... powiadamiam zespół sieciowy.' To fundamentalna zmiana."

#### Wyjaśnienie — 5 komponentów
1. **LLM** — rozumienie i decyzje
2. **Tools** — API, bazy danych, systemy
3. **Memory** — kontekst rozmowy, preferencje
4. **Planning** — rozbicie zadania na kroki
5. **Monitoring** — kontrola poprawności

#### Ćwiczenie: Whiteboard Design (~15 min)
- Grupy 2-3 osoby (breakout rooms w Zoom lub chat)
- Zadanie: „Zaprojektuj agenta dla swojej firmy"
- Schemat: Input → Analiza → Decyzja → Akcja
- Określ: jakie tools? Jaka memory? Jakie reguły?
- Prezentacja: 1 minuta na grupę

#### Wskazówki
- Jeśli zdalnie: poproś o wpisanie schematu na czacie tekstowo
- Jeśli ktoś nie wie, co wymyślić: podaj przykład agenta HR
- **Puenta**: „Po obiedzie zbudujemy prawdziwego agenta w Pythonie — to, co teraz zaprojektowaliście na papierze."

---

## 🔹 Blok 3: Python Agent Workshop (13:45–14:45)

### Intro — co powiedzieć
„Przed przerwą projektowaliśmy agentów na papierze. Teraz czas na kod. 5 kroków — od prostego wywołania LLM do pełnego agenta z narzędziami, pamięcią i structured output. Wszystko w Pythonie, wszystko lokalnie na Ollama."

### Storytelling
„To jak budowanie robota z LEGO Technic. Krok 1: sam silnik — obraca się, ale nic nie robi. Krok 2: dodajemy koła. Krok 3: kierownicę. Krok 4: GPS. Krok 5: ładunek. Na końcu mamy działającego robota."

### Jak poprowadzić — krok po kroku

#### Krok 1: Podstawowe wywołanie LLM (~8 min)
- Pokaż funkcję `call_llm()` — 5 linijek, HTTP request do Ollama
- Moment „wow": „To wszystko? Tak, 5 linijek = wywołanie modelu AI."
- Daj 2-3 min na zmianę promptu

#### Krok 2: Rejestr narzędzi (~10 min)
- 3 narzędzia: `classify_ticket`, `search_knowledge_base`, `get_ticket_status`
- Pokaż, jak agent decyduje, które narzędzie użyć
- **Kluczowy punkt**: model nie „wie" — decyduje na podstawie promptu i listy dostępnych narzędzi

#### Krok 3: Pamięć (~10 min)
- Klasa `ITAgent` z historią ostatnich 5 wymian
- Pokaż, jak agent pamięta kontekst: „A tamto zgłoszenie?" → wie, o czym mowa
- **Storytelling**: „Bez pamięci agent ma Alzheimera — każda rozmowa to od nowa."

#### Krok 4: Structured Output (~10 min)
- JSON z `{category, confidence, reasoning, next_step}`
- Porównaj z Krokiem 1: tekst vs JSON
- **Storytelling**: „To jak różnica między ustną odpowiedzią a wypełnionym formularzem."

#### Krok 5: Dostęp do danych (~10 min)
- Narzędzie `query_tickets` pracujące na `large_tickets.csv`
- Agent odpowiada na pytania o rzeczywiste dane
- „Ile zgłoszeń sieciowych było w tym miesiącu?" → agent szuka w CSV

### Fallback
- Notebook ma pre-computed results dla każdego kroku
- Jeśli Ollama nie działa na Colab: uruchom na laptopie trenera i pokaż ekran

### Aktywizacja po zakończeniu
- „Co byście dodali do tego agenta?"
- „Jakie narzędzia dalibyście agentowi w waszej firmie?"
- „Gdzie jest granica — co agent powinien robić sam, a co z człowiekiem?"

---

## 🔹 Blok 4: LangGraph — Orkiestracja agentów (15:00–16:10)

### Intro — co powiedzieć
„Nasz agent Pythonowy to jedna ścieżka — klasyfikuj → odpowiedz. Ale co jeśli chcemy różne ścieżki? Pewne zgłoszenie → szybka klasyfikacja. Niepewne → szukaj w bazie wiedzy. Krytyczne → eskalacja do człowieka. To jest orkiestracja."

### Storytelling
„Wyobraźcie sobie szpitalny oddział ratunkowy. Nie każdy pacjent idzie tą samą ścieżką. Złamana ręka → rentgen → gips. Ból w klatce → EKG → kardiolog. Lekki ból głowy → paracetamol → do domu. Każdy pacjent ma inną ścieżkę — ale wszystkie są w jednym szpitalu, z jednym systemem triażu. To jest LangGraph."

„Nasz Python agent to lekarz, który robi wszystko sam. LangGraph to cały szpital z triażem, specjalistami i ścieżkami decyzyjnymi."

### Wyjaśnienie — kluczowe pojęcia
- **Graf** = zbiór węzłów (kroków) i krawędzi (połączeń)
- **Węzły (Nodes)** = funkcje przetwarzające: classify, search_kb, reclassify, route
- **Krawędzie** = przepływ: który węzeł po którym
- **Krawędzie warunkowe** = „jeśli confidence >= 0.8 → szybka ścieżka, inaczej → RAG"
- **Stan (State)** = dane, które przepływają przez graf (TypedDict)

### Jak poprowadzić notebook

#### Część 1: Teoria grafu (~10 min)
- Narysuj graf na whiteboard: 4 kółka (classify → search_kb → reclassify → route)
- Strzałka warunkowa z classify: „pewność >= 80%?"
- YES → route (szybka ścieżka)
- NO → search_kb → reclassify → route (RAG ścieżka)

#### Część 2: Budowa grafu w kodzie (~15 min)
- TypedDict `TicketState` — pokaż, że to „formularz" przepływający przez system
- Każdy węzeł to funkcja Pythonowa
- `StateGraph` — budujemy graf, dodajemy węzły, krawędzie
- `add_conditional_edges` — kluczowy moment

#### Część 3: Uruchomienie na 10 zgłoszeniach (~15 min)
- Te same 10 zgłoszeń co w combined_exercise
- Pokaż, że różne zgłoszenia idą różnymi ścieżkami
- **Moment wow**: „Drukarka sieciowa" idzie RAG ścieżką i zmienia z Sprzęt na Sieć

#### Część 4: Wizualizacja (~10 min)
- 3-panelowy wykres: ścieżki, pewność per ticket, accuracy per ścieżka
- Dyskusja: kiedy fast path, kiedy RAG, kiedy human review?

### Aktywizacja
- „Gdybyście dodali 5. węzeł — co by robił?"
- „Gdzie w waszej firmie widzicie takie warunkowe ścieżki?"
- „Jaki procent zgłoszeń powinien iść do człowieka?"

### Fallback
- Notebook ma `fallback_classifications` i `fallback_rag_results` — pre-computed results
- Jeśli LangGraph nie installuje się: pokaż graf na whiteboard i omów logicznie

---

## 🔹 Blok 5: Ryzyka AI (16:10–16:30)

### Intro — co powiedzieć
„Zbudowaliśmy agentów, orkiestrację, systemy AI. Ale zanim puścimy to do produkcji — musimy porozmawiać o ryzykach. Bo AI, które robi błędy autonomicznie, robi je szybko i na dużą skalę."

### Storytelling
„W jednej firmie prawniczej AI miał pomagać w research — szukać precedensów sądowych. Prawnik użył wyników w sądzie. Problem? AI wymyślił 3 z 5 cytowanych przypadków. Sędzia sprawdził i... prawnik musiał się tłumaczyć. To nie anegdota — to realny przypadek z 2023."

### Ćwiczenie: Hallucination Hunt (~7 min)

#### Jak poprowadzić
1. Uczestnicy otwierają ChatGPT / Claude / Ollama
2. Zadają jedno z pytań ze slajdu:
   - „Podaj 3 badania naukowe o wpływie kawy na produktywność programistów"
   - „Jakie książki napisał Jan Kowalski-Nowak?" (wymyślone)
   - „Opisz wypadek na autostradzie A4 z 15 marca 2024"
3. Weryfikują odpowiedzi w Google
4. Dzielą się na czacie: „Ile z moich wyników to prawda?"

#### Puenta
„Im pewniej brzmi odpowiedź AI, tym bardziej powinniśmy ją weryfikować. Dlatego RAG i weryfikacja to nie 'nice to have' — to konieczność."

### Mini-challenge: Jailbreak (~3 min)
- Nie ćwiczenie w pełnym sensie — bardziej dyskusja
- „Czy model lokalny (Ollama) ma takie same zabezpieczenia jak ChatGPT?"
- Szybki test: to samo pytanie w Ollama vs ChatGPT
- Puenta: „Dlatego w produkcji potrzebujemy guardrails, monitoring, human-in-the-loop."

### Zasady bezpieczeństwa (~5 min)
- Nie wrzucaj wrażliwych danych do publicznych modeli
- Modele lokalne = dane zostają u Ciebie
- Human-in-the-loop: agent proponuje, człowiek zatwierdza
- Loguj decyzje agenta — audytowalność

---

## 🔹 Podsumowanie (16:30–16:45)

### Co dziś zrobiliśmy — szybkie podsumowanie
1. Zrozumieliśmy tokenizację i attention — jak LLM „myśli"
2. Context Engineering — tools, structured output, RAG
3. Ollama Modelfile — własny specjalista IT
4. Python Agent — od zera do pełnego systemu
5. LangGraph — inteligentny router zgłoszeń
6. Ryzyka — halucynacje, jailbreak, prywatność

### Mity o AI
Pokaż tabelę ze slajdu. Kluczowy nowy mit:
- ❌ „Wystarczy napisać dobry prompt"
- ✅ „Context Engineering: tools + memory + RAG + structured output"

### Refleksja
- „Co zapamiętasz najbardziej?"
- „Co chciałbyś spróbować w swojej pracy?"
- Poproś o reakcje emoji: 👍 przydatne, 🔁 zastosuję, ❓ chcę pogłębić

### Dalsze zasoby
- Nie przytłaczaj listą — poleć 2-3 rzeczy:
  1. „Weźcie notebooki z dzisiejszego dnia i zmodyfikujcie je pod swój problem"
  2. „Jeśli lubicie video: Andrej Karpathy 'Let's build GPT' na YouTube"
  3. „Do codziennej pracy: zainstalujcie Ollama i bawcie się Modelfile'ami"

### Zakończenie
- Podziękuj za aktywność
- Pochwal konkretne osoby/momenty
- „Materiały zostają z Wami — notebooki, slajdy, linki. Bawcie się nimi!"
- „Jeśli macie pytania po szkoleniu — piszcie, chętnie pomogę."

---

## 🚨 Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| Colab nie łączy z GPU | Runtime → Change runtime → T4 GPU. Restart jeśli potrzeba |
| Ollama na Colab nie działa | Użyj fallback results. Lub pokaż na laptopie trenera |
| LangGraph install fails | `!pip install langgraph` ponownie. Restart kernel |
| Model się ładuje zbyt wolno | Opowiadaj storytelling w trakcie. Phi-4 ładuje się ~3 min |
| Uczestnicy nie mają Ollama | Pokaż na projektorze. Alternatywa: ChatGPT z Custom Instructions |
| Chatbot Arena nie działa | Alternatywa: pokaż Poe.com lub Hugging Face Chat |
| Notebook ma błędy JSON | Sprawdź polskie znaki — zamień „ na " |
| Mało czasu | Pomiń Chatbot Arena i skróć whiteboard exercise |
| Za dużo czasu | Dodaj Ollama Vision demo lub LM Studio comparison |

---

## 📋 Przydatne linki (otwórz przed sesją)

| Link | Do czego |
|------|----------|
| https://poloclub.github.io/transformer-explainer/ | Demo Transformer |
| https://lmarena.ai | Chatbot Arena — blind test |
| https://platform.openai.com/tokenizer | Tokenizer OpenAI |
| https://bbycroft.net/llm | 3D wizualizacja LLM |
| https://colab.research.google.com | Google Colab |
| http://localhost:11434 | Ollama API (lokalne) |
