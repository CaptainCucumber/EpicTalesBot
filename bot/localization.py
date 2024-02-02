import os
import gettext

# Define the language and domain
lang = "ru"
domain = "epictales"

# Define the absolute location of your translation files
current_dir = os.path.dirname(os.path.abspath(__file__))
localedir = os.path.join(current_dir, "locales")

# Get the translation object for the specified language
translation = gettext.translation(domain, localedir, languages=[lang], fallback=False)

# Install the translation object
translation.install()

_ = translation.gettext
