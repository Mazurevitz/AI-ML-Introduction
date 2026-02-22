
# 🧠 Notatki trenera — Porównanie 5 podejść do klasyfikacji zgłoszeń IT

**Notebook:** `day2_01_ml_vs_llm_comparison.ipynb`
**Czas:** ~55 minut
**Wymagania:** Google Colab (GPU nie jest wymagane!), klucz API OpenRouter (https://openrouter.ai/keys)

---

## ✅ Checklist przed warsztatem

- [ ] Notebook otwarty w Colab (lub VS Code) — runtime domyślny (CPU wystarczy!)
- [ ] `large_tickets.csv` wgrany do Colab (lub w tym samym folderze co notebook)
- [ ] Komórki setup (0) uruchomione — biblioteki zainstalowane
- [ ] **Klucz API OpenRouter** skonfigurowany (jeden z poniższych sposobów):
  - Colab: dodaj `OPENROUTER_API_KEY` w Secrets (ikona 🔑 po lewej)
  - Lokalnie (VS Code): utwórz plik `.env` obok notebooka z: `OPENROUTER_API_KEY=sk-or-...`
  - Terminal: `export OPENROUTER_API_KEY="sk-or-..."`
- [ ] Komórka API test (cell-15) zwraca „🔌 API: ✅ działa!"
- [ ] Jeśli brak klucza API: sprawdzić, że fallback_llm_results i fallback_rag_results działają
- [ ] Przygotować tablicę/whiteboard do zapisania wyników grupowych
- [ ] Opcjonalnie: `pip install python-dotenv` (jeśli uruchamiasz lokalnie z plikiem `.env`)

---

## ⏱️ Plan czasowy

| Czas | Część | Co się dzieje |
|------|-------|---------------|
| 0:00 | Setup | Otwieranie Colab, import bibliotek |
| 0:02 | Część 1 | Klasyfikacja ręczna — uczestnicy wpisują odpowiedzi |
| 0:07 | Część 2 | Supervised ML — trening modelu, omówienie wyników |
| 0:22 | Część 3 | KMeans — klastry bez etykiet, PCA wizualizacja |
| 0:32 | Część 4 | LLM zero-shot — API call, klasyfikacja |
| 0:40 | Część 5 | RAG — baza wiedzy + LLM, porównanie z Częścią 4 |
| 0:50 | Podsumowanie | Wykres, tabela, dyskusja |
| 0:55 | Koniec | |

---

## 🔹 Część 1: Klasyfikacja ręczna (~5 min)

### Intro — co powiedzieć
„Zanim uruchomimy jakikolwiek model, zróbmy coś starego jak świat — sklasyfikujmy zgłoszenia sami. To będzie nasz punkt odniesienia: human baseline. Zobaczymy, czy maszyna potrafi nas pobić."

### Wyjaśnienie — punkty techniczne
- **Baseline** to fundamentalna koncepcja w ML — bez niego nie wiemy, czy model jest dobry
- Ludzie klasyfikują na podstawie doświadczenia i intuicji
- Problem: różni eksperci mogą sklasyfikować to samo zgłoszenie inaczej (inter-annotator agreement)
- 4 z 10 zgłoszeń jest **celowo niejednoznacznych** — tu widać różnice

### Storytelling
„Wyobraźcie sobie helpdesk w dużej firmie. Przychodzi 500 zgłoszeń dziennie. Nowy pracownik ma je ręcznie przydzielać do zespołów: Sprzęt, Sieć, Oprogramowanie, Konto. Ile pomyłek zrobi w pierwszym tygodniu? A ile po roku?"

„Albo: wyobraźcie sobie sortowanie paczek na poczcie. Osoba sortująca musi patrzeć na adres i wrzucać do odpowiedniego worka. Proste, ale nie skalowalne."

### Aktywizacja — pytania do grupy
- „Kto przypisał 'Drukarka sieciowa nie odpowiada' do Sprzęt? A kto do Sieć? Dlaczego?"
- „Jakie informacje pomogłyby wam podjąć lepszą decyzję?"
- „Czy 10/10 jest realistyczne? Czy ekspert zawsze ma rację?"

### Wskazówki do moderowania
- **Flaga SKIP_MANUAL**: w notebooku jest `SKIP_MANUAL = True` — zmień na `False`, jeśli chcesz, żeby uczestnicy wpisywali odpowiedzi ręcznie. Przy `True` notebook używa pre-set odpowiedzi eksperta IT (z celowymi 2 błędami na niejednoznacznych zgłoszeniach)
- **Jeśli ktoś nie zna kategorii**: powiedz „Kieruj się intuicją — nie ma złych odpowiedzi na tym etapie"
- **Jeśli ktoś wpisze błędnie**: accuracy_score wymaga dokładnego stringa — pokaż poprawną pisownię
- **Typowy wynik**: 6-8/10 dla grupy. Jeśli ktoś ma 10/10, pochwal i zapytaj o logikę
- **Ważne**: NIE podawaj poprawnych odpowiedzi przed uruchomieniem — niech komórka je wyświetli
- **Rada**: przy dużej grupie (>10 osób) użyj `SKIP_MANUAL = True` i niech uczestnicy zapiszą odpowiedzi na kartce — oszczędza czas

### Przejście do Części 2
„OK, zobaczyliście, że nawet dla nas to nie jest trywialne. A teraz dajmy te same zgłoszenia maszynie, która **nauczyła się z 200 przykładów**."

---

## 🔹 Część 2: Supervised ML (~15 min)

### Intro — co powiedzieć
„To klasyczne podejście ML: mamy zbiór danych z etykietami, trenujemy model, testujemy. Zobaczymy czy 200 przykładów wystarczy, żeby model dobrze klasyfikował nowe zgłoszenia."

### Wyjaśnienie — punkty techniczne
- **TF-IDF** = zamiana tekstu na liczby z uwzględnieniem ważności słów
  - TF: ile razy słowo występuje w dokumencie
  - IDF: jak rzadkie jest słowo w całym zbiorze
  - Efekt: „drukarka" dostaje wysoką wagę w kategorii Sprzęt, „hasło" w Konto
- **Logistic Regression** = prosty, interpretowalny klasyfikator
  - Uczy się wag dla każdego słowa
  - Szybki w trenowaniu, dobry na małych zbiorach
- **Classification report**: precision, recall, f1-score — wyjaśnij na przykładzie
  - Precision: „z tych co model nazwał Sprzęt, ile naprawdę było Sprzętem?"
  - Recall: „z wszystkich zgłoszeń Sprzęt, ile model znalazł?"
- **Confusion matrix**: wizualnie pokazuje, co z czym model myli

### Storytelling
„TF-IDF to jak doświadczony pracownik helpdesku, który wie, że słowo 'drukarka' to prawie na pewno Sprzęt, ale 'nie odpowiada' może być cokolwiek. Model wyłapuje takie wzorce ze statystyki."

„Pomyślcie o tym jak o filtrze spamu w poczcie: model nauczył się, że pewne słowa (free, win, prize) = spam. Tak samo nasz model uczy się, że pewne słowa = Sieć."

### Aktywizacja — pytania do grupy
- „Na jakich zgłoszeniach model się pomylił? Dlaczego?"
- „Czy 200 przykładów to dużo czy mało?"
- „Co by się stało, gdybyśmy mieli 2000 przykładów?"
- „Czy model poradzi sobie ze zgłoszeniem w języku, którego nie widział?"

### Wskazówki do moderowania
- **Jeśli brakuje CSV**: sprawdź, czy `large_tickets.csv` jest wgrany do Colab
- **Jeśli accuracy jest niskie**: to normalne na 200 próbkach i krótkich tekstach — omów dlaczego
- **Jeśli ktoś pyta o inne modele**: „Dobra uwaga! Można użyć RandomForest, SVM, Naive Bayes. Zasada jest ta sama."
- **Confusion matrix**: pokaż palcem, gdzie model myli Sieć z Kontem — to kluczowy pattern

### Przejście do Części 3
„Model supervised wymaga etykiet — ktoś musi ręcznie oznaczyć dane. Co jeśli **nie mamy etykiet**? Czy maszyna może sama odkryć grupy?"

---

## 🔹 Część 3: Unsupervised Learning — KMeans (~10 min)

### Intro — co powiedzieć
„KMeans nie wie, jakie są kategorie. Szuka naturalnych grup w danych — klastrów. Porównamy je z naszymi 4 kategoriami."

### Wyjaśnienie — punkty techniczne
- **KMeans**: iteracyjny algorytm — losuje centroidy, przypisuje punkty, przesuwa centroidy
- **PCA**: redukcja wymiarów z TF-IDF (setki wymiarów) do 2D dla wizualizacji
- **n_clusters=4**: my wiemy, że są 4 kategorie, ale w realnym scenariuszu to hiperparametr
- **Crosstab**: tabela krzyżowa pokazuje, jak klastry mapują się na prawdziwe etykiety
  - Idealnie: 1 klaster = 1 kategoria
  - W praktyce: nakładanie się, szczególnie Sieć/Konto

### Storytelling
„Wyobraźcie sobie, że dostajecie 10 000 zgłoszeń bez żadnych etykiet. Nikt ich nie kategoryzował. KMeans to jak danie tych zgłoszeń stażyście i powiedzenie: 'posegreguj je w 4 kupki, jak ci się wydaje najlogiczniej'."

„PCA to jak zdjęcie satelitarne miasta: nie widać szczegółów, ale widać dzielnice."

### Aktywizacja — pytania do grupy
- „Porównajcie lewy i prawy wykres — co widzicie?"
- „Czy klaster 0 odpowiada jednej kategorii, czy jest mieszany?"
- „Co jeśli ustawimy n_clusters=3? A 6?"
- „Kiedy w firmie byłoby przydatne unsupervised learning?"

### Wskazówki do moderowania
- **Jeśli klastry się źle mapują**: to normalne — krótkie teksty po polsku to trudne dane. Podkreśl, że unsupervised nie gwarantuje „dobrych" grup
- **Wykresy PCA mogą być zaskakujące**: punkty mogą się nakładać — wyjaśnij, że 2D to uproszczenie
- **Typowa obserwacja**: Konto i Sieć się mieszają (bo oba mówią o „logowaniu")

### Przejście do Części 4
„OK, ML radzi sobie nieźle, ale wymaga danych treningowych. A co jeśli mamy model, który **już rozumie język** i nie trzeba go trenować?"

---

## 🔹 Część 4: LLM — klasyfikacja zero-shot przez API (~8 min)

### Intro — co powiedzieć
„Teraz coś zupełnie innego: Large Language Model. Model, który widzi nasze zgłoszenia pierwszy raz. Zero-shot — zero przykładów treningowych. Wysyłamy jedno zapytanie do API i dostajemy klasyfikację wszystkich 10 zgłoszeń."

### Wyjaśnienie — punkty techniczne
- **Zero-shot**: model nie widział naszych danych ani naszych kategorii wcześniej
- **OpenRouter API**: uniwersalne API do wielu modeli (Llama, Gemma, Qwen, GPT, Claude) — jeden klucz, wiele modeli
- **Model**: `meta-llama/llama-3.1-8b-instruct` — dobry stosunek jakość/cena. Koszt klasyfikacji 10 zgłoszeń: < $0.001
- **Batch classification**: wszystkie 10 zgłoszeń w jednym API call — tańsze i szybsze niż 10 osobnych
- **Prompt engineering**: jedyne „trenowanie" to dobry prompt — prosimy o JSON array z kategoriami
- **Dlaczego model się myli na niejednoznacznych?**: nie zna naszych wewnętrznych procedur
  - „Drukarka sieciowa" → LLM widzi „drukarka" i mówi Sprzęt (bo w internecie drukarka = hardware)
  - „Zalogować się do WiFi" → LLM widzi „zalogować" i mówi Konto

### Storytelling
„LLM to jak nowy, bardzo inteligentny konsultant: świetnie rozumie język, ale nie zna waszych procedur. Mówicie mu 'sklasyfikuj to zgłoszenie' i on robi co może na podstawie ogólnej wiedzy. Ale nie wie, że w waszej firmie 'drukarka sieciowa' to dział Sieć."

„Zwróćcie uwagę, że wysyłamy **jedno zapytanie** z 10 zgłoszeniami i dostajemy odpowiedź w 2 sekundy. To samo w firmie — można klasyfikować setki zgłoszeń w minutę za grosze."

### Aktywizacja — pytania do grupy
- „Porównajcie wynik LLM z waszym ręcznym — na czym się zgadzacie?"
- „Dlaczego LLM pomylił 'drukarkę sieciową'? Co mu brakuje?"
- „Jak moglibyśmy poprawić prompt, żeby LLM lepiej klasyfikował?"
- „Ile to kosztuje? Czy opłaca się vs zatrudnienie człowieka do klasyfikacji?"

### Wskazówki do moderowania
- **Jeśli brak klucza API**: notebook automatycznie przełącza się na fallback (pre-computed results). Powiedz: „Wyniki są pre-computed — w firmie podpinamy swój klucz API."
- **API odpowiada w 1-3 sekundy**: dużo szybciej niż ładowanie lokalnego modelu. Podkreśl prostotę — zero instalacji, zero GPU
- **Jeśli API zwraca błąd**: sprawdź klucz, sprawdź saldo na openrouter.ai. Fallback zadziała automatycznie
- **Jeśli model daje dziwne odpowiedzi**: pokaż raw JSON response — czasem LLM dodaje komentarze do JSON
- **Porównanie z ML**: jeśli ML > LLM, to doskonały moment na lekcję: „dane > model!"
- **Zmiana modelu**: w komórce konfiguracji można zmienić `LLM_MODEL` na inny — dobra okazja, żeby porównać modele

### Przejście do Części 5
„LLM nie zna naszych procedur — dlatego myli się na niejednoznacznych zgłoszeniach. A co jeśli **damy mu naszą dokumentację**? To właśnie robi RAG."

---

## 🔹 Część 5: RAG — LLM + baza wiedzy (~10 min)

### Intro — co powiedzieć
„RAG = Retrieval-Augmented Generation. Zamiast pytać LLM 'na ślepo', najpierw wyszukujemy w naszej dokumentacji fragmenty, które mogą pomóc, i dołączamy je do prompta."

### Wyjaśnienie — punkty techniczne
- **Knowledge base**: fragmenty runbooków IT — procedury klasyfikacji
- **Retrieval**: tu uproszczony (keyword matching), w produkcji: embeddings + vector DB
- **Augmented Generation**: prompt zawiera kontekst → LLM podejmuje lepszą decyzję
- **Kluczowa zmiana**: te same 4 niejednoznaczne zgłoszenia teraz mają kontekst
  - „Drukarka sieciowa" + RUNBOOK → model wie, że problem sieciowy → Sieć
  - „Zmiana hasła w ERP" + RUNBOOK → model wie, że to zarządzanie kontem → Konto

### Storytelling
„RAG to jak danie nowemu konsultantowi podręcznika firmowego. Zamiast 'zgadnij', mówisz 'przeczytaj tę stronę procedury i na tej podstawie zdecyduj'. Nagle z 60% robi się 100%."

„W prawdziwym życiu: wyobraźcie sobie helpdesk bot, który zanim odpowie klientowi, przeszukuje waszą bazę wiedzy. To jest RAG w produkcji."

### Aktywizacja — pytania do grupy
- „Które zgłoszenia RAG naprawił? Dlaczego akurat te?"
- „Co by się stało, gdybyśmy mieli złą dokumentację w bazie wiedzy?"
- „Jak RAG zmniejsza halucynacje?"
- „Jakie dokumenty z waszej firmy mogłyby trafić do bazy wiedzy RAG?"

### Wskazówki do moderowania
- **Kluczowy moment aha**: pokażcie side-by-side LLM vs RAG — te same zgłoszenia, różne wyniki
- **Jeśli ktoś pyta o vector search**: „Świetne pytanie! W produkcji użylibyśmy ChromaDB lub Pinecone. Tu upraszczamy do keyword matching."
- **Fallback działa dobrze**: nawet bez klucza API, wyniki RAG są demonstracyjne i pouczające
- **Jeśli RAG nie poprawia wszystkiego**: omów jakość bazy wiedzy — garbage in, garbage out

### Przejście do Podsumowania
„Zobaczmy teraz wszystko na jednym wykresie."

---

## 🔹 Podsumowanie (~5 min)

### Intro — co powiedzieć
„Czas na punchline. Mamy 5 podejść, te same 10 zgłoszeń. Kto wygrał?"

### Wyjaśnienie — kluczowe wnioski
1. **Dane > Model**: dobrze wytrenowany ML może pokonać LLM bez kontekstu
2. **Kontekst jest królem**: RAG poprawia wyniki tam, gdzie brakuje wiedzy domenowej
3. **Nie ma jednej metody**: wybór zależy od zasobów (dane, API, dokumentacja, budżet)
4. **Człowiek + AI**: najlepsze wyniki w produkcji daje human-in-the-loop

### Storytelling — finał
„To jak ewolucja helpdesku:
- **2005**: człowiek czyta i sortuje (Część 1)
- **2015**: algorytm wytrenowany na historii (Część 2)
- **2020**: odkrywanie wzorców w danych (Część 3)
- **2024**: AI rozumie tekst bez trenowania — jeden API call (Część 4)
- **2025+**: AI + wiedza firmowa (RAG) = prawie perfekcja (Część 5)"

### Aktywizacja — pytania końcowe
- „Którą metodę zastosowalibyście w swoim dziale?"
- „Jakie dane w waszej firmie nadawałyby się do klasyfikacji?"
- „Co was najbardziej zaskoczyło w wynikach?"

---

## 🚨 Strategie awaryjne (Fallback)

### Brak klucza API OpenRouter
- Notebook automatycznie przełącza się na **fallback** (pre-computed results) — Części 4 i 5 działają bez API
- Fallback wyniki realistycznie symulują typowe zachowanie LLM (błędy na niejednoznacznych) i RAG (poprawki)
- Powiedz: „Wyniki są pre-computed z prawdziwego modelu — w firmie podpinamy swój klucz API"
- Aby uzyskać klucz: https://openrouter.ai/keys (rejestracja przez Google, darmowe credits na start)

### API zwraca błąd
- **401 Unauthorized**: klucz API jest nieprawidłowy lub wygasł — sprawdź na openrouter.ai/keys
- **402 Payment Required**: brak środków — doładuj saldo (klasyfikacja kosztuje < $0.001)
- **429 Rate Limit**: za dużo zapytań — poczekaj minutę lub zmień model na płatny (bez sufiksu `:free`)
- **Timeout / SSL error**: problem z siecią — sprawdź połączenie internetowe
- W każdym przypadku notebook automatycznie przełączy się na fallback

### Uruchamianie lokalnie (VS Code / Jupyter)
- Utwórz plik `.env` obok notebooka: `OPENROUTER_API_KEY=sk-or-...`
- Zainstaluj: `pip install python-dotenv requests scikit-learn pandas matplotlib seaborn`
- **Ważne**: upewnij się, że VS Code używa właściwego Pythona (venv) — sprawdź w prawym dolnym rogu
- Jeśli SSL się zawiesza: prawdopodobnie złe środowisko Python — utwórz nowy venv

### CSV nie ładuje się
- Upewnij się, że `large_tickets.csv` jest w tym samym folderze co notebook
- W Colab: użyj File → Upload lub zamontuj Google Drive

### Uczestnicy mają problemy z input()
- Ustaw `SKIP_MANUAL = True` (domyślnie) — pomija ręczne wpisywanie
- Jeśli chcesz interaktywność: zmień na `False`, w Colab input() działa (wymaga kliknięcia w pole)
- Alternatywnie: niech każdy zapisze odpowiedzi na kartce i porówna po reveal

---

## 🔗 Zasoby interaktywne (do slajdów po „Historia AI")

> **Wskazówka:** Wszystkie narzędzia poniżej są darmowe i działają w przeglądarce (z wyjątkiem Orange). Przy słabym internecie — załaduj strony przed sesją. Narzędzia Polo Club (CNN Explainer, Transformer Explainer, GAN Lab, Diffusion Explainer) pochodzą z Georgia Tech i mają spójną jakość wizualną.

### 🗺️ Mapa AI / Typy modeli
- **FirstMark MAD Landscape** — https://mad.firstmark.com — interaktywna, przeszukiwalna mapa ekosystemu ML/AI/Data (edycja 2025, z sekcją Agent Stack i Local AI)
- **Elements of AI** — https://course.elementsofai.com/ — darmowy kurs University of Helsinki z interaktywnymi quizami (2M+ studentów, 170 krajów)
- **Hugging Face Tasks** — https://huggingface.co/tasks — interaktywna mapa zadań AI z demo dla każdego typu

### 🧠 Sieci neuronowe
- **TensorFlow Playground** — https://playground.tensorflow.org *(już w slajdach)*
- **Brendan Bycroft's LLM Visualization** — https://bbycroft.net/llm — oszałamiająca wizualizacja 3D architektury transformera krok po kroku (embedding, attention, prediction). **Najlepszy efekt wow w klasie!**
- **Transformer Explainer** — https://poloclub.github.io/transformer-explainer/ — uruchamia GPT-2 w przeglądarce, można wpisać własny tekst i obserwować attention maps w czasie rzeczywistym
- **CNN Explainer** — https://poloclub.github.io/cnn-explainer/ — wizualizacja sieci konwolucyjnych: warstwy, pooling, softmax z animacjami
- **Adam Harley's NN Vis** — https://adamharley.com/nn_vis/ — narysuj cyfrę i obserwuj jak sieć ją przetwarza warstwa po warstwie

### ✨ Generatywna AI
- **Chatbot Arena (LMArena)** — https://lmarena.ai/ — blind test dwóch LLM side-by-side z głosowaniem i rankingiem Elo. Bez rejestracji!
- **Diffusion Explainer** — https://poloclub.github.io/diffusion-explainer/ — interaktywna wizualizacja Stable Diffusion: zmień prompt, dostosuj parametry, obserwuj generowanie obrazu
- **GAN Lab** — https://poloclub.github.io/ganlab/ — interaktywna wizualizacja GAN w przeglądarce: rysuj dane, obserwuj trening w slow-motion
- **Artificial Analysis** — https://artificialanalysis.ai/models — porównanie modeli AI: benchmarki, ceny, szybkość, jakość

### 📚 RAG
- **RAG Playground** — https://ragplay.vercel.app/experiment — **najlepsza wizualizacja RAG**: chunking, embeddings, semantic search, generowanie w real-time
- **RAG-O-MATIC** — https://rag-o-matic.vercel.app/ — edukacyjne demo RAG z śledzeniem kosztów (unikatowa funkcja!)
- **Neo4j RAG Demo** — https://neo4j.com/labs/genai-ecosystem/rag-demo/ — RAG chatbot na knowledge graph (dokumenty SEC), prawdziwy case

### 💻 Modele lokalne
- **Ollama** — https://ollama.com *(już planowane jako live demo)*
- **WebLLM** — https://webllm.mlc.ai/ — LLM w przeglądarce przez WebGPU! Llama 3, Phi 3, Gemma — bez instalacji, bez serwera. **Świetne jako demo „local model w przeglądarce"**
- **LM Studio** — https://lmstudio.ai — GUI do uruchamiania modeli lokalnie (wymaga pobrania)

### 🔄 Proces ML
- **Teachable Machine (Google)** — https://teachablemachine.withgoogle.com — wytrenuj model ML w przeglądarce w 5 minut (kamera/mikrofon/pliki). 125K+ modeli stworzonych przez użytkowników
- **R2D3: Visual Introduction to ML** — http://www.r2d3.us/visual-intro-to-machine-learning-part-1/ — jedna z najelegantszych wizualizacji ML: animowany scroll-through budowania drzewa decyzyjnego. **Idealna na projektor**
- **ML Playground** — https://mlplaygrounds.com/ — eksperymentuj z algorytmami: SVM, k-NN, drzewa — zmień parametry, obserwuj granice decyzyjne

### 📊 Szybka tabela — Top Pick na live demo

| Temat | Narzędzie | URL |
|-------|-----------|-----|
| Mapa AI | FirstMark MAD Landscape | https://mad.firstmark.com |
| Modele lokalne | WebLLM | https://webllm.mlc.ai/ |
| RAG | RAG Playground | https://ragplay.vercel.app/experiment |
| Sieci neuronowe | Brendan Bycroft's LLM Viz | https://bbycroft.net/llm |
| Generatywna AI | Chatbot Arena | https://lmarena.ai/ |
| Proces ML | Google Teachable Machine | https://teachablemachine.withgoogle.com/ |

---

## 📝 Notatki po warsztacie

*(Uzupełnij po przeprowadzeniu:)*

- Średnia dokładność ręczna grupy: ___/10
- Najczęściej mylone zgłoszenie: ___
- Najciekawsze pytanie uczestnika: ___
- Co zmienić na następny raz: ___
