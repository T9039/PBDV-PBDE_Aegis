import os
import random
import shutil

from app import app, db
from models import User

# Define our paths based on your screenshot
SOURCE_DIR = os.path.join("static", "images", "profiles")
DEST_DIR = os.path.join(
    "static", "images", "avatars"
)  # We create a new folder for the renamed copies!


def assign_random_profiles():
    with app.app_context():
        # 1. Ensure the destination directory exists
        if not os.path.exists(DEST_DIR):
            os.makedirs(DEST_DIR)

        # 2. Get all the image filenames from your source folder
        if not os.path.exists(SOURCE_DIR):
            print(f"❌ Error: Source directory '{SOURCE_DIR}' not found!")
            return

        available_images = [
            f
            for f in os.listdir(SOURCE_DIR)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
        ]

        if not available_images:
            print(f"❌ Error: No images found in '{SOURCE_DIR}'!")
            return

        print(f"📸 Found {len(available_images)} images to use as a pool.")

        # 3. Get all users
        users = User.query.all()
        print(f"🔄 Assigning profiles to {len(users)} users...")

        for user in users:
            # Pick a random image from the pool
            random_img = random.choice(available_images)
            src_path = os.path.join(SOURCE_DIR, random_img)

            # Extract the extension (e.g., .jpg) and create the new filename
            ext = os.path.splitext(random_img)[1]
            new_filename = f"user_{user.id}_avatar{ext}"
            dest_path = os.path.join(DEST_DIR, new_filename)

            # Copy and rename the file
            shutil.copy2(src_path, dest_path)

            # Update the database (saving the relative path for easy URL generation)
            user.profile_picture = f"images/avatars/{new_filename}"

        # Save all changes to the database
        db.session.commit()
        print("✅ Success! All users have been assigned random profile pictures.")


if __name__ == "__main__":
    assign_random_profiles()
