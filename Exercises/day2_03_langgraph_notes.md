
# 🔀 Notatki trenera — Agent Orchestration z LangGraph

**Notebook:** `day2_03_langgraph_orchestration.ipynb`
**Czas:** ~50 minut
**Wymagania:** Google Colab (GPU nie wymagane!), klucz API OpenRouter (https://openrouter.ai/keys)

---

## ✅ Checklist przed warsztatem

- [ ] Notebook otwarty w Colab (lub VS Code)
- [ ] **Klucz API OpenRouter** skonfigurowany (ten sam co w day2_02)
- [ ] Test połączenia zwraca „API: działa!" (komórka setup)
- [ ] `!pip install langgraph` wykonane — brak błędów instalacji
- [ ] Jeśli brak klucza API: fallback classifications i fallback RAG działają poprawnie
- [ ] Rozumiesz notebooka day2_02 (Python Agent) — LangGraph buduje na tych samych koncepcjach
- [ ] Ten dokument na drugim ekranie

---

## ⏱️ Plan czasowy

| Czas | Krok | Co się dzieje |
|------|------|---------------|
| 0:00 | Setup | Instalacja LangGraph, klucz API |
| 0:03 | Krok 1 | State (TypedDict) — „notatnik" agenta |
| 0:08 | Krok 2 | Węzły (Nodes) — 4 funkcje + baza wiedzy |
| 0:23 | Krok 3 | Krawędź warunkowa — próg pewności |
| 0:28 | Krok 4 | Budowa grafu — `StateGraph`, `compile()` |
| 0:33 | Krok 5 | Uruchomienie na 10 zgłoszeniach |
| 0:43 | Krok 6 | Wizualizacja wyników — 3 wykresy |
| 0:50 | Koniec | Podsumowanie wzorców orkiestracji |

---

## 🔹 Krok 0: Setup (~3 min)

### Intro — co powiedzieć
„Nasz agent Pythonowy to jedna ścieżka — klasyfikuj → odpowiedz. Ale co jeśli chcemy różne ścieżki? Pewne zgłoszenie → szybka klasyfikacja. Niepewne → szukaj w bazie wiedzy. To jest orkiestracja — i do tego służy LangGraph."

### Wyjaśnienie — punkty techniczne
- **LangGraph** = framework do budowania agentów jako grafów (węzły + krawędzie)
- Instalacja: `!pip install langgraph` — wymaga Pythona 3.9+
- **Ten sam klucz API OpenRouter** co w poprzednim notebooku — nie trzeba konfigurować od nowa
- `call_llm(prompt, system="")` — uproszczona wersja (tekst in, tekst out) zamiast pełnego chat completions

### Wskazówki do moderowania
- **Jeśli LangGraph nie installuje się**: restart kernel i `!pip install langgraph` ponownie
- **Jeśli conflict z innymi pakietami**: `!pip install --force-reinstall langgraph`
- **Fallback**: notebook ma pre-computed wyniki — działa bez API

### Storytelling
„Wyobraźcie sobie szpitalny oddział ratunkowy. Nie każdy pacjent idzie tą samą ścieżką. Złamana ręka → rentgen → gips. Ból w klatce → EKG → kardiolog. Każdy pacjent ma inną ścieżkę — ale wszystkie są w jednym szpitalu, z jednym systemem triażu. To jest LangGraph."

### Przejście
„LangGraph zainstalowany, API działa. Zacznijmy od fundamentu — co agent pamięta między krokami."

---

## 🔹 Krok 1: Definiujemy State (~5 min)

### Intro — co powiedzieć
„State to 'notatnik' agenta. Każdy węzeł czyta ze State i zapisuje do niego. State przepływa przez cały graf — dlatego definiujemy go jasno z typami."

### Wyjaśnienie — punkty techniczne
- **TypedDict `TicketState`** — 7 pól:
  - `text` — oryginalny tekst zgłoszenia
  - `category` — przewidywana kategoria
  - `confidence` — pewność klasyfikacji (0-1)
  - `context` — kontekst z bazy wiedzy (dla RAG)
  - `route` — docelowy zespół
  - `needs_review` — flaga dla ludzkiego przeglądu
  - `path` — lista odwiedzonych węzłów (do wizualizacji)

### Storytelling
„State to jak formularz, który przepływa przez biuro. Na początku jest prawie pusty — tylko tekst zgłoszenia. Każdy dział (węzeł) dopisuje swoją sekcję: klasyfikację, kontekst, routing. Na końcu formularz jest kompletny."

### Aktywizacja
- „Jakie inne pola dodalibyście? (np. `processing_time_ms`, `created_by`, `escalated`)"
- „Dlaczego `path` jest przydatny? (Debugging, audyt, wizualizacja)"

### Przejście
„Mamy 'formularz'. Teraz potrzebujemy ludzi — węzły, które go wypełniają."

---

## 🔹 Krok 2: Węzły (Nodes) (~15 min)

### Intro — co powiedzieć
„Każdy węzeł to funkcja Pythona. Przyjmuje State, coś robi — np. wywołuje LLM — i zwraca zaktualizowany fragment State. LangGraph sam łączy wyniki."

### Wyjaśnienie — 4 węzły

| # | Węzeł | Co robi | Typ |
|---|-------|---------|-----|
| 1 | `classify_node` | Klasyfikuje zgłoszenie przez LLM | LLM call |
| 2 | `search_kb_node` | Szuka w bazie wiedzy (keyword matching) | Retrieval |
| 3 | `reclassify_node` | Reklasyfikuje z kontekstem (RAG) | LLM call + kontekst |
| 4 | `route_node` | Routuje do zespołu | Logika |

#### Baza wiedzy (KNOWLEDGE_BASE)
- 5 artykułów z keywords — uproszczony retrieval
- Pokrywa niejednoznaczne przypadki: drukarka sieciowa, WiFi login, hasło w ERP
- `TEAM_ROUTING` — mapowanie kategorii na zespoły (email + lokalizacja)

#### classify_node — kluczowy
- Prompt: „Classify this IT ticket. Return ONLY JSON: {category, confidence}"
- Parsuje JSON z odpowiedzi LLM (znajduje `{...}` w tekście)
- **Fallback**: `FALLBACK_CLASSIFICATIONS` — pre-computed wyniki z celowo niskimi confidence na niejednoznacznych

#### search_kb_node — prosty
- Keyword matching po `KNOWLEDGE_BASE`
- Zwraca połączone artykuły jako `context`

#### reclassify_node — RAG
- Ten sam prompt co classify, ale z dodanym `Context: ...`
- **Fallback**: `FALLBACK_RAG` — poprawione wyniki po dodaniu kontekstu

#### route_node — logika
- Mapuje kategorię na zespół przez `TEAM_ROUTING`
- Ustawia `needs_review = True` jeśli confidence < 0.7

### Storytelling
„To jest jak linia produkcyjna. Pierwsza osoba (classify) patrzy na zgłoszenie i próbuje sklasyfikować. Jeśli jest pewna — przekazuje dalej. Jeśli nie — przekazuje do eksperta (search_kb + reclassify), który ma pod ręką dokumentację. Na końcu router wysyła do odpowiedniego zespołu."

### Aktywizacja — pytania do grupy
- „Popatrzcie na FALLBACK_CLASSIFICATIONS — które zgłoszenia mają niskie confidence. Dlaczego?"
- „Dlaczego 'Drukarka sieciowa nie odpowiada' dostaje 0.55? (Dwuznaczna: Sprzęt czy Sieć?)"
- „Co reclassify_node zmienia w porównaniu z classify_node? (Dodaje kontekst!)"

### Wskazówki do moderowania
- **Prowadź szybko przez kod narzędzi** — uczestnicy widzieli już te dane w day2_01 i day2_02
- **Podkreśl różnicę**: classify (bez kontekstu) vs reclassify (z kontekstem) = to jest RAG w akcji
- **Jeśli ktoś pyta o lepszy retrieval**: „Świetne pytanie! W produkcji użylibyśmy embeddings + vector DB. Tu upraszczamy."

### Przejście
„Mamy 4 węzły. Ale kiedy idziemy ścieżką szybką, a kiedy RAG? Tu wchodzą krawędzie warunkowe."

---

## 🔹 Krok 3: Krawędzie warunkowe (~5 min)

### Intro — co powiedzieć
„Krawędź warunkowa to punkt decyzyjny. Na podstawie State agent wybiera ścieżkę. Tu: jeśli pewność >= 80% → routuj od razu. Jeśli nie → szukaj w bazie wiedzy."

### Wyjaśnienie — punkty techniczne
- **`CONFIDENCE_THRESHOLD = 0.8`** — próg decyzyjny
- **`check_confidence(state)`** → zwraca `"route"` lub `"search_kb"`
- `Literal["route", "search_kb"]` — LangGraph wie, jakie są opcje

### Storytelling
„To jest triage. Pacjent z oczywistym złamaniem (confidence 95%) idzie prosto na rentgen. Pacjent z nieokreślonym bólem brzucha (confidence 50%) idzie najpierw na dodatkowe badania."

### Aktywizacja
- „Co się stanie, jeśli zmienimy próg na 0.6? (Więcej na szybkiej ścieżce, mniej RAG)"
- „A na 0.95? (Prawie wszystko idzie przez RAG)"
- „Jaki próg ustawilibyście w produkcji?"

### Przejście
„Mamy węzły, mamy decyzję. Czas złożyć graf."

---

## 🔹 Krok 4: Budowa grafu (~5 min)

### Intro — co powiedzieć
„Teraz łączymy wszystko: definiujemy graf, dodajemy węzły, krawędzie i kompilujemy. LangGraph tworzy z tego wykonywalny pipeline."

### Wyjaśnienie — punkty techniczne
- **`StateGraph(TicketState)`** — tworzymy graf z typowanym State
- **`add_node("name", function)`** — dodajemy 4 węzły
- **`add_edge(START, "classify")`** — start → classify
- **`add_conditional_edges("classify", check_confidence, {...})`** — krawędź warunkowa
- **`compile()`** — tworzy wykonywalny obiekt `app`

### Diagram na whiteboard
```
START → [classify] → {confidence >= 0.8?}
                       ├── YES → [route] → END
                       └── NO  → [search_kb] → [reclassify] → [route] → END
```

### Wskazówki do moderowania
- **Narysuj graf na whiteboard/share screen** — wizualizacja pomaga zrozumieć
- **Podkreśl**: `compile()` tworzy obiekt, który możesz wywołać jak funkcję: `app.invoke(state)`
- **Jeśli ktoś pyta o inne frameworki**: „LangGraph to jeden z wielu — jest też CrewAI, AutoGen, Haystack. Zasady grafowe są uniwersalne."

### Przejście
„Graf skompilowany. Czas go uruchomić na tych samych 10 zgłoszeniach, które widzieliśmy w każdym ćwiczeniu."

---

## 🔹 Krok 5: Uruchomienie na 10 zgłoszeniach (~10 min)

### Intro — co powiedzieć
„Te same 10 zgłoszeń co we wszystkich poprzednich ćwiczeniach. Teraz widzimy, którą ścieżką przeszło każde — szybką (2 węzły) czy RAG (4 węzły)."

### Wyjaśnienie — co obserwować
- **Każde zgłoszenie** wypisuje: kategorię, pewność, ścieżkę (Fast/RAG), routing, needs_review
- **Ikony**: ✅ poprawna klasyfikacja, ❌ błędna
- **Ścieżka Fast (⚡)**: classify → route — 2 węzły
- **Ścieżka RAG (📚)**: classify → search_kb → reclassify → route — 4 węzły
- `correct_labels` — ground truth do porównania

### Aktywizacja — kluczowe obserwacje
- „Które zgłoszenia poszły ścieżką RAG? Dlaczego akurat te?" (niskie confidence = niejednoznaczne)
- **Moment wow**: „Drukarka sieciowa nie odpowiada" — classify mówi Hardware (0.55), RAG poprawia na Network (0.92)
- „Porównajcie z day2_01 — LLM zero-shot vs LangGraph. Co się poprawiło?"
- „Które zgłoszenia nadal mają needs_review? (confidence < 0.7)"

### Wskazówki do moderowania
- **Jeśli accuracy jest niskie z API**: model może odpowiadać niestabilnie — to normalny problem z małymi modelami
- **Fallback daje czyste wyniki**: celowo zaprojektowane do demonstracji obu ścieżek
- **Dodaj własne zgłoszenie**: zachęć uczestników do dodania 11. zgłoszenia i sprawdzenia ścieżki

### Przejście
„Zobaczmy to na wykresach — ile poszło ścieżką szybką, ile przez RAG, i jaka jest dokładność."

---

## 🔹 Krok 6: Wizualizacja wyników (~7 min)

### Intro — co powiedzieć
„3 wykresy podsumowujące: rozkład ścieżek, pewność per zgłoszenie, dokładność per ścieżka."

### Wyjaśnienie — 3 panele
1. **Rozkład ścieżek**: ile Fast vs RAG — typowo ~6:4 lub 7:3
2. **Pewność per zgłoszenie**: barplot z progiem 0.8 (pomarańczowa linia). Zielony = poprawne, czerwony = błąd
3. **Dokładność per ścieżka**: Fast accuracy vs RAG accuracy vs Total

### Aktywizacja — pytania końcowe
- „Która ścieżka ma lepszą dokładność? Dlaczego?" (RAG, bo dodaje kontekst do trudnych przypadków)
- „Co by się stało z progiem 0.6?" (Mniej RAG, ale potencjalnie gorsze wyniki na trudnych)
- „Gdybyście dodali 5. węzeł — co by robił?" (human_review, escalation, logging)

### Wzorce orkiestracji (slajd podsumowujący w notebooku)
| Wzorzec | Opis | Przykład |
|---------|------|----------|
| **Router** | Klasyfikuj → Routuj (nasz graf!) | Helpdesk, triage |
| **Plan-and-Execute** | Model planuje, tani model wykonuje | Redukcja kosztów |
| **Reflect** | Agent sprawdza swój wynik | QA, recenzje |
| **Human-in-the-Loop** | Agent pyta człowieka | Finanse, medycyna |

### Puenta
„Agenci, którzy działają w produkcji, to te nudne: wąskie, wyspecjalizowane, głęboko zintegrowane. Nie AGI — ale agenty, które robią jedną rzecz dobrze."

---

## 🚨 Strategie awaryjne (Fallback)

### Brak klucza API OpenRouter
- Notebook ma **pre-computed fallback** — `FALLBACK_CLASSIFICATIONS` i `FALLBACK_RAG`
- Celowo zaprojektowane: 6 zgłoszeń z wysokim confidence (Fast path), 4 z niskim (RAG path)
- RAG fallback poprawia wszystkie 4 trudne przypadki → demonstracja wartości RAG
- Powiedz: „Wyniki są pre-computed z prawdziwego modelu"

### LangGraph nie installuje się
- `!pip install langgraph --quiet` → restart kernel → ponowna instalacja
- Jeśli nadal nie działa: **narysuj graf na whiteboard** i omów logicznie
- Alternatywa: pokaż plain Python z if/else — ta sama logika bez frameworka

### API zwraca niestabilne wyniki
- Małe modele (8B) mogą zwracać niespójne JSON → `try/except` w classify_node obsługuje to
- Jeśli większość wyników to „Unknown": zmień model na `llama-3.3-70b-instruct`
- Opcja: przełącz na fallback: `USE_API = False`

### Wykresy nie renderują się
- `matplotlib` powinien być preinstalowany w Colab
- Jeśli nie: `!pip install matplotlib`
- Jeśli inline nie działa: `%matplotlib inline` na początku notebooka

---

## 📝 Notatki po warsztacie

*(Uzupełnij po przeprowadzeniu:)*

- Accuracy z API vs fallback: ___
- Ile zgłoszeń poszło ścieżką RAG: ___
- Czy reclassify poprawił trudne przypadki: ___
- Najciekawsze pytanie uczestnika: ___
- Czy ktoś dodał własne zgłoszenie/węzeł: ___
- Co zmienić na następny raz: ___
