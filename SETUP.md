# Abhay's Animated GitHub Profile

## 1. Create the profile repository

Create a **public repository named exactly `abhay23459`**. GitHub uses that repository as your profile README.

If the repository already exists, replace its README and add the files from this folder.

## 2. Copy the files

Keep this structure:

```text
abhay23459/
├── README.md
├── avi-ascii.svg
├── info-card.svg
├── contrib-heatmap.svg
├── data/
│   └── contributions.json
├── scripts/
│   ├── fetch_contributions.py
│   ├── render_heatmap_svg.py
│   └── requirements.txt
└── .github/
    └── workflows/
        └── update-profile-art.yml
```

## 3. First run

The included contribution JSON is only a starter snapshot. After pushing the files:

1. Open **Actions** in your profile repository.
2. Select **Update profile art**.
3. Click **Run workflow**.
4. The workflow fetches your public contribution calendar, regenerates the SVG and commits it.

After that, it runs automatically every day.

## 4. Update your personal details

Edit `info-card.svg` and the About section in `README.md` whenever you want to change your role, stack, projects or achievements.

## 5. Regenerate the portrait

The included `avi-ascii.svg` was generated from the photo you provided. If you change the photo later, regenerate the SVG with your own preferred image-to-ASCII script or replace the SVG.

## Important

The contribution scraper depends on GitHub's public contributions HTML structure. If GitHub changes that markup, update `scripts/fetch_contributions.py` accordingly.
