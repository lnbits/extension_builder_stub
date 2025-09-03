import os
import zipfile


def replace_text_in_files(directory, old_text, new_text, file_extensions=None):
    """
    Recursively replaces text in all files under the given directory.

    Parameters:
    - directory (str): Root directory to start searching.
    - old_text (str): Text to search for.
    - new_text (str): Text to replace with.
    - file_extensions (list[str], optional): Only process files with these extensions.
    """
    for root, _, files in os.walk(directory):
        if root.startswith(".") or root in ["__pycache__", "node_modules"]:
            continue
        for filename in files:
            if file_extensions:
                if not any(filename.endswith(ext) for ext in file_extensions):
                    continue
            if filename in ["ext_rename.py", "ext_replace.py"]:
                continue

            file_path = os.path.join(root, filename)
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
                if old_text in content:
                    new_content = content.replace(old_text, new_text)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated: {file_path}")
            except (UnicodeDecodeError, PermissionError, FileNotFoundError) as e:
                print(f"Skipped {file_path}: {e}")


def rename_files_and_dirs_in_directory(directory, old_text, new_text):
    """
    Recursively renames files and directories by replacing part of their names.

    Parameters:
    - directory (str): Root directory to start renaming.
    - old_text (str): Text to be replaced.
    - new_text (str): Text to replace with.
    """
    # First rename directories (bottom-up) so we don't lose paths while renaming
    for root, dirs, files in os.walk(directory, topdown=False):
        # Rename files
        for filename in files:
            if old_text in filename:
                old_path = os.path.join(root, filename)
                new_filename = filename.replace(old_text, new_text)
                new_path = os.path.join(root, new_filename)
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed file: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Failed to rename file {old_path}: {e}")

        # Rename directories
        for dirname in dirs:
            if old_text in dirname:
                old_dir_path = os.path.join(root, dirname)
                new_dir_name = dirname.replace(old_text, new_text)
                new_dir_path = os.path.join(root, new_dir_name)
                try:
                    os.rename(old_dir_path, new_dir_path)
                    print(f"Renamed directory: {old_dir_path} -> {new_dir_path}")
                except Exception as e:
                    print(f"Failed to rename directory {old_dir_path}: {e}")


def zip_directory(source_dir, zip_path):
    """
    Zips the contents of a directory (including subdirectories and files).

    Parameters:
    - source_dir (str): The path of the directory to zip.
    - zip_path (str): The path where the .zip file will be saved.
    """
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            if root.startswith(".") or root in ["__pycache__", "node_modules"]:
                continue
            for file in files:
                full_path = os.path.join(root, file)
                # Add file with a relative path inside the zip
                relative_path = os.path.relpath(full_path, start=source_dir)
                zipf.write(full_path, arcname=relative_path)
    print(f"Directory '{source_dir}' zipped to '{zip_path}'")


# def test():

    # replace_text_in_files(
    #     directory='.',
    #     old_text='MyExtension',
    #     new_text='Extension Builder Stub',
    #     file_extensions=['.js', '.html', '.md']
    # )




def test2():
    replace_text_in_files(
        directory=".",
        old_text="extension_builder_stub",
        new_text="donations",
        file_extensions=[".py", ".js", ".html", ".md", ".json", ".toml"],
    )
    replace_text_in_files(
        directory=".",
        old_text="OwnerData",
        new_text="DonationsCampaign",
        file_extensions=[".py"],
    )
    replace_text_in_files(
        directory=".",
        old_text="Owner Data",
        new_text="Donations Campaign",
        file_extensions=[".py"],
    )
    replace_text_in_files(
        directory=".",
        old_text="ClientData",
        new_text="UserDonation",
        file_extensions=[".py"],
    )
    replace_text_in_files(
        directory=".",
        old_text="Client Data",
        new_text="User Donation",
        file_extensions=[".py"],
    )

    replace_text_in_files(
        directory=".",
        old_text="owner_data",
        new_text="donations_campaign",
        file_extensions=[".py"],
    )
    replace_text_in_files(
        directory=".",
        old_text="owner data",
        new_text="donations campaign",
        file_extensions=[".py"],
    )

    rename_files_and_dirs_in_directory(
        directory=".", old_text="extension_builder_stub", new_text="donations"
    )

    zip_directory(".", "donations.zip")


test2()
