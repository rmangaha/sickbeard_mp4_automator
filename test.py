from resources.readsettings import ReadSettings
from autoprocess import sonarr, radarr
from resources.log import getLogger
import sys

log = getLogger("Test")
settings = ReadSettings()
log.info("Initiating Test")
log.debug(sys.argv[1])
# sonarr.processEpisode(sys.argv[1], settings, importMode="Copy", logger=log)
radarr.processMovie(sys.argv[1], settings, importMode="Copy", logger=log)