# Identity Kit: Decide Once — Muhammad Arsalan

**Track:** General AI Fluency (Foundations) — Week 3  
**Assignment:** Decide Once: Build Your Identity Kit  
**Focus:** Applied AI, Machine Learning, & Robotics  

---

## 1. Visual Brand Assets (Rendered)

### Horizontal Logo Wordmark
![Muhammad Arsalan Logo Wordmark](../assets/logo.svg)

### Minimalist Favicon Icon
![Muhammad Arsalan Favicon](../assets/favicon.svg)

---

## 2. Typography (Google Fonts)

Two free, fast-loading fonts chosen once for maximum readability and structured engineering hierarchy:

| Role | Font Family | Weights | Rationale |
|---|---|---|---|
| **Headings** | **Space Grotesk** | `600` (Semi-Bold), `700` (Bold) | Clean, geometric, technical tone that gives a confident, intentional face without being decorative. |
| **Body & UI** | **Inter** | `400` (Regular), `500` (Medium) | Neutral, screen-optimized grotesque with tall x-height for comfortable reading of technical case studies. |
| **Code & Metrics** | **JetBrains Mono** | `500` (Medium) | Monospaced font for metric comparison tables, precision scores, and Python snippets. |

---

## 3. Color Palette (Tight 4-Color System)

A restrained, high-contrast palette designed so that project screenshots, charts, and metrics are the loudest elements on every page:

| Swatch Role | Color Name | Hex Code | Purpose & Contrast Ratio |
|---|---|---|---|
| **Background (Main)** | Canvas Off-White | `#F9FAFB` | Calm, non-glare canvas that makes cards and screenshots pop. |
| **Surface / Card** | Pure White | `#FFFFFF` | Background for case study containers and code blocks. |
| **Text (Primary)** | Ink Dark | `#111827` | High-contrast body & heading text (WCAG AAA compliant: 15.3:1 contrast ratio). |
| **Text (Muted)** | Slate Gray | `#4B5563` | Subtitles, metadata dates, captions (WCAG AA compliant: 7.2:1 contrast ratio). |
| **Border / Line** | Light Gray | `#E5E7EB` | Subtle structural card borders and section dividers. |
| **Accent / Action** | Mint Emerald | `#059669` | Interactive links, CTA buttons, key metric highlights. |
| **Accent Hover** | Deep Emerald | `#047857` | Button hover and active states. |

---

## 4. Logo & Favicon Specifications

- **Favicon (`work/assets/favicon.svg`):** Minimalist $64 \times 64$ app mark featuring a rounded `#111827` dark container, crisp off-white `MA` monogram in Space Grotesk, and a vibrant `#059669` terminal cursor block `_`.
- **Logo Wordmark (`work/assets/logo.svg`):** Horizontal header badge combining the `[MA_]` dark icon badge with the full name *"Muhammad Arsalan"* in Space Grotesk Bold and *"Applied AI & ML Engineer"* subtitle in Inter.

---

## 5. Reusable Two-Line Style Note

> **Fonts:** Space Grotesk (Headings), Inter (Body), JetBrains Mono (Code).  
> **Colors:** `#F9FAFB` (Canvas Background), `#111827` (Ink Text), `#FFFFFF` (Card Surface), `#059669` (Emerald Accent), `#E5E7EB` (Borders).  
> **Mood:** Quiet, confident, engineering-first — generous whitespace and crisp typography so real code, live demos, and verified metrics remain the star of the page.

---

## 6. Build Snippet (Standing Instruction for AI Prompts)

```css
:root {
  --font-heading: 'Space Grotesk', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  --color-bg: #F9FAFB;
  --color-surface: #FFFFFF;
  --color-ink: #111827;
  --color-muted: #4B5563;
  --color-border: #E5E7EB;
  --color-accent: #059669;
  --color-accent-hover: #047857;

  --max-width: 960px;
  --radius-card: 10px;
  --spacing-section: 64px;
}
```
