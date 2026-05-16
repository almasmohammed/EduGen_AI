import streamlit as st
from database.db import save_document, get_all_documents, delete_document
from utils.helpers import extract_text_from_file, truncate_text, detect_file_type


def render():
    st.markdown("## 📤 Upload Study Materials")
    st.markdown("Upload your educational documents and we'll extract the content for quiz and flashcard generation.")

    # ── Upload widget ──────────────────────────────────────────────────────
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded = st.file_uploader(
            "Choose a file",
            type=["pdf", "txt", "docx", "md"],
            help="Supported formats: PDF, TXT, DOCX, Markdown",
        )

    with col2:
        st.markdown("#### 📋 Supported Formats")
        st.markdown("""
        - 📕 PDF documents
        - 📝 Text files (.txt)
        - 📄 Word documents (.docx)
        - 📓 Markdown (.md)
        """)

    if uploaded:
        file_bytes = uploaded.read()
        file_type = detect_file_type(uploaded.name)

        st.markdown("---")
        st.markdown(f"**File:** `{uploaded.name}` · **Size:** {len(file_bytes)/1024:.1f} KB · **Type:** `{file_type.upper()}`")

        with st.spinner("🔍 Extracting text from document..."):
            try:
                text = extract_text_from_file(file_bytes, uploaded.name)
                word_count = len(text.split())

                st.success(f"✅ Successfully extracted **{word_count:,} words** from your document!")

                with st.expander("📖 Preview extracted content", expanded=False):
                    st.text_area("", truncate_text(text, 1500), height=200, disabled=True)

                col_a, col_b = st.columns([1, 3])
                with col_a:
                    if st.button("💾 Save to Library", type="primary", use_container_width=True):
                        doc_id = save_document(uploaded.name, file_type, text)
                        st.success(f"✅ Saved! Document ID: **{doc_id}**")
                        st.session_state["last_doc_id"] = doc_id
                        st.session_state["last_doc_content"] = text
                        st.rerun()

            except Exception as e:
                st.error(f"❌ Error processing file: {e}")
                st.info("💡 Make sure the file is not corrupted and contains readable text.")

    # ── Library ───────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 📚 Document Library")

    docs = get_all_documents()

    if not docs:
        st.info("📭 No documents uploaded yet. Upload your first study material above!")
        return

    st.markdown(f"**{len(docs)} document(s)** in your library")

    for doc in docs:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                icon = {"pdf": "📕", "docx": "📄", "txt": "📝", "md": "📓"}.get(doc["file_type"], "📎")
                st.markdown(f"{icon} **{doc['filename']}**")
                st.caption(f"Uploaded: {doc['upload_time'][:16]}")
            with col2:
                st.metric("Words", f"{doc['word_count']:,}")
            with col3:
                st.caption(doc["file_type"].upper())
            with col4:
                if st.button("🗑️", key=f"del_{doc['id']}", help="Delete document"):
                    delete_document(doc["id"])
                    st.rerun()

        st.divider()
