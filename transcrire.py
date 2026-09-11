# -*- coding: utf-8 -*-
"""
Transcription automatique de vidéos YouTube / Shorts / TikTok
================================================================

Ce script :
1. Lit les liens dans liens.txt (un lien par ligne)
2. Télécharge l'audio de chaque vidéo avec yt-dlp
3. Transcrit l'audio avec Whisper (détection automatique de la langue)
4. Enregistre le résultat dans resultats.csv

Utilisation : double-cliquer sur lancer.bat, ou taper "python transcrire.py"
dans un terminal ouvert dans ce dossier.
"""

import csv
import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

# ------------------------------------------------------------------
# CONFIGURATION - à modifier si besoin
# ------------------------------------------------------------------
LIENS_FICHIER = "liens.txt"
CSV_FICHIER = "resultats.csv"
MODELE_WHISPER = "base"   # tiny / base / small / medium / large
# ------------------------------------------------------------------


def charger_liens(chemin):
    if not os.path.exists(chemin):
        print(f"[ERREUR] Le fichier '{chemin}' est introuvable.")
        print(f"         Crée un fichier '{chemin}' a cote de ce script,")
        print(f"         avec un lien YouTube/TikTok par ligne.")
        sys.exit(1)

    with open(chemin, "r", encoding="utf-8") as f:
        liens = [
            ligne.strip()
            for ligne in f
            if ligne.strip() and not ligne.strip().startswith("#")
        ]

    if not liens:
        print(f"[ERREUR] Le fichier '{chemin}' est vide.")
        print("         Ajoute au moins un lien YouTube/TikTok dedans.")
        sys.exit(1)

    return liens


def detecter_source(url):
    """Devine la plateforme d'origine d'un lien, pour le message final."""
    url_min = url.lower()
    if "tiktok.com" in url_min:
        return "TikTok"
    if "youtube.com" in url_min or "youtu.be" in url_min:
        return "YouTube"
    if "instagram.com" in url_min:
        return "Instagram"
    return "autre site"


def proposer_mise_a_jour_yt_dlp(echecs_par_source):
    """Affiche un résumé des échecs de téléchargement par plateforme et
    propose de mettre à jour yt-dlp si l'utilisateur le souhaite."""
    print()
    for source, nb in echecs_par_source.items():
        video_mot = "vidéo n'a" if nb == 1 else "vidéos n'ont"
        print(f"{nb} {video_mot} pas pu être retranscrite(s) ({source}).")

    print(
        "Cela peut venir d'une version trop ancienne de yt-dlp "
        "(surtout pour TikTok, qui change souvent son fonctionnement)."
    )

    try:
        reponse = input(
            "Veux-tu essayer de mettre à jour yt-dlp maintenant ? (o/n) : "
        ).strip().lower()
    except (EOFError, KeyboardInterrupt):
        reponse = "n"

    if reponse not in ("o", "oui", "y", "yes"):
        print("D'accord, pas de mise à jour pour cette fois.")
        return

    print("\nMise à jour de yt-dlp en cours...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-U", "yt-dlp"],
            check=True,
        )
        print("\nyt-dlp a été mis à jour avec succès.")
        print("Relance lancer.bat pour réessayer les vidéos qui ont échoué.")
    except Exception as e:
        print(f"\nLa mise à jour a échoué : {e}")
        print("Tu peux réessayer manuellement avec : pip install -U yt-dlp")


def telecharger_audio(url, dossier_tmp):
    """Télécharge l'audio d'une vidéo avec yt-dlp.

    Renvoie (titre, chemin_du_fichier_audio).
    """
    import yt_dlp

    chemin_sortie = os.path.join(dossier_tmp, "%(id)s.%(ext)s")

    options = {
        "format": "bestaudio/best",
        "outtmpl": chemin_sortie,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        titre = info.get("title") or "Titre inconnu"
        video_id = info.get("id")

    chemin_audio = os.path.join(dossier_tmp, f"{video_id}.wav")

    if not os.path.exists(chemin_audio):
        # Sécurité : si l'extension finale n'est pas .wav pour une raison
        # quelconque, on cherche n'importe quel fichier avec cet id.
        candidats = list(Path(dossier_tmp).glob(f"{video_id}.*"))
        if candidats:
            chemin_audio = str(candidats[0])
        else:
            raise FileNotFoundError(
                "Fichier audio introuvable après téléchargement."
            )

    return titre, chemin_audio


def transcrire_audio(modele, chemin_audio):
    """Transcrit un fichier audio avec Whisper (détection auto de langue)."""
    resultat = modele.transcribe(chemin_audio, language=None, fp16=False)
    texte = resultat["text"].strip()
    langue = resultat.get("language", "")
    return texte, langue


def main():
    print("=" * 60)
    print(" Transcription automatique de vidéos")
    print("=" * 60)

    liens = charger_liens(LIENS_FICHIER)
    total = len(liens)
    print(f"\n{total} lien(s) trouve(s) dans '{LIENS_FICHIER}'.\n")

    print("Chargement du modele Whisper... (peut prendre quelques secondes)")
    import whisper
    modele = whisper.load_model(MODELE_WHISPER)
    print(f"Modele '{MODELE_WHISPER}' charge.\n")

    resultats = []
    echecs_par_source = {}

    with tempfile.TemporaryDirectory() as dossier_tmp:
        for i, url in enumerate(liens, start=1):
            print(f"[{i}/{total}] Telechargement : {url}")

            try:
                titre, chemin_audio = telecharger_audio(url, dossier_tmp)
            except Exception as e:
                print(f"[{i}/{total}] X Erreur pendant le telechargement : {e}\n")
                source = detecter_source(url)
                echecs_par_source[source] = echecs_par_source.get(source, 0) + 1
                resultats.append(
                    {
                        "url": url,
                        "titre": "ERREUR TELECHARGEMENT",
                        "langue": "",
                        "transcription": str(e),
                    }
                )
                continue

            print(f"[{i}/{total}] Transcription...")
            try:
                texte, langue = transcrire_audio(modele, chemin_audio)
            except Exception as e:
                print(f"[{i}/{total}] X Erreur pendant la transcription : {e}\n")
                resultats.append(
                    {
                        "url": url,
                        "titre": titre,
                        "langue": "",
                        "transcription": f"ERREUR TRANSCRIPTION: {e}",
                    }
                )
                continue
            finally:
                # Nettoyage du fichier audio temporaire, meme en cas d'erreur
                try:
                    if os.path.exists(chemin_audio):
                        os.remove(chemin_audio)
                except Exception:
                    pass

            resultats.append(
                {
                    "url": url,
                    "titre": titre,
                    "langue": langue,
                    "transcription": texte,
                }
            )
            print(f"[{i}/{total}] OK Termine : {titre}\n")

    # Écriture du CSV. encoding="utf-8-sig" pour qu'Excel affiche bien
    # les accents des le double-clic (sans ca, Excel affiche des caracteres
    # bizarres sur Windows).
    with open(CSV_FICHIER, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["url", "titre", "langue", "transcription"],
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()
        writer.writerows(resultats)

    print("=" * 60)
    print(f"CSV cree : {CSV_FICHIER}")
    print(f"{len(resultats)} video(s) traitee(s) sur {total}.")
    print("=" * 60)

    if echecs_par_source:
        proposer_mise_a_jour_yt_dlp(echecs_par_source)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrompu par l'utilisateur.")
    except Exception:
        print("\n[ERREUR INATTENDUE]\n")
        traceback.print_exc()
    finally:
        input("\nAppuie sur Entree pour fermer cette fenetre...")
