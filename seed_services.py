import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
import models

def seed_services():
    db = SessionLocal()
    
    print(f"Synchronizing services from frontend list...")

    # List of all services extracted from services.tsx
    services_data = [
        # Instagram
        { "id": 1, "title": "Instagram Followers [Premium]", "description": "Abonnés de haute qualité, profil réel, garantie 30 jours.", "price": 2.49, "unit": "1000", "category": "Instagram", "platform": "Instagram", "min_quantity": 100, "max_quantity": 100000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Haute Qualité", "Garantie 30j", "Vitesse Rapide"] },
        { "id": 2, "title": "Instagram Likes [Vrais]", "description": "Likes instantanés de profils actifs, sans perte.", "price": 0.89, "unit": "1000", "category": "Instagram", "platform": "Instagram", "min_quantity": 50, "max_quantity": 50000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Instantané", "Profils Réels", "Sans Perte"] },
        { "id": 3, "title": "Instagram Views [Reels]", "description": "Vues pour vos Reels avec une excellente rétention.", "price": 0.15, "unit": "1000", "category": "Instagram", "platform": "Instagram", "min_quantity": 100, "max_quantity": 1000000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Max Rétention", "Viral Boost", "Pas de Mot de Passe"] },
        { "id": 4, "title": "Instagram Auto-Likes [Mensuel]", "description": "Likes automatiques sur chaque nouvelle publication.", "price": 19.99, "unit": "mois", "category": "Instagram", "platform": "Instagram", "min_quantity": 1, "max_quantity": 1, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Bot Automatisé", "Engagement Continu", "Support 24/7"] },
        { "id": 5, "title": "Instagram Comments [Custom]", "description": "Commentaires personnalisés rédigés par vous ou par IA.", "price": 5.50, "unit": "50", "category": "Instagram", "platform": "Instagram", "min_quantity": 10, "max_quantity": 1000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Texte Libre", "Ciblage Langue", "Modération"] },
        { "id": 6, "title": "Instagram Story Views", "description": "Vues sur vos stories Instagram pour booster la visibilité.", "price": 0.50, "unit": "1000", "category": "Instagram", "platform": "Instagram", "min_quantity": 100, "max_quantity": 20000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Instantané", "Discret", "Pas de Perte"] },
        { "id": 7, "title": "Instagram Profile Visits", "description": "Bousculez l'algorithme avec des visites de profil réelles.", "price": 1.20, "unit": "1000", "category": "Instagram", "platform": "Instagram", "min_quantity": 100, "max_quantity": 50000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Algorithme Boost", "Provenance Mondiale", "Légal"] },
        { "id": 33, "title": "Instagram Followers [Élite]", "description": "Abonnés ultra-premium, garantie à vie, profils européens.", "price": 12.50, "unit": "1000", "category": "Instagram", "platform": "Instagram", "min_quantity": 50, "max_quantity": 25000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Garantie à vie", "Ciblage UE", "Service Élite"] },
        { "id": 34, "title": "Instagram Likes [Vitesse Éclair]", "description": "100k likes délivrés en moins de 10 minutes.", "price": 0.50, "unit": "1000", "category": "Instagram", "platform": "Instagram", "min_quantity": 100, "max_quantity": 100000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Ultra Rapide", "Pas cher", "Stable"] },
        { "id": 41, "title": "Instagram Power Likes", "description": "Likes de comptes avec plus de 50k abonnés.", "price": 45.00, "unit": "100", "category": "Instagram", "platform": "Instagram", "min_quantity": 10, "max_quantity": 1000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Explorer Boost", "Haut Authority", "Viral"] },
        { "id": 44, "title": "Instagram Live Stream Views", "description": "Spectateurs en direct pendant que vous diffusez.", "price": 15.00, "unit": "1000", "category": "Instagram", "platform": "Instagram", "min_quantity": 100, "max_quantity": 5000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Démarrage 0-5min", "Reste 60min", "Stable"] },
        { "id": 53, "title": "Instagram Save [Algorithm]", "description": "Enregistrements pour booster le SEO de vos posts.", "price": 0.40, "unit": "1000", "category": "Instagram", "platform": "Instagram", "min_quantity": 100, "max_quantity": 100000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Algorithm Secret", "Growth Hack", "Sûr"] },
        { "id": 54, "title": "Instagram Mentions [Targeted]", "description": "Mentionnez des utilisateurs sur vos photos de manière massive.", "price": 25.00, "unit": "1000", "category": "Instagram", "platform": "Instagram", "min_quantity": 100, "max_quantity": 10000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Ciblage Précis", "Viralité", "Pro-User"] },
        { "id": 55, "title": "Instagram TV Views", "description": "Boostez vos vidéos IGTV (Legacy support).", "price": 0.10, "unit": "1000", "category": "Instagram", "platform": "Instagram", "min_quantity": 100, "max_quantity": 100000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Instantané", "Discret", "Stable"] },
        { "id": 56, "title": "Instagram DM Mass Sending", "description": "Envoi massif de messages direct à votre audience cible.", "price": 55.00, "unit": "1000", "category": "Instagram", "platform": "Instagram", "min_quantity": 500, "max_quantity": 50000, "icon_name": "InstagramIcon", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "features": ["Lead Gen", "Custom Text", "High Conversion"] },

        # TikTok
        { "id": 8, "title": "TikTok Followers [Real]", "description": "Abonnés TikTok stables pour augmenter votre autorité.", "price": 4.99, "unit": "1000", "category": "TikTok", "platform": "TikTok", "min_quantity": 100, "max_quantity": 100000, "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "features": ["Profils Actifs", "Safe & Secure", "Livraison Rapide"] },
        { "id": 9, "title": "TikTok Likes [Instant]", "description": "Boostez l'engagement de vos vidéos TikTok instantanément.", "price": 1.20, "unit": "1000", "category": "TikTok", "platform": "TikTok", "min_quantity": 100, "max_quantity": 50000, "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "features": ["Pas de Chute", "Support 24/7", "Premium Apparence"] },
        { "id": 10, "title": "TikTok Views [For You Page]", "description": "Vues ciblées pour aider à passer dans les 'Pour Toi'.", "price": 0.10, "unit": "1000", "category": "TikTok", "platform": "TikTok", "min_quantity": 1000, "max_quantity": 10000000, "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "features": ["FYP Boost", "Rétention Elevée", "Service sûr"] },
        { "id": 11, "title": "TikTok Shares [Viral]", "description": "Partages réels pour rendre vos vidéos virales.", "price": 0.75, "unit": "1000", "category": "TikTok", "platform": "TikTok", "min_quantity": 100, "max_quantity": 50000, "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "features": ["Growth Hack", "Engagement Pro", "Instantané"] },
        { "id": 12, "title": "TikTok Save [Boost]", "description": "Enregistrements de vidéos pour tromper l'algorithme.", "price": 0.60, "unit": "1000", "category": "TikTok", "platform": "TikTok", "min_quantity": 100, "max_quantity": 50000, "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "features": ["SEO Video", "Secret Boost", "Stable"] },
        { "id": 35, "title": "TikTok Followers [Arab Fans]", "description": "Abonnés TikTok avec profils et noms arabes.", "price": 7.99, "unit": "1000", "category": "TikTok", "platform": "TikTok", "min_quantity": 50, "max_quantity": 10000, "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "features": ["Ciblage Arabe", "Vrais Profils", "Garantie 30j"] },
        { "id": 42, "title": "TikTok Shares [France Only]", "description": "Partages réels provenant d'utilisateurs en France.", "price": 5.50, "unit": "1000", "category": "TikTok", "platform": "TikTok", "min_quantity": 50, "max_quantity": 5000, "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "features": ["Ciblage FR", "Rétention Locale", "Viral"] },
        { "id": 57, "title": "TikTok Live Stream [Concurrent]", "description": "Spectateurs stables pour vos lives TikTok.", "price": 12.00, "unit": "500", "category": "TikTok", "platform": "TikTok", "min_quantity": 100, "max_quantity": 2000, "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "features": ["Stable Live", "Instant", "Algorithm Boost"] },
        { "id": 58, "title": "TikTok Comments [AI Custom]", "description": "Commentaires intelligents rédigés par IA sur vos vidéos.", "price": 8.50, "unit": "100", "category": "TikTok", "platform": "TikTok", "min_quantity": 10, "max_quantity": 500, "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "features": ["Natural Text", "Safe", "Fast"] },

        # YouTube
        { "id": 13, "title": "YouTube Subscribers [No Drop]", "description": "Abonnés YouTube de haute qualité avec garantie à vie.", "price": 15.00, "unit": "1000", "category": "YouTube", "platform": "YouTube", "min_quantity": 100, "max_quantity": 10000, "icon_name": "YoutubeIcon", "color": "text-red-500", "bg_color": "bg-red-500/10", "features": ["Anti-Drop", "Sécurisé ADS", "Monétisation OK"] },
        { "id": 14, "title": "YouTube High Retention Views", "description": "Vues optimisées pour la monétisation et le SEO.", "price": 3.50, "unit": "1000", "category": "YouTube", "platform": "YouTube", "min_quantity": 1000, "max_quantity": 1000000, "icon_name": "YoutubeIcon", "color": "text-red-500", "bg_color": "bg-red-500/10", "features": ["Retention 60s+", "SEO Optimized", "ADS Safe"] },
        { "id": 15, "title": "YouTube Watch Time [4000H]", "description": "Heures de visionnage pour activer la monétisation.", "price": 89.00, "unit": "pack", "category": "YouTube", "platform": "YouTube", "min_quantity": 1, "max_quantity": 1, "icon_name": "YoutubeIcon", "color": "text-red-500", "bg_color": "bg-red-500/10", "features": ["Monetization Ready", "Qualité Max", "Support Dédié"] },
        { "id": 16, "title": "YouTube Likes [Non-Drop]", "description": "Likes stables pour vos vidéos YouTube.", "price": 2.10, "unit": "1000", "category": "YouTube", "platform": "YouTube", "min_quantity": 100, "max_quantity": 50000, "icon_name": "YoutubeIcon", "color": "text-red-500", "bg_color": "bg-red-500/10", "features": ["Garantie 60j", "Livraison Naturelle", "Profils Réels"] },
        { "id": 17, "title": "YouTube Comments [AI]", "description": "Commentaires intelligents adaptés à votre contenu.", "price": 12.00, "unit": "100", "category": "YouTube", "platform": "YouTube", "min_quantity": 5, "max_quantity": 500, "icon_name": "YoutubeIcon", "color": "text-red-500", "bg_color": "bg-red-500/10", "features": ["Rédigé par IA", "Mots-clés SEO", "Naturel"] },
        { "id": 36, "title": "YouTube Subscribers [USA Targeting]", "description": "Subscribers provenant exclusivement des USA.", "price": 45.00, "unit": "1000", "category": "YouTube", "platform": "YouTube", "min_quantity": 50, "max_quantity": 5000, "icon_name": "YoutubeIcon", "color": "text-red-500", "bg_color": "bg-red-500/10", "features": ["Geo-Targeted", "High Authority", "Safe"] },
        { "id": 43, "title": "YouTube Views [AdWords Method]", "description": "Vues réelles via le réseau Google Ads.", "price": 8.50, "unit": "1000", "category": "YouTube", "platform": "YouTube", "min_quantity": 500, "max_quantity": 100000, "icon_name": "YoutubeIcon", "color": "text-red-500", "bg_color": "bg-red-500/10", "features": ["100% Légal Google", "SEO Power", "Retention Max"] },
        { "id": 66, "title": "YouTube Shorts Views [Viral]", "description": "Boostez vos Shorts pour atteindre des millions de vues.", "price": 0.25, "unit": "1000", "category": "YouTube", "platform": "YouTube", "min_quantity": 1000, "max_quantity": 5000000, "icon_name": "YoutubeIcon", "color": "text-red-500", "bg_color": "bg-red-500/10", "features": ["Shorts Feed", "Instantané", "Sûr"] },
        { "id": 67, "title": "YouTube Live Stream [1 Hour]", "description": "Spectateurs pour vos diffusions en direct.", "price": 18.00, "unit": "1000", "category": "YouTube", "platform": "YouTube", "min_quantity": 100, "max_quantity": 2000, "icon_name": "YoutubeIcon", "color": "text-red-500", "bg_color": "bg-red-500/10", "features": ["Stable Live", "Fast Start", "Safe"] },
        { "id": 68, "title": "YouTube Dislikes [Targeted]", "description": "Envoyez des avis négatifs (usage stratégique).", "price": 4.50, "unit": "1000", "category": "YouTube", "platform": "YouTube", "min_quantity": 50, "max_quantity": 5000, "icon_name": "YoutubeIcon", "color": "text-red-500", "bg_color": "bg-red-500/10", "features": ["Strategic Use", "Stable", "Safe"] },

        # Facebook
        { "id": 18, "title": "Facebook Page Likes + Followers", "description": "Développez la crédibilité de votre page Facebook.", "price": 9.50, "unit": "1000", "category": "Facebook", "platform": "Facebook", "min_quantity": 100, "max_quantity": 50000, "icon_name": "FacebookIcon", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "features": ["Likes Pro", "Followers Inclus", "Stable"] },
        { "id": 19, "title": "Facebook Post Likes [EMOJIS]", "description": "Réactions (Love, Haha, Wow) sur vos publications.", "price": 1.80, "unit": "1000", "category": "Facebook", "platform": "Facebook", "min_quantity": 50, "max_quantity": 20000, "icon_name": "FacebookIcon", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "features": ["Réactions Mixtes", "Instantané", "Discret"] },
        { "id": 20, "title": "Facebook Video Views", "description": "Vues pour vos vidéos et Facebook Watch.", "price": 0.90, "unit": "1000", "category": "Facebook", "platform": "Facebook", "min_quantity": 500, "max_quantity": 1000000, "icon_name": "FacebookIcon", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "features": ["Ads Monetization", "Global Reach", "High Speed"] },
        { "id": 37, "title": "Facebook Group Members", "description": "Augmentez la taille de votre groupe Facebook.", "price": 12.00, "unit": "1000", "category": "Facebook", "platform": "Facebook", "min_quantity": 100, "max_quantity": 20000, "icon_name": "FacebookIcon", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "features": ["Public/Privé OK", "Stable", "Safe"] },
        { "id": 46, "title": "Facebook Live Stream Views", "description": "Spectateurs pour vos sessions Live Facebook.", "price": 12.00, "unit": "500", "category": "Facebook", "platform": "Facebook", "min_quantity": 50, "max_quantity": 2000, "icon_name": "FacebookIcon", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "features": ["Stable Live", "Instant Start", "Global Reach"] },
        { "id": 76, "title": "Facebook Profile Followers", "description": "Abonnés pour votre profil personnel Facebook.", "price": 5.50, "unit": "1000", "category": "Facebook", "platform": "Facebook", "min_quantity": 100, "max_quantity": 50000, "icon_name": "FacebookIcon", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "features": ["Real Profiles", "High Retention", "Secure"] },
        { "id": 77, "title": "Facebook Review [5 Stars]", "description": "Avis positifs pour votre page ou établissement.", "price": 1.50, "unit": "avis", "category": "Facebook", "platform": "Facebook", "min_quantity": 1, "max_quantity": 10, "icon_name": "FacebookIcon", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "features": ["Verified Quality", "Custom Text", "Safe"] },

        # Twitter
        { "id": 21, "title": "Twitter Followers [Premium]", "description": "Abonnés pour votre profil X avec garantie.", "price": 12.00, "unit": "1000", "category": "Twitter", "platform": "Twitter", "min_quantity": 100, "max_quantity": 25000, "icon_name": "TwitterIcon", "color": "text-sky-400", "bg_color": "bg-sky-500/10", "features": ["Garantie 30j", "Profils avec Photo", "Sûr"] },
        { "id": 22, "title": "Twitter Retweets [Viral]", "description": "Boostez la portée de vos Tweets instantanément.", "price": 3.50, "unit": "1000", "category": "Twitter", "platform": "Twitter", "min_quantity": 50, "max_quantity": 10000, "icon_name": "TwitterIcon", "color": "text-sky-400", "bg_color": "bg-sky-500/10", "features": ["Instant Speed", "Global Users", "Safe"] },
        { "id": 23, "title": "Twitter Likes [X Boost]", "description": "Likes de haute qualité pour vos statuts.", "price": 1.90, "unit": "1000", "category": "Twitter", "platform": "Twitter", "min_quantity": 50, "max_quantity": 20000, "icon_name": "TwitterIcon", "color": "text-sky-400", "bg_color": "bg-sky-500/10", "features": ["Fast Delivery", "Stable", "Unlimited"] },
        { "id": 38, "title": "Twitter Views [Impression Boost]", "description": "Améliorez vos statistiques X pour la monétisation.", "price": 0.05, "unit": "1000", "category": "Twitter", "platform": "Twitter", "min_quantity": 1000, "max_quantity": 10000000, "icon_name": "TwitterIcon", "color": "text-sky-400", "bg_color": "bg-sky-500/10", "features": ["Stats Ads", "Ultra Cheap", "Viral Boost"] },
        { "id": 86, "title": "Twitter Poll Votes", "description": "Votes pour vos sondages Twitter/X.", "price": 1.20, "unit": "1000", "category": "Twitter", "platform": "Twitter", "min_quantity": 100, "max_quantity": 50000, "icon_name": "TwitterIcon", "color": "text-sky-400", "bg_color": "bg-sky-500/10", "features": ["Custom Choice", "Fast", "Safe"] },

        # Snapchat
        { "id": 24, "title": "Snapchat Followers [Public]", "description": "Followers pour profils publics Snapchat.", "price": 25.00, "unit": "1000", "category": "Snapchat", "platform": "Snapchat", "min_quantity": 50, "max_quantity": 5000, "icon_name": "SnapchatIcon", "color": "text-yellow-400", "bg_color": "bg-yellow-500/10", "features": ["New Tech", "Profils Réels", "High Quality"] },
        { "id": 25, "title": "Snapchat Spotlight Views", "description": "Vues sur vos vidéos Spotlight pour percer.", "price": 1.50, "unit": "1000", "category": "Snapchat", "platform": "Snapchat", "min_quantity": 1000, "max_quantity": 1000000, "icon_name": "SnapchatIcon", "color": "text-yellow-400", "bg_color": "bg-yellow-500/10", "features": ["Viral Chance", "Fast Delivery", "No Passwort"] },
        { "id": 47, "title": "Snapchat Discovery Boost", "description": "Mise en avant de votre Story dans Discover.", "price": 150.00, "unit": "j", "category": "Snapchat", "platform": "Snapchat", "min_quantity": 1, "max_quantity": 30, "icon_name": "SnapchatIcon", "color": "text-yellow-400", "bg_color": "bg-yellow-500/10", "features": ["High Exposure", "Mass Reach", "Exclusive"] },

        # Telegram
        { "id": 26, "title": "Telegram Channel Members", "description": "Membres stables pour votre canal ou groupe.", "price": 1.20, "unit": "1000", "category": "Telegram", "platform": "Telegram", "min_quantity": 100, "max_quantity": 100000, "icon_name": "TelegramIcon", "color": "text-sky-500", "bg_color": "bg-sky-500/10", "features": ["Non-Drop", "Global Members", "Auto-Refill"] },
        { "id": 27, "title": "Telegram Post Views", "description": "Vues sur vos derniers messages Telegram.", "price": 0.05, "unit": "1000", "category": "Telegram", "platform": "Telegram", "min_quantity": 100, "max_quantity": 1000000, "icon_name": "TelegramIcon", "color": "text-sky-500", "bg_color": "bg-sky-500/10", "features": ["One-Time Speed", "Cheap", "Reliable"] },
        { "id": 28, "title": "Telegram Reations [Premium]", "description": "Réactions Premium sur vos posts Telegram.", "price": 2.50, "unit": "100", "category": "Telegram", "platform": "Telegram", "min_quantity": 10, "max_quantity": 1000, "icon_name": "TelegramIcon", "color": "text-sky-500", "bg_color": "bg-sky-500/10", "features": ["Premium Users", "Custom Emojis", "Slow/Fast"] },
        { "id": 39, "title": "Telegram Members [Real Active]", "description": "Utilisateurs réels pour votre groupe Telegram.", "price": 10.00, "unit": "1000", "category": "Telegram", "platform": "Telegram", "min_quantity": 50, "max_quantity": 5000, "icon_name": "TelegramIcon", "color": "text-sky-500", "bg_color": "bg-sky-500/10", "features": ["Real Users", "Slow Delivery", "No Ban"] },
        { "id": 48, "title": "Telegram Voice Chat Members", "description": "Utilisateurs qui rejoignent votre chat vocal.", "price": 15.50, "unit": "500", "category": "Telegram", "platform": "Telegram", "min_quantity": 50, "max_quantity": 1000, "icon_name": "TelegramIcon", "color": "text-sky-500", "bg_color": "bg-sky-500/10", "features": ["Audio Engagement", "Stable", "Fast"] },

        # Discord
        { "id": 29, "title": "Discord Server Members", "description": "Membres réels ou bots pour votre serveur.", "price": 8.00, "unit": "1000", "category": "Discord", "platform": "Discord", "min_quantity": 50, "max_quantity": 5000, "icon_name": "DiscordIcon", "color": "text-indigo-400", "bg_color": "bg-indigo-500/10", "features": ["Semi-Real", "Offline/Online", "Stable"] },
        { "id": 30, "title": "Discord Post Reactions", "description": "Réactions emojis sur vos messages Discord.", "price": 3.50, "unit": "100", "category": "Discord", "platform": "Discord", "min_quantity": 10, "max_quantity": 1000, "icon_name": "DiscordIcon", "color": "text-indigo-400", "bg_color": "bg-indigo-500/10", "features": ["Any Emoji", "Custom Speed", "Secure"] },
        { "id": 40, "title": "Discord Server Boost [Lvl 3]", "description": "Boostez votre serveur au niveau maximum.", "price": 35.00, "unit": "pack", "category": "Discord", "platform": "Discord", "min_quantity": 1, "max_quantity": 1, "icon_name": "DiscordIcon", "color": "text-indigo-400", "bg_color": "bg-indigo-500/10", "features": ["Level 3 Boost", "Nitro Features", "Instant"] },

        # Spotify
        { "id": 106, "title": "Spotify Artist Followers", "description": "Augmentez le nombre de followers sur votre profil artiste.", "price": 2.50, "unit": "1000", "category": "Spotify", "platform": "Spotify", "min_quantity": 100, "max_quantity": 50000, "icon_name": "MusicIcon", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "features": ["Artist Boost", "Safe", "Stable"] },
        { "id": 107, "title": "Spotify Track Plays [USA]", "description": "Écoutes provenant exclusivement d'utilisateurs aux USA.", "price": 1.90, "unit": "1000", "category": "Spotify", "platform": "Spotify", "min_quantity": 1000, "max_quantity": 1000000, "icon_name": "MusicIcon", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "features": ["Royalty Eligible", "Safe", "GEO-Targeted"] },
        { "id": 108, "title": "Spotify Playlist Followers", "description": "Boostez la popularité de vos playlists Spotify.", "price": 0.80, "unit": "1000", "category": "Spotify", "platform": "Spotify", "min_quantity": 100, "max_quantity": 50000, "icon_name": "MusicIcon", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "features": ["Curator Growth", "Fast", "Secure"] },
        { "id": 109, "title": "Spotify Podcast Plays", "description": "Augmentez les écoutes pour vos épisodes de podcast.", "price": 3.50, "unit": "1000", "category": "Spotify", "platform": "Spotify", "min_quantity": 500, "max_quantity": 100000, "icon_name": "MusicIcon", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "features": ["Podcast Feed", "Algorithm", "Engagement"] },

        # Twitch
        { "id": 110, "title": "Twitch Channel Followers", "description": "Abonnés pour votre chaîne Twitch.", "price": 2.50, "unit": "1000", "category": "Twitch", "platform": "Twitch", "min_quantity": 100, "max_quantity": 10000, "icon_name": "TwitchIcon", "color": "text-purple-500", "bg_color": "bg-purple-500/10", "features": ["Fast Delivery", "Stable", "Safe"] },
        { "id": 111, "title": "Twitch Live Viewers [1 Hour]", "description": "Spectateurs en direct pour vos streams.", "price": 15.00, "unit": "1000", "category": "Twitch", "platform": "Twitch", "min_quantity": 50, "max_quantity": 2000, "icon_name": "TwitchIcon", "color": "text-purple-500", "bg_color": "bg-purple-500/10", "features": ["Affiliate Ready", "Instant Start", "Stable"] },
        { "id": 112, "title": "Twitch Clip Views", "description": "Boostez les vues de vos meilleurs moments.", "price": 0.50, "unit": "1000", "category": "Twitch", "platform": "Twitch", "min_quantity": 1000, "max_quantity": 100000, "icon_name": "TwitchIcon", "color": "text-purple-500", "bg_color": "bg-purple-500/10", "features": ["Viral Clips", "Fast", "High Quality"] },

        # SEO & Web
        { "id": 31, "title": "Traffic Web Premium", "description": "Visiteurs réels du pays de votre choix.", "price": 0.99, "unit": "1000", "category": "SEO", "platform": "Web", "min_quantity": 1000, "max_quantity": 1000000, "icon_name": "Globe", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "features": ["Ciblage Géo", "Google Analytics OK", "Stable"] },
        { "id": 32, "title": "Backlinks SEO Autorité", "description": "Liens depuis des sites DR 50+ pour booster Google.", "price": 49.00, "unit": "pack", "category": "SEO", "platform": "Web", "min_quantity": 1, "max_quantity": 1, "icon_name": "Zap", "color": "text-purple-400", "bg_color": "bg-purple-500/10", "features": ["Montez en Rank", "Dofollow", "Permanent"] },
        { "id": 49, "title": "Trustpilot Reviews [5 Stars]", "description": "Avis vérifiés pour votre page Trustpilot.", "price": 45.00, "unit": "10", "category": "SEO", "platform": "Web", "min_quantity": 1, "max_quantity": 10, "icon_name": "StarIcon", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "features": ["Vérifié", "Pas de Suppression", "Premium"] },
        { "id": 50, "title": "Google Maps Reviews", "description": "Boostez la réputation de votre établissement local.", "price": 55.00, "unit": "10", "category": "SEO", "platform": "Web", "min_quantity": 1, "max_quantity": 10, "icon_name": "Globe", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "features": ["Local Guides", "Géo-Ciblé", "Sûr"] },
        { "id": 113, "title": "SEO Audit Complete [IA]", "description": "Rapport détaillé sur les failles de votre site.", "price": 19.00, "unit": "audit", "category": "SEO", "platform": "Web", "min_quantity": 1, "max_quantity": 1, "icon_name": "Zap", "color": "text-purple-400", "bg_color": "bg-purple-500/10", "features": ["Deep Scan", "IA Recommendations", "Action Plan"] },
    ]

    # To avoid primary key conflicts if some already exist, we can use a merge-like approach
    count = 0
    for s_data in services_data:
        existing = db.query(models.Service).filter(models.Service.id == s_data["id"]).first()
        if existing:
            # Update existing one
            existing.title = s_data["title"]
            existing.description = s_data["description"]
            existing.price = s_data["price"]
            existing.unit = s_data["unit"]
            existing.category = s_data["category"]
            existing.platform = s_data["platform"]
            existing.min_quantity = s_data["min_quantity"]
            existing.max_quantity = s_data["max_quantity"]
            existing.icon_name = s_data["icon_name"]
            existing.color = s_data["color"]
            existing.bg_color = s_data["bg_color"]
            existing.features = s_data["features"]
        else:
            # Create new
            service = models.Service(
                id=s_data["id"],
                title=s_data["title"],
                description=s_data["description"],
                price=s_data["price"],
                unit=s_data["unit"],
                category=s_data["category"],
                platform=s_data["platform"],
                min_quantity=s_data["min_quantity"],
                max_quantity=s_data["max_quantity"],
                icon_name=s_data["icon_name"],
                color=s_data["color"],
                bg_color=s_data["bg_color"],
                features=s_data["features"]
            )
            db.add(service)
        count += 1
    
    db.commit()
    print(f"Successfully seeded/synchronized {count} services.")
    db.close()

if __name__ == "__main__":
    seed_services()
