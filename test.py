from resources.readsettings import ReadSettings
from autoprocess import sonarr
import sys

settings = ReadSettings()
sonarr.processEpisode(sys.argv[1], settings, importMode="Copy")
