
# 🤖 Notatki trenera — Budujemy agenta AI w Pythonie

**Notebook:** `day2_02_python_agent.ipynb`
**Czas:** ~60 minut
**Wymagania:** Google Colab (GPU nie wymagane!), klucz API OpenRouter (https://openrouter.ai/keys)

---

## ✅ Checklist przed warsztatem

- [ ] Notebook otwarty w Colab (lub VS Code)
- [ ] **Klucz API OpenRouter** skonfigurowany (jeden z poniższych sposobów):
  - Colab: dodaj `OPENROUTER_API_KEY` w Secrets (ikona klucza po lewej)
  - Lokalnie (VS Code): `export OPENROUTER_API_KEY="sk-or-..."`
  - Notebook zapyta interaktywnie przez `getpass()` jeśli brak
- [ ] Test połączenia zwraca „API: działa!"
- [ ] Jeśli brak klucza API: sprawdź, że tryb fallback ([FALLBACK]) działa
- [ ] `large_tickets.csv` opcjonalnie wgrany (notebook ma wbudowane 24 zgłoszenia)
- [ ] Ten dokument na drugim ekranie

---

## ⏱️ Plan czasowy

| Czas | Krok | Co się dzieje |
|------|------|---------------|
| 0:00 | Setup | Klucz API, test połączenia |
| 0:03 | Krok 1 | Podstawowe wywołanie LLM — `call_llm()` |
| 0:13 | Krok 2 | Definiowanie 4 narzędzi + JSON Schema |
| 0:28 | Krok 3 | Pętla agenta — `agent_chat()` + 4 testy |
| 0:43 | Krok 4 | Pamięć — `ITAgent` klasa, rozmowa wieloturowa |
| 0:53 | Krok 5 | Pełne demo — 4-krokowy scenariusz |
| 0:60 | Koniec | |

---

## 🔹 Krok 0: Setup (~3 min)

### Intro — co powiedzieć
„Dziś budujemy agenta AI od zera w Pythonie. Żadnego frameworka, żadnego GPU — czyste HTTP requesty do modelu w chmurze. Ten sam klucz API OpenRouter co wcześniej."

### Wyjaśnienie — punkty techniczne
- **OpenRouter** = uniwersalne API do wielu modeli (Llama, GPT, Claude, Gemma)
- **Model**: `meta-llama/llama-3.1-8b-instruct` — dobry stosunek jakość/cena (~$0.06/M tokenów)
- **Trzy sposoby konfiguracji klucza**: `os.environ` → Colab Secrets → `getpass()`
- **Fallback mode**: notebook działa bez API — zwraca `[FALLBACK] Odpowiedź na: ...`

### Wskazówki do moderowania
- **Jeśli ktoś nie ma klucza**: udostępnij swój na czacie. Koszt 20 uczestników przez 60 min: <$2
- **Jeśli test zwraca błąd**: sprawdź saldo na openrouter.ai, sprawdź czy klucz nie wygasł
- **Jeśli `getpass()` nie działa w Colab**: użyj Colab Secrets (ikona klucza po lewej)

### Przejście
„Test mówi 'API działa' — mamy połączenie z modelem. Teraz zbudujmy funkcję, która go wywołuje."

---

## 🔹 Krok 1: Podstawowe wywołanie LLM (~10 min)

### Intro — co powiedzieć
„Każdy agent AI zaczyna od jednej umiejętności: wywołania modelu. Funkcja `call_llm()` to 'mózg' agenta — wysyłamy pytanie, dostajemy odpowiedź."

### Wyjaśnienie — punkty techniczne
- **Chat completions format**: lista wiadomości z rolami (`system`, `user`, `assistant`)
- Ten sam format używają OpenAI, Anthropic, Google — standard branżowy
- Funkcja zwraca **pełny obiekt message**, nie tylko tekst — bo za chwilę będziemy potrzebować `tool_calls`
- `requests.post()` + JSON payload = cały interfejs do AI

### Storytelling
„To jest moment, w którym zdajecie sobie sprawę, że cała magia AI to jeden HTTP POST. Requests.post() i mamy AI. To wszystko. Żadnego GPU, żadnej instalacji, żadnego czekania na pobieranie modelu."

### Aktywizacja — pytania do grupy
- „Zmieńcie `system_prompt` na coś innego — np. 'Jesteś pirackim kapitanem'. Jak zmienia się ton?"
- „Co się stanie, jeśli nie podamy system prompt?"
- „Dlaczego zwracamy pełny obiekt message, a nie tylko tekst?"

### Wskazówki do moderowania
- **Kluczowy punkt**: podkreśl, że `call_llm()` zwraca cały obiekt message — to ważne dla Kroku 3
- **Jeśli model odpowiada po angielsku**: system prompt mówi „odpowiadaj po polsku" — pokaż, że to działa
- **Daj 2-3 min** na zmianę system promptu — to buduje engagement
- **Fallback**: w trybie fallback odpowiedź to `[FALLBACK] Odpowiedź na: ...` — wyjaśnij, że to mock

### Przejście
„Mamy mózg. Ale mózg bez rąk nic nie zrobi. Czas dać agentowi narzędzia."

---

## 🔹 Krok 2: Definiowanie narzędzi (Tools) (~15 min)

### Intro — co powiedzieć
„Agent to nie chatbot. Chatbot odpowiada na pytania. Agent ma narzędzia i SAM decyduje, którego użyć. Definiujemy 4 narzędzia — te same co poznaliśmy wcześniej."

### Wyjaśnienie — punkty techniczne
- **4 narzędzia** jako funkcje Pythona:
  1. `search_knowledge_base(query)` — szuka w 8 runbookach IT (keyword matching)
  2. `get_ticket_status(ticket_id)` — sprawdza status zgłoszenia w DataFrame
  3. `query_ticket_stats(action, category)` — statystyki (count/top/sample)
  4. `create_ticket(summary, category, priority)` — tworzy nowe zgłoszenie
- **JSON Schema** — opis narzędzi, który model dostaje:
  - `name`: nazwa funkcji
  - `description`: co narzędzie robi (model to czyta!)
  - `parameters`: typy i opisy parametrów
- **Native tool calling**: model zwraca strukturalne wywołanie, nie wolny tekst do parsowania
- **24 wbudowane zgłoszenia** (6 per kategoria) — notebook jest samodzielny, bez plików
- **Klasyfikacja NIE jest narzędziem** — to rozumowanie, które model robi natywnie

### Storytelling
„Wyobraźcie sobie, że dajecie nowemu pracownikowi instrukcję: 'Masz dostęp do 4 systemów. Tu sprawdzisz bazę wiedzy. Tu status zgłoszenia. Tu statystyki. Tu tworzysz nowe. Sam decyduj, kiedy którego użyć.' To dokładnie to, co robimy z modelem — JSON Schema to instrukcja."

„A klasyfikacja? To jak pytanie kelnerowi 'Co polecasz?'. Nie potrzebuje narzędzia — poleca na podstawie wiedzy i rozumowania."

### Aktywizacja — pytania do grupy
- „Popatrzcie na JSON Schema create_ticket — co model widzi? Nazwy, opisy, typy."
- „Dlaczego description jest tak ważne? (Bo model na jego podstawie decyduje, kiedy użyć narzędzia!)"
- „Jakie 5. narzędzie byłoby przydatne? (np. `escalate_ticket`, `assign_ticket`)"

### Wskazówki do moderowania
- **Pokaż pełny schemat `create_ticket`**: to najlepszy przykład — 3 parametry, enum, required
- **Podkreśl rozróżnienie**: narzędzia READ (search, get, query) vs WRITE (create)
- **Jeśli ktoś pyta o `TOOL_FUNCTIONS` dict**: to mapowanie nazwa → funkcja, potrzebne w Kroku 3
- **Nie wchodź głęboko w dane**: uczestnicy znają je z day2_01 — prowadź szybko

### Przejście
„Mamy narzędzia i ich opisy. Ale kto decyduje, kiedy którego użyć? Model. I tu zaczyna się magia — pętla agenta."

---

## 🔹 Krok 3: Pętla agenta (Agent Loop) (~15 min)

### Intro — co powiedzieć
„To jest serce agenta. Wysyłamy pytanie + listę narzędzi do modelu. Model decyduje: czy potrzebuję narzędzia? Jeśli tak — którego i z jakimi parametrami? Zwraca `tool_calls` — my je wykonujemy — i dajemy wynik modelowi, żeby odpowiedział na oryginalne pytanie."

### Wyjaśnienie — punkty techniczne
- **Pętla agenta**:
  ```
  Użytkownik → pytanie → LLM + tools
                              │
                    ┌─── tool_calls? ───┐
                    │                   │
                   TAK                 NIE
                    │                   │
              Wykonaj tool        Zwróć odpowiedź
                    │
              Dodaj wynik do messages
                    │
              Wywołaj LLM ponownie
                    │
              Zwróć końcową odpowiedź
  ```
- **Native tool_calls**: model zwraca `tool_calls` jako strukturalny JSON, nie tekst
- `execute_tool(name, arguments)` — dispatcher: mapuje nazwę na funkcję
- `agent_chat(user_message, messages)` — pełna pętla: pytanie → (opcjonalnie tools) → odpowiedź

### Storytelling
„To jest ta magiczna pętla. Pytasz agenta 'Jaki jest status T-007?'. Agent myśli: 'Potrzebuję narzędzia get_ticket_status z argumentem T-007.' Wywołuje. Dostaje wynik. I dopiero teraz formułuje odpowiedź dla Ciebie. Dwa wywołania LLM — jedno na decyzję, drugie na odpowiedź."

### Aktywizacja — 4 testy w notebooku
- **Test 1**: „Mam problem z drukarką sieciową" → wywołuje `search_knowledge_base`
- **Test 2**: „Jaki jest status T-007?" → wywołuje `get_ticket_status`
- **Test 3**: „Ile mamy otwartych zgłoszeń?" → wywołuje `query_ticket_stats`
- **Test 4**: „Utwórz zgłoszenie: laptop nie włącza się" → wywołuje `create_ticket`

### Wskazówki do moderowania
- **Test 4 to moment wow**: agent SAM decyduje o kategorii (Sprzęt) i priorytecie (P1) — podkreśl to!
- **Wypisz na głos**: „Klasyfikacja to rozumowanie, nie narzędzie!"
- **Pokaż logi**: każde wywołanie narzędzia wypisuje `Narzędzie: ... → Wynik: ...`
- **Jeśli model nie wywołuje narzędzia**: niektóre tanie modele mają słaby tool calling. Opcja: zmień na `meta-llama/llama-3.3-70b-instruct`
- **Jeśli model wywołuje złe narzędzie**: to moment dydaktyczny — „Dlatego description w JSON Schema jest tak ważne!"

### Przejście
„Agent działa! Ale zauważcie — każde pytanie to osobna rozmowa. Agent nie pamięta, że przed chwilą szukał w bazie wiedzy. Czas na pamięć."

---

## 🔹 Krok 4: Pamięć (Memory) (~10 min)

### Intro — co powiedzieć
„Pamięć to po prostu lista wiadomości. Przy każdym wywołaniu dodajemy całą historię do kontekstu. Model widzi poprzednie pytania i odpowiedzi."

### Wyjaśnienie — punkty techniczne
- **Klasa `ITAgent`** z `self.messages` — pełna historia rozmowy
- `chat(user_message)` — dodaje wiadomość, wywołuje `agent_chat()`, utrzymuje messages
- `show_memory()` — wypisuje pełny ślad rozmowy (role + content + tool_calls)
- **Pamięć = messages list** — rosnie z każdą wymianą
- **Context window** = limit pamięci — dlatego context engineering jest ważny

### Storytelling
„Bez pamięci agent ma Alzheimera — każda rozmowa to od nowa. Z pamięcią potrafi powiedzieć 'Wcześniej szukałem w bazie wiedzy o VPN — na tej podstawie tworzę zgłoszenie.' To fundamentalna zmiana jakości."

### Aktywizacja — 4-turowa rozmowa
1. „Jaki jest status zgłoszenia T-007?" → narzędzie + odpowiedź
2. „A co z T-001?" → narzędzie + odpowiedź (agent wie, że porównujemy!)
3. „Przeszukaj bazę wiedzy — co mogę zrobić z problemem VPN?" → narzędzie + odpowiedź
4. „Na podstawie tego co znaleźliśmy — utwórz zgłoszenie" → agent PAMIĘTA kontekst!

### Wskazówki do moderowania
- **Tura 4 to moment wow**: agent tworzy zgłoszenie na podstawie wcześniej znalezionej informacji
- **`show_memory()`**: pokaż pełny ślad — uczestnicy zobaczą, ile wiadomości przepływa
- **Pytanie prowokacyjne**: „Co się stanie, jeśli rozmowa ma 1000 tur? (Context window się wyczerpie)"
- **Ćwiczenie**: „Jak ograniczylibyście pamięć do N ostatnich wiadomości?"

### Przejście
„Mamy kompletnego agenta: mózg, narzędzia, pętlę decyzyjną i pamięć. Czas na pełne demo."

---

## 🔹 Krok 5: Pełne demo (~10 min)

### Intro — co powiedzieć
„Łączymy wszystko w jeden scenariusz: użytkownik zgłasza problem, agent szuka w bazie, tworzy zgłoszenie, sprawdza statystyki. 4 tury — pełny workflow."

### Wyjaśnienie — scenariusz demo
1. „Drukarka sieciowa na 2. piętrze nie odpowiada od rana" → agent rozpoznaje problem
2. „Przeszukaj bazę wiedzy, co mogę sprawdzić?" → `search_knowledge_base`
3. „OK, utwórz zgłoszenie o tym problemie" → `create_ticket` (agent decyduje: Sieć, P2)
4. „Ile mamy teraz zgłoszeń w kategorii Sieć?" → `query_ticket_stats`

### Aktywizacja — pytania końcowe
- „Co byście dodali do tego agenta?"
- „Jakie narzędzia dalibyście agentowi w waszej firmie?"
- „Gdzie jest granica — co agent powinien robić sam, a co z człowiekiem?"
- „Kto zauważył, że klasyfikacja to rozumowanie, nie narzędzie? Dlaczego to ważne?"

### Opcjonalna interaktywna pętla
- Komórka z `interactive_agent` jest zakomentowana — odkomentuj jeśli czas pozwala
- Pozwól uczestnikom wpisywać własne pytania
- Sugerowane pytania w notebooku

---

## 🚨 Strategie awaryjne (Fallback)

### Brak klucza API OpenRouter
- Notebook automatycznie przełącza się na **fallback mode** — odpowiedzi to `[FALLBACK] Odpowiedź na: ...`
- Wszystkie komórki działają — pętla agenta, pamięć, testy
- Powiedz: „Logika agenta jest taka sama — jedyne co brakuje to prawdziwy model"
- Udostępnij swój klucz na czacie jako Plan B

### Model nie wywołuje narzędzi
- `meta-llama/llama-3.1-8b-instruct` dobrze obsługuje tool calling
- Jeśli problemy: zmień na `meta-llama/llama-3.3-70b-instruct` (droższy, ale lepszy tool calling)
- Opcja: pokaż raw response — `print(json.dumps(response, indent=2))`

### API zwraca błędy
- **401**: klucz nieprawidłowy → wygeneruj nowy na openrouter.ai/keys
- **402**: brak salda → doładuj ($5 wystarczy na szkolenie)
- **429**: rate limit → poczekaj 30s
- **Timeout**: problem z siecią → sprawdź połączenie

### Notebook nie uruchamia się w Colab
- Sprawdź, czy runtime jest ustawiony (Runtime → Change Runtime → CPU wystarczy)
- Jeśli `import requests` nie działa: `!pip install requests`

---

## 📝 Notatki po warsztacie

*(Uzupełnij po przeprowadzeniu:)*

- Czy tool calling działał niezawodnie: ___
- Najczęstsze pytanie uczestnika: ___
- Który test zrobił największe wrażenie (1-4): ___
- Ile osób zrobiło ćwiczenie `escalate_ticket`: ___
- Co zmienić na następny raz: ___
