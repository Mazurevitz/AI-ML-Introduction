
# 🖥️ LM Studio Live Demo — Trainer Guide

**When:** Day 1, after "Modele lokalne" slides (alternative or complement to Ollama demo)
**Time:** ~20 minutes
**What you need:** Laptop with LM Studio installed, projector
**Version:** 0.4.3+ (download from https://lmstudio.ai)

> **Why LM Studio alongside Ollama?** Ollama is command-line — great for developers. LM Studio is GUI — great for everyone else. Showing both demonstrates that local AI is accessible regardless of technical skill.

---

## ✅ Before the session (do this the night before!)

1. Download and install LM Studio from https://lmstudio.ai
2. Open the app, go to **Discover** tab (⌘+2 / Ctrl+2)
3. Download these models:

| Model | Search for | Size | Why |
|-------|-----------|------|-----|
| Gemma 3 4B | `gemma-3-4b` | ~3 GB | Fast, good quality, **already supports vision (images!)** |
| Phi-4 Mini | `phi-4-mini` | ~2.5 GB | Microsoft, same family as notebook exercise |

4. Load Gemma 3 once to verify it works (⌘+L / Ctrl+L)
5. Enable Developer Mode: **Settings** (⌘+, / Ctrl+,) → **Developer** → toggle ON

**Checklist:**
- [ ] LM Studio opens without errors
- [ ] 2 models downloaded (check **My Models** tab)
- [ ] Developer Mode enabled
- [ ] App font/zoom large enough for projector
- [ ] A test image saved on desktop (for vision demo)
- [ ] This guide open on second screen

---

## Keyboard shortcuts cheat sheet

| Action | Mac | Windows/Linux |
|--------|-----|---------------|
| Discover tab | ⌘+2 | Ctrl+2 |
| Load model | ⌘+L | Ctrl+L |
| New chat | ⌘+N | Ctrl+N |
| Settings | ⌘+, | Ctrl+, |
| Search models | ⌘+Shift+M | Ctrl+Shift+M |

---

## Demo 1: First Impression — Download & Chat (~4 min)

> **What to say:** *"LM Studio to aplikacja desktopowa do uruchamiania modeli AI lokalnie. Bez terminala, bez kodu, bez chmury. Zobaczmy jak to wygląda."*

### Step by step:

**1. Show the Discover tab**
- Click **Discover** in the left sidebar (or ⌘+2)
- Point at the search bar and model cards

> **Say:** *"To jest jak 'sklep z modelami'. Tysiące modeli open-source z Hugging Face, gotowych do pobrania jednym kliknięciem."*

**2. Show a model is already downloaded**
- Click **My Models** in the sidebar
- Point at the downloaded models, their sizes, and format columns

> **Say:** *"Tu widzimy nasze pobrane modele. Gemma 3 od Google, 4 miliardy parametrów, waży 3 GB. Dla porównania — ChatGPT ma setki miliardów parametrów i działa na serwerowni. Ten działa na moim laptopie."*

**3. Load the model**
- Press ⌘+L (or Ctrl+L) to open the model loader
- Select **Gemma 3 4B**
- Click **Load**
- Wait a few seconds (RAM allocation)

> **Say:** *"Ładowanie = alokacja pamięci RAM. Model zajmuje ~3 GB pamięci. Dlatego potrzebujemy minimum 16 GB RAM do wygodnej pracy."*

**4. Chat!**
- The **Chat** tab activates automatically
- Type:

```
What is machine learning? Answer in 2 sentences.
```

- Wait for the response, then try Polish:

```
Wyjaśnij czym jest sztuczna inteligencja. 3 zdania, prosty język.
```

> **Point out:** *"Odpowiedź generuje się lokalnie. Żadne dane nie wychodzą z tego komputera. Zobaczcie szybkość — tokeny na sekundę widać na dole okna."*

---

## Demo 2: IT Ticket Classification (~4 min)

> **What to say:** *"Użyjmy tego modelu do naszego zadania z klasyfikacją zgłoszeń IT."*

### Step by step:

**1. Start a new chat** (⌘+N / Ctrl+N)

**2. Set the system prompt**
- Look for the **System Prompt** field at the top of the chat (above the message input)
- Click on it and type:

```
You are an IT helpdesk classifier. Classify each ticket into exactly one category: Hardware, Network, Software, Account. Reply with ONLY the category name.
```

**3. Send test tickets**

Type:

```
1. Drukarka nie drukuje
2. VPN nie łączy się z siecią firmową
3. Aplikacja CRM zawiesza się po aktualizacji
4. Nie mogę się zalogować do poczty
5. Drukarka sieciowa nie odpowiada
```

> **Ask the group:** *"Zgłoszenie 5 — drukarka sieciowa. Co powiedział model? Hardware? Pamiętacie z ćwiczenia RAG, że poprawna odpowiedź to Network?"*

**4. Now add RAG context**

Start another new chat (⌘+N), set this system prompt:

```
You are an IT helpdesk classifier. Use ONLY these rules:
- Network printers (connected via IP/WiFi): classify as Network
- WiFi login issues: classify as Network (not Account)
- Password changes in any app (ERP, CRM): classify as Account

Classify each ticket into: Hardware, Network, Software, Account. Reply with ONLY the category.
```

Paste the same 5 tickets again.

> **Point out:** *"Z kontekstem model zmienił odpowiedź dla drukarki sieciowej. To jest RAG w praktyce — dokładnie to, co robiliśmy w notebooku, ale tutaj w GUI, bez linijki kodu."*

---

## Demo 3: Split View — Model Comparison (~3 min)

> **What to say:** *"LM Studio ma jedną unikalną funkcję: porównanie modeli side-by-side."*

### Step by step:

**1. Load a second model**
- Press ⌘+L / Ctrl+L
- Select **Phi-4 Mini** and load it
- Now you have two models loaded

**2. Open Split View**
- You should have two chat tabs open
- Drag one tab to the right side of the window — the screen splits in two
- In the left chat, select **Gemma 3 4B** from the model dropdown
- In the right chat, select **Phi-4 Mini** from the model dropdown

**3. Ask the same question in both**

Type in both:

```
Explain RAG (Retrieval-Augmented Generation) in 3 sentences. Use a simple analogy.
```

> **Point out:**
> - *"Dwa modele, to samo pytanie, odpowiedzi obok siebie"*
> - *"Zobaczcie różnicę w jakości, stylu, szybkości"*
> - *"W firmie tak testujecie, który model najlepiej pasuje do waszego zadania"*

---

## Demo 4: Temperature — Creativity Dial (~3 min)

> **What to say:** *"Pokażmy jak parametr temperature wpływa na odpowiedzi."*

### Step by step:

**1. Open the inference settings**
- In the right sidebar of the Chat tab, find the parameter controls
- Look for **Temperature** slider

**2. Set Temperature to 0**
- Drag the slider to 0 (or type 0)
- Ask:

```
Write a one-sentence slogan for an IT helpdesk.
```

- Send it 3 times (copy-paste). **Answers should be identical.**

> **Say:** *"Temperature 0 = ten sam wynik za każdym razem. Deterministyczne. Idealne do klasyfikacji."*

**3. Set Temperature to 1.5**
- Drag the slider to 1.5
- Send the same question 3 times. **Answers will be wildly different.**

> **Say:** *"Temperature 1.5 = pełna kreatywność. Dobre do burzy mózgów. Złe do klasyfikacji."*

**4. Show other parameters** (just point, don't change)
- **Top P** — nucleus sampling
- **Max Tokens** — response length limit
- **Context Length** — how much conversation the model remembers

> **Say:** *"Każdy z tych parametrów wpływa na zachowanie modelu. W produkcji ustawiamy je raz i zapisujemy jako preset."*

---

## Demo 5: Document Chat — Built-in RAG (~3 min)

> **What to say:** *"LM Studio ma wbudowany RAG. Możemy przeciągnąć dokument do chatu i model będzie odpowiadał na jego podstawie."*

### Step by step:

**1. Prepare a document**

Before the demo, save this as a `.txt` file on your desktop (e.g., `it_procedures.txt`):

```
IT HELPDESK PROCEDURES

Network printers: If a printer connected via IP or WiFi is not responding,
the issue is the network connection. Classify as: Network.
If the printer physically does not react (LEDs off, no paper feed) → Hardware.

WiFi login problems: This is a wireless connection problem, not an account
issue. Classify as: Network.

Password changes in applications: Even if the ticket mentions a specific app
(ERP, CRM), the root cause is account management. Classify as: Account.

Access issues after password change: The account needs Active Directory
synchronization. Root cause: password change. Classify as: Account.
```

**2. Start a new chat** (⌘+N)

**3. Drag the file into the chat window**
- Drag `it_procedures.txt` from your desktop into the LM Studio chat
- The file icon appears, confirming the document is attached

**4. Ask a question about the document**

```
Based on the attached procedures, how should I classify: "Network printer is not responding"?
```

> **Point out:** *"Model przeczytał dokument i odpowiedział na jego podstawie. To jest RAG — ale bez pisania ani jednej linijki kodu. Przeciągnij dokument, zadaj pytanie, gotowe."*

**5. Try another question**

```
A user reports: "I can't access shared folders after changing my password." What category and why?
```

> **Say:** *"Wyobraźcie sobie: wrzucacie do chatu wasz wewnętrzny regulamin, procedury, FAQ — i model odpowiada na pytania pracowników. Lokalnie, prywatnie, za darmo."*

---

## Demo 6: Vision — Model That Sees (~5 min)

> **What to say:** *"Gemma 3 to model multimodalny — nie tylko czyta tekst, ale też widzi obrazy. Nie potrzebujemy osobnego modelu. Zobaczmy."*

**Gemma 3 4B already supports vision** — no extra model needed!

### Prepare these images before the session (save to Desktop):

1. **Screenshot of an error message** — any Blue Screen, Python traceback, or app crash dialog
2. **Photo of a handwritten note or whiteboard** — write a few bullet points during the break
3. **Screenshot of the confusion matrix** from the notebook exercise (after running Part 2)
4. **Photo of a business document** — invoice, table, or form (can be blurred/dummy)

### Step by step:

**1. Make sure Gemma 3 4B is loaded** (it should still be from earlier demos)

**2. Start a new chat** (⌘+N)

**3. Example A: Read an error message**
- Drag a screenshot of an error dialog/traceback into the chat
- Type:

```
What error is shown? What is the likely cause and how would you fix it?
```

> **Say:** *"Wyobraźcie sobie: pracownik robi screenshot błędu, wrzuca do helpdesk bota, bot od razu analizuje i sugeruje rozwiązanie. Bez opisywania problemu słowami."*

**4. Example B: Read a handwritten note**
- Drag a photo of handwritten text (whiteboard, sticky note, notebook page)
- Type:

```
Read the handwritten text in this image and type it out.
```

> **Say:** *"Model czyta pismo odręczne. Notatki ze spotkania, rysunki na tablicy, odręczne formularze — wszystko można zdigitalizować lokalnie."*

**5. Example C: Analyze a chart or table**
- Drag the confusion matrix screenshot from the notebook
- Type:

```
Describe this chart. What does it show? Which categories are most confused with each other?
```

> **Say:** *"Model nie tylko opisuje co widzi, ale interpretuje dane. Zobaczcie — rozpoznał, że to macierz pomyłek i wskazał, które kategorie się mylą."*

**6. Example D: Read a document/invoice**
- Drag a photo of any printed document (invoice, form, table)
- Type:

```
Extract all key information from this document: dates, amounts, names, reference numbers.
```

> **Say:** *"OCR + ekstrakcja danych w jednym kroku. Lokalnie, prywatnie. Idealne do faktur, umów, formularzy — żadne dane nie opuszczają waszego komputera."*

> **Point out:** *"Jeden model — Gemma 3, 3 GB — czyta tekst, klasyfikuje zgłoszenia, analizuje obrazy, wyciąga dane z dokumentów. Wszystko na laptopie."*

---

## Demo 7: Local Server — API for Developers (~2 min, optional)

> **What to say:** *"Dla deweloperów: LM Studio działa też jako serwer API, kompatybilny z OpenAI."*

### Step by step:

**1. Go to the Developer tab** in the sidebar

**2. Start the server**
- The local server panel shows the endpoint: `http://localhost:1234`
- Toggle the server ON

**3. Show the API call** (open a terminal next to LM Studio)

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-4b",
    "messages": [
      {"role": "system", "content": "Classify IT tickets into: Hardware, Network, Software, Account."},
      {"role": "user", "content": "Network printer is not responding"}
    ]
  }'
```

> **Point out:** *"API kompatybilne z OpenAI. Jeśli macie aplikację, która używa ChatGPT API, wystarczy zmienić URL na localhost:1234 i działa z modelem lokalnym. Zero zmian w kodzie."*

---

## Wrap-up — LM Studio vs Ollama (~1 min)

> **Show this comparison:**

| | **LM Studio** | **Ollama** |
|---|---|---|
| Interface | GUI (click) | CLI (terminal) |
| For whom | Everyone | Developers |
| Model comparison | Split View side-by-side | Manual switching |
| Built-in RAG | Drag & drop documents | Requires code |
| Vision | Drag & drop images | CLI path to file |
| API | OpenAI-compatible, 1 click | OpenAI-compatible, `ollama serve` |
| Custom models | GUI settings | Modelfile |
| Server/headless | llmster | ollama serve |

> **Say:** *"Oba narzędzia robią to samo — uruchamiają modele lokalnie. LM Studio to Swiss Army knife z GUI. Ollama to skalpel dla deweloperów. Wybierz to, co pasuje do twojego zespołu."*

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| Model won't load | Check RAM — close other apps. Unload previous model first |
| Slow responses | Use smaller model or reduce context length |
| App crashes on load | Model too large for available RAM. Try a smaller quantization (Q4 instead of Q8) |
| Split View not working | Drag the tab — don't just click. Grab the tab header and pull to the edge |
| Document RAG not working | Check file format — TXT, PDF, DOCX supported. Very large files may be slow |
| Vision not working | Make sure you loaded Gemma 3 (multimodal). Phi-4 Mini does NOT support images |
| Server won't start | Check if port 1234 is free. Or change port in Developer settings |
| "No models found" | Go to Discover tab, download at least one model |

---

## 📋 Quick demo flow (if short on time — 10 min version)

| Time | Demo | Key moment |
|------|------|------------|
| 0:00 | Show Discover tab + My Models | "Thousands of free models" |
| 1:00 | Load model, chat in Polish | "Runs on your laptop" |
| 3:00 | IT ticket classification | Connects to notebook exercise |
| 5:00 | Drag document into chat | "RAG without code" |
| 7:00 | Split View comparison | Side-by-side wow |
| 9:00 | Show API endpoint | "Drop-in OpenAI replacement" |
