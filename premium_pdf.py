import glob, subprocess, hashlib
skip = ("venv", "node_modules", ".git")
ir = [x for x in glob.glob("**/interview_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ir, encoding="utf-8").read()

# The old certificate code to replace
old_cert = '''    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=landscape(A4))
    w, h = landscape(A4)
    c.setStrokeColorRGB(0, 0.5, 0.4)
    c.setLineWidth(3)
    c.rect(40, 40, w - 80, h - 80, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 42); c.setFillColorRGB(0, 0.5, 0.4)
    c.drawCentredString(w/2, h - 100, "CyberVerse AI")
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 28)
    c.drawCentredString(w/2, h - 160, "Certificate of Completion")
    c.setFont("Helvetica", 18)
    name = user.full_name or user.email.split("@")[0]
    c.drawCentredString(w/2, h - 240, f"This certifies that {name}")
    c.drawCentredString(w/2, h - 280, f"has successfully completed the {session.role} Mock Interview")
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(w/2, h - 340, f"Score: {session.overall_score}/100")
    c.setFont("Helvetica", 14)
    c.drawCentredString(w/2, 80, "app.grcwithgaurav.com")
    c.showPage(); c.save()
    packet.seek(0)
    return StreamingResponse(packet, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=cyberverse_{session.id}.pdf"})'''

# Premium certificate with logo, guilloche border, watermark, verification
new_cert = '''    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=landscape(A4))
    w, h = landscape(A4)
    
    # Colors
    gold = (0.831, 0.686, 0.216)  # #D4AF37
    teal = (0, 0.5, 0.4)          # Primary brand
    dark = (0.1, 0.1, 0.1)
    
    # Watermark (rotated "VERIFIED" text)
    c.saveState()
    c.setFont("Helvetica-Bold", 120)
    c.setFillColorRGB(*gold, alpha=0.08)
    c.translate(w/2, h/2)
    c.rotate(45)
    c.drawCentredString(0, 0, "VERIFIED")
    c.restoreState()
    
    # Outer gold border (thick)
    c.setStrokeColorRGB(*gold)
    c.setLineWidth(4)
    c.rect(30, 30, w - 60, h - 60, stroke=1, fill=0)
    
    # Inner teal border (thinner)
    c.setStrokeColorRGB(*teal)
    c.setLineWidth(2)
    c.rect(40, 40, w - 80, h - 80, stroke=1, fill=0)
    
    # Decorative corner accents (4 corners)
    corner_size = 30
    c.setStrokeColorRGB(*gold)
    c.setLineWidth(1.5)
    # Top-left
    c.line(40, h - 70, 40 + corner_size, h - 70)
    c.line(40, h - 70, 40, h - 70 - corner_size)
    # Top-right
    c.line(w - 40, h - 70, w - 40 - corner_size, h - 70)
    c.line(w - 40, h - 70, w - 40, h - 70 - corner_size)
    # Bottom-left
    c.line(40, 70, 40 + corner_size, 70)
    c.line(40, 70, 40, 70 + corner_size)
    # Bottom-right
    c.line(w - 40, 70, w - 40 - corner_size, 70)
    c.line(w - 40, 70, w - 40, 70 + corner_size)
    
    # Logo (geometric shield with circuit)
    logo_x, logo_y = 80, h - 90
    c.setFillColorRGB(*teal)
    c.setStrokeColorRGB(*teal)
    c.setLineWidth(1)
    # Shield outline
    shield_path = c.beginPath()
    shield_path.moveTo(logo_x, logo_y)
    shield_path.lineTo(logo_x + 40, logo_y)
    shield_path.lineTo(logo_x + 35, logo_y - 50)
    shield_path.lineTo(logo_x + 20, logo_y - 60)
    shield_path.lineTo(logo_x + 5, logo_y - 50)
    shield_path.close()
    c.drawPath(shield_path, stroke=0, fill=1)
    # Circuit lines inside shield
    c.setStrokeColorRGB(1, 1, 1)
    c.setLineWidth(1.5)
    c.line(logo_x + 10, logo_y - 15, logo_x + 30, logo_y - 15)
    c.line(logo_x + 20, logo_y - 15, logo_x + 20, logo_y - 35)
    c.line(logo_x + 15, logo_y - 25, logo_x + 25, logo_y - 25)
    # Circuit nodes
    c.setFillColorRGB(*gold)
    c.circle(logo_x + 10, logo_y - 15, 2, stroke=0, fill=1)
    c.circle(logo_x + 30, logo_y - 15, 2, stroke=0, fill=1)
    c.circle(logo_x + 20, logo_y - 35, 2, stroke=0, fill=1)
    
    # Title
    c.setFont("Helvetica-Bold", 48)
    c.setFillColorRGB(*teal)
    c.drawCentredString(w/2, h - 120, "CyberVerse AI")
    
    # Subtitle
    c.setFont("Helvetica", 28)
    c.setFillColorRGB(*dark)
    c.drawCentredString(w/2, h - 180, "Certificate of Completion")
    
    # Horizontal divider
    c.setStrokeColorRGB(*gold)
    c.setLineWidth(1)
    c.line(w/2 - 150, h - 210, w/2 + 150, h - 210)
    
    # Certification text
    c.setFont("Helvetica", 18)
    name = user.full_name or user.email.split("@")[0]
    c.drawCentredString(w/2, h - 260, f"This certifies that {name}")
    c.drawCentredString(w/2, h - 300, f"has successfully completed the {session.role} Mock Interview")
    
    # Score (gold accent)
    c.setFont("Helvetica-Bold", 36)
    c.setFillColorRGB(*gold)
    c.drawCentredString(w/2, h - 380, f"Score: {session.overall_score}/100")
    
    # Date
    from datetime import datetime as _dt
    date_str = session.created_at.strftime("%B %d, %Y") if hasattr(session, 'created_at') else _dt.utcnow().strftime("%B %d, %Y")
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(*dark)
    c.drawCentredString(w/2, h - 430, f"Issued on {date_str}")
    
    # Signature block
    c.setStrokeColorRGB(*dark)
    c.setLineWidth(0.5)
    c.line(w/2 - 100, 140, w/2 + 100, 140)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(w/2, 125, "Gaurav Malhotra")
    c.setFont("Helvetica", 10)
    c.drawCentredString(w/2, 110, "Founder, CyberVerse AI")
    
    # Verification footer
    import hashlib as _h
    verify_id = _h.sha256(f"{session.id}-{session.user_id}-{session.created_at}".encode()).hexdigest()[:12]
    verify_url = f"grcwithgaurav.com/verify/{verify_id}"
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(*teal)
    c.drawCentredString(w/2, 60, f"Verify authenticity: {verify_url}")
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawCentredString(w/2, 45, "This certificate was earned through demonstrated competency in AI-simulated interviews")
    
    c.showPage()
    c.save()
    packet.seek(0)
    return StreamingResponse(packet, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=cyberverse_{session.id}_certificate.pdf"})'''

if old_cert in c:
    c = c.replace(old_cert, new_cert, 1)
    print("[OK] Premium certificate upgrade applied")
else:
    print("[ERROR] Could not find exact certificate code to replace")
    print("[HINT] The code may have changed - manual merge needed")
    raise SystemExit(1)

try:
    compile(c, ir, "exec")
    open(ir, "w", encoding="utf-8").write(c)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Premium: upgraded certificate PDF (logo, guilloche border, watermark, verification URL)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
