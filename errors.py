class EmptyArtistDirError(Exception):
    def __init__(self, folder):
        self.folder = folder

    def __str__(self):
        return f"No audio files in: {self.folder}"

class DestinationExistsError(Exception):
    def __init__(self, dst):
        self.dst = dst

    def __str__(self):
        return f"Destination already exists: \"{self.dst}\""

class TopLevelItemFoundError(Exception):
    def __init__(self, item, folder):
        self.item = item
        self.folder = folder

    def __str__(self):
        return f"\"{self.item}\" is not a folder in {self.folder}"