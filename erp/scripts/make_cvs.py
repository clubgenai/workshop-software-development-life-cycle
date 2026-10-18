"""Génère un CV PDF fictif par profil de cvs.json (dossier cvs/)."""
import json, os, random, unicodedata, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

INK, MUTED, AMBER, AMBER_DEEP, LINE = HexColor("#1B1B1B"), HexColor("#5C564F"), HexColor("#E5A040"), HexColor("#845400"), HexColor("#E2DED8")

ROLES = {
 "Développeuse Full-stack": ("Je conçois des applications web de bout en bout, de l'API à l'interface.", ["TypeScript", "React", "Node.js", "PostgreSQL", "Docker"]),
 "Développeur Full-stack": ("Je conçois des applications web de bout en bout, de l'API à l'interface.", ["TypeScript", "React", "Node.js", "PostgreSQL", "Docker"]),
 "Développeur Back-end": ("Je construis des API robustes et des services qui tiennent la charge.", ["Java", "Spring Boot", "Kotlin", "PostgreSQL", "Kafka"]),
 "Développeur Front-end": ("Je développe des interfaces accessibles, rapides et soignées.", ["TypeScript", "React", "Next.js", "CSS", "Accessibilité"]),
 "Développeuse Front-end": ("Je développe des interfaces accessibles, rapides et soignées.", ["TypeScript", "Vue.js", "Nuxt", "CSS", "Accessibilité"]),
 "Architecte Cloud": ("J'accompagne les équipes dans la conception d'architectures cloud sûres et maîtrisées en coût.", ["Google Cloud", "AWS", "Terraform", "Kubernetes", "FinOps"]),
 "Data Scientist": ("Je transforme les données en modèles utiles pour les métiers.", ["Python", "scikit-learn", "SQL", "Statistiques", "MLOps"]),
 "Data Engineer": ("Je construis des pipelines de données fiables et documentés.", ["Python", "Spark", "dbt", "BigQuery", "Airflow"]),
 "Product Owner": ("Je traduis les besoins métier en backlog priorisé et en critères d'acceptation clairs.", ["Discovery", "User stories", "Critères d'acceptation", "Roadmap", "Atelier"]),
 "Ingénieur DevOps": ("J'automatise la chaîne de livraison, du commit à la production.", ["CI/CD", "GitLab", "Docker", "Kubernetes", "Terraform"]),
 "UX Designer": ("Je conçois des parcours simples, testés avec de vrais utilisateurs.", ["Figma", "Recherche utilisateur", "Prototypage", "Design system", "Accessibilité"]),
 "Tech Lead": ("J'anime une équipe technique et je garde l'architecture lisible dans la durée.", ["Architecture", "Revue de code", "Java", "TypeScript", "Mentorat"]),
 "Ingénieur SRE": ("Je rends les services observables, fiables et rapides à rétablir.", ["Observabilité", "Kubernetes", "Prometheus", "SLO", "Go"]),
 "Scrum Master": ("Je facilite le travail d'équipe et l'amélioration continue.", ["Scrum", "Kanban", "Facilitation", "Rétrospective", "Coaching"]),
 "Ingénieure IA": ("Je mets en production des systèmes à base de LLM, évalués et maîtrisés.", ["Python", "LLM", "RAG", "Évaluation", "Agents"]),
 "QA Engineer": ("Je construis des stratégies de test qui donnent confiance à chaque livraison.", ["Playwright", "Cypress", "Tests d'API", "Stratégie de test", "CI"]),
}
COMPANIES = ["Atelier Numérique", "Nova Retail", "Banque du Littoral", "Énergie Ouest", "Mobilis Transport", "Santé Connect", "Éditions Horizon", "AgroTech Sud", "Assurances Rive Gauche", "Logistique Express"]
SCHOOLS = ["Master Informatique, Université de Bordeaux", "Diplôme d'ingénieur, INSA Lyon", "Master MIAGE, Université de Lille", "Diplôme d'ingénieur, IMT Atlantique", "Master Data Science, Université Paris Cité", "Bachelor Design numérique, École de Design Nantes"]

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", ".", s).strip(".")

def wrap(c, text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if c.stringWidth(t, font, size) <= width: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def make(p, out):
    rnd = random.Random(p["id"])
    summary, skills = ROLES[p["metier"]]
    c = canvas.Canvas(out, pagesize=A4)
    W, H = A4
    c.setTitle(f"CV {p['prenom']} {p['nom']}")
    c.setAuthor("CVthèque · données fictives")
    c.setFillColor(AMBER); c.rect(0, H - 14, W, 14, stroke=0, fill=1)
    x, y = 56, H - 90
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 28); c.drawString(x, y, f"{p['prenom']} {p['nom']}")
    y -= 26; c.setFillColor(AMBER_DEEP); c.setFont("Helvetica-Bold", 14); c.drawString(x, y, p["metier"])
    y -= 20; c.setFillColor(MUTED); c.setFont("Helvetica", 10.5)
    years = rnd.randint(2, 14)
    c.drawString(x, y, f"{p['localisation']}  ·  {years} ans d'expérience  ·  {slug(p['prenom'])}.{slug(p['nom'])}@exemple.fr")
    y -= 18; c.setStrokeColor(LINE); c.setLineWidth(1); c.line(x, y, W - x, y)

    def section(title):
        nonlocal y
        y -= 30; c.setFillColor(AMBER_DEEP); c.setFont("Helvetica-Bold", 10); c.drawString(x, y, title.upper()); y -= 6

    section("Profil")
    c.setFillColor(INK); c.setFont("Helvetica", 11)
    for line in wrap(c, summary, "Helvetica", 11, W - 2 * x): y -= 16; c.drawString(x, y, line)

    section("Expériences")
    comps = rnd.sample(COMPANIES, 2)
    end = 2026
    for i, comp in enumerate(comps):
        start = end - rnd.randint(2, 5)
        y -= 20; c.setFillColor(INK); c.setFont("Helvetica-Bold", 11.5)
        c.drawString(x, y, f"{p['metier']} · {comp}")
        c.setFillColor(MUTED); c.setFont("Helvetica", 10.5); c.drawRightString(W - x, y, f"{start} – {'aujourd’hui' if i == 0 else end}")
        tasks = [f"Contribution à un produit utilisé au quotidien par les équipes {rnd.choice(['métier', 'commerciales', 'support', 'finance'])}.",
                 "Mise en place de pratiques autour de {} et de {}.".format(*rnd.sample(skills, 2)),
                 "Travail en équipe pluridisciplinaire, avec des livraisons régulières en production."]
        c.setFont("Helvetica", 10.5)
        for t in tasks:
            for j, line in enumerate(wrap(c, t, "Helvetica", 10.5, W - 2 * x - 14)):
                y -= 15; c.setFillColor(INK)
                if j == 0: c.setFillColor(AMBER); c.circle(x + 3, y + 3.5, 2, stroke=0, fill=1); c.setFillColor(INK)
                c.drawString(x + 14, y, line)
        end = start

    section("Compétences")
    y -= 22; cx = x; c.setFont("Helvetica", 10.5)
    for s in skills:
        w = c.stringWidth(s, "Helvetica", 10.5) + 18
        c.setFillColor(HexColor("#F1F1F1")); c.setStrokeColor(LINE); c.roundRect(cx, y - 6, w, 20, 3, stroke=1, fill=1)
        c.setFillColor(INK); c.drawString(cx + 9, y, s); cx += w + 8

    section("Formation")
    y -= 18; c.setFillColor(INK); c.setFont("Helvetica", 11); c.drawString(x, y, rnd.choice(SCHOOLS))

    c.setFillColor(MUTED); c.setFont("Helvetica-Oblique", 8.5)
    c.drawString(x, 40, "CV fictif généré pour le TP Club GenAI · Intégrer l'IA dans son SDLC. Toute ressemblance serait fortuite.")
    c.showPage(); c.save()

if __name__ == "__main__":
    import sys
    root = sys.argv[1]
    data = json.load(open(os.path.join(root, "cvs.json"), encoding="utf-8"))
    for p in data:
        out = os.path.join(root, p["cv"]); os.makedirs(os.path.dirname(out), exist_ok=True); make(p, out)
    print(len(data), "CV générés")
