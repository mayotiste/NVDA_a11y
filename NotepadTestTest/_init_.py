import globalPluginHandler
import speech
import api
import keyboard
import appModuleHandler

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super().__init__()

    def script_go_to_next_function(self, gesture):
        """Navigue vers la définition de la fonction suivante dans Notepad++"""
        import ctypes
        from time import sleep

        # Interaction avec Notepad++ via un raccourci clavier pour aller à la fonction suivante
        # Notepad++ utilise le raccourci F12 pour aller à la définition de la fonction (si définie dans les préférences).
        
        # Simuler la pression de la touche F12 (dans Notepad++, cela navigue vers la fonction suivante)
        keyboard.press_and_release('f12')
        
        # Attente pour s'assurer que l'action est bien prise en compte
        sleep(1)
        
        # On annonce que l'on a navigué vers la fonction suivante
        speech.speak("Fonction suivante")

    # Définir le raccourci clavier
    __gestures = {
        "kb:f2": script_go_to_next_function,
    }
