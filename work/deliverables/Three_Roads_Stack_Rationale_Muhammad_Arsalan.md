# Three Roads: Choose Your Stack with AI — Muhammad Arsalan

**Track:** General AI Fluency (Build Phase) — Week 4  
**Assignment:** Three Roads: Choose Your Stack with AI  
**Role:** Applied AI & ML Engineer  
**Live Site Proof:** [https://arslanflyrankweb1.netlify.app/](https://arslanflyrankweb1.netlify.app/)  
**GitHub Repository:** [https://github.com/24pwai0015-max/flyrank-ml-muhammad-arsalan](https://github.com/24pwai0015-max/flyrank-ml-muhammad-arsalan)  

---

## 1. The Four Constraints (Input to AI)

Before asking AI for stack recommendations, I fed it my actual project constraints rather than asking for a generic suggestion:

1. **Free Only:** Absolute $0 budget for domain, hosting, CI/CD, and tooling. Must remain free permanently without trial expirations.
2. **Honest Skill Level:** 4th-semester AI student. Proficient in Python, machine learning algorithms, OpenCV, and mathematical modeling; beginner in web frontend; comfortable writing plain HTML/CSS and using Git, but want to avoid spending two weeks debugging npm package conflicts or webpack configs.
3. **What the Portfolio Must Do (Content Map Alignment):**
   - 4-page structure (`Home`, `Work`, `About`, `Contact`).
   - Host 3 distinct case studies with the three-beat narrative (*Setup*, *Catch*, *Consequence*):
     1. **FlyRank ML Search Intelligence & Content Refresh** (Flagship ranking model, Precision@50, client-holdout validation).
     2. **AI Attendance System** (Computer vision, OpenCV, Streamlit UI, hardware-software integration).
     3. **Delivery Time Prediction** (Multi-variable regression, Random Forest vs XGBoost vs Linear Regression).
   - Global sticky CTA laddering up to one target action: **Book a 15-minute intro call** or **send an email**.
4. **How My Work Must Be Displayed:**
   - Real SVG pipeline benchmark charts and class distribution diagrams.
   - High-contrast code snippets with `JetBrains Mono` formatting.
   - Streamlit application screen captures and live Google Colab badges.
   - An interactive 3D WebGL element that shows technical polish without slowing down page load times.
5. **Dynamic at Launch?**
   - **No.** An embedded Calendly widget and direct email `mailto:` link completely fulfill user communication without needing a custom database, authentication, or server backend.

---

## 2. The Three Stack Options Evaluated (Simplest to Most Powerful)

```
[Road 1: No-Code]           [Road 2: Plain Code + AI]           [Road 3: Full JS Framework]
  (Carrd / Framer)            (HTML5 / CSS / Netlify)             (Next.js / Astro / Vercel)
         │                               │                                    │
  Simplest road                   The Sweet Spot                     Most powerful
  No code written                 Zero dependencies                  High complexity
  Trapped in builder              Complete ownership                 Overkill for 4 pages
                                  ★ CHOSEN ROAD ★
```

---

### Road 1: No-Code Builder (Simplest)
- **How I Would Build It:** Use a visual drag-and-drop platform like Carrd or Framer. Select a template, customize typography, and drag elements into place.
- **Where I Would Host (Free):** Carrd free tier (`.carrd.co` subdomain) or Framer free tier.
- **Does It Need a Backend?** No. Forms and hosting are handled natively by the builder.
- **How Well It Shows ML Work:** Mediocre. It works well for visual design portfolios (fashion, photography), but feels awkward for technical ML portfolios. Embedding Google Colab badges, rendering responsive SVG data charts, and linking local GitHub repositories feels artificial and clunky.
- **The Real Trade-Off:** **Lack of technical credibility.** A hiring manager or researcher evaluating an Applied AI & ML Engineer wants to see that the candidate understands code, version control, and web standards. Using a no-code drag-and-drop builder signals that the engineer cannot deploy a simple web page. Furthermore, free tiers enforce branded badges ("Made with Carrd") and restrict custom scripts.

---

### Road 2: Plain Code with AI on Free Host (The Sweet Spot — CHOSEN)
- **How I Would Build It:** Write semantic HTML5, modern CSS custom properties (`:root`), and lightweight vanilla JavaScript (including Three.js via CDN for interactive 3D WebGL animations). Pair with an AI assistant to write clean, modular markup.
- **Where I Would Host (Free):** **Netlify** (via Netlify Drop or Git CI) and **GitHub Pages**.
- **Does It Need a Backend?** **Not yet.** Form submissions can be handled with a direct `mailto:` link or a 1-line Netlify Forms attribute (`<form netlify>`). Appointments are handled via an embedded Calendly link. Zero backend servers required.
- **How Well It Shows ML Work:** **Exceptional.** Plain HTML gives 100% control over typography (`Space Grotesk`, `Inter`, `JetBrains Mono`), allows pixel-perfect inline SVG vector charts (`outputs/charts/*.svg`), seamlessly embeds interactive 3D WebGL canvases, and links directly to GitHub repositories. The repository itself doubles as proof of shipping competence.
- **The Real Trade-Off:** Requires reading and editing HTML/CSS markup manually. However, because there are zero npm dependencies, the site is indestructible: it will never fail a build step or suffer dependency rot.

---

### Road 3: Full-Stack JavaScript Framework (Most Powerful)
- **How I Would Build It:** Scaffold a Next.js (React) or Astro project with Tailwind CSS, TypeScript, and dynamic routing.
- **Where I Would Host (Free):** Vercel or Cloudflare Pages with automated GitHub CI/CD webhooks.
- **Does It Need a Backend?** Technically no (can export static SSG), but introduces full Node.js build pipelines and API route capabilities.
- **How Well It Shows ML Work:** Very good if building a dynamic web SaaS application, but adds zero incremental value for displaying static case studies, charts, and articles.
- **The Real Trade-Off:** **Massive complexity and maintenance debt.** Scaffolding Next.js introduces hundreds of megabytes of `node_modules`, breaking version updates, hydration errors, and complex build scripts. In a 2-week sprint, I would spend 70% of my time fighting npm package errors and Vercel build timeouts instead of polishing my machine learning proofs.

---

## 3. Pressure-Testing the Front-Runner (The Four Tough Questions)

Before committing to Road 2, I pressure-tested the choice against the four core evaluation questions:

| Pressure-Test Question | Honest Answer & Analysis |
|---|---|
| **1. What breaks if I pick the simplest (Road 1: No-Code)?** | My engineering credibility breaks. An ML recruiter looking at a Carrd site wonders why an engineer claiming to build computer vision and ranking pipelines couldn't write an `index.html` file. Furthermore, free tiers block custom scripts and embed tags, preventing custom 3D WebGL rendering. |
| **2. What do I maintain if I pick the most powerful (Road 3: Framework)?** | I inherit an endless maintenance burden. Node.js versions depreciate, npm packages suffer security vulnerabilities, and React dependency updates cause breaking changes. A portfolio built in Next.js today often fails to build 12 months from now without code refactoring. |
| **3. Can I finish in two weeks?** | **Yes, easily with Road 2.** With plain HTML/CSS, the empty shell was live in under 10 minutes. I don't need to configure bundlers, compilers, or routing tables. Every hour of Week 5 can be dedicated directly to writing the case studies and embedding the charts. |
| **4. Does it show my work the way it needs to be shown?** | **Yes, better than any other option.** My work requires clean mathematical typography, responsive vector benchmark charts, code blocks, and fast page loads (<150ms). Plain HTML5 + CSS delivers that natively without bloat. |

---

## 4. The Final Decision & Rationale (In My Own Words)

> ### **My Choice: Plain Semantic HTML5 + Modern CSS + Three.js on Netlify & GitHub Pages**
>
> *"I chose Road 2 (Plain Code on Netlify and GitHub Pages) because the portfolio of an Applied AI & Machine Learning engineer should be quiet, robust, and fast. The site exists to frame the work, not to showcase a frontend framework I don't need.*
>
> *I deliberately rejected Road 1 (No-Code) because drag-and-drop builders damage technical credibility, restrict SVG data visualizations, and lock me into proprietary platforms.*
>
> *I deliberately rejected Road 3 (Next.js / Framework) because bringing a complex React framework to build a 4-page portfolio is bringing a bulldozer to plant a flower. I would rather spend my time training models, auditing feature leakage, and verifying Precision@50 than debugging npm build scripts.*
>
> ***Can I maintain this?*** *Yes, 100%. Plain HTML and CSS have no build tools, no package dependencies, and no security vulnerabilities. It will render identically in any browser ten years from now.*
>
> ***Does it show my work well?*** *Yes. It instantly renders my SVG feature importance charts, formats my machine learning benchmarks with JetBrains Mono, powers an interactive 3D WebGL canvas with Three.js, and links directly to my open-source code repositories.*
>
> ***The Backend Question:*** *I am choosing **'not yet.'** An embedded Calendly scheduler and a direct email mailto link give recruiters everything they need to take action without exposing a database or maintaining a backend server."*

---

## 5. Pass / Revise Self-Check

- [x] **Three Genuine Options Considered:** Road 1 (No-Code), Road 2 (Plain Code + AI), and Road 3 (Full Framework) evaluated with real trade-offs.
- [x] **Chosen Stack is Free & Matched to Needs:** Plain HTML5/CSS on Netlify & GitHub Pages ($0 forever, instant load speeds, perfect chart rendering).
- [x] **Written in My Own Words:** Clear, candid rationale explaining why an ML candidate favors plain code over React frameworks and no-code builders.
- [x] **"Can I Maintain This" Addressed:** Confirmed zero dependency maintenance debt.
- [x] **Honest Backend Decision:** Answered "Not yet" — static site with email/Calendly CTA is the right engineering call.
- [x] **Live Proof Verified:** Active and verified on [https://arslanflyrankweb1.netlify.app/](https://arslanflyrankweb1.netlify.app/).
