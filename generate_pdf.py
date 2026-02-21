from fpdf import FPDF
import sys

# Ensure utf-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Resume Backend: Page d\'Accueil & Sign In', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('Arial', '', 12)

# Introduction
pdf.chapter_title("Introduction")
pdf.chapter_body(
    "Ce document resume l'architecture backend pour deux pages cles de l'application :\n"
    "1. La page d'inscription / connexion (Sign In)\n"
    "2. La page d'accueil (Dashboard / Generateur)"
)

# Section 1: Sign In (Authentification)
pdf.chapter_title("1. Page Sign In (Authentification)")
pdf.chapter_body(
    "Le backend gere l'inscription et la connexion via des endpoints securises.\n\n"
    "Endpoint d'inscription (POST /auth/register):\n"
    "- Cree un nouvel utilisateur dans la base de donnees (table 'users').\n"
    "- Hash le mot de passe avec bcrypt pour la securite.\n"
    "- Initialise une session Stripe pour le paiement de l'abonnement.\n"
    "- Si le paiement est requis, redirige vers Stripe Checkout.\n\n"
    "Endpoint de connexion (POST /auth/login):\n"
    "- Verifie les identifiants (email + mot de passe).\n"
    "- Verifie si le compte est actif (paiement effectue).\n"
    "- Si valide, retourne un token JWT (JSON Web Token) pour l'acces securise.\n\n"
    "Endpoint Google Auth (POST /auth/google):\n"
    "- Verifie le token ID de Google serverside.\n"
    "- Cree un compte utilisateur si inexistant.\n"
    "- Procede au flux de paiement si necessaire."
)

# Section 2: Page d'Accueil (Dashboard & Generateur)
pdf.chapter_title("2. Page d'Accueil (Dashboard & Generateur)")
pdf.chapter_body(
    "Une fois connecte, l'utilisateur accede au Dashboard qui sert de page d'accueil applicative.\n\n"
    "Donnees du Dashboard (GET /dashboard/stats):\n"
    "- Recupere les statistiques d'utilisation (nombre de generations, campagnes actives).\n"
    "- Affiche le score SEO moyen.\n"
    "- Verifie le plan de l'utilisateur (Starter, Pro, Enterprise).\n\n"
    "Historique (GET /history):\n"
    "- Liste les dernieres generations de contenu (Landing pages, SEO, Social posts).\n\n"
    "Generation de Contenu (POST /generate/*):\n"
    "- L'utilisateur soumet les details du produit.\n"
    "- Le backend verifie les quotas mensuels selon le plan.\n"
    "- Appelle l'API Claude (Anthropic) pour generer le contenu.\n"
    "- Sauvegarde le resultat dans la base de donnees (table 'generations')."
)

# Conclusion
pdf.chapter_title("Conclusion")
pdf.chapter_body(
    "Le backend est structure autour de FastAPI, utilisant SQLAlchemy pour la base de donnees SQLite/PostgreSQL.\n"
    "La securite est assuree par JWT et le hachage des mots de passe.\n"
    "Les paiements sont geres via Stripe."
)

try:
    pdf.output("Resume_Backend.pdf", 'F')
    print("PDF genere avec succes : Resume_Backend.pdf")
except Exception as e:
    print(f"Erreur lors de la generation du PDF: {e}")
