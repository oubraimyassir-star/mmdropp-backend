import json
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from datetime import datetime

# Services Data from Frontend
INITIAL_SERVICES = [
    # INSTAGRAM
    { "id": 1, "title": "Instagram Followers [Premium]", "description": "Abonnés de haute qualité, profil réel, garantie 30 jours.", "price": 2.49, "unit": "1000", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Haute Qualité", "Garantie 30j", "Vitesse Rapide"], "min_quantity": 100, "max_quantity": 100000 },
    { "id": 2, "title": "Instagram Likes [Vrais]", "description": "Likes instantanés de profils actifs, sans perte.", "price": 0.89, "unit": "1000", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Instantané", "Profils Réels", "Sans Perte"], "min_quantity": 50, "max_quantity": 50000 },
    { "id": 3, "title": "Instagram Views [Reels]", "description": "Vues pour vos Reels avec une excellente rétention.", "price": 0.15, "unit": "1000", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Max Rétention", "Viral Boost", "Pas de Mot de Passe"], "min_quantity": 100, "max_quantity": 1000000 },
    { "id": 4, "title": "Instagram Auto-Likes [Mensuel]", "description": "Likes automatiques sur chaque nouvelle publication.", "price": 19.99, "unit": "mois", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Bot Automatisé", "Engagement Continu", "Support 24/7"], "min_quantity": 1, "max_quantity": 1 },
    { "id": 5, "title": "Instagram Comments [Custom]", "description": "Commentaires personnalisés rédigés par vous ou par IA.", "price": 5.50, "unit": "50", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Texte Libre", "Ciblage Langue", "Modération"], "min_quantity": 10, "max_quantity": 1000 },
    { "id": 6, "title": "Instagram Story Views", "description": "Vues sur vos stories Instagram pour booster la visibilité.", "price": 0.50, "unit": "1000", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Instantané", "Discret", "Pas de Perte"], "min_quantity": 100, "max_quantity": 20000 },
    { "id": 7, "title": "Instagram Profile Visits", "description": "Bousculez l'algorithme avec des visites de profil réelles.", "price": 1.20, "unit": "1000", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Algorithme Boost", "Provenance Mondiale", "Légal"], "min_quantity": 100, "max_quantity": 50000 },
    { "id": 33, "title": "Instagram Followers [Élite]", "description": "Abonnés ultra-premium, garantie à vie, profils européens.", "price": 12.50, "unit": "1000", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Garantie à vie", "Ciblage UE", "Service Élite"], "min_quantity": 50, "max_quantity": 25000 },
    { "id": 34, "title": "Instagram Likes [Vitesse Éclair]", "description": "100k likes délivrés en moins de 10 minutes.", "price": 0.50, "unit": "1000", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Ultra Rapide", "Pas cher", "Stable"], "min_quantity": 100, "max_quantity": 100000 },
    { "id": 41, "title": "Instagram Power Likes", "description": "Likes de comptes avec plus de 50k abonnés.", "price": 45.00, "unit": "100", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Explorer Boost", "Haut Authority", "Viral"], "min_quantity": 10, "max_quantity": 1000 },
    { "id": 44, "title": "Instagram Live Stream Views", "description": "Spectateurs en direct pendant que vous diffusez.", "price": 15.00, "unit": "1000", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Démarrage 0-5min", "Reste 60min", "Stable"], "min_quantity": 100, "max_quantity": 5000 },
    { "id": 53, "title": "Instagram Save [Algorithm]", "description": "Enregistrements pour booster le SEO de vos posts.", "price": 0.40, "unit": "1000", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Algorithm Secret", "Growth Hack", "Sûr"], "min_quantity": 100, "max_quantity": 100000 },
    { "id": 54, "title": "Instagram Mentions [Targeted]", "description": "Mentionnez des utilisateurs sur vos photos de manière massive.", "price": 25.00, "unit": "1000", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Ciblage Précis", "Viralité", "Pro-User"], "min_quantity": 100, "max_quantity": 10000 },
    { "id": 55, "title": "Instagram TV Views", "description": "Boostez vos vidéos IGTV (Legacy support).", "price": 0.10, "unit": "1000", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Instantané", "Discret", "Stable"], "min_quantity": 100, "max_quantity": 100000 },
    { "id": 56, "title": "Instagram DM Mass Sending", "description": "Envoi massif de messages direct à votre audience cible.", "price": 55.00, "unit": "1000", "icon_name": "Instagram", "color": "text-pink-400", "bg_color": "bg-pink-500/10", "category": "Instagram", "platform": "Instagram", "features": ["Lead Gen", "Custom Text", "High Conversion"], "min_quantity": 500, "max_quantity": 50000 },

    # TIKTOK
    { "id": 8, "title": "TikTok Followers [Real]", "description": "Abonnés TikTok stables pour augmenter votre autorité.", "price": 4.99, "unit": "1000", "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "category": "TikTok", "platform": "TikTok", "features": ["Profils Actifs", "Safe & Secure", "Livraison Rapide"], "min_quantity": 100, "max_quantity": 100000 },
    { "id": 9, "title": "TikTok Likes [Instant]", "description": "Boostez l'engagement de vos vidéos TikTok instantanément.", "price": 1.20, "unit": "1000", "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "category": "TikTok", "platform": "TikTok", "features": ["Pas de Chute", "Support 24/7", "Premium Apparence"], "min_quantity": 100, "max_quantity": 50000 },
    { "id": 10, "title": "TikTok Views [For You Page]", "description": "Vues ciblées pour aider à passer dans les 'Pour Toi'.", "price": 0.10, "unit": "1000", "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "category": "TikTok", "platform": "TikTok", "features": ["FYP Boost", "Rétention Elevée", "Service sûr"], "min_quantity": 1000, "max_quantity": 10000000 },
    { "id": 11, "title": "TikTok Shares [Viral]", "description": "Partages réels pour rendre vos vidéos virales.", "price": 0.75, "unit": "1000", "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "category": "TikTok", "platform": "TikTok", "features": ["Growth Hack", "Engagement Pro", "Instantané"], "min_quantity": 100, "max_quantity": 50000 },
    { "id": 12, "title": "TikTok Save [Boost]", "description": "Enregistrements de vidéos pour tromper l'algorithme.", "price": 0.60, "unit": "1000", "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "category": "TikTok", "platform": "TikTok", "features": ["SEO Video", "Secret Boost", "Stable"], "min_quantity": 100, "max_quantity": 50000 },
    { "id": 35, "title": "TikTok Followers [Arab Fans]", "description": "Abonnés TikTok avec profils et noms arabes.", "price": 7.99, "unit": "1000", "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "category": "TikTok", "platform": "TikTok", "features": ["Ciblage Arabe", "Vrais Profils", "Garantie 30j"], "min_quantity": 50, "max_quantity": 10000 },
    { "id": 42, "title": "TikTok Shares [France Only]", "description": "Partages réels provenant d'utilisateurs en France.", "price": 5.50, "unit": "1000", "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "category": "TikTok", "platform": "TikTok", "features": ["Ciblage FR", "Rétention Locale", "Viral"], "min_quantity": 50, "max_quantity": 5000 },
    { "id": 57, "title": "TikTok Live Stream [Concurrent]", "description": "Spectateurs stables pour vos lives TikTok.", "price": 12.00, "unit": "500", "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "category": "TikTok", "platform": "TikTok", "features": ["Stable Live", "Instant", "Algorithm Boost"], "min_quantity": 100, "max_quantity": 2000 },
    { "id": 58, "title": "TikTok Comments [AI Custom]", "description": "Commentaires intelligents rédigés par IA sur vos vidéos.", "price": 8.50, "unit": "100", "icon_name": "Video", "color": "text-cyan-400", "bg_color": "bg-cyan-500/10", "category": "TikTok", "platform": "TikTok", "features": ["Natural Text", "Safe", "Fast"], "min_quantity": 10, "max_quantity": 500 },

    # YOUTUBE
    { "id": 13, "title": "YouTube Subscribers [No Drop]", "description": "Abonnés YouTube de haute qualité avec garantie à vie.", "price": 15.00, "unit": "1000", "icon_name": "Youtube", "color": "text-red-500", "bg_color": "bg-red-500/10", "category": "YouTube", "platform": "YouTube", "features": ["Anti-Drop", "Sécurisé ADS", "Monétisation OK"], "min_quantity": 100, "max_quantity": 10000 },
    { "id": 14, "title": "YouTube High Retention Views", "description": "Vues optimisées pour la monétisation et le SEO.", "price": 3.50, "unit": "1000", "icon_name": "Youtube", "color": "text-red-500", "bg_color": "bg-red-500/10", "category": "YouTube", "platform": "YouTube", "features": ["Retention 60s+", "SEO Optimized", "ADS Safe"], "min_quantity": 1000, "max_quantity": 1000000 },
    { "id": 15, "title": "YouTube Watch Time [4000H]", "description": "Heures de visionnage pour activer la monétisation.", "price": 89.00, "unit": "pack", "icon_name": "Youtube", "color": "text-red-500", "bg_color": "bg-red-500/10", "category": "YouTube", "platform": "YouTube", "features": ["Monetization Ready", "Qualité Max", "Support Dédié"], "min_quantity": 1, "max_quantity": 1 },
    { "id": 16, "title": "YouTube Likes [Non-Drop]", "description": "Likes stables pour vos vidéos YouTube.", "price": 2.10, "unit": "1000", "icon_name": "Youtube", "color": "text-red-500", "bg_color": "bg-red-500/10", "category": "YouTube", "platform": "YouTube", "features": ["Garantie 60j", "Livraison Naturelle", "Profils Réels"], "min_quantity": 100, "max_quantity": 50000 },
    { "id": 17, "title": "YouTube Comments [AI]", "description": "Commentaires intelligents adaptés à votre contenu.", "price": 12.00, "unit": "100", "icon_name": "Youtube", "color": "text-red-500", "bg_color": "bg-red-500/10", "category": "YouTube", "platform": "YouTube", "features": ["Rédigé par IA", "Mots-clés SEO", "Naturel"], "min_quantity": 5, "max_quantity": 500 },
    { "id": 36, "title": "YouTube Subscribers [USA Targeting]", "description": "Subscribers provenant exclusivement des USA.", "price": 45.00, "unit": "1000", "icon_name": "Youtube", "color": "text-red-500", "bg_color": "bg-red-500/10", "category": "YouTube", "platform": "YouTube", "features": ["Geo-Targeted", "High Authority", "Safe"], "min_quantity": 50, "max_quantity": 5000 },
    { "id": 43, "title": "YouTube Views [AdWords Method]", "description": "Vues réelles via le réseau Google Ads.", "price": 8.50, "unit": "1000", "icon_name": "Youtube", "color": "text-red-500", "bg_color": "bg-red-500/10", "category": "YouTube", "platform": "YouTube", "features": ["100% Légal Google", "SEO Power", "Retention Max"], "min_quantity": 500, "max_quantity": 100000 },
    { "id": 66, "title": "YouTube Shorts Views [Viral]", "description": "Boostez vos Shorts pour atteindre des millions de vues.", "price": 0.25, "unit": "1000", "icon_name": "Youtube", "color": "text-red-500", "bg_color": "bg-red-500/10", "category": "YouTube", "platform": "YouTube", "features": ["Shorts Feed", "Instantané", "Sûr"], "min_quantity": 1000, "max_quantity": 5000000 },
    { "id": 67, "title": "YouTube Live Stream [1 Hour]", "description": "Spectateurs pour vos diffusions en direct.", "price": 18.00, "unit": "1000", "icon_name": "Youtube", "color": "text-red-500", "bg_color": "bg-red-500/10", "category": "YouTube", "platform": "YouTube", "features": ["Stable Live", "Fast Start", "Safe"], "min_quantity": 100, "max_quantity": 2000 },
    { "id": 68, "title": "YouTube Dislikes [Targeted]", "description": "Envoyez des avis négatifs (usage stratégique).", "price": 4.50, "unit": "1000", "icon_name": "Youtube", "color": "text-red-500", "bg_color": "bg-red-500/10", "category": "YouTube", "platform": "YouTube", "features": ["Strategic Use", "Stable", "Safe"], "min_quantity": 50, "max_quantity": 5000 },

    # FACEBOOK
    { "id": 18, "title": "Facebook Page Likes + Followers", "description": "Développez la crédibilité de votre page Facebook.", "price": 9.50, "unit": "1000", "icon_name": "Facebook", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "category": "Facebook", "platform": "Facebook", "features": ["Likes Pro", "Followers Inclus", "Stable"], "min_quantity": 100, "max_quantity": 50000 },
    { "id": 19, "title": "Facebook Post Likes [EMOJIS]", "description": "Réactions (Love, Haha, Wow) sur vos publications.", "price": 1.80, "unit": "1000", "icon_name": "Facebook", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "category": "Facebook", "platform": "Facebook", "features": ["Réactions Mixtes", "Instantané", "Discret"], "min_quantity": 50, "max_quantity": 20000 },
    { "id": 20, "title": "Facebook Video Views", "description": "Vues pour vos vidéos et Facebook Watch.", "price": 0.90, "unit": "1000", "icon_name": "Facebook", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "category": "Facebook", "platform": "Facebook", "features": ["Ads Monetization", "Global Reach", "High Speed"], "min_quantity": 500, "max_quantity": 1000000 },
    { "id": 37, "title": "Facebook Group Members", "description": "Augmentez la taille de votre groupe Facebook.", "price": 12.00, "unit": "1000", "icon_name": "Facebook", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "category": "Facebook", "platform": "Facebook", "features": ["Public/Privé OK", "Stable", "Safe"], "min_quantity": 100, "max_quantity": 20000 },
    { "id": 46, "title": "Facebook Live Stream Views", "description": "Spectateurs pour vos sessions Live Facebook.", "price": 12.00, "unit": "500", "icon_name": "Facebook", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "category": "Facebook", "platform": "Facebook", "features": ["Stable Live", "Instant Start", "Global Reach"], "min_quantity": 50, "max_quantity": 2000 },
    { "id": 76, "title": "Facebook Profile Followers", "description": "Abonnés pour votre profil personnel Facebook.", "price": 5.50, "unit": "1000", "icon_name": "Facebook", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "category": "Facebook", "platform": "Facebook", "features": ["Real Profiles", "High Retention", "Secure"], "min_quantity": 100, "max_quantity": 50000 },
    { "id": 77, "title": "Facebook Review [5 Stars]", "description": "Avis positifs pour votre page ou établissement.", "price": 1.50, "unit": "avis", "icon_name": "Facebook", "color": "text-blue-500", "bg_color": "bg-blue-500/10", "category": "Facebook", "platform": "Facebook", "features": ["Verified Quality", "Custom Text", "Safe"], "min_quantity": 1, "max_quantity": 10 },

    # TWITTER
    { "id": 21, "title": "Twitter Followers [Premium]", "description": "Abonnés pour votre profil X avec garantie.", "price": 12.00, "unit": "1000", "icon_name": "Hash", "color": "text-sky-400", "bg_color": "bg-sky-500/10", "category": "Twitter", "platform": "Twitter", "features": ["Garantie 30j", "Profils avec Photo", "Sûr"], "min_quantity": 100, "max_quantity": 25000 },
    { "id": 22, "title": "Twitter Retweets [Viral]", "description": "Boostez la portée de vos Tweets instantanément.", "price": 3.50, "unit": "1000", "icon_name": "Hash", "color": "text-sky-400", "bg_color": "bg-sky-500/10", "category": "Twitter", "platform": "Twitter", "features": ["Instant Speed", "Global Users", "Safe"], "min_quantity": 50, "max_quantity": 10000 },
    { "id": 23, "title": "Twitter Likes [X Boost]", "description": "Likes de haute qualité pour vos statuts.", "price": 1.90, "unit": "1000", "icon_name": "Hash", "color": "text-sky-400", "bg_color": "bg-sky-500/10", "category": "Twitter", "platform": "Twitter", "features": ["Fast Delivery", "Stable", "Unlimited"], "min_quantity": 50, "max_quantity": 20000 },
    { "id": 38, "title": "Twitter Views [Impression Boost]", "description": "Améliorez vos statistiques X pour la monétisation.", "price": 0.05, "unit": "1000", "icon_name": "Hash", "color": "text-sky-400", "bg_color": "bg-sky-500/10", "category": "Twitter", "platform": "Twitter", "features": ["Stats Ads", "Ultra Cheap", "Viral Boost"], "min_quantity": 1000, "max_quantity": 10000000 },
    { "id": 86, "title": "Twitter Poll Votes", "description": "Votes pour vos sondages Twitter/X.", "price": 1.20, "unit": "1000", "icon_name": "Hash", "color": "text-sky-400", "bg_color": "bg-sky-500/10", "category": "Twitter", "platform": "Twitter", "features": ["Custom Choice", "Fast", "Safe"], "min_quantity": 100, "max_quantity": 50000 },

    # SNAPCHAT
    { "id": 24, "title": "Snapchat Followers [Public]", "description": "Followers pour profils publics Snapchat.", "price": 25.00, "unit": "1000", "icon_name": "MessageCircle", "color": "text-yellow-400", "bg_color": "bg-yellow-500/10", "category": "Snapchat", "platform": "Snapchat", "features": ["New Tech", "Profils Réels", "High Quality"], "min_quantity": 50, "max_quantity": 5000 },
    { "id": 25, "title": "Snapchat Spotlight Views", "description": "Vues sur vos vidéos Spotlight pour percer.", "price": 1.50, "unit": "1000", "icon_name": "MessageCircle", "color": "text-yellow-400", "bg_color": "bg-yellow-500/10", "category": "Snapchat", "platform": "Snapchat", "features": ["Viral Chance", "Fast Delivery", "No Passwort"], "min_quantity": 1000, "max_quantity": 1000000 },
    { "id": 47, "title": "Snapchat Discovery Boost", "description": "Mise en avant de votre Story dans Discover.", "price": 150.00, "unit": "j", "icon_name": "MessageCircle", "color": "text-yellow-400", "bg_color": "bg-yellow-500/10", "category": "Snapchat", "platform": "Snapchat", "features": ["High Exposure", "Mass Reach", "Exclusive"], "min_quantity": 1, "max_quantity": 30 },

    # TELEGRAM
    { "id": 26, "title": "Telegram Channel Members", "description": "Membres stables pour votre canal ou groupe.", "price": 1.20, "unit": "1000", "icon_name": "Send", "color": "text-sky-500", "bg_color": "bg-sky-500/10", "category": "Telegram", "platform": "Telegram", "features": ["Non-Drop", "Global Members", "Auto-Refill"], "min_quantity": 100, "max_quantity": 100000 },
    { "id": 27, "title": "Telegram Post Views", "description": "Vues sur vos derniers messages Telegram.", "price": 0.05, "unit": "1000", "icon_name": "Send", "color": "text-sky-500", "bg_color": "bg-sky-500/10", "category": "Telegram", "platform": "Telegram", "features": ["One-Time Speed", "Cheap", "Reliable"], "min_quantity": 100, "max_quantity": 1000000 },
    { "id": 28, "title": "Telegram Reations [Premium]", "description": "Réactions Premium sur vos posts Telegram.", "price": 2.50, "unit": "100", "icon_name": "Send", "color": "text-sky-500", "bg_color": "bg-sky-500/10", "category": "Telegram", "platform": "Telegram", "features": ["Premium Users", "Custom Emojis", "Slow/Fast"], "min_quantity": 10, "max_quantity": 1000 },
    { "id": 39, "title": "Telegram Members [Real Active]", "description": "Utilisateurs réels pour votre groupe Telegram.", "price": 10.00, "unit": "1000", "icon_name": "Send", "color": "text-sky-500", "bg_color": "bg-sky-500/10", "category": "Telegram", "platform": "Telegram", "features": ["Real Users", "Slow Delivery", "No Ban"], "min_quantity": 50, "max_quantity": 5000 },
    { "id": 48, "title": "Telegram Voice Chat Members", "description": "Utilisateurs qui rejoignent votre chat vocal.", "price": 15.50, "unit": "500", "icon_name": "Send", "color": "text-sky-500", "bg_color": "bg-sky-500/10", "category": "Telegram", "platform": "Telegram", "features": ["Audio Engagement", "Stable", "Fast"], "min_quantity": 50, "max_quantity": 1000 },

    # DISCORD
    { "id": 29, "title": "Discord Server Members", "description": "Membres réels ou bots pour votre serveur.", "price": 8.00, "unit": "1000", "icon_name": "Disc", "color": "text-indigo-400", "bg_color": "bg-indigo-500/10", "category": "Discord", "platform": "Discord", "features": ["Semi-Real", "Offline/Online", "Stable"], "min_quantity": 50, "max_quantity": 5000 },
    { "id": 30, "title": "Discord Post Reactions", "description": "Réactions emojis sur vos messages Discord.", "price": 3.50, "unit": "100", "icon_name": "Disc", "color": "text-indigo-400", "bg_color": "bg-indigo-500/10", "category": "Discord", "platform": "Discord", "features": ["Any Emoji", "Custom Speed", "Secure"], "min_quantity": 10, "max_quantity": 1000 },
    { "id": 40, "title": "Discord Server Boost [Lvl 3]", "description": "Boostez votre serveur au niveau maximum.", "price": 35.00, "unit": "pack", "icon_name": "Disc", "color": "text-indigo-400", "bg_color": "bg-indigo-500/10", "category": "Discord", "platform": "Discord", "features": ["Level 3 Boost", "Nitro Features", "Instant"], "min_quantity": 1, "max_quantity": 1 },

    # SPOTIFY
    { "id": 106, "title": "Spotify Artist Followers", "description": "Augmentez le nombre de followers sur votre profil artiste.", "price": 2.50, "unit": "1000", "icon_name": "Music", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "category": "Spotify", "platform": "Spotify", "features": ["Artist Boost", "Safe", "Stable"], "min_quantity": 100, "max_quantity": 50000 },
    { "id": 107, "title": "Spotify Track Plays [USA]", "description": "Écoutes provenant exclusivement d'utilisateurs aux USA.", "price": 1.90, "unit": "1000", "icon_name": "Music", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "category": "Spotify", "platform": "Spotify", "features": ["Royalty Eligible", "Safe", "GEO-Targeted"], "min_quantity": 1000, "max_quantity": 1000000 },
    { "id": 108, "title": "Spotify Playlist Followers", "description": "Boostez la popularité de vos playlists Spotify.", "price": 0.80, "unit": "1000", "icon_name": "Music", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "category": "Spotify", "platform": "Spotify", "features": ["Curator Growth", "Fast", "Secure"], "min_quantity": 100, "max_quantity": 50000 },
    { "id": 109, "title": "Spotify Podcast Plays", "description": "Augmentez les écoutes pour vos épisodes de podcast.", "price": 3.50, "unit": "1000", "icon_name": "Music", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "category": "Spotify", "platform": "Spotify", "features": ["Podcast Feed", "Algorithm", "Engagement"], "min_quantity": 500, "max_quantity": 100000 },

    # TWITCH
    { "id": 110, "title": "Twitch Channel Followers", "description": "Abonnés pour votre chaîne Twitch.", "price": 2.50, "unit": "1000", "icon_name": "Twitch", "color": "text-purple-500", "bg_color": "bg-purple-500/10", "category": "Twitch", "platform": "Twitch", "features": ["Fast Delivery", "Stable", "Safe"], "min_quantity": 100, "max_quantity": 10000 },
    { "id": 111, "title": "Twitch Live Viewers [1 Hour]", "description": "Spectateurs en direct pour vos streams.", "price": 15.00, "unit": "1000", "icon_name": "Twitch", "color": "text-purple-500", "bg_color": "bg-purple-500/10", "category": "Twitch", "platform": "Twitch", "features": ["Affiliate Ready", "Instant Start", "Stable"], "min_quantity": 50, "max_quantity": 2000 },
    { "id": 112, "title": "Twitch Clip Views", "description": "Boostez les vues de vos meilleurs moments.", "price": 0.50, "unit": "1000", "icon_name": "Twitch", "color": "text-purple-500", "bg_color": "bg-purple-500/10", "category": "Twitch", "platform": "Twitch", "features": ["Viral Clips", "Fast", "High Quality"], "min_quantity": 1000, "max_quantity": 100000 },

    # SEO & WEB
    { "id": 31, "title": "Traffic Web Premium", "description": "Visiteurs réels du pays de votre choix.", "price": 0.99, "unit": "1000", "icon_name": "Globe", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "category": "SEO", "platform": "Web", "features": ["Ciblage Géo", "Google Analytics OK", "Stable"], "min_quantity": 1000, "max_quantity": 1000000 },
    { "id": 32, "title": "Backlinks SEO Autorité", "description": "Liens depuis des sites DR 50+ pour booster Google.", "price": 49.00, "unit": "pack", "icon_name": "Zap", "color": "text-purple-400", "bg_color": "bg-purple-500/10", "category": "SEO", "platform": "Web", "features": ["Montez en Rank", "Dofollow", "Permanent"], "min_quantity": 1, "max_quantity": 1 },
    { "id": 49, "title": "Trustpilot Reviews [5 Stars]", "description": "Avis vérifiés pour votre page Trustpilot.", "price": 45.00, "unit": "10", "icon_name": "Star", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "category": "SEO", "platform": "Web", "features": ["Vérifié", "Pas de Suppression", "Premium"], "min_quantity": 1, "max_quantity": 10 },
    { "id": 50, "title": "Google Maps Reviews", "description": "Boostez la réputation de votre établissement local.", "price": 55.00, "unit": "10", "icon_name": "Globe", "color": "text-emerald-400", "bg_color": "bg-emerald-500/10", "category": "SEO", "platform": "Web", "features": ["Local Guides", "Géo-Ciblé", "Sûr"], "min_quantity": 1, "max_quantity": 10 },
    { "id": 113, "title": "SEO Audit Complete [IA]", "description": "Rapport détaillé sur les failles de votre site.", "price": 19.00, "unit": "audit", "icon_name": "Zap", "color": "text-purple-400", "bg_color": "bg-purple-500/10", "category": "SEO", "platform": "Web", "features": ["Deep Scan", "IA Recommendations", "Action Plan"], "min_quantity": 1, "max_quantity": 1 },
]

def migrate():
    print("Creating tables...")
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    print("Migrating services...")
    
    try:
        # Check if services already exist to avoid duplicates
        count = db.query(models.Service).count()
        if count > 0:
            print(f"Skipping population: {count} services already exist.")
            return

        for svc_data in INITIAL_SERVICES:
            service = models.Service(
                id=svc_data["id"],
                title=svc_data["title"],
                description=svc_data["description"],
                price=svc_data["price"],
                unit=svc_data["unit"],
                category=svc_data["category"],
                platform=svc_data["platform"],
                min_quantity=svc_data["min_quantity"],
                max_quantity=svc_data["max_quantity"],
                icon_name=svc_data["icon_name"],
                color=svc_data["color"],
                bg_color=svc_data["bg_color"],
                features=svc_data["features"]
            )
            db.merge(service) # merge allows specifying ID
        
        db.commit()
        print("Services migrated successfully!")
        
    except Exception as e:
        print(f"Error migrating services: {e}")
    
    # --- ADMIN USER PROMOTION ---
    print("Checking Admin User...")
    try:
        from auth import get_password_hash
        admin_email = "admin@smmadroop.com"
        admin = db.query(models.User).filter(models.User.email == admin_email).first()
        
        if admin:
            print(f"User {admin_email} found. Upgrading to admin...")
            admin.role = "admin"
            admin.is_active = True
        else:
            print(f"User {admin_email} not found. Creating admin user...")
            admin = models.User(
                name="Super Admin",
                email=admin_email,
                password_hash=get_password_hash("adminpassword123"),
                role="admin",
                is_active=True,
                plan="hero" # unlimited
            )
            db.add(admin)
            
        db.commit()
        print(f"SUCCESS: You can now log in with {admin_email} / adminpassword123")
        
    except Exception as e:
        print(f"Error setting up admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
