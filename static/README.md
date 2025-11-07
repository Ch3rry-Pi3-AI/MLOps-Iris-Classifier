# 🎨 **`static/` Folder — Front-End Assets**

The `static/` directory contains all **front-end resources** for the **Flask-based Iris Species Prediction App**.
These assets define the **visual identity**, **layout**, and **user experience** of the web interface that serves the trained MLOps Iris Classifier model.

## 📁 **Folder Overview**

```text
static/
├─ style.css            # 🎨 Core stylesheet controlling layout and design
└─ img/
   └─ app_background.jpg # 🌄 Subtle background image with light transparency
```

## 🧩 **Purpose**

The assets inside this folder are automatically served by Flask when referenced using `url_for('static', filename=...)`.
They control all aspects of the app’s appearance — typography, layout, form controls, button styles, and background visuals.

| File / Directory         | Description                                                                                           |
| ------------------------ | ----------------------------------------------------------------------------------------------------- |
| `style.css`              | Main stylesheet defining fonts, grid layout, colour palette, spacing, buttons, and responsive design. |
| `img/`                   | Contains static media files such as background images and future icons or logos.                      |
| `img/app_background.jpg` | The faint background texture applied via `.bg-overlay` with 20% opacity for visual depth.             |

## 🎨 **Key Design Features**

* **Modern Typography** — Uses [Google Fonts: Poppins](https://fonts.google.com/specimen/Poppins) for a clean, readable interface.
* **Responsive Grid Layouts** — Adaptive two-column form and guidance cards, collapsing into a single column on smaller screens.
* **Consistent Colour Palette** — Neutral whites and blues for accessibility and contrast; success and error colours defined via CSS variables.
* **Subtle Background Overlay** — `app_background.jpg` is lightly transparent (20%) to create a polished, professional aesthetic without visual distraction.
* **Full-Width Predict Button** — Clearly visible call-to-action that spans the entire form width for easy interaction.

## 🧠 **Technical Notes**

* The background image is injected via a `<style>` block in `index.html` using:

  ```html
  <style>
    .bg-overlay {
      background-image: url("{{ url_for('static', filename='img/app_background.jpg') }}");
    }
  </style>
  ```

  This ensures Flask correctly resolves the static path during runtime.

* CSS variables (`--brand`, `--text`, `--ok`, etc.) are defined in `:root` for quick theming and consistent styling.

* All layout elements (e.g., `.container`, `.form-grid`, `.stats-grid`) are **responsive** and **centrally aligned** to improve usability across devices.

## 🧱 **Integration in Flask Templates**

In `templates/index.html`, assets are referenced as follows:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<img src="{{ url_for('static', filename='img/app_background.jpg') }}" alt="Background">
```

This makes the front-end modular and portable across different Flask deployment environments.

## ✅ **In Summary**

The `static/` folder provides:

* A **consistent design system** for the Iris prediction interface
* **Responsive** and **accessible** styling using CSS grid and variables
* **Separation of concerns** between Flask logic and presentation
* A ready-to-extend foundation for future UI enhancements (e.g., icons, charts, or animations)

Together, these assets make the Iris web app **intuitive**, **aesthetically pleasing**, and **user-friendly**, complementing the back-end machine learning workflow.