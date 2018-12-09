import kivy
import os

kivy.require("1.10.1")

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

# ------------------------------------------------------------------------------
# Dialogs. Must match kv file
class LoadDialog(FloatLayout):
    def __init__(self, on_file_selected, **kwargs):
        """
        @param on_file_selected: callback that returns the filename of the selected
        file
        """
        super().__init__(**kwargs)
        self._filechooser = self.ids.filechooser
        self._on_file_selected = on_file_selected
        self._btn_cancel = self.ids.btn_cancel
        self._btn_cancel.on_release = self._dismiss_popup
        self._btn_open = self.ids.btn_open
        self._btn_open.on_release = self._btn_open_clicked
        self._popup = Popup(title="Open file", content=self, size_hint=(0.8, 0.8))

    def show(self):
        print("show open")
        self._popup.open()

    def _dismiss_popup(self):
        self._popup.dismiss()

    def _btn_open_clicked(self):
        print("file selected")
        filename = self._filechooser.selection
        self._on_file_selected(filename)
        self._dismiss_popup()


class SaveDialog(FloatLayout):
    def __init__(self, on_file_selected, **kwargs):
        """
        @param on_file_selected: callback that returns the filename of the selected
        file
        """
        super().__init__(**kwargs)
        self._on_file_selected = on_file_selected
        self._filechooser = self.ids.filechooser
        self._filechooser.bind(selection=lambda obj, value: self._on_selection())

        self._btn_cancel = self.ids.btn_cancel
        self._btn_cancel.on_release = self._dismiss_popup

        self._btn_save = self.ids.btn_save
        self._btn_save.on_release = self._btn_save_clicked

        self._text_input = self.ids.text_input

        self._popup = Popup(title="Save file", content=self, size_hint=(0.8, 0.8))

    def show(self):
        self._popup.open()

    def _dismiss_popup(self):
        self._popup.dismiss()

    def _btn_save_clicked(self):
        path = self._filechooser.path
        filename = self._filechooser.selection and self._filechooser.selection[0] or ""
        content = self._text_input.text
        self._on_file_selected(path, filename)
        self._dismiss_popup()

    def _on_selection(self):
        self._text_input.text = (
            self._filechooser.selection and self._filechooser.selection[0] or ""
        )


class SaveChangesDialog(FloatLayout):
    def __init__(self, on_yes, on_no, **kwargs):
        super().__init__(**kwargs)
        self._on_yes = on_yes
        self._on_no = on_no

        self._btn_yes = self.ids.btn_yes
        self._btn_yes.on_release = self._on_yes_clicked

        self._btn_no = self.ids.btn_no
        self._btn_no.on_release = self._on_no_clicked

        self._btn_cancel = self.ids.btn_cancel
        self._btn_cancel.on_release = self._dismiss_popup

        self._popup = Popup(title="Save changes?", content=self, size_hint=(0.6, 0.6))

    def show(self):
        self._popup.open()

    def _on_yes_clicked(self):
        self._on_yes()
        self._dismiss_popup()

    def _on_no_clicked(self):
        self._on_no()
        self._dismiss_popup()

    def _dismiss_popup(self):
        self._popup.dismiss()

class AboutDialog(FloatLayout):
    def __init__(self, **kwargs):
        # Always call the __init__ function of super class
        # super(GUI, self).__init__(**kwargs)
        super().__init__(**kwargs)
        self._popup = Popup(title="about", content=self, size_hint=(0.8, 0.8))

    def show(self):
        print("show about")
        self._popup.open()

class HelpDialog(FloatLayout):
    def __init__(self, **kwargs):
        # Always call the __init__ function of super class
        # super(GUI, self).__init__(**kwargs)
        super().__init__(**kwargs)
        self._popup = Popup(title="help", content=self, size_hint=(0.8, 0.8))

    def show(self):
        print("show help")
        self._popup.open()


# ------------------------------------------------------------------------------
# Main GUI
class GUI(FloatLayout):
    def __init__(self, **kwargs):
        # Always call the __init__ function of super class
        # super(GUI, self).__init__(**kwargs)
        super().__init__(**kwargs)

        # Initialize class variables
        self.modified = False
        self.path_and_file_name = None
        self._popup = Popup()

        # Retrieve your widgets
        self._init_menu()

        self._textpad = self.ids.textpad
        self._textpad.bind(text=lambda obj, value: self.text_modified())
        
        self._load_dlg = LoadDialog(on_file_selected=self.open_file)
        self._about_dlg = AboutDialog()
        self._help_dlg = HelpDialog()
        self._save_dlg = SaveDialog(on_file_selected=self.save_file)
        self._savechanges_dlg = SaveChangesDialog(
            on_yes=self.show_save_file, on_no=self.new_file
        )
        self._saveexit_dlg = SaveChangesDialog(
            on_yes=self.show_save_file, on_no=self.exit
        )

    def _init_menu(self):
        self._menu_new = self.ids.menu_new
        self._menu_new.on_release = self.show_new_file

        self._menu_open = self.ids.menu_open
        self._menu_open.on_release = self.show_open_file

        self._menu_save = self.ids.menu_save
        self._menu_save.on_release = self.show_save_file

        self._menu_save_as = self.ids.menu_save_as
        self._menu_save_as.on_release = self.show_save_file_as

        self._menu_exit = self.ids.menu_exit
        self._menu_exit.on_release = self.show_exit

        self._menu_about = self.ids.menu_about
        self._menu_about.on_release = self.show_about

        self._menu_help = self.ids.menu_help
        self._menu_help.on_release = self.show_help

    def dismiss_popup(self):
        # Closes the popup (new, save, etc)
        self._popup.dismiss()

    def text_modified(self):
        # Sets a flag whenever the text changes
        self.modified = True
    
    def show_new_file(self):
        if self.modified:
            # If the text as modified, opens a dialog asking
            # if the user wants to save the changes
            self._savechanges_dlg.show()
        else:
            # Otherwise, just clear the text
            self.new_file()

    def new_file(self):
        # Deletes all the text in the widget
        self._textpad.text = ""
        self.modified = False

    def show_open_file(self):
        self._load_dlg.show()

    def show_about(self):
        self._about_dlg.show()

    def show_help(self):
        self._help_dlg.show()

    def open_file(self, filename):
        # Reads the content of a given file and puts its text into the widget
        self.path_and_file_name = filename[0]
        with open(self.path_and_file_name) as stream:
            self._textpad.text = stream.read()
        self.modified = False
        
    def show_save_file_as(self):
        self._save_dlg.show()

    def show_save_file(self):
        # If the name of the file does not exist
        # Opens the dialog allowing to set a name for the file
        # Otherwise, saves the file using the current name

        if self.path_and_file_name is None:
            self.show_save_file_as()
        else:
            self.save_file("", self.path_and_file_name)

    def save_file(self, path, filename):
        # Writes the content of the widget into a file
        self.path_and_file_name = os.path.join(path, filename)
        with open(self.path_and_file_name, "w") as stream:
            stream.write(self._textpad.text)
        self.modified = False

    def show_exit(self):
        if self.modified:
            # If the text as modified, opens a dialog asking if the user wants to save the changes
            self._saveexit_dlg.show()
        else:
            self.exit()

    def exit(self):
        App.get_running_app().stop()


# ------------------------------------------------------------------------------
# Builds the GUI
class GUIApp(App):
    def build(self):
        return GUI()


# ------------------------------------------------------------------------------
# Runs the application
if __name__ == "__main__":
    GUIApp().run()
