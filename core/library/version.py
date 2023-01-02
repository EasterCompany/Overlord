
class Version():

    def __init__(self, version_data=None):
        # Default version control
        from core.tools import __version_control__
        version_data = __version_control__
        # Initialize version data
        self.type = version_data['type']
        self.major = version_data['major']
        self.minor = version_data['minor']
        self.patch = version_data['patch']

    def __str__(self):
        # Return string representation of software version eg; 1.0.0 DEV
        return f"{self.major}.{self.minor}.{self.patch} {self.type}"

    def increment_patch_count(self):
        self.patch = int(self.patch) + 1

    def increment_minor_count(self):
        self.patch = 0
        self.minor = int(self.minor) + 1

    def increment_major_count(self):
        self.patch = 0
        self.minor = 0
        self.major = int(self.major) + 1
