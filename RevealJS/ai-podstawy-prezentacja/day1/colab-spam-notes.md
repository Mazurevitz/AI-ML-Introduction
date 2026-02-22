
# 🧠 Rozszerzone notatki trenera – Klasyfikator SPAM vs NIE-SPAM

---

## 🔹 Etap 1: Dane treningowe
- Pokazuję bardzo mały zbiór tekstów – 9 przykładów (3 SPAM, 6 NIE-SPAM).
- Wyjaśniam: „To bardzo uproszczony przypadek – idealny do pokazania mechanizmu działania ML.”
- Klasyfikacja binarna: 1 = SPAM, 0 = NIE-SPAM
- Pytanie do grupy: „Czy taki zbiór może być wystarczający?” → dyskusja o wielkości danych

---

## 🔹 Etap 2: CountVectorizer + LogisticRegression

### CountVectorizer:
- Zamienia tekst na liczby – liczy, ile razy każde słowo pojawia się w tekście (bag-of-words).
- Przykład: „win prize” → [1, 1, 0, 0] (czyli obecność słów w słowniku)
- Nie uwzględnia kontekstu, kolejności ani znaczenia słów.

### LogisticRegression:
- Klasyczny model regresji – uczy się granicy między klasami.
- Bazuje na funkcji logistycznej – predykcja to wartość od 0 do 1 (czyli prawdopodobieństwo).
- Działa dobrze przy małych, niezbyt złożonych zbiorach danych.

---

## 🧪 Etap 3: Testowanie własnego tekstu
- Uczestnicy wpisują własne przykłady.
- Omawiam wynik predykcji i wartości prawdopodobieństwa.
- Pokazuję `predict_proba` i tłumaczę, że możemy zmienić próg decyzji (np. 0.6 zamiast domyślnego 0.5).
- Zachęcam do eksperymentów: „Co się stanie, jeśli dodamy słowo ‘free’?”

---

## 🔄 Etap 4: Multinomial Naive Bayes

### Co to jest?
- Model probabilistyczny oparty na teorii Bayesa.
- Zakłada niezależność cech (naiwne założenie – stąd nazwa).
- Zakłada, że dane wejściowe to liczności słów (idealnie pasuje do CountVectorizer).
- Bardzo szybki, dobrze działa przy małych zbiorach i klasyfikacji tekstu.

### Dlaczego działa inaczej niż LogisticRegression?
- LogisticRegression uczy się wag – każdemu słowu przypisuje wartość wpływu na wynik.
- Naive Bayes działa statystycznie – porównuje prawdopodobieństwo wystąpienia słów w obu klasach.
- Może lepiej radzić sobie z rzadkimi słowami i małymi zbiorami.

---

## 🧮 Etap 5: TF-IDF Vectorizer

### Co to jest?
- TF = Term Frequency (ile razy słowo występuje w dokumencie)
- IDF = Inverse Document Frequency (czy słowo jest unikalne w całym zbiorze)
- Działa jak „ważenie” – częste, ale mało informacyjne słowa (np. „the”, „your”, „please”) dostają niższą wagę.

### Co zmienia?
- Zmniejsza wpływ słów, które są zbyt popularne.
- Wzmacnia znaczenie słów specyficznych dla danej klasy.
- Może poprawić jakość modelu, szczególnie gdy dane są duplikaty lub mają spamowe frazy.

---

## 🧠 Etap 6: Ważność cech

- Pokażę, które słowa model uważa za typowe dla SPAM i NIE-SPAM.
- To pierwszy krok do interpretowalności modelu.
- Czasem model wybiera dziwne słowa – np. „download” jako spamowe.
- Pytam grupę: „Co was zaskoczyło w tej liście?”

---

## ✅ Na koniec
- Zachęcam uczestników do zmiany tekstu, dodania nowych przykładów.
- Mogą przetestować różne modele i vectorizery.
- To świetny moment, żeby opowiedzieć o różnicy między „dobrym accuracy” a „dobrym zrozumieniem danych”.
