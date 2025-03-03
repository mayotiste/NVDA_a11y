import appModuleHandler
import logging
import speech
import textInfos
import gui  # Pour les boîtes de dialogue
import api
import wx
import subprocess  # Pour lancer un terminal
import os  # Pour manipuler les chemins de fichiers
import keyboardHandler  # Pour simuler l'appui sur la touche Suppr
import tempfile  # Pour créer des fichiers temporaires

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

    def _getIndentationLevel(self, lineText):
        """Retourne le niveau d'indentation d'une ligne."""
        return len(lineText) - len(lineText.lstrip())
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

    def script_selectCurrentClass(self, gesture):
        """Sélectionne la classe entière à partir de la position du curseur en fonction de l'indentation."""
        # Envoyer un message dans le journal de NVDA
        log.debug("Raccourci DETECTE (Shift+F8)")

        # Vérifier si l'objet d'édition est disponible
        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)  # Étendre à la ligne entière
                currentLineText = caretInfo.text.strip()  # Obtenir le texte de la ligne actuelle

                # Vérifier si la ligne actuelle contient une déclaration de classe
                if currentLineText.startswith("class "):
                    # Si c'est le cas, on commence la sélection à partir de cette ligne
                    startInfo = caretInfo.copy()
                    startIndentation = self._getIndentationLevel(currentLineText)
                else:
                    # Sinon, on cherche la déclaration de classe précédente
                    while True:
                        caretInfo.move(textInfos.UNIT_LINE, -1)
                        caretInfo.expand(textInfos.UNIT_LINE)
                        lineText = caretInfo.text.strip()

                        if lineText.startswith("class "):
                            startInfo = caretInfo.copy()
                            startIndentation = self._getIndentationLevel(lineText)
                            break

                        # Si on atteint le début du document, on arrête la recherche
                        if caretInfo.bookmark.startOffset <= 0:
                            log.debug("Aucune déclaration de classe trouvée.")
                            speech.speakMessage("Aucune déclaration de classe trouvée.")
                            return

                # Trouver la fin de la classe en parcourant les lignes suivantes
                endInfo = startInfo.copy()
                endInfo.expand(textInfos.UNIT_LINE)
                endInfo.collapse(end=True)

                lineCounter = 0  # Compteur de lignes

                while True:
                    endInfo.move(textInfos.UNIT_LINE, 1)
                    endInfo.expand(textInfos.UNIT_LINE)
                    lineText = endInfo.text
                    currentIndentation = self._getIndentationLevel(lineText)

                    # Si l'indentation est inférieure ou égale à celle de la déclaration
                    if currentIndentation <= startIndentation:
                        # Si la ligne contient du texte, on s'arrête
                        if lineText.strip():
                            # Revenir en arrière d'une ligne
                            endInfo.move(textInfos.UNIT_LINE, -1)
                            endInfo.expand(textInfos.UNIT_LINE)
                            break

                    lineCounter += 1

                # Appliquer la sélection
                selectionInfo = self.edit.makeTextInfo(startInfo)
                selectionInfo.setEndPoint(endInfo, "endToEnd")
                self.edit.selection = selectionInfo

                log.debug(f"Classe sélectionnée avec succès. Nombre de lignes sélectionnées : {lineCounter}")
                speech.speakMessage(f"Classe sélectionnée. {lineCounter} lignes sélectionnées.")

            except Exception as e:
                log.error(f"Erreur lors de la sélection de la classe : {e}")
                speech.speakMessage("Erreur lors de la sélection de la classe.")
        else:
            log.debug("Aucun objet d'édition trouvé.")

    def script_selectClass(self, gesture):
        """Sélectionne la classe entière à partir de la première ligne."""
        log.debug("Raccourci détecté (Ctrl+Shift+R)")


        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)  # Étendre à la ligne entière
                lineText = caretInfo.text.strip()


                # Vérifier si la ligne commence par "class " (déclaration de classe Python)
                if lineText.startswith("class "):
                    self._selectClass(caretInfo)
                    log.debug("Classe sélectionnée avec succès.")
                    speech.speakMessage("Classe sélectionnée.")
                else:
                    log.debug("Le curseur n'est pas sur une déclaration de classe.")
                    speech.speakMessage("Le curseur n'est pas sur une déclaration de classe.")


            except Exception as e:
                log.error(f"Erreur lors de la sélection de la classe : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")


    # Ajout du raccourci clavier correspondant dans Notepad++
    script_selectClass.__doc__ = _("Sélectionne la classe entière")
    script_selectClass.category = "Notepad++"


    def script_selectCurrentFunction(self, gesture):
        """Sélectionne la fonction entière à partir de la position du curseur en fonction de l'indentation."""
        # Envoyer un message dans le journal de NVDA
        log.debug("Raccourci DETECTE (Shift+F3)")

        # Vérifier si l'objet d'édition est disponible
        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)  # Étendre à la ligne entière
                currentLineText = caretInfo.text.strip()  # Obtenir le texte de la ligne actuelle

                # Vérifier si la ligne actuelle contient une déclaration de fonction
                if currentLineText.startswith("def "):
                    # Si c'est le cas, on commence la sélection à partir de cette ligne
                    startInfo = caretInfo.copy()
                    startIndentation = self._getIndentationLevel(currentLineText)
                else:
                    # Sinon, on cherche la déclaration de fonction précédente
                    while True:
                        caretInfo.move(textInfos.UNIT_LINE, -1)
                        caretInfo.expand(textInfos.UNIT_LINE)
                        lineText = caretInfo.text.strip()

                        if lineText.startswith("def "):
                            startInfo = caretInfo.copy()
                            startIndentation = self._getIndentationLevel(lineText)
                            break

                        # Si on atteint le début du document, on arrête la recherche
                        if caretInfo.bookmark.startOffset <= 0:
                            log.debug("Aucune déclaration de fonction trouvée.")
                            speech.speakMessage("Aucune déclaration de fonction trouvée.")
                            return

                # Trouver la fin de la fonction en parcourant les lignes suivantes
                endInfo = startInfo.copy()
                endInfo.expand(textInfos.UNIT_LINE)
                endInfo.collapse(end=True)

                lineCounter = 0  # Compteur de lignes

                while True:
                    endInfo.move(textInfos.UNIT_LINE, 1)
                    endInfo.expand(textInfos.UNIT_LINE)
                    lineText = endInfo.text
                    currentIndentation = self._getIndentationLevel(lineText)

                    # Si l'indentation est inférieure ou égale à celle de la déclaration
                    if currentIndentation <= startIndentation:
                        # Si la ligne contient du texte, on s'arrête
                        if lineText.strip():
                            # Revenir en arrière d'une ligne
                            endInfo.move(textInfos.UNIT_LINE, -1)
                            endInfo.expand(textInfos.UNIT_LINE)
                            break

                    lineCounter += 1

                # Appliquer la sélection
                selectionInfo = self.edit.makeTextInfo(startInfo)
                selectionInfo.setEndPoint(endInfo, "endToEnd")
                self.edit.selection = selectionInfo

                log.debug(f"Fonction sélectionnée avec succès. Nombre de lignes sélectionnées : {lineCounter}")
                speech.speakMessage(f"Fonction sélectionnée. {lineCounter} lignes sélectionnées.")

            except Exception as e:
                log.error(f"Erreur lors de la sélection de la fonction : {e}")
                speech.speakMessage("Erreur lors de la sélection de la fonction.")
        else:
            log.debug("Aucun objet d'édition trouvé.")


    def script_selectFunction(self, gesture):
        """Sélectionne la fonction entière à partir de la première ligne."""
        log.debug("Raccourci détecté (Ctrl+R)")


        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)  # Étendre à la ligne entière
                lineText = caretInfo.text.strip()


                # Vérifier si la ligne commence par "def " (déclaration de fonction Python)
                if lineText.startswith("def "):
                    self._selectFunction(caretInfo)
                    log.debug("Fonction sélectionnée avec succès.")
                    speech.speakMessage("Fonction sélectionnée.")
                else:
                    log.debug("Le curseur n'est pas sur une déclaration de fonction.")
                    speech.speakMessage("Le curseur n'est pas sur une déclaration de fonction.")


            except Exception as e:
                log.error(f"Erreur lors de la sélection de la fonction : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")


    # Ajout du raccourci clavier correspondant dans Notepad++
    script_selectFunction.__doc__ = _("Sélectionne la fonction entière")
    script_selectFunction.category = "Notepad++"

    

    def _deleteClass(self, caretInfo):
        """Supprime la classe entière à partir de la position du curseur après confirmation."""
        try:
            # Trouver le début de la classe (ligne contenant "class")
            startInfo = caretInfo.copy()
            startInfo.expand(textInfos.UNIT_LINE)
            startInfo.collapse()

            # Obtenir le texte de la ligne de déclaration de la classe
            startLineText = startInfo.text
            startIndentation = self._getIndentationLevel(startLineText)

            # Trouver la fin de la classe en parcourir les lignes suivantes
            endInfo = startInfo.copy()
            endInfo.expand(textInfos.UNIT_LINE)
            endInfo.collapse(end=True)

            lineCounter = 0  # Compteur de lignes

            while True:
                endInfo.move(textInfos.UNIT_LINE, 1)
                endInfo.expand(textInfos.UNIT_LINE)
                lineText = endInfo.text
                currentIndentation = self._getIndentationLevel(lineText)

                # Si l'indentation est inférieure ou égale à celle de la déclaration
                if currentIndentation <= startIndentation:
                    # Si la ligne contient du texte, on s'arrête
                    if lineText.strip():
                        # Revenir en arrière d'une ligne
                        endInfo.move(textInfos.UNIT_LINE, -1)
                        endInfo.expand(textInfos.UNIT_LINE)
                        break

                lineCounter += 1

            # Appliquer la sélection
            selectionInfo = self.edit.makeTextInfo(startInfo)
            selectionInfo.setEndPoint(endInfo, "endToEnd")
            self.edit.selection = selectionInfo
            speech.speakMessage(f"êtes vous sûr de vouloir supprimer la classe?")
            # Demander confirmation avant suppression avec un message personnalisé
            if gui.messageBox(
                "Voulez-vous vraiment supprimer cette classe ?",  # Message personnalisé
                "Confirmation de suppression",  # Titre de la boîte de dialogue
                wx.YES_NO | wx.ICON_QUESTION  # Boutons Oui/Non et icône de question
            ) == wx.YES:
                # Simuler l'appui sur la touche Suppr pour supprimer la sélection
                keyboardHandler.KeyboardInputGesture.fromName("delete").send()
                log.debug(f"Classe supprimée avec succès. Nombre de lignes supprimées : {lineCounter}")
                speech.speakMessage(f"Classe supprimée. {lineCounter} lignes supprimées.")
            else:
                log.debug("Suppression annulée par l'utilisateur.")
                speech.speakMessage("Suppression annulée.")

        except Exception as e:
            log.error(f"Erreur lors de la suppression de la classe : {e}")
            speech.speakMessage("Erreur lors de la suppression de la classe.")

    def script_deleteCurrentClass(self, gesture):
        """Supprime la classe entière sur laquelle le curseur est positionné après confirmation."""
        # Envoyer un message dans le journal de NVDA
        log.debug("Raccourci DETECTE (Ctrl+Shift+Delete)")

        # Vérifier si l'objet d'édition est disponible
        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)  # Étendre à la ligne entière
                currentLineText = caretInfo.text.strip()  # Obtenir le texte de la ligne actuelle

                # Vérifier si la ligne actuelle contient une déclaration de classe
                if currentLineText.startswith("class "):
                    # Si c'est le cas, on commence la suppression à partir de cette ligne
                    startInfo = caretInfo.copy()
                    startIndentation = self._getIndentationLevel(currentLineText)
                else:
                    # Sinon, on cherche la déclaration de classe précédente
                    while True:
                        caretInfo.move(textInfos.UNIT_LINE, -1)
                        caretInfo.expand(textInfos.UNIT_LINE)
                        lineText = caretInfo.text.strip()

                        if lineText.startswith("class "):
                            startInfo = caretInfo.copy()
                            startIndentation = self._getIndentationLevel(lineText)
                            break

                        # Si on atteint le début du document, on arrête la recherche
                        if caretInfo.bookmark.startOffset <= 0:
                            log.debug("Aucune déclaration de classe trouvée.")
                            speech.speakMessage("Aucune déclaration de classe trouvée.")
                            return

                # Trouver la fin de la classe en parcourant les lignes suivantes
                endInfo = startInfo.copy()
                endInfo.expand(textInfos.UNIT_LINE)
                endInfo.collapse(end=True)

                lineCounter = 0  # Compteur de lignes

                while True:
                    endInfo.move(textInfos.UNIT_LINE, 1)
                    endInfo.expand(textInfos.UNIT_LINE)
                    lineText = endInfo.text
                    currentIndentation = self._getIndentationLevel(lineText)

                    # Si l'indentation est inférieure ou égale à celle de la déclaration
                    if currentIndentation <= startIndentation:
                        # Si la ligne contient du texte, on s'arrête
                        if lineText.strip():
                            # Revenir en arrière d'une ligne
                            endInfo.move(textInfos.UNIT_LINE, -1)
                            endInfo.expand(textInfos.UNIT_LINE)
                            break

                    lineCounter += 1

                # Appliquer la sélection
                selectionInfo = self.edit.makeTextInfo(startInfo)
                selectionInfo.setEndPoint(endInfo, "endToEnd")
                self.edit.selection = selectionInfo

                # Demander confirmation avant suppression avec un message personnalisé
                speech.speakMessage(f"êtes vous sûr de vouloir supprimer la classe?")
                if gui.messageBox(
                    "Voulez-vous vraiment supprimer cette classe ?",  # Message personnalisé
                    "Confirmation de suppression",  # Titre de la boîte de dialogue
                    wx.YES_NO | wx.ICON_QUESTION  # Boutons Oui/Non et icône de question
                ) == wx.YES:
                    # Simuler l'appui sur la touche Suppr pour supprimer la sélection
                    keyboardHandler.KeyboardInputGesture.fromName("delete").send()
                    log.debug(f"Classe supprimée avec succès. Nombre de lignes supprimées : {lineCounter}")
                    speech.speakMessage(f"Classe supprimée. {lineCounter} lignes supprimées.")
                else:
                    log.debug("Suppression annulée par l'utilisateur.")
                    speech.speakMessage("Suppression annulée.")

            except Exception as e:
                log.error(f"Erreur lors de la suppression de la classe : {e}")
                speech.speakMessage("Erreur lors de la suppression de la classe.")
        else:
            log.debug("Aucun objet d'édition trouvé.")


    def _deleteFunction(self, caretInfo):
        """Supprime la fonction entière à partir de la position du curseur après confirmation."""
        try:
            # Trouver le début de la fonction (ligne contenant "def")
            startInfo = caretInfo.copy()
            startInfo.expand(textInfos.UNIT_LINE)
            startInfo.collapse()


            # Obtenir le texte de la ligne de déclaration de la fonction
            startLineText = startInfo.text
            startIndentation = self._getIndentationLevel(startLineText)


            # Trouver la fin de la fonction en parcourir les lignes suivantes
            endInfo = startInfo.copy()
            endInfo.expand(textInfos.UNIT_LINE)
            endInfo.collapse(end=True)


            lineCounter = 0  # Compteur de lignes


            while True:
                endInfo.move(textInfos.UNIT_LINE, 1)
                endInfo.expand(textInfos.UNIT_LINE)
                lineText = endInfo.text
                currentIndentation = self._getIndentationLevel(lineText)


                # Si l'indentation est inférieure ou égale à celle de la déclaration
                if currentIndentation <= startIndentation:
                    # Si la ligne contient du texte, on s'arrête
                    if lineText.strip():
                        # Revenir en arrière d'une ligne
                        endInfo.move(textInfos.UNIT_LINE, -1)
                        endInfo.expand(textInfos.UNIT_LINE)
                        break


                lineCounter += 1


            # Appliquer la sélection
            selectionInfo = self.edit.makeTextInfo(startInfo)
            selectionInfo.setEndPoint(endInfo, "endToEnd")
            self.edit.selection = selectionInfo

            speech.speakMessage(f"êtes vous sûr de vouloir supprimer la fonction?")

            # Demander confirmation avant suppression
            if gui.messageBox(
                "Voulez-vous vraiment supprimer cette fonction ?",
                "Confirmation de suppression",
                wx.YES_NO | wx.ICON_QUESTION
            ) == wx.YES:
                # Simuler l'appui sur la touche Suppr pour supprimer la sélection
                keyboardHandler.KeyboardInputGesture.fromName("delete").send()
                log.debug(f"Fonction supprimée avec succès. Nombre de lignes supprimées : {lineCounter}")
                speech.speakMessage(f"Fonction supprimée. {lineCounter} lignes supprimées.")
            else:
                log.debug("Suppression annulée par l'utilisateur.")
                speech.speakMessage("Suppression annulée.")


        except Exception as e:
            log.error(f"Erreur lors de la suppression de la fonction : {e}")
            speech.speakMessage("Erreur lors de la suppression de la fonction.")


    def script_deleteCurrentFunction(self, gesture):
        """Supprime la fonction entière sur laquelle le curseur est positionné après confirmation."""
        # Envoyer un message dans le journal de NVDA
        log.debug("Raccourci DETECTE (Ctrl+Shift+Delete)")

        # Vérifier si l'objet d'édition est disponible
        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)  # Étendre à la ligne entière
                currentLineText = caretInfo.text.strip()  # Obtenir le texte de la ligne actuelle

                # Vérifier si la ligne actuelle contient une déclaration de fonction
                if currentLineText.startswith("def "):
                    # Si c'est le cas, on commence la suppression à partir de cette ligne
                    startInfo = caretInfo.copy()
                    startIndentation = self._getIndentationLevel(currentLineText)
                else:
                    # Sinon, on cherche la déclaration de fonction précédente
                    while True:
                        caretInfo.move(textInfos.UNIT_LINE, -1)
                        caretInfo.expand(textInfos.UNIT_LINE)
                        lineText = caretInfo.text.strip()

                        if lineText.startswith("def "):
                            startInfo = caretInfo.copy()
                            startIndentation = self._getIndentationLevel(lineText)
                            break

                        # Si on atteint le début du document, on arrête la recherche
                        if caretInfo.bookmark.startOffset <= 0:
                            log.debug("Aucune déclaration de fonction trouvée.")
                            speech.speakMessage("Aucune déclaration de fonction trouvée.")
                            return

                # Trouver la fin de la fonction en parcourant les lignes suivantes
                endInfo = startInfo.copy()
                endInfo.expand(textInfos.UNIT_LINE)
                endInfo.collapse(end=True)

                lineCounter = 0  # Compteur de lignes

                while True:
                    endInfo.move(textInfos.UNIT_LINE, 1)
                    endInfo.expand(textInfos.UNIT_LINE)
                    lineText = endInfo.text
                    currentIndentation = self._getIndentationLevel(lineText)

                    # Si l'indentation est inférieure ou égale à celle de la déclaration
                    if currentIndentation <= startIndentation:
                        # Si la ligne contient du texte, on s'arrête
                        if lineText.strip():
                            # Revenir en arrière d'une ligne
                            endInfo.move(textInfos.UNIT_LINE, -1)
                            endInfo.expand(textInfos.UNIT_LINE)
                            break

                    lineCounter += 1

                # Appliquer la sélection
                selectionInfo = self.edit.makeTextInfo(startInfo)
                selectionInfo.setEndPoint(endInfo, "endToEnd")
                self.edit.selection = selectionInfo

                # Demander confirmation avant suppression avec un message personnalisé
                speech.speakMessage(f"êtes vous sûr de vouloir supprimer la fonction?")
                if gui.messageBox(
                    "Voulez-vous vraiment supprimer cette fonction ?",  # Message personnalisé
                    "Confirmation de suppression",  # Titre de la boîte de dialogue
                    wx.YES_NO | wx.ICON_QUESTION  # Boutons Oui/Non et icône de question
                ) == wx.YES:
                    # Simuler l'appui sur la touche Suppr pour supprimer la sélection
                    keyboardHandler.KeyboardInputGesture.fromName("delete").send()
                    log.debug(f"Fonction supprimée avec succès. Nombre de lignes supprimées : {lineCounter}")
                    speech.speakMessage(f"Fonction supprimée. {lineCounter} lignes supprimées.")
                else:
                    log.debug("Suppression annulée par l'utilisateur.")
                    speech.speakMessage("Suppression annulée.")

            except Exception as e:
                log.error(f"Erreur lors de la suppression de la fonction : {e}")
                speech.speakMessage("Erreur lors de la suppression de la fonction.")
        else:
            log.debug("Aucun objet d'édition trouvé.")
    # Ajout du raccourci clavier correspondant dans Notepad++



    def _executePythonCode(self):
        """Exécute le code Python dans un terminal."""
        try:
            # Obtenir le texte sélectionné ou le fichier entier
            if self.edit.selection.text:
                code = self.edit.selection.text
                log.debug("Exécution du code sélectionné.")
            else:
                # Si rien n'est sélectionné, exécuter tout le fichier
                code = self.edit.makeTextInfo(textInfos.POSITION_ALL).text
                log.debug("Exécution du fichier entier.")


            # Créer un fichier temporaire dans le répertoire TEMP de l'utilisateur
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name


            # Ouvrir un terminal et exécuter le script temporaire
            systeme = os.name
            if systeme == "nt":  # Windows
                subprocess.Popen(["cmd", "/k", f"python {temp_file_path}"], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:  # Linux et macOS
                subprocess.Popen(["x-terminal-emulator", "-e", f"python3 {temp_file_path}"], close_fds=True)
               
            log.debug(f"Terminal ouvert et code exécuté. Fichier temporaire : {temp_file_path}")
            speech.speakMessage("Code exécuté dans un terminal.")


        except Exception as e:
            log.error(f"Erreur lors de l'exécution du code : {e}")
            speech.speakMessage("Erreur lors de l'exécution du code.")


    def script_executePythonCode(self, gesture):
        """Lance un terminal et exécute le code en cours."""
        log.debug("Raccourci détecté (F5)")


        if self.edit:
            try:
                self._executePythonCode()
                log.debug("Code exécuté avec succès.")
                speech.speakMessage("Code exécuté.")
            except Exception as e:
                log.error(f"Erreur lors de l'exécution du code : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")


    # Ajout du raccourci clavier correspondant dans Notepad++
    script_executePythonCode.__doc__ = ("Exécute le code Python dans un terminal")
    script_executePythonCode.category = "Notepad++"


    def script_moveToNextIndentLevel(self, gesture):
        """Déplace le curseur vers le prochain niveau d'indentation et annonce le niveau actuel."""
        # Envoyer un message dans le journal de NVDA
        log.debug("Raccourci DETECTE (Alt+Down)")

        # Vérifier si l'objet d'édition est disponible
        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)  # Étendre à la ligne entière
                currentLineText = caretInfo.text

                # Calculer l'indentation actuelle en tenant compte des tabulations
                currentIndent = 0
                for char in currentLineText:
                    if char == '\t':
                        currentIndent += 4  # Une tabulation = 4 espaces (ajuste selon ton éditeur)
                    elif char == ' ':
                        currentIndent += 1
                    else:
                        break

                # Initialiser la position de la ligne actuelle
                currentLine = caretInfo.bookmark.startOffset

                # Parcourir les lignes suivantes pour trouver un niveau d'indentation différent
                while True:
                    # Déplacer le curseur à la ligne suivante
                    caretInfo.move(textInfos.UNIT_LINE, 1)
                    caretInfo.expand(textInfos.UNIT_LINE)
                    lineText = caretInfo.text

                    # Calculer l'indentation de la ligne suivante
                    lineIndent = 0
                    for char in lineText:
                        if char == '\t':
                            lineIndent += 4  # Une tabulation = 4 espaces (ajuste selon ton éditeur)
                        elif char == ' ':
                            lineIndent += 1
                        else:
                            break

                    # Vérifier si l'indentation est différente de l'actuelle
                    if lineIndent != currentIndent:
                        # Déplacer le curseur au début de la ligne
                        caretInfo.updateCaret()
                        log.debug(f"Niveau d'indentation suivant trouvé : {lineText.strip()}")

                        # Annoncer le niveau d'indentation actuel de la nouvelle ligne
                        speech.speakMessage(f"Indentation actuel : {lineIndent}")
                        break

                    # Si on atteint la fin du document, arrêter la recherche
                    if caretInfo.bookmark.startOffset <= currentLine:
                        log.debug("Aucun niveau d'indentation suivant trouvé.")
                        speech.speakMessage("Fin du document atteinte.")
                        break

                    # Mettre à jour la position actuelle pour éviter les boucles infinies
                    currentLine = caretInfo.bookmark.startOffset

            except Exception as e:
                log.error(f"Erreur lors de la recherche du niveau d'indentation suivant : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")
    
    def script_moveToPreviousIndentLevel(self, gesture):
        """Déplace le curseur vers le niveau d'indentation précédent et annonce le niveau actuel."""
        log.debug("Raccourci Alt+Up détecté, exécution de moveToPreviousIndentLevel.")

        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)
                currentLineText = caretInfo.text
                currentIndent = len(currentLineText) - len(currentLineText.lstrip())  # Calculer l'indentation actuelle
                currentLine = caretInfo.bookmark.startOffset  # Initialiser la position de la ligne actuelle

                # Annoncer le niveau d'indentation actuel
                speech.speakMessage(f"Niveau d'indentation actuel : {currentIndent}")

                # Parcourir les lignes précédentes pour trouver un niveau d'indentation différent
                while True:
                    # Déplacer le curseur à la ligne précédente
                    caretInfo.move(textInfos.UNIT_LINE, -1)
                    caretInfo.expand(textInfos.UNIT_LINE)
                    lineText = caretInfo.text
                    lineIndent = len(lineText) - len(lineText.lstrip())  # Calculer l'indentation de la ligne

                    # Vérifier si l'indentation est différente de l'actuelle
                    if lineIndent != currentIndent:
                        # Déplacer le curseur au début de la ligne
                        caretInfo.updateCaret()
                        log.debug(f"Niveau d'indentation précédent trouvé : {lineText.strip()}")
                        speech.speakMessage(f"Niveau d'indentation précédent trouvé : {lineIndent}")
                        break

                    # Si on atteint le début du document, arrêter la recherche
                    if caretInfo.bookmark.startOffset >= currentLine:
                        log.debug("Aucun niveau d'indentation précédent trouvé.")
                        speech.speakMessage("Aucun niveau d'indentation précédent trouvé.")
                        break

                    # Mettre à jour la position actuelle pour éviter les boucles infinies
                    currentLine = caretInfo.bookmark.startOffset

            except Exception as e:
                log.error(f"Erreur lors de la recherche du niveau d'indentation précédent : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")

        
    def script_moveToNextIndentedLine(self, gesture):
        """Déplace le curseur vers la ligne suivante ayant le même niveau d'indentation et annonce le niveau actuel."""
        log.debug("Raccourci Control+Alt+Down détecté, exécution de moveToNextIndentedLine.")

        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)  # Étendre à la ligne entière
                currentLineText = caretInfo.text

                # Calculer l'indentation actuelle en tenant compte des tabulations
                currentIndent = 0
                for char in currentLineText:
                    if char == '\t':
                        currentIndent += 4  # Une tabulation = 4 espaces (ajuste selon ton éditeur)
                    elif char == ' ':
                        currentIndent += 1
                    else:
                        break

                # Annoncer le niveau d'indentation actuel
                speech.speakMessage(f"Indentation actuel : {currentIndent}")

                # Initialiser la position de la ligne actuelle
                currentLine = caretInfo.bookmark.startOffset

                # Parcourir les lignes suivantes pour trouver une ligne avec le même niveau d'indentation
                while True:
                    # Déplacer le curseur à la ligne suivante
                    caretInfo.move(textInfos.UNIT_LINE, 1)
                    caretInfo.expand(textInfos.UNIT_LINE)
                    lineText = caretInfo.text

                    # Calculer l'indentation de la ligne suivante
                    lineIndent = 0
                    for char in lineText:
                        if char == '\t':
                            lineIndent += 4  # Une tabulation = 4 espaces (ajuste selon ton éditeur)
                        elif char == ' ':
                            lineIndent += 1
                        else:
                            break

                    # Vérifier si l'indentation est égale à l'actuelle
                    if lineIndent == currentIndent:
                        # Déplacer le curseur au début de la ligne
                        caretInfo.updateCaret()
                        log.debug(f"Ligne suivante avec le même niveau d'indentation trouvée : {lineText.strip()}")
                        speech.speakMessage(f"Ligne suivante avec le même niveau d'indentation trouvée : {lineText.strip()}")
                        break

                    # Si on atteint la fin du document, arrêter la recherche
                    if caretInfo.bookmark.startOffset <= currentLine:
                        log.debug("Aucune ligne suivante avec le même niveau d'indentation trouvée.")
                        speech.speakMessage("Fin du document atteinte.")
                        break

                    # Mettre à jour la position actuelle pour éviter les boucles infinies
                    currentLine = caretInfo.bookmark.startOffset

            except Exception as e:
                log.error(f"Erreur lors de la recherche de la ligne suivante avec le même niveau d'indentation : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")


    def script_moveToPreviousIndentLevel(self, gesture):
        """Déplace le curseur vers le niveau d'indentation précédent et annonce le niveau actuel."""
        log.debug("Raccourci Alt+Up détecté, exécution de moveToPreviousIndentLevel.")

        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)  # Étendre à la ligne entière
                currentLineText = caretInfo.text

                # Calculer l'indentation actuelle en tenant compte des tabulations
                currentIndent = 0
                for char in currentLineText:
                    if char == '\t':
                        currentIndent += 4  # Une tabulation = 4 espaces (ajuste selon ton éditeur)
                    elif char == ' ':
                        currentIndent += 1
                    else:
                        break

                # Initialiser la position de la ligne actuelle
                currentLine = caretInfo.bookmark.startOffset

                # Parcourir les lignes précédentes pour trouver un niveau d'indentation différent
                while True:
                    # Déplacer le curseur à la ligne précédente
                    caretInfo.move(textInfos.UNIT_LINE, -1)
                    caretInfo.expand(textInfos.UNIT_LINE)
                    lineText = caretInfo.text

                    # Calculer l'indentation de la ligne précédente
                    lineIndent = 0
                    for char in lineText:
                        if char == '\t':
                            lineIndent += 4  # Une tabulation = 4 espaces (ajuste selon ton éditeur)
                        elif char == ' ':
                            lineIndent += 1
                        else:
                            break

                    # Vérifier si l'indentation est différente de l'actuelle
                    if lineIndent != currentIndent:
                        # Déplacer le curseur au début de la ligne
                        caretInfo.updateCaret()
                        log.debug(f"Niveau d'indentation précédent trouvé : {lineText.strip()}")

                        # Annoncer le niveau d'indentation actuel de la nouvelle ligne
                        speech.speakMessage(f"Indentation actuel : {lineIndent}")
                        break

                    # Si on atteint le début du document, arrêter la recherche
                    if caretInfo.bookmark.startOffset >= currentLine:
                        log.debug("Aucun niveau d'indentation précédent trouvé.")
                        speech.speakMessage("Aucun niveau d'indentation précédent trouvé.")
                        break

                    # Mettre à jour la position actuelle pour éviter les boucles infinies
                    currentLine = caretInfo.bookmark.startOffset

            except Exception as e:
                log.error(f"Erreur lors de la recherche du niveau d'indentation précédent : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")

            
    def script_selectToPreviousIndentLevel(self, gesture):
        """Sélectionne le texte jusqu'au niveau d'indentation précédent, puis place le curseur au début de la sélection."""
        log.debug("Raccourci Shift+Alt+Up détecté, exécution de selectToPreviousIndentLevel.")

        if self.edit:
            try:
                # Obtenir la position actuelle du curseur
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)
                currentLineText = caretInfo.text
                currentIndent = len(currentLineText) - len(currentLineText.lstrip())  # Calculer l'indentation actuelle
                startPosition = caretInfo.bookmark.startOffset  # Position de départ de la ligne actuelle

                # Créer un objet TextInfo pour la sélection
                selectionInfo = self.edit.makeTextInfo(textInfos.POSITION_SELECTION)
                selectionInfo.setEndPoint(caretInfo, "endToEnd")  # Définir le point de départ de la sélection

                # Parcourir les lignes précédentes pour trouver un niveau d'indentation différent
                while True:
                    # Déplacer le curseur à la ligne précédente
                    caretInfo.move(textInfos.UNIT_LINE, -1)
                    caretInfo.expand(textInfos.UNIT_LINE)
                    lineText = caretInfo.text
                    lineIndent = len(lineText) - len(lineText.lstrip())  # Calculer l'indentation de la ligne

                    # Vérifier si l'indentation est différente de l'actuelle
                    if lineIndent != currentIndent:
                        # Sélectionner depuis la ligne actuelle jusqu'à cette ligne
                        selectionInfo.setEndPoint(caretInfo, "startToStart")  # Définir le point de fin de la sélection
                        selectionInfo.updateSelection()
                        log.debug(f"Sélection jusqu'au niveau d'indentation précédent : {lineText.strip()}")
                        speech.speakMessage(f"Sélection jusqu'au niveau d'indentation précédent : {lineText.strip()}")

                        # Déplacer le curseur au début de la sélection
                        startSelection = selectionInfo.copy()
                        startSelection.collapse(start=True)  # Déplacer le curseur au début de la sélection
                        startSelection.updateCaret()

                        log.debug("Curseur déplacé au début de la sélection.")
                        speech.speakMessage("Curseur déplacé au début de la sélection.")
                        break

                    # Si on atteint le début du document, arrêter la recherche
                    if caretInfo.bookmark.startOffset >= startPosition:
                        log.debug("Aucun niveau d'indentation précédent trouvé.")
                        speech.speakMessage("Aucun niveau d'indentation précédent trouvé.")
                        break

            except Exception as e:
                log.error(f"Erreur lors de la sélection jusqu'au niveau d'indentation précédent : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")


    def script_selectToNextIndentLevel(self, gesture):
        """Sélectionne le texte jusqu'au prochain niveau d'indentation."""
        log.debug("Raccourci Shift+Alt+Down détecté, exécution de selectToNextIndentLevel.")

        if self.edit:
            try:
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)
                currentLineText = caretInfo.text
                currentIndent = len(currentLineText) - len(currentLineText.lstrip())
                startPosition = caretInfo.bookmark.startOffset

                while True:
                    caretInfo.move(textInfos.UNIT_LINE, 1)
                    caretInfo.expand(textInfos.UNIT_LINE)
                    lineText = caretInfo.text
                    lineIndent = len(lineText) - len(lineText.lstrip())

                    if lineIndent != currentIndent:
                        # Sélectionner jusqu'à cette ligne
                        selectionInfo = self.edit.makeTextInfo(textInfos.POSITION_SELECTION)
                        selectionInfo.setEndPoint(caretInfo, "endToEnd")
                        selectionInfo.updateSelection()
                        log.debug(f"Sélection jusqu'au niveau d'indentation suivant : {lineText.strip()}")
                        speech.speakMessage(f"Sélection jusqu'au niveau d'indentation suivant : {lineText.strip()}")
                        break

                    if caretInfo.bookmark.startOffset <= startPosition:
                        log.debug("Aucun niveau d'indentation suivant trouvé.")
                        speech.speakMessage("Aucun niveau d'indentation suivant trouvé.")
                        break

            except Exception as e:
                log.error(f"Erreur lors de la sélection jusqu'au niveau d'indentation suivant : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")


    def script_moveToFirstLineInIndentation(self, gesture):
        """Déplace le curseur vers la première ligne du niveau d'indentation actuel."""
        log.debug("Raccourci Alt+Home détecté, exécution de moveToFirstLineInIndentation.")

        if self.edit:
            try:
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)
                currentLineText = caretInfo.text
                currentIndent = len(currentLineText) - len(currentLineText.lstrip())
                currentLine = caretInfo.bookmark.startOffset

                while True:
                    caretInfo.move(textInfos.UNIT_LINE, -1)
                    caretInfo.expand(textInfos.UNIT_LINE)
                    lineText = caretInfo.text
                    lineIndent = len(lineText) - len(lineText.lstrip())

                    if lineIndent != currentIndent:
                        # Revenir à la ligne précédente (la première du niveau actuel)
                        caretInfo.move(textInfos.UNIT_LINE, 1)
                        caretInfo.updateCaret()
                        log.debug(f"Première ligne du niveau d'indentation actuel trouvée : {caretInfo.text.strip()}")
                        speech.speakMessage(f"Première ligne du niveau d'indentation actuel trouvée : {caretInfo.text.strip()}")
                        break

                    if caretInfo.bookmark.startOffset >= currentLine:
                        log.debug("Début du fichier atteint.")
                        speech.speakMessage("Début du fichier atteint.")
                        break

            except Exception as e:
                log.error(f"Erreur lors de la recherche de la première ligne du niveau d'indentation actuel : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")

    def script_moveToLastLineInIndentation(self, gesture):
        """Déplace le curseur vers la dernière ligne du niveau d'indentation actuel."""
        log.debug("Raccourci Alt+End détecté, exécution de moveToLastLineInIndentation.")

        if self.edit:
            try:
                caretInfo = self.edit.makeTextInfo(textInfos.POSITION_CARET)
                caretInfo.expand(textInfos.UNIT_LINE)
                currentLineText = caretInfo.text
                currentIndent = len(currentLineText) - len(currentLineText.lstrip())
                currentLine = caretInfo.bookmark.startOffset

                while True:
                    caretInfo.move(textInfos.UNIT_LINE, 1)
                    caretInfo.expand(textInfos.UNIT_LINE)
                    lineText = caretInfo.text
                    lineIndent = len(lineText) - len(lineText.lstrip())

                    if lineIndent != currentIndent:
                        # Revenir à la ligne précédente (la dernière du niveau actuel)
                        caretInfo.move(textInfos.UNIT_LINE, -1)
                        caretInfo.updateCaret()
                        log.debug(f"Dernière ligne du niveau d'indentation actuel trouvée : {caretInfo.text.strip()}")
                        speech.speakMessage(f"Dernière ligne du niveau d'indentation actuel trouvée : {caretInfo.text.strip()}")
                        break

                    if caretInfo.bookmark.startOffset <= currentLine:
                        log.debug("Fin du fichier atteinte.")
                        speech.speakMessage("Fin du fichier atteinte.")
                        break

            except Exception as e:
                log.error(f"Erreur lors de la recherche de la dernière ligne du niveau d'indentation actuel : {e}")
        else:
            log.debug("Aucun objet d'édition trouvé.")
    
    
    __gestures = {
    "kb:NVDA+F2": "moveToNextFunction",      
    "kb:Shift+F2": "moveToPreviousFunction",
    "kb:F7": "moveToNextClass",
    "kb:Shift+F7": "moveToPreviousClass",
    "kb:control+shift+r": "selectCurrentClass",
    "kb:control+r": "selectCurrentFunction",
    "kb:control+shift+delete": "deleteCurrentClass",
    "kb:control+delete": "deleteCurrentFunction",
    "kb:control+F5": "executePythonCode",
    "kb:alt+downArrow": "moveToNextIndentLevel",
    "kb:alt+upArrow": "moveToPreviousIndentLevel",      
    "kb:control+alt+downArrow": "moveToNextIndentedLine",
    "kb:control+alt+upArrow": "moveToPreviousIndentedLine",
    "kb:shift+alt+downArrow": "selectToNextIndentLevel",
    "kb:shift+alt+upArrow": "selectToPreviousIndentLevel",
    "kb:alt+!": "moveToFirstLineInIndentation",
    "kb:alt+:": "moveToLastLineInIndentation",
}