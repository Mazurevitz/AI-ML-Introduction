
# 🦙 Ollama Live Demo — Trainer Guide

**When:** Day 1, after "Modele lokalne" slides
**Time:** ~20-25 minutes
**What you need:** Laptop with Ollama installed, projector, internet (for first pull only)

---

## ✅ Before the session (do this the night before!)

```bash
# Install Ollama (macOS)
brew install ollama

# Start the service
ollama serve

# Pre-download models (this takes time — do it before the workshop!)
ollama pull gemma3:4b          # 3.3 GB — small, fast, good quality, supports vision (images!)
ollama pull phi4-mini           # 2.5 GB — Microsoft, same family as in our notebook

# Verify everything is ready
ollama list
```

**Checklist:**
- [ ] Ollama running (`ollama list` works)
- [ ] 2 models downloaded
- [ ] Terminal font size large enough for projector (⌘+ to zoom)
- [ ] A test image saved on desktop (for vision demo)
- [ ] This guide open on second screen

---

## Demo 1: First Contact (~3 min)

> **What to say:** *"Zobaczmy jak wygląda uruchomienie modelu AI na naszym komputerze. Zero chmury, zero API, zero opłat."*

```bash
ollama run gemma3:4b
```

Wait for the `>>>` prompt, then type:

```
What is machine learning? Answer in 2 sentences.
```

> **Point out:** *"Ten model ma 4 miliardy parametrów i działa na moim laptopie. Odpowiedź generuje się lokalnie — nic nie wychodzi do internetu."*

Then try Polish:

```
Wyjaśnij czym jest sztuczna inteligencja w 3 zdaniach, prostym językiem.
```

> **Point out:** *"Model rozumie polski, mimo że był trenowany głównie na angielskim. To siła dużych modeli językowych."*

Type `/bye` to exit.

---

## Demo 2: IT Ticket Classifier (~5 min)

> **What to say:** *"Pamiętacie nasze ćwiczenie z klasyfikacją zgłoszeń IT? Zróbmy to samo, ale z modelem lokalnym."*

```bash
ollama run gemma3:4b
```

Paste this prompt:

```
You are an IT helpdesk classifier. Classify each ticket into exactly one category: Hardware, Network, Software, Account.

Reply with ONLY the category name for each ticket.

1. Drukarka nie drukuje
2. VPN nie łączy się z siecią firmową
3. Aplikacja CRM zawiesza się po aktualizacji
4. Nie mogę się zalogować do poczty
5. Drukarka sieciowa nie odpowiada
```

> **Wait for response, then ask the group:** *"Zgłoszenie 5 — drukarka sieciowa. Model powiedział Hardware czy Network? Dlaczego? Pamiętacie, jak w ćwiczeniu RAG dodanie dokumentacji zmieniło odpowiedź?"*

Now paste the RAG version — same tickets but WITH context:

```
You are an IT helpdesk classifier. Use the following internal documentation to classify tickets.

DOCUMENTATION:
- Network printers: if a printer connected via IP/WiFi is not responding, the issue is the network connection. Classify as: Network.
- WiFi login issues: this is a wireless connection problem, not an account issue. Classify as: Network.
- Password changes in any application (ERP, CRM): root cause is account management. Classify as: Account.

Now classify these tickets (reply with ONLY the category for each):
1. Drukarka sieciowa nie odpowiada
2. Nie mogę zalogować się do sieci WiFi
3. System ERP nie pozwala na zmianę hasła
```

> **Point out:** *"Z dokumentacją model zmienił odpowiedzi. To jest dokładnie to, co robi RAG — dajemy modelowi kontekst, żeby podejmował lepsze decyzje. I to wszystko dzieje się lokalnie, na naszym komputerze."*

Type `/bye` to exit.

---

## Demo 3: System Prompt — Building a Specialist (~3 min)

> **What to say:** *"A co jeśli chcemy, żeby model ZAWSZE zachowywał się jak nasz specjalista IT?"*

```bash
ollama run gemma3:4b
```

First, set the system prompt:

```
/set system You are a senior IT support specialist at a Polish corporation. You always respond in Polish. You are precise, professional, and always suggest a specific next step. You classify issues into: Sprzęt, Sieć, Oprogramowanie, Konto.
```

Now just type tickets naturally, one by one:

```
Monitor migocze i komputer się wyłącza
```

```
Brak dostępu do folderu po zmianie hasła
```

```
Aplikacja zamyka się po aktualizacji
```

> **Point out:** *"Zauważcie — nie musimy za każdym razem powtarzać instrukcji. System prompt to 'osobowość' modelu. W produkcji to jest dokładnie tak skonfigurowane — użytkownik pisze krótko, a model wie co robić."*

Type `/bye` to exit.

---

## Demo 4: Temperature — Creativity Dial (~3 min)

> **What to say:** *"Modele mają parametr 'temperature' — im wyższy, tym bardziej kreatywny (ale mniej przewidywalny). Zobaczmy różnicę."*

```bash
ollama run gemma3:4b
```

Set temperature to 0 (deterministic):

```
/set parameter temperature 0
```

Ask:

```
Write a one-sentence company slogan for an IT helpdesk.
```

Run it 3 times (press up arrow to repeat). **The answer should be identical each time.**

> **Point out:** *"Temperature 0 = ten sam wynik za każdym razem. Idealne do klasyfikacji, raportów, danych."*

Now crank it up:

```
/set parameter temperature 1.5
```

Ask the same question 3 times. **Answers will be wildly different each time.**

> **Point out:** *"Temperature 1.5 = kreatywność na maksa. Dobre do burzy mózgów, storytellingu. Złe do klasyfikacji — model 'fantazjuje'."*

Type `/bye` to exit.

---

## Demo 5: Model Size Comparison (~4 min)

> **What to say:** *"Czy większy model = lepszy? Porównajmy dwa modele na tym samym zadaniu."*

Run the small model first:

```bash
ollama run phi4-mini "Explain what RAG (Retrieval-Augmented Generation) is. Use a simple analogy. Max 3 sentences."
```

Then the medium model:

```bash
ollama run gemma3:4b "Explain what RAG (Retrieval-Augmented Generation) is. Use a simple analogy. Max 3 sentences."
```

> **Point out:**
> - *"Zauważcie różnicę w szybkości — mniejszy model odpowiada szybciej"*
> - *"A jakość? Czasem mniejszy model daje wystarczająco dobrą odpowiedź"*
> - *"To jest trade-off: szybkość i koszt vs jakość. W produkcji dobieramy model do zadania."*

**Pro tip:** Run with `/set verbose` first to show tokens/second stats — participants love seeing the numbers.

---

## Demo 6: Vision — Model That Sees (~5 min)

> **What to say:** *"Gemma 3 to model multimodalny — nie tylko czyta tekst, ale też widzi obrazy. Ten sam model, który klasyfikował zgłoszenia, potrafi analizować zdjęcia."*

**Gemma 3 4B already supports vision** — no extra model needed!

### Prepare these images before the session (save to Desktop):

1. **Screenshot of an error message** — Blue Screen, Python traceback, app crash
2. **Photo of handwritten notes or whiteboard** — write a few bullet points during the break
3. **Screenshot of confusion matrix** from the notebook exercise
4. **Photo of a document** — invoice, form, table

```bash
ollama run gemma3:4b
```

**Example A: Read an error message**

```
What error is shown and how to fix it? /Users/macmini/Desktop/error_screenshot.png
```

> **Say:** *"Pracownik robi screenshot błędu, wysyła do bota, bot analizuje i sugeruje rozwiązanie."*

**Example B: Read handwritten text**

```
Read the handwritten text in this image and type it out: /Users/macmini/Desktop/whiteboard_photo.jpg
```

> **Say:** *"Notatki ze spotkania, rysunki na tablicy — model czyta pismo odręczne."*

**Example C: Analyze a chart**

```
Describe this chart. What does it show? Which categories get confused? /Users/macmini/Desktop/confusion_matrix.png
```

> **Say:** *"Nie tylko opisuje, ale interpretuje dane. Rozpoznał macierz pomyłek i wskazał problematyczne kategorie."*

**Example D: Extract data from a document**

```
Extract all key information from this document — dates, amounts, names: /Users/macmini/Desktop/invoice.jpg
```

> **Say:** *"OCR + ekstrakcja danych w jednym kroku. Faktura, formularz, umowa — lokalnie, prywatnie, za darmo."*

> **Point out:** *"Jeden model — Gemma 3, 3 GB — tekst, klasyfikacja, obrazy, dokumenty. Wszystko na laptopie."*

Type `/bye` to exit.

---

## Demo 7: API — For Developers (~3 min, optional)

> **What to say:** *"Ollama to nie tylko terminal. Ma API, które można podłączyć do dowolnej aplikacji."*

Open a **second terminal** (keep it visible on the projector) and run:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3:4b",
  "prompt": "Classify this IT ticket: Drukarka sieciowa nie odpowiada. Reply with one word: Hardware, Network, Software, or Account.",
  "stream": false
}' | python3 -m json.tool
```

> **Point out:** *"Jeden request HTTP — to wszystko. Możecie to podłączyć do formularza na intranecie, bota na Slacku, systemu ticketowego. Model działa lokalnie, dane nie opuszczają waszej sieci."*

For Python fans, show this one-liner:

```bash
python3 -c "
import requests, json
r = requests.post('http://localhost:11434/api/generate', json={
    'model': 'gemma3:4b',
    'prompt': 'What are 3 benefits of running AI locally?',
    'stream': False
})
print(json.loads(r.text)['response'])
"
```

> **Point out:** *"5 linijek Pythona. Tyle wystarczy, żeby mieć AI w waszej aplikacji."*

---

## Demo 8: Custom Model — Modelfile (~3 min, optional)

> **What to say:** *"Możemy też stworzyć własny model — z nazwą, osobowością i parametrami."*

Create a file on the spot (or have it ready):

```bash
cat << 'EOF' > /tmp/ITBot
FROM gemma3:4b
PARAMETER temperature 0
PARAMETER num_ctx 4096
SYSTEM """You are ITBot, an internal IT helpdesk assistant for a Polish corporation.

Rules:
- Always respond in Polish
- Classify every ticket into: Sprzęt, Sieć, Oprogramowanie, Konto
- Always explain your reasoning in one sentence
- Always suggest one next step
- Be concise and professional"""
EOF

ollama create itbot -f /tmp/ITBot
```

Now run it:

```bash
ollama run itbot
```

Test it:

```
Drukarka sieciowa nie odpowiada po awarii prądu
```

```
Kolega nie może się zalogować po urlopie
```

```
Excel zawiesza się przy dużych plikach
```

> **Point out:** *"Stworzyliście własnego specjalistę IT w 30 sekund. Ma ustawioną temperaturę na 0 (deterministic), zawsze odpowiada po polsku, zawsze klasyfikuje i sugeruje kolejny krok. W firmie można takich 'botów' mieć kilka — do HR, do IT, do finansów."*

Type `/bye` to exit.

---

## Wrap-up — What to say (~1 min)

> *"Podsumujmy co zobaczyliśmy:*
> 1. *Model AI działający 100% lokalnie — zero chmury*
> 2. *Klasyfikacja zgłoszeń — z RAG i bez*
> 3. *System prompt — budowanie specjalisty*
> 4. *Temperature — kontrola kreatywności*
> 5. *Porównanie modeli — mniejszy vs większy*
> 6. *Vision — model, który czyta obrazy*
> 7. *API — integracja z dowolną aplikacją*
> 8. *Modelfile — własny asystent w 30 sekund*
>
> *Wszystko za darmo, na waszym laptopie, bez wysyłania danych do nikogo. To jest przyszłość AI w enterprise."*

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ollama: command not found` | Run `brew install ollama` or download from ollama.com |
| Model downloads during demo | Always `ollama pull` the night before! |
| Slow responses | Close other apps, use smaller model (`phi4-mini`) |
| `Error: model not found` | Check exact name: `ollama list` |
| Vision model won't load image | Use absolute path, check file exists |
| Out of memory | Use smaller model or close Chrome (it eats RAM) |
| API not responding | Run `ollama serve` in another terminal |

---

## 📋 Quick reference card (print this)

```
ollama run gemma3:4b              # Start chatting
ollama run phi4-mini              # Smaller, faster model
ollama run gemma3:4b              # Also does vision (multimodal!)

/set parameter temperature 0      # Deterministic
/set parameter temperature 1.5    # Creative
/set verbose                      # Show speed stats
/bye                              # Exit

ollama list                       # What models do I have?
ollama ps                         # What's running now?

# One-shot (no interactive mode)
ollama run gemma3:4b "Your question here"

# API
curl http://localhost:11434/api/generate -d '{"model":"gemma3:4b","prompt":"Hello","stream":false}'
```
