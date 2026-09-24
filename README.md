# KnowledgeShare

KnowledgeShare is a polished, dependency-free visual gallery for learning software, data, and AI. Each banner groups related supplied reference sheets into one field guide. Opening a banner shows the original KnowledgeShare visual, readable takeaways, every full-frame local page, and one grouped multi-page PDF.

## Run locally

From the repository root, start any static web server:

```bash
python3 -m http.server 4173
```

Then open [http://localhost:4173](http://localhost:4173).

The app is plain HTML/CSS/JavaScript, so no install or build step is required. Stop the server with `Ctrl+C`.

## Included topics

- APIs & testing
- Prompt systems
- Math & probability
- Machine learning
- Python & data analysis
- SQL & data systems
- Deep learning
- LLMs & generative AI
- RAG & agents
- Computer vision
- MLOps
- AI learning paths

Cards can be filtered by theme and opened with a mouse, `Enter`, or `Space` for a detailed, readable explainer view.

Each detail view includes an **Open grouped PDF** link. The local previews and PDFs are generated from one copy of each distinct attachment, with the small MLTut mark reconstructed from adjacent pixels rather than hidden behind a white rectangle. Pages keep their source aspect ratio and dimensions, so no diagram, footer, or edge is cropped.

## Rebuilding the reference library

The generated files are committed under `assets/reference/`. If the supplied attachments are available locally, the library can be regenerated with Pillow:

```bash
python3 generate_reference_assets.py /path/to/attachments
```

The script removes duplicate attachment copies, groups related sheets, writes full-frame JPEG previews, creates multi-page PDFs, and updates `assets/reference/catalog.json`.

## Deploy to Vercel

This is a static site and needs no build command, framework preset, or environment variables.

### Vercel dashboard

1. Import this GitHub repository into Vercel.
2. Keep the detected framework as **Other**.
3. Leave **Build Command** empty.
4. Leave **Output Directory** empty (the repository root is the site root).
5. Deploy.

The included `vercel.json` keeps clean URLs enabled and disables trailing slashes. The app and all reference images/PDFs are served directly from the repository.

### Vercel CLI

After installing and authenticating the Vercel CLI, run from the repository root:

```bash
vercel
```
