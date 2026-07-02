# Public Static Pages

This directory contains static HTML and PDF files for the BardBox Monitoring Platform.
They are intended to be served directly by Nginx on `bard-box.org`,
independent of any BardBox monitoring application.

These files do not depend on the CESH Air FastAPI app, Python, JavaScript, or
any backend service. Do not add FastAPI routes for these pages.

Expected public URLs after deployment:

- `https://bard-box.org/privacy`
- `https://bard-box.org/terms`
- `https://bard-box.org/consent`
- `https://bard-box.org/consent.pdf`

Suggested Nginx deployment, assuming the repository is cloned to `/opt/bardbox`:

```nginx
location = /privacy {
    alias /opt/bardbox/public/privacy.html;
}

location = /terms {
    alias /opt/bardbox/public/terms.html;
}

location = /consent {
    alias /opt/bardbox/public/consent.html;
}

location = /consent.pdf {
    alias /opt/bardbox/public/consent.pdf;
}
```

Regenerate the RKC Monitor SMS Alert consent PDF after changing the form copy:

```bash
python3 scripts/generate_consent_pdf.py
```
