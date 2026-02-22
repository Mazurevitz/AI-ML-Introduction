
# 🔌 Notatki trenera — Budujemy wlasny MCP Server z FastMCP

**Notebook:** `day2_04_mcp_server.ipynb`
**Plik serwera:** `it_helpdesk_mcp.py` (do zabrania do domu)
**Czas:** ~35 minut
**Wymagania:** Google Colab lub Python 3.9+ (GPU nie wymagane, API nie wymagane!)

---

## ✅ Checklist przed warsztatem

- [ ] Notebook otwarty w Colab (lub VS Code)
- [ ] `!pip install fastmcp` wykonane — brak błędów
- [ ] Plik `it_helpdesk_mcp.py` dostępny w materiałach (do rozdania uczestnikom)
- [ ] Rozumiesz day2_02 (Python Agent) — MCP Server używa tych samych narzędzi
- [ ] Opcjonalnie: Claude Desktop zainstalowane na laptopie trenera (do szybkiego demo na końcu)
- [ ] Ten dokument na drugim ekranie

---

## ⏱️ Plan czasowy

| Czas | Krok | Co się dzieje |
|------|------|---------------|
| 0:00 | Instalacja | `pip install fastmcp`, import |
| 0:02 | Krok 1 | Pierwszy serwer MCP — `FastMCP()` + `@mcp.tool` + `ping()` |
| 0:07 | Krok 2 | 4 narzędzia IT helpdesk — baza wiedzy, zgłoszenia, systemy |
| 0:17 | Krok 3 | Test przez protokół MCP — `Client(mcp)`, `list_tools()`, `call_tool()` |
| 0:27 | Krok 4 | Export — `it_helpdesk_mcp.py` + konfiguracja Claude Desktop |
| 0:32 | Podsumowanie | 5 kluczowych lekcji + ćwiczenie końcowe |
| 0:35 | Koniec | |

---

## 🔹 Kontekst — dlaczego MCP po Python Agent?

### Intro — co powiedzieć
„Wczoraj poznaliście MCP od strony konsumenta — Claude Desktop używa narzędzi. Przed chwilą zbudowaliście agenta w Pythonie z narzędziami. Teraz przejdziemy na drugą stronę: zbudujecie własny serwer MCP. Wasze narzędzia, wasze dane, wasze zasady — ale w standardzie, który rozumie każdy klient AI."

### Storytelling
„To jak różnica między używaniem API a budowaniem API. Przed chwilą byliście klientem restauracji — zamówiliście danie. Teraz wchodzicie do kuchni. Tworzycie menu, przygotowujecie składniki, definiujecie jak je podać."

### Kluczowa różnica vs Python Agent
- **day2_02**: narzędzia jako funkcje Pythona + JSON Schema → native tool calling przez API
- **day2_04**: narzędzia jako MCP tools → **każdy** klient MCP (Claude Desktop, Cursor, dowolny agent) może ich użyć
- Analogia: HTTP API → każda przeglądarka rozumie. MCP tool → każdy klient AI rozumie.

---

## 🔹 Krok 0: Instalacja (~2 min)

### Wyjaśnienie — punkty techniczne
- **FastMCP** = biblioteka Pythona do budowy serwerów MCP
- Analogia: **FastMCP jest dla MCP tym, czym Flask jest dla HTTP**
- Instalacja: `!pip install fastmcp` — ciągnie zależności (pydantic, etc.)
- Import: `from fastmcp import FastMCP`

### Wskazówki do moderowania
- **Szybka instalacja**: nie zatrzymuj się na tym — 30 sekund i dalej
- **Jeśli instalacja trwa długo**: w międzyczasie wyjaśnij, czym jest FastMCP

---

## 🔹 Krok 1: Pierwszy serwer MCP (~5 min)

### Intro — co powiedzieć
„Cały serwer MCP w 3 liniach: utwórz serwer, dodaj narzędzie, gotowe. FastMCP robi resztę — generuje schematy, obsługuje protokół, serwuje narzędzia."

### Wyjaśnienie — punkty techniczne
- **`mcp = FastMCP("IT Helpdesk")`** — tworzy serwer z nazwą
- **`@mcp.tool`** — dekorator rejestrujący funkcję jako narzędzie MCP
- **Dekorator NIE zmienia funkcji** — można ją nadal wywoływać normalnie: `ping()`
- FastMCP automatycznie generuje:
  - Nazwę narzędzia z nazwy funkcji
  - Opis z docstringa
  - Schemat parametrów z type hints

### Storytelling
„To CAŁE API do budowy serwera MCP. Jedna linia setup, jeden dekorator. W day2_02 musieliście ręcznie pisać JSON Schema — tu FastMCP generuje go automatycznie z type hints i docstringów."

### Aktywizacja
- „Dodajcie własne narzędzie `goodbye()` — zwraca pożegnanie. 30 sekund."
- „Co się stanie, jeśli nie napiszecie docstringa? (Model nie będzie wiedział, do czego służy narzędzie!)"

### Wskazówki do moderowania
- **Moment wow**: podkreśl prostotę — 3 linie kodu to cały serwer
- **Porównaj z day2_02**: tam ręczny JSON Schema (20 linii), tu automatyczny z dekoratora

### Przejście
„Mamy serwer z jednym narzędziem. Czas dodać prawdziwe narzędzia IT helpdesk."

---

## 🔹 Krok 2: 4 narzędzia IT Helpdesk (~10 min)

### Intro — co powiedzieć
„Budujemy 4 narzędzia — te same co w naszym agencie Pythonowym! Ale teraz jako MCP tools — każdy klient MCP może ich użyć."

### Wyjaśnienie — 4 narzędzia

| # | Narzędzie | Dane | Typ |
|---|-----------|------|-----|
| 1 | `search_knowledge_base(query)` | 5 runbooków (keyword matching) | Read |
| 2 | `get_ticket(ticket_id)` | 5 zgłoszeń (dict) | Read |
| 3 | `create_ticket(summary, category, priority)` | Nowe zgłoszenie | Write |
| 4 | `check_system_status(system_name)` | 5 systemów IT | Read |

#### Kluczowe różnice vs day2_02
- **Prostsze dane**: 5 zgłoszeń (dict) zamiast 24 (DataFrame) — szybciej, czytelniej
- **Inny 4. tool**: `check_system_status` zamiast `query_ticket_stats` — bliżej rzeczywistego MCP use case
- **Type hints + docstrings**: FastMCP generuje z nich JSON Schema automatycznie

### Prowadzenie — szybko!
- Uczestnicy widzieli te dane już dwa razy (day2_01, day2_02) — nie tłumacz szczegółów
- Każde narzędzie: pokaż dekorator → uruchom test → następne
- Zwróć uwagę na wyniki testów — każda komórka wypisuje output

### Aktywizacja
- „Dodajcie 5. narzędzie: `list_tickets()` — zwraca listę wszystkich zgłoszeń"
- „Jakie narzędzia z waszej firmy podłączylibyście jako MCP?"

### Wskazówki do moderowania
- **Prowadź szybko**: max 10 min na wszystkie 4 narzędzia
- **Nie wchodź w dane**: uczestnicy je znają
- **Podkreśl dekorator**: `@mcp.tool` — to jedyna różnica od zwykłej funkcji

### Przejście
„Mamy 5 narzędzi. Do tej pory wywoływaliśmy je jako zwykłe funkcje Pythona. Ale to NIE jest MCP — to po prostu Python. Teraz przetestujemy przez prawdziwy protokół MCP."

---

## 🔹 Krok 3: Test przez protokół MCP (~10 min)

### Intro — co powiedzieć
„Do tej pory `search_knowledge_base('vpn')` to zwykłe wywołanie funkcji Pythona. Teraz użyjemy prawdziwego klienta MCP — dokładnie tego samego protokołu, którego używa Claude Desktop."

### Wyjaśnienie — punkty techniczne
- **`from fastmcp.client import Client`** — klient MCP wbudowany w FastMCP
- **`async with Client(mcp) as client:`** — łączy się in-process (bez osobnego procesu)
- **`list_tools()`** — zwraca schematy wszystkich narzędzi (JSON Schema!)
- **`call_tool("name", {"param": "value"})`** — wywołuje narzędzie przez protokół MCP
- **Różnica kluczowa**:
  - Wcześniej: `search_knowledge_base("vpn")` — Python function call
  - Teraz: `client.call_tool("search_knowledge_base", {"query": "vpn"})` — MCP protocol call

### Storytelling
„To jest moment prawdy. Wcześniej wywolywaliście funkcje bezpośrednio — jak wchodzenie do kuchni i gotowanie samemu. Teraz zamawiamy przez kelnera (protokół MCP). Ten sam obiad, ale przez oficjalny kanał — dokładnie tak, jak to robi Claude Desktop."

### Co pokazać
1. **list_tools()** — wypisuje 5 narzędzi z automatycznie wygenerowanymi schematami JSON
   - „Widzicie? FastMCP wygenerował schematy z type hints i docstringów. Model AI widzi dokładnie to."
2. **call_tool("ping", {})** — najprostszy test
3. **call_tool("search_knowledge_base", {"query": "vpn problemy"})** — real data
4. **call_tool("get_ticket", {"ticket_id": "T-001"})** — odczyt
5. **call_tool("create_ticket", {...})** — zapis

### Aktywizacja
- „Porównajcie schemat z list_tools() ze schematem, który ręcznie pisaliście w day2_02. Który łatwiejszy?"
- „Wywołajcie call_tool z własnym zapytaniem — np. wyszukajcie w bazie wiedzy o drukarce"
- „Co widzicie w `.data`? (Wynik narzędzia — string, tak jak go zwraca funkcja)"

### Wskazówki do moderowania
- **To jest kluczowy krok** — różnica między „Python z dekoratorem" a „prawdziwy MCP"
- **Podkreśl**: `list_tools()` → schematy JSON → to widzi model AI
- **`r.data`** vs `r.content` — FastMCP zwraca wynik w `.data`; jeśli Error: sprawdź wersję FastMCP
- **Async w Jupyter**: `await test_mcp_server()` działa bezpośrednio w Jupyter/Colab
- **Jeśli ktoś pyta o „prawdziwą" komunikację**: „W produkcji serwer działa jako osobny proces. Client łączy się przez stdio lub SSE. Tu testujemy in-process — ten sam protokół, łatwiejszy setup."

### Puenta po tym kroku
„To jest siła MCP: piszesz zwykłe funkcje Pythona → FastMCP generuje schemat → dowolny klient AI może ich używać. Claude Desktop, Cursor, wasz własny agent — wszyscy mówią tym samym protokołem."

### Przejście
„Serwer działa w notebooku. Ale żeby Claude Desktop mógł go użyć, potrzebujemy osobnego pliku i konfiguracji."

---

## 🔹 Krok 4: Export + konfiguracja (~5 min)

### Intro — co powiedzieć
„Notebook to świetne miejsce do prototypowania. Ale do produkcji potrzebujemy samodzielnego pliku `.py` i konfiguracji klienta."

### Wyjaśnienie — co pokazać
1. **Plik `it_helpdesk_mcp.py`** — dołączony do materiałów
   - Te same narzędzia co w notebooku
   - `if __name__ == "__main__": mcp.run()` na końcu
   - Gotowy do uruchomienia: `python it_helpdesk_mcp.py`

2. **Konfiguracja Claude Desktop**:
   ```json
   {
     "mcpServers": {
       "it-helpdesk": {
         "command": "python",
         "args": ["PELNA_SCIEZKA/it_helpdesk_mcp.py"]
       }
     }
   }
   ```
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%/Claude/claude_desktop_config.json`

### Aktywizacja
- „Kto ma Claude Desktop? Spróbujcie podłączyć w domu!"
- „Jakie narzędzia z waszej firmy podłączylibyście jako MCP server?"

### Wskazówki do moderowania
- **Nie rób live demo podłączania do Claude Desktop** — za dużo zmiennych, za mało czasu
- **Pokaż konfigurację i ścieżkę** — to wystarczy, żeby uczestnicy zrobili to w domu
- **Podkreśl**: `it_helpdesk_mcp.py` to take-home artifact — zabierz, podłącz, używaj

---

## 🔹 Podsumowanie (~3 min)

### 5 kluczowych lekcji
1. **MCP tool = zwykła funkcja Pythona** z dekoratorem `@mcp.tool`
2. **FastMCP generuje schemat automatycznie** z type hints i docstrings
3. **Ten sam serwer działa z każdym klientem MCP** — Claude Desktop, Cursor, własny agent
4. **Wczoraj: konsument MCP. Dziś: producent MCP.** Pełne koło.
5. **Prawdziwy MCP**: `Client(mcp)` + `call_tool()` ≠ zwykłe wywołanie funkcji

### Puenta
„Wczoraj używaliście narzędzi MCP. Dziś je budujecie. Jutro połączycie je z systemami w swojej firmie."

### Ćwiczenie końcowe (do zrobienia w domu)
Rozszerz serwer o narzędzie `escalate_ticket(ticket_id, reason)`:
1. Zmienia priorytet zgłoszenia na P1
2. Dodaje komentarz z powodem eskalacji
3. Zwraca potwierdzenie

---

## 🚨 Strategie awaryjne (Fallback)

### FastMCP nie installuje się
- `!pip install fastmcp --quiet` → restart kernel
- Jeśli conflict: `!pip install --force-reinstall fastmcp`
- Minimalna wersja Pythona: 3.9

### Client nie działa / import error
- Sprawdź wersję: `!pip show fastmcp` — potrzebujesz >= 2.0
- Jeśli `from fastmcp.client import Client` nie działa: `from fastmcp import Client`
- Alternatywa: pokaż narzędzia jako zwykłe funkcje i wyjaśnij, że w produkcji idą przez protokół

### Async nie działa w Jupyter
- W Colab: `await` działa bezpośrednio w komórce
- W VS Code/Jupyter: dodaj `import nest_asyncio; nest_asyncio.apply()` przed `await`
- Alternatywa: `import asyncio; asyncio.run(test_mcp_server())`

### Brak Claude Desktop
- Nie jest wymagane — notebook działa samodzielnie
- Konfiguracja to take-home — uczestnicy mogą podłączyć po szkoleniu
- Opcja: pokaż na swoim laptopie jeśli masz zainstalowane

### Brak czasu
- Pomiń ćwiczenia opcjonalne (goodbye, list_tickets, escalate_ticket)
- Prowadź Krok 2 szybciej — uczestnicy znają te dane
- Krok 4 (export) można omówić słownie zamiast uruchamiać

---

## 📝 Notatki po warsztacie

*(Uzupełnij po przeprowadzeniu:)*

- Czy FastMCP zainstalował się bez problemów: ___
- Czy Client/MCP testing działał: ___
- Ile osób planuje podłączyć do Claude Desktop: ___
- Najciekawsze pytanie uczestnika: ___
- Czy ktoś zaproponował ciekawe narzędzie dla swojej firmy: ___
- Co zmienić na następny raz: ___
