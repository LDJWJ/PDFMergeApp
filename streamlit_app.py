import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def merge_pdfs(uploaded_files):
    """
    Merge multiple PDF files into a single PDF.

    :param uploaded_files: List of uploaded PDF files
    :return: BytesIO object containing the merged PDF
    """
    writer = PdfWriter()

    for uploaded_file in uploaded_files:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            writer.add_page(page)

    # Save merged PDF to a BytesIO object
    merged_pdf = BytesIO()
    writer.write(merged_pdf)
    merged_pdf.seek(0)
    return merged_pdf

def main():
    st.title('📄 PDF Merger')

    st.sidebar.header('Instructions')
    st.sidebar.write("1. Upload multiple PDF files.")
    st.sidebar.write("2. Click 'Merge PDFs' to create a single merged PDF.")

    # File uploader for multiple PDF files
    uploaded_files = st.file_uploader(
        "Upload multiple PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Select multiple PDF files to merge"
    )

    if uploaded_files:
        st.subheader("Uploaded Files")
        for uploaded_file in uploaded_files:
            st.write(uploaded_file.name)

        if st.button("Merge PDFs"):
            try:
                merged_pdf = merge_pdfs(uploaded_files)

                # Provide download link for the merged PDF
                st.subheader("Download Merged PDF")
                st.download_button(
                    label="Download Merged PDF",
                    data=merged_pdf,
                    file_name="merged.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"Error merging PDFs: {e}")

if __name__ == '__main__':
    main()
