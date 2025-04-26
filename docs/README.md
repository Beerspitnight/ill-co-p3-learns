# 🎨 ill-Co-P3-Learns  
_Tag it, teach it, train it — or at least try to._

> “We were gonna train an AI on design principles… but then we realized we know nothing about design or graphics.”  
> — Probably BeerSpit, Somewhere Around Week 53

---

## 🤖 What Is This?

This is **ill-Co-P3-Learns** — the lovable, chaotic sibling of your pristine design school notes and your messy bookmarks folder. It's an attempt to teach a machine 🧠 how to *see* design. Like, really *see* it. With context. With captions. With just enough judgment to say: “Yikes, that spacing is a crime.”

At its core, this is:

- A 🗂️ **dataset curation tool** for pairing images + captions  
- A 🔧 **Streamlit tagging UI** with Firebase auto-save (no Submit button here, folks 🙅‍♂️)  
- A 📚 **book enrichment pipeline** for collecting full-text design knowledge  
- A ✨ slightly neurotic, slightly brilliant system to build AI training data — with taste

---

## 🧱 Project Structure (The IKEA Manual We Actually Read)

```
ill-co-p3.2/
├── learning_app/
│   ├── data/                  ← all raw stuff (images, html)
│   ├── output/                ← all processed stuff (tags, books, exports)
│   │   ├── books_enriched/
│   │   ├── pairs/
│   │   │   ├── combined_pairs.json
│   │   │   ├── tagged_results.json
│   │   │   ├── image_urls.json
│   │   │   └── html_extracted_pairs_labeled.json
│   ├── scripts/               ← all Python brains
│   ├── styles/                ← CSS (yes we care)
│   ├── utils/                 ← helpers, prompts, etc.
│   └── templates/             ← HTML, SVGs, and dreams
└── secrets/                   ← shhh 🤫
```

---

## 🧩 The Pipeline (Or: How a JPEG Becomes Wisdom)

1. 🖼️ **Image + Caption Extraction**  
   → From PDFs or HTML or even psychic intent.  
   → Output: `html_extracted_pairs_labeled.json`

2. 💬 **AI Labeling (Optional)**  
   → We run GPT-3.5 on your pairs and get confident, yet suspiciously poetic tags.

3. 🧑‍🎨 **Tagging UI**  
   → Built with Streamlit. Firebase handles your login, tags, and judgment.  
   → Elements? Principles? Notes? Flags? You bet.  
   → Output: Saved to Firebase in real-time + exportable as CSV or JSON

4. 📚 **Book Enrichment**  
   → Google Books + OpenLibrary. ISBN-first. Full text preferred.  
   → Output: `output/books_enriched/*.json`

5. 🧾 **Exports for Training**  
   → Get your beautiful mess into `tagged_results_export.json` and `.csv`  
   → Optional: Sort, clean, rinse, repeat.

---

## 🧠 Tagging Philosophy

We’re not just labeling images. We’re whispering ancient truths into the ears of a baby AI 👶.

### You Can Tag:
- 🟠 **Primary/Secondary Elements** — line, shape, color, etc.
- 🔵 **Primary/Secondary Principles** — balance, contrast, unity, etc.
- 🟡 **Flag It** — blurry, watermark, weird cropping, offensive, reject
- 📝 **Leave Notes** — "this feels off" is a valid input

---

## 🧪 Scripts You Might Love (or Fear)

| Script | What It Does | Status |
|-------|---------------|--------|
| `extract_images.py` | Slices PDFs into image pages | ✅ Working |
| `match_text_image.py` | Marries image + caption | ✅ Working |
| `extract_from_html.py` | Finds juicy image-caption HTML pairs | ✅ Working |
| `suggest_labels_gpt.py` | GPT guesser on design principle | ✅ Working |
| `export_firebase_tags.py` | Turns Firebase chaos into clean CSV | ✅ Working |
| `bulk_enrich_books.py` | Pulls full text & metadata from APIs | 🚧 In Progress |
| `dataset_interface2.py` | Your main UI for tagging | ✅ Glorious |
| `firebase_service.py` | The Firebase whisperer | ✅ Fully synced |
| `auth.py` | Email/password login with Firebase | ✅ Locked + loaded |

---

## 🧠 Dataset Topics (Text, Images, Structure)

According to the plan BeerSpt made at 3am with big 😴💭, 🌲🌬️, and too much ☕:

- **Text:** Theory, tools, tutorials, typography, workflows, design manifestos
- **Images:** Logos, posters, UI mockups, redesigns, style guides
- **Structure:** Font metadata, color palettes, design project tags

📦 BeerSpit is aiming for 10k–100k pairs.  
🏆 Bonus points if your AI can explain why Helvetica doesn’t solve everything.

---

## 🌐 API Endpoints (For the Overachievers)

You also built a local API, because you like your data like your coffee — piped straight to terminal:

- `/search_books?query=design+principles`
- `/batch_search?file=search_terms.csv&source=both`
- `/extract_full_text?book_limit=50`
- `/list_results` ← We all forget what we did last night

More in `ILL-CO-P3 API Documentation.docx` — it’s documented so you don’t have to remember.

---

## 📤 Deployment Notes

This project runs beautifully on:
- ✅ Your local Streamlit dev server (`streamlit run main_learns.py`)
- ✅ Streamlit Cloud (because you did the secrets setup 💪)
- ⛔ Heroku (we don’t speak of Heroku)

---

## 🚧 Known Quirks

- Auto-save = magic 🪄 but sometimes confusing. Tags save instantly. No undo (yet).
- The UI has a glow-up pending — you’ll get there.
- GPT will sometimes hallucinate 🌲🌬️. Like us all.
- The README author is also the project lead, UI designer, dev, QA tester, and midnight bug fixer. So, manage expectations 🤷‍♂️

---

## 💡 Future Dreams

- [ ] Filtering logic in UI (only untagged? only lines? only chaos?)
- [ ] GPT fine-tuning round 1
- [ ] Beautiful backups with timestamps like a proud parent
- [ ] Datasets merged, labeled, exported, published
- [ ] AI that critiques your Canva post with love and clarity

---

## 📬 Contact (aka: Scream Into the Firebase Void)

- GitHub: [@Beerspitnight](https://github.com/Beerspitnight)
- Email: [illco.p.learning@gmail.com](mailto:illco.p.learning@gmail.com)
- Twitter: [@ill_co_p3](https://twitter.com/ill_co_p3)
- Playlist that started it all: [Killer Design Playlist](https://open.spotify.com/playlist/4NgWuA0aWDaKxbKMwWnl8r)

---

## 🖤 Final Words

This isn't just a dataset.

It's a manifesto in JSON.
A design bootcamp run by ghosts.
A collaborative meditation on good taste.
A 💀 of a project you're probably gonna finish.

Thanks for tagging. Thanks for teaching. Thanks for making the internet just a little more beautiful.

— *ill-Co-P3-Learns Team (mostly you + a lot of caffeine)*