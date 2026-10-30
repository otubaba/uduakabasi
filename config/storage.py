
from pathlib import PurePosixPath
from cloudinary_storage.storage import MediaCloudinaryStorage


class DynamicMediaCloudinaryStorage(MediaCloudinaryStorage):
    """Use Cloudinary's video resource type for video files."""

    def _get_resource_type(self, name):
        extension = PurePosixPath(name).suffix.lower()

        video_extensions = {
            ".mp4",
            ".mov",
            ".avi",
            ".webm",
            ".mkv",
        }

        if extension in video_extensions:
            return "video"

        return "image"
