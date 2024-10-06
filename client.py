import streamlit as st
import ftplib
import io

def connect_ftp(host, port, username, password):
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, int(port))
        ftp.login(username, password)
        return ftp
    except Exception as e:
        st.error(f"Failed to connect: {str(e)}")
        return None

def upload_file(ftp, file):
    try:
        ftp.storbinary(f"STOR {file.name}", file)
        st.success(f"File {file.name} uploaded successfully!")
    except Exception as e:
        st.error(f"Failed to upload file: {str(e)}")

def download_file(ftp, filename):
    try:
        bio = io.BytesIO()
        ftp.retrbinary(f"RETR {filename}", bio.write)
        return bio
    except Exception as e:
        st.error(f"Failed to download file: {str(e)}")
        return None

def main():
    st.title("FTP Client")

    # FTP connection details
    host = st.text_input("FTP Host IP", "192.168.1.X")
    port = st.text_input("FTP Port", "2121")
    username = st.text_input("Username", "user")
    password = st.text_input("Password", type="password")

    if st.button("Connect"):
        ftp = connect_ftp(host, port, username, password)
        if ftp:
            st.session_state.ftp = ftp
            st.success("Connected to FTP server!")

    if 'ftp' in st.session_state:
        ftp = st.session_state.ftp

        # File upload
        uploaded_file = st.file_uploader("Choose a file to upload", type=["txt", "pdf", "png", "jpg"])
        if uploaded_file is not None:
            if st.button("Upload"):
                upload_file(ftp, uploaded_file)

        # File list and download
        st.write("Files on the server:")
        try:
            files = ftp.nlst()
            for file in files:
                col1, col2 = st.columns([3, 1])
                col1.write(file)
                if col2.button(f"Download {file}"):
                    bio = download_file(ftp, file)
                    if bio:
                        st.download_button(
                            label=f"Click to save {file}",
                            data=bio.getvalue(),
                            file_name=file,
                            mime="application/octet-stream"
                        )
        except Exception as e:
            st.error(f"Failed to list files: {str(e)}")

if __name__ == "__main__":
    main()