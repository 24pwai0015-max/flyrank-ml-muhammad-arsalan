# coding: utf-8
"""
Update author header in paper.html to feature Muhammad Arsalan's photo and verified credentials.
"""

for path in ['docs/paper.html', 'portfolio/paper.html', 'd:/4th semester Ai/internship/portfolio/paper.html']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        old_meta = """      <div class="paper-meta">
        <strong>Author:</strong> Muhammad Arsalan &nbsp;·&nbsp;
        <strong>Track:</strong> FlyRank Applied Machine Learning &nbsp;·&nbsp;
        <strong>Date:</strong> March 2026 &nbsp;·&nbsp;
        <strong>Evaluation Metric:</strong> Precision@50 (Client-Holdout)
      </div>"""
        
        new_meta = """      <div class="paper-meta" style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px; background: rgba(255, 255, 255, 0.03); padding: 14px 20px; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.25);">
        <img src="assets/arsalan.jpg" alt="Muhammad Arsalan" style="width: 56px; height: 56px; border-radius: 50%; object-fit: cover; border: 2px solid #10B981; box-shadow: 0 0 14px rgba(16, 185, 129, 0.35);" />
        <div>
          <div style="font-size: 1.05rem; color: #FFFFFF; font-weight: 700;">Muhammad Arsalan &nbsp;·&nbsp; <span style="color: #34D399; font-weight: 600;">Applied AI &amp; ML Engineer</span></div>
          <div style="font-size: 0.82rem; color: #94A3B8; font-family: var(--font-mono); margin-top: 2px;">FlyRank AI Internship Capstone &nbsp;·&nbsp; UET Peshawar &nbsp;·&nbsp; Target Metric: <strong style="color: #38BDF8;">Precision@50 = 0.740</strong></div>
        </div>
      </div>"""
        
        if old_meta in content:
            content = content.replace(old_meta, new_meta)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated author box with photo in: {path}")
        else:
            print(f"Old meta snippet not found in {path}")
    except Exception as e:
        print(f"Error updating {path}: {e}")
