import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from streamlit_sortables import sort_items

def merge_pdfs(files, order):
    """
    Merge multiple PDF files into a single PDF in the specified order.

    :param files: List of uploaded PDF files
    :param order: List of file indices specifying the order
    :return: BytesIO object containing the merged PDF
    """
    writer = PdfWriter()

    for index in order:
        reader = PdfReader(files[index])
        for page in reader.pages:
            writer.add_page(page)

    merged_pdf = BytesIO()
    writer.write(merged_pdf)
    merged_pdf.seek(0)
    return merged_pdf

def main():
    st.title('📄 PDF Merger with Sorting')
    
    st.sidebar.header('Instructions')
    st.sidebar.write("1. Upload multiple PDF files.")
    st.sidebar.write("2. Drag and drop to reorder the files.")
    st.sidebar.write("3. Click 'Merge PDFs' to create a single merged PDF.")
    
    uploaded_files = st.file_uploader(
        "Upload multiple PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Select multiple PDF files to merge"
    )

    if uploaded_files:
        file_names = [file.name for file in uploaded_files]
        
        st.subheader("Uploaded Files")
        st.write("Drag and drop to reorder the files:")
        
        # Enable drag-and-drop sorting
        ordered_file_names = sort_items(file_names)
        order = [file_names.index(name) for name in ordered_file_names]
        
        st.write("Sorted Files:")
        st.write(ordered_file_names)

        if st.button("Merge PDFs"):
            try:
                merged_pdf = merge_pdfs(uploaded_files, order)
                
                st.subheader("Download Merged PDF")
                st.download_button(
                    label="Download Merged PDF",
                    data=merged_pdf,
                    file_name="merged_sorted.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error merging PDFs: {e}")

if __name__ == "__main__":
    main()
