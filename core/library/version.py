
init_version = {
    'type': 'DEV',
    'major': 0,
    'minor': 0,
    'patch': 0,
    'release': 0
}


class Version():

    def __init__(self, version_data=None):
        # Default version control
        if version_data is None:
            version_data = init_version

        # Initialize version data
        self.type = version_data['type']
        self.major = version_data['major']
        self.minor = version_data['minor']
        self.patch = version_data['patch']
        self.release = version_data['release']

    def __str__(self):
        # Return string representation of software version eg; R1 1.0.0 dev
        return f"R{self.release} {self.major}.{self.minor}.{self.patch} {self.type}"

    def increment_patch_count(self):
        self.patch = int(self.patch) + 1

    def increment_minor_count(self):
        self.patch = 0
        self.minor = int(self.minor) + 1

    def increment_major_count(self):
        self.patch = 0
        self.minor = 0
        self.major = int(self.major) + 1

    def set_dev_type(self):
        self.release = 'DEV'

    def set_staging_type(self):
        self.release = 'STAGING'

    def set_production_type(self):
        self.release = 'PRODUCTION'
