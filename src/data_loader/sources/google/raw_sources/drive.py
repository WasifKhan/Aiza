from data_loader.sources.base_processor import BaseProcessor


class Drive(BaseProcessor):
    def __init__(self, service):
        self.service = service
        '''
        print("\n📂 **Google Drive Files:**")
        for file in self.get_data()[0:5]:
            print(f"- {file['name']} (ID: {file['id']})")
        '''

    def get_data(self):
        """Fetches all files and folders from Google Drive."""
        query = "'root' in parents or mimeType != 'application/vnd.google-apps.folder'"
        results = self.service.files().list(q=query, pageSize=1000, fields="files(id, name, mimeType)").execute()
        all_files = results.get("files", [])
        return all_files[0:20]

    def process_file(self, file, generate_data):
        """Processes a file from Google Drive without downloading it."""
        file_id = file["id"]
        file_name = file["name"]
        mime_type = file["mimeType"]
        GOOGLE_DOC_EXPORTS = {
            "application/vnd.google-apps.document": "text/plain",  # Google Docs → Plain Text
            "application/vnd.google-apps.spreadsheet": "text/csv",  # Google Sheets → CSV
            "application/vnd.google-apps.presentation": "text/plain"  # Google Slides → Plain Text
        }

        print(f"📂 Processing: {file_name} ({mime_type})")

        if mime_type in GOOGLE_DOC_EXPORTS:
            # Google Docs, Sheets, and Slides: Export & Process as text
            request = self.service.files().export_media(fileId=file_id, mimeType=GOOGLE_DOC_EXPORTS[mime_type])
            file_content = request.execute().decode("utf-8")
            print(f"📜 Extracted Content (Google Doc/Sheet): {file_content[:500]}...\n")

        elif mime_type.startswith("image/"):
            return None
            # Image Processing: Just log (OCR or AI processing can be done here)
            print(f"🖼️ Skipping image file: {file_name}")

        elif mime_type == "application/pdf":
            # PDF Processing: Extract text without saving
            request = self.service.files().get_media(fileId=file_id)
            file_content = BytesIO(request.execute())  # Stream content
            print(f"📄 PDF processed: {file_name} (Size: {len(file_content.getvalue())} bytes)\n")

        elif mime_type.startswith("text/"):
            # Plain text files: Read content
            request = self.service.files().get_media(fileId=file_id)
            file_content = request.execute().decode("utf-8")
            print(f"📝 Text File Content: {file_content[:500]}...\n")

        else:
            print(f"⚠️ Unsupported file type: {mime_type}")
            return None
        datapoint = generate_data(file_content)
        print(f"file content:\n{file_content}\n{'*'*10}\nRESPONSE\n{'*'*10}\n")
        print(f"{datapoint}\n")

        return file_content


