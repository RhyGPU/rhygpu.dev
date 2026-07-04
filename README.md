# rhygpu.dev

rhygpu.dev is the public portfolio and development archive for RhyGPU projects. It turns project repos, devlogs, screenshots, and build history into a layered reader path: homepage, project case studies, development journal, and profile pages.

This repo is a static Astro site. It is not just a generic personal homepage; it is the portfolio hub, case-study site, devlog surface, and meta-build archive for RhyGPU work.

## Links

- Live site: [https://rhygpu.dev/](https://rhygpu.dev/)
- Projects: [https://rhygpu.dev/projects/](https://rhygpu.dev/projects/)
- Devlog: [https://rhygpu.dev/devlog/](https://rhygpu.dev/devlog/)
- About: [https://rhygpu.dev/about/](https://rhygpu.dev/about/)
- Resume: [https://rhygpu.dev/resume/](https://rhygpu.dev/resume/)

## Site Structure

- `/` - portfolio hub and entry point.
- `/projects/` - project index.
- `/projects/mnemosyne/` - Mnemosyne case study.
- `/projects/omniplanner/` - OmniPlanner case study.
- `/projects/pythagorean-harmony/` - Pythagorean Harmony case study.
- `/projects/rhygpu-dev/` - rhygpu.dev case study.
- `/devlog/` - development journal and archive.
- `/about/` - profile and background.
- `/resume/` - resume page.
- `/contact/` - contact page.

## Project Model

Project case studies live in `src/content/projects/`. Devlog entries live in `src/content/devlogs/`.

Project metadata can include:

- `repo` - enables the repository CTA when present.
- `devlog` - enables the devlog CTA when present.
- `devlogLabel` - controls the devlog CTA label text.
- `media` - screenshots, diagrams, and other project visuals.
- `proofNotes` - implementation notes, evidence, or source-status notes.
- `architecture` - system structure, technical model, or design notes.

Project CTAs are metadata-driven: repo links appear only when `repo` exists, devlog links appear only when `devlog` exists, and `devlogLabel` controls the displayed label.

## Current Project Pages

- Mnemosyne - flagship local-first AI memory architecture.
- OmniPlanner - desktop-first planning workspace.
- Pythagorean Harmony - equation-duel combat prototype; source currently private while the prototype is cleaned up.
- rhygpu.dev - portfolio system, devlog hub, and meta-build archive.

## Development

Install dependencies:

```bash
npm install
```

Start the local development server:

```bash
npm run dev
```

Build the site:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

Keep generated and local-only folders untracked:

- `node_modules/`
- `dist/`
- `.astro/`
- `.claude/`

The screenshots under `public/projects/*` are intentionally tracked because the project pages depend on them as portfolio evidence.

The `rhygpu.dev chat log/` folder is intentionally tracked as archive/source material when present. It preserves build-session context used to shape the devlog and meta-project history.
