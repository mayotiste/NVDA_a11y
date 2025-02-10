import appModuleHandler
import logging
import speech
import textInfos


# Configuration du logger
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Utiliser le niveau DEBUG pour voir tous les logs
handler = logging.StreamHandler()  # Afficher les logs dans la console (le débogueur de NVDA)
handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
log.addHandler(handler)


class AppModule(appModuleHandler.AppModule):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.debug("Module Notepad++ chargé avec succès.")
        self.edit = None  # Initialiser l'objet d'édition


    def event_gainFocus(self, obj, nextHandler):
        """Lorsque le focus est sur Notepad++, enregistrer l'objet d'édition."""
        self.edit = obj  # Enregistrer l'objet d'édition
        nextHandler()


    def event_loseFocus(self, obj, nextHandler):
        """Lorsque Notepad++ perd le focus, nettoyer l'objet d'édition."""
        self.edit = None  # Nettoyer l'objet d'édition
        nextHandler()


    def script_moveToNextFunction(self, gesture):
        """Déplace le curseur vers la première ligne de la déclaration de fonction Python suivante."""
        # Envoyer un message dans le journal de NVDA
        log.debug("Raccourci DETECTE (NVDA+F2)")


        # Vérifier si l'objet d'édition est disponible
        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)  # Étendre à la ligne entière
                currentLine = caretInfo.bookmark.startOffset  # Position de départ de la ligne actuelle


                # Parcourir les lignes suivantes pour trouver la déclaration de fonction
                while True:
                    # Déplacer le curseur à la ligne suivante
                    caretInfo.move(textInfos.UNIT_LINE, 1)
                    caretInfo.expand(textInfos.UNIT_LINE)
                    lineText = caretInfo.text.strip()  # Obtenir le texte de la ligne


                    # Vérifier si la ligne commence par "def " (déclaration de fonction Python)
                    if lineText.startswith("def "):
                        # Déplacer le curseur au début de la ligne
                        caretInfo.updateCaret()
                        log.debug(f"Déclaration de fonction suivante trouvée : {lineText}")
                        speech.speakMessage(f"Déclaration de fonction suivante trouvée : {lineText}")
                        break


                    # Si on atteint la fin du document, arrêter la recherche
                    if caretInfo.bookmark.startOffset <= currentLine:
                        log.debug("Aucune déclaration de fonction suivante trouvée.")
                        speech.speakMessage("Aucune déclaration de fonction suivante trouvée.")
                        break


                    # Mettre à jour la position actuelle pour éviter les boucles infinies
                    currentLine = caretInfo.bookmark.startOffset


            except Exception as e:
                log.error(f"Erreur lors de la recherche de la déclaration de fonction suivante : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")


    def script_moveToPreviousFunction(self, gesture):
        """Déplace le curseur vers la première ligne de la déclaration de fonction Python précédente."""
        # Envoyer un message dans le journal de NVDA
        log.debug("Raccourci DETECTE (Shift+F2)")


        # Vérifier si l'objet d'édition est disponible
        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)  # Étendre à la ligne entière
                currentLine = caretInfo.bookmark.startOffset  # Position de départ de la ligne actuelle


                # Parcourir les lignes précédentes pour trouver la déclaration de fonction
                while True:
                    # Déplacer le curseur à la ligne précédente
                    caretInfo.move(textInfos.UNIT_LINE, -1)
                    caretInfo.expand(textInfos.UNIT_LINE)
                    lineText = caretInfo.text.strip()  # Obtenir le texte de la ligne


                    # Vérifier si la ligne commence par "def " (déclaration de fonction Python)
                    if lineText.startswith("def "):
                        # Déplacer le curseur au début de la ligne
                        caretInfo.updateCaret()
                        log.debug(f"Déclaration de fonction précédente trouvée : {lineText}")
                        speech.speakMessage(f"Déclaration de fonction précédente trouvée : {lineText}")
                        break


                    # Si on atteint le début du document, arrêter la recherche
                    if caretInfo.bookmark.startOffset >= currentLine:
                        log.debug("Aucune déclaration de fonction précédente trouvée.")
                        speech.speakMessage("Aucune déclaration de fonction précédente trouvée.")
                        break


                    # Mettre à jour la position actuelle pour éviter les boucles infinies
                    currentLine = caretInfo.bookmark.startOffset


            except Exception as e:
                log.error(f"Erreur lors de la recherche de la déclaration de fonction précédente : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")


    # Associer les raccourcis NVDA+F2 et Shift+F2 aux fonctions correspondantes


    def script_moveToNextClass(self, gesture):
    # Envoyer un message dans le journal de NVDA
        log.debug("Raccourci DETECTE (F7)")


    # Vérifier si l'objet d'édition est disponible
        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)  # Étendre à la ligne entière
                currentLine = caretInfo.bookmark.startOffset  # Position de départ de la ligne actuelle


                # Parcourir les lignes suivantes pour trouver la déclaration de classe
                while True:
                    # Déplacer le curseur à la ligne suivante
                    caretInfo.move(textInfos.UNIT_LINE, 1)
                    caretInfo.expand(textInfos.UNIT_LINE)
                    lineText = caretInfo.text.strip()  # Obtenir le texte de la ligne


                    # Vérifier si la ligne commence par "class " (déclaration de classe Python)
                    if lineText.startswith("class "):
                        # Déplacer le curseur au début de la ligne
                        caretInfo.updateCaret()
                        log.debug(f"Déclaration de classe suivante trouvée : {lineText}")
                        speech.speakMessage(f"Déclaration de classe suivante trouvée : {lineText}")
                        break


                    # Si on atteint la fin du document, arrêter la recherche
                    if caretInfo.bookmark.startOffset <= currentLine:
                        log.debug("Aucune déclaration de classe suivante trouvée.")
                        speech.speakMessage("Aucune déclaration de classe suivante trouvée.")
                        break


                    # Mettre à jour la position actuelle pour éviter les boucles infinies
                    currentLine = caretInfo.bookmark.startOffset


            except Exception as e:
                log.error(f"Erreur lors de la recherche de la déclaration de classe suivante : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")


    def script_moveToPreviousClass(self, gesture):
        """Déplace le curseur vers la première ligne de la déclaration de classe Python précédente."""
        # Envoyer un message dans le journal de NVDA
        log.debug("Raccourci DETECTE (Shift+F7)")


        # Vérifier si l'objet d'édition est disponible
        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)  # Étendre à la ligne entière
                currentLine = caretInfo.bookmark.startOffset  # Position de départ de la ligne actuelle


                # Parcourir les lignes précédentes pour trouver la déclaration de classe
                while True:
                    # Déplacer le curseur à la ligne précédente
                    caretInfo.move(textInfos.UNIT_LINE, -1)
                    caretInfo.expand(textInfos.UNIT_LINE)
                    lineText = caretInfo.text.strip()  # Obtenir le texte de la ligne


                    # Vérifier si la ligne commence par "class " (déclaration de classe Python)
                    if lineText.startswith("class "):
                        # Déplacer le curseur au début de la ligne
                        caretInfo.updateCaret()
                        log.debug(f"Déclaration de classe précédente trouvée : {lineText}")
                        speech.speakMessage(f"Déclaration de classe précédente trouvée : {lineText}")
                        break


                    # Si on atteint le début du document, arrêter la recherche
                    if caretInfo.bookmark.startOffset >= currentLine:
                        log.debug("Aucune déclaration de classe précédente trouvée.")
                        speech.speakMessage("Aucune déclaration de classe précédente trouvée.")
                        break


                    # Mettre à jour la position actuelle pour éviter les boucles infinies
                    currentLine = caretInfo.bookmark.startOffset


            except Exception as e:
                log.error(f"Erreur lors de la recherche de la déclaration de classe précédente : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")

    __gestures = {
        "kb:NVDA+F2": "moveToNextFunction",
        "kb:Shift+F2": "moveToPreviousFunction",
        "kb:F7": "moveToNextClass",
        "kb:Shift+F7": "moveToPreviousClass",
    }