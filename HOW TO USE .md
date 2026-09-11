# Transcription YouTube / TikTok — Guide d'utilisation

Ce dossier permet de transcrire automatiquement des vidéos YouTube, YouTube
Shorts et TikTok, et de récupérer le résultat dans un fichier Excel/CSV.

Tu n'as besoin d'aucune connaissance en informatique pour l'utiliser.

---

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `installer.bat` | À lancer **une seule fois**, au tout début. Installe tout automatiquement. |
| `lancer.bat` | À lancer **à chaque fois** que tu veux transcrire des vidéos. |
| `liens.txt` | Le fichier où tu colles tes liens YouTube/TikTok. |
| `transcrire.py` | Le programme (tu n'as pas besoin d'y toucher). |
| `requirements.txt` | Liste technique utilisée par l'installation (tu n'as pas besoin d'y toucher). |
| `resultats.csv` | Apparaît après chaque utilisation — c'est ton résultat final. |

---

## Étape 1 — Installation (une seule fois)

1. Double-clique sur **`installer.bat`**.
2. Une fenêtre noire s'ouvre et affiche ce qu'elle est en train de faire. Laisse-la travailler, ne la ferme pas.
3. **Deux cas possibles :**
   - Soit elle affiche à la fin **`INSTALLATION TERMINEE !`** → c'est fini, passe à l'étape 2.
   - Soit elle te dit de **fermer la fenêtre et de redouble-cliquer sur `installer.bat`** → fais exactement ça, c'est normal (ça arrive quand Python ou FFmpeg viennent d'être installés et que Windows a besoin d'une fenêtre "fraîche" pour les reconnaître). Répète jusqu'à voir `INSTALLATION TERMINEE !`.
4. Si une erreur rouge du type `[ERREUR]` s'affiche et reste bloquée, prends une capture d'écran et envoie-la-moi.

*Cette étape peut prendre plusieurs minutes la première fois (téléchargements).*

---

## Étape 2 — Ajouter tes vidéos

1. Ouvre le fichier **`liens.txt`** (clic droit → Ouvrir avec → Bloc-notes, si besoin).
2. Colle un lien YouTube ou TikTok par ligne. Exemple :
   ```
   https://www.youtube.com/watch?v=XXXXXXXXXXX
   https://www.youtube.com/shorts/XXXXXXXXXXX
   https://www.tiktok.com/@compte/video/1234567890123456789
   ```
3. Enregistre le fichier (Ctrl+S) puis ferme-le.

---

## Étape 3 — Lancer la transcription

1. Double-clique sur **`lancer.bat`**.
2. Une fenêtre noire affiche la progression, vidéo par vidéo :
   ```
   [1/3] Telechargement : https://...
   [1/3] Transcription...
   [1/3] OK Termine : Titre de la video

   [2/3] Telechargement : ...
   ...
   CSV cree : resultats.csv
   ```
3. Selon le nombre de vidéos et leur longueur, ça peut prendre de quelques secondes à plusieurs minutes par vidéo — c'est normal, laisse tourner.
4. À la fin, appuie sur Entrée pour fermer la fenêtre.

---

## Étape 4 — Récupérer le résultat

Un fichier **`resultats.csv`** apparaît dans le dossier. Double-clique dessus pour l'ouvrir avec Excel. Il contient, pour chaque vidéo : le lien, le titre, la langue détectée et la transcription complète.

---

## Si une vidéo échoue

C'est normal que ça arrive de temps en temps (vidéo privée, supprimée, ou TikTok qui a changé quelque chose). Le programme :
- continue automatiquement avec les vidéos suivantes ;
- note l'erreur à la place de la transcription dans le CSV pour cette vidéo-là.

À la toute fin, s'il y a eu des échecs, il te proposera :
```
2 vidéos n'ont pas pu être retranscrite(s) (TikTok).
Veux-tu essayer de mettre à jour yt-dlp maintenant ? (o/n) :
```
Tape **o** puis Entrée, attends que ça se termine, puis relance `lancer.bat` pour réessayer ces vidéos.

---

## Utilisation au quotidien (résumé)

Une fois l'installation faite (étape 1, une seule fois dans toute la vie du dossier) :

**coller les liens dans `liens.txt` → double-clic sur `lancer.bat` → récupérer `resultats.csv`**

---

## En cas de blocage

Si quelque chose ne fonctionne pas et que ce guide ne suffit pas, prends une capture d'écran complète de la fenêtre noire au moment du blocage et envoie-la-moi — ce sera beaucoup plus simple pour comprendre ce qui se passe.
