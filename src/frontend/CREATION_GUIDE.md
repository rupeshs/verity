# How to Build a Modern AI Streaming App with React

This guide explains how to build a high-performance, aesthetically pleasing React application that supports Server-Sent Events (SSE) and real-time markdown streaming using the `streamdown` package.

## 1. Project Initialization

Start by creating a new React project using Vite:

```bash
npx create-vite@latest my-ai-app --template react
cd my-ai-app
npm install
```

## 2. Install Dependencies

Install the necessary packages for styling, icons, and streaming:

```bash
# Styling and Utilities
npm install -D tailwindcss @tailwindcss/vite @tailwindcss/typography
npm install lucide-react clsx tailwind-merge framer-motion

# Streaming Markdown and Syntax Highlighting
npm install streamdown @streamdown/code @streamdown/mermaid @streamdown/math @streamdown/cjk shiki katex mermaid
```

## 3. Configure Tailwind CSS v4

Update your `vite.config.js` to include the Tailwind plugin:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
})
```

Initialize your `src/index.css` with Tailwind v4 directives:

```css
@import "tailwindcss";
@plugin "@tailwindcss/typography";
@source "../node_modules/streamdown/dist/*.js";

@theme {
  --font-sans: "Inter", "system-ui", "sans-serif";
  --color-dark-bg: #171717;
  --color-dark-surface: #262626;
  --color-dark-border: #333333;
}

@custom-variant dark (&:where(.dark, .dark *));
```

## 4. Implementation Steps

### A. Create the SSE Hook
Create `src/hooks/useSSE.js` to manage the `EventSource` connection. This hook should handle various event types (`token`, `search`, `done`, etc.).

### B. Build Modular Components
- **Header**: Contains the logo and the dark mode toggle logic.
- **SearchInput**: A smart `textarea` that auto-resizes and includes a "Clear" button.
- **ResponseArea**: The most critical part. It wraps the `Streamdown` component in a `prose` container to ensure typography styles apply correctly.

### C. Configure Streamdown
In your `ResponseArea`, configure `Streamdown` with the plugins for code highlighting and math:

```javascript
import { Streamdown } from "streamdown";
import { code } from "@streamdown/code";
import { mermaid } from "@streamdown/mermaid";
import { math } from "@streamdown/math";
import { cjk } from "@streamdown/cjk";

// Inside component:
<Streamdown 
  mode="streaming" 
  plugins={{ code, mermaid, math, cjk }}
  isAnimating={isStreaming}
  shikiTheme={['github-light', 'github-dark']}
>
  {data}
</Streamdown>
```

## 5. Key Design Principles Used
1.  **Typography**: Always use a premium font like **Inter**.
2.  **Soft Dark Mode**: Use deep greys (#171717) rather than pure black (#000) for a more modern, professional look.
3.  **Micro-interactions**: Use `framer-motion` or CSS transitions for theme toggles and status indicators.
4.  **Auto-Scroll**: Implement an `useEffect` with `scrollIntoView` to keep the user focused on the latest tokens as they stream in.

## 6. Running the App

```bash
npm run dev
```

The app will now be live, ready to handle real-time AI streams!
