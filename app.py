import streamlit as st
import dropbox
from dropbox.files import WriteMode, UploadSessionCursor, CommitInfo
from datetime import datetime
from pathlib import PurePosixPath
import time

st.set_page_config(
    page_title="Αλέξης & Βασιλίνα",
    page_icon="🧡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DROPBOX_FOLDER = "/Alexis & Vasilina Wedding"

# ΣΩΣΤΟ Dropbox File Request
LARGE_VIDEO_URL = "https://www.dropbox.com/request/ws9oyzx9oaf25ror8ub9"

# Από 32MB και πάνω χρησιμοποιούμε chunked upload
SIMPLE_UPLOAD_LIMIT = 32 * 1024 * 1024
CHUNK_SIZE = 8 * 1024 * 1024


def get_dropbox():
    return dropbox.Dropbox(
        app_key=st.secrets["DROPBOX_APP_KEY"],
        app_secret=st.secrets["DROPBOX_APP_SECRET"],
        oauth2_refresh_token=st.secrets["DROPBOX_REFRESH_TOKEN"],
        timeout=900,
    )


def safe_filename(filename):
    filename = PurePosixPath(filename).name
    return filename.replace("/", "_").replace("\\", "_")


def upload_to_dropbox(dbx, uploaded_file, destination):
    uploaded_file.seek(0)
    size = uploaded_file.size

    # Μικρά αρχεία
    if size <= SIMPLE_UPLOAD_LIMIT:
        data = uploaded_file.read()

        dbx.files_upload(
            data,
            destination,
            mode=WriteMode.add,
            autorename=True,
            mute=True,
        )

        del data
        return

    # Μεγαλύτερα αρχεία → chunked upload
    first_chunk = uploaded_file.read(CHUNK_SIZE)

    session = dbx.files_upload_session_start(first_chunk)

    cursor = UploadSessionCursor(
        session_id=session.session_id,
        offset=len(first_chunk),
    )

    commit = CommitInfo(
        path=destination,
        mode=WriteMode.add,
        autorename=True,
        mute=True,
    )

    while cursor.offset < size:
        remaining = size - cursor.offset
        chunk = uploaded_file.read(min(CHUNK_SIZE, remaining))

        if not chunk:
            raise RuntimeError("Το upload σταμάτησε απροσδόκητα.")

        if cursor.offset + len(chunk) >= size:
            dbx.files_upload_session_finish(
                chunk,
                cursor,
                commit,
            )
            cursor.offset += len(chunk)
        else:
            dbx.files_upload_session_append_v2(
                chunk,
                cursor,
            )
            cursor.offset += len(chunk)


def inject_css():
    st.markdown(
        """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=GFS+Didot&family=Noto+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Noto+Serif:ital,wght@0,400;0,500;1,400&display=swap');

        .stApp {
            background:
                radial-gradient(circle at 50% 0%, rgba(218,91,43,.045), transparent 34rem),
                #fffaf4;
            color:#29231f;
        }

        header[data-testid="stHeader"] {
            background:transparent;
        }

        #MainMenu, footer {
            visibility:hidden;
        }

        .block-container {
            max-width:780px;
            padding-top:2.6rem;
            padding-bottom:4rem;
        }

        html, body, [class*="css"] {
            font-family:"Noto Sans", Arial, sans-serif;
        }

        .av-date {
            width:max-content;
            margin:0 auto 1.25rem auto;
            padding:.55rem 1.25rem;
            border:1px solid rgba(211,91,43,.30);
            border-radius:999px;
            font-size:.72rem;
            letter-spacing:.35em;
            color:#c65c35;
        }

        .av-names {
            text-align:center;
            font-family:"GFS Didot","Noto Serif","Times New Roman",serif;
            font-size:clamp(2.15rem,5.8vw,3.35rem);
            line-height:1;
            letter-spacing:-.015em;
            color:#29231f;
            white-space:nowrap;
        }

        .av-amp {
            display:inline-block;
            font-size:.68em;
            padding:0 .14em;
            color:#d65e31;
        }

        .av-partyline {
            text-align:center;
            margin-top:.7rem;
            font-family:"Noto Serif","Times New Roman",serif;
            font-style:italic;
            font-size:1.05rem;
            color:#d45e31;
        }

        .av-rule {
            width:74%;
            height:1px;
            background:rgba(211,91,43,.20);
            margin:2rem auto 1.8rem auto;
        }

        .av-copy {
            text-align:center;
            font-size:.86rem;
            color:#a5654e;
            margin-bottom:1.1rem;
        }

        div[data-testid="stFileUploader"] {
            border:1px solid rgba(211,91,43,.18);
            border-radius:28px;
            padding:.45rem;
            box-shadow:0 10px 30px rgba(95,55,35,.05);
            background:rgba(255,255,255,.45);
        }

        div[data-testid="stFileUploaderDropzone"] {
            border:1px dashed rgba(211,91,43,.35);
            border-radius:22px;
            min-height:140px;
            background:rgba(255,255,255,.38);
        }

        div[data-testid="stFileUploaderDropzone"] button {
            font-family:"Noto Sans",Arial,sans-serif !important;
        }

        div[data-testid="stButton"] button {
            width:100%;
            min-height:58px;
            border-radius:999px;
            border:1px solid rgba(80,55,45,.22);
            background:transparent;
            color:#c28d7c;
            letter-spacing:.18em;
            font-family:"Noto Sans",Arial,sans-serif;
            font-size:.74rem;
        }

        div[data-testid="stButton"] button:hover {
            border-color:#d65e31;
            color:#d65e31;
        }

        .av-large {
            margin-top:2.7rem;
            text-align:center;
        }

        .av-large-title {
            font-family:"GFS Didot","Noto Serif","Times New Roman",serif;
            font-style:italic;
            font-size:1.55rem;
            color:#29231f;
            margin-bottom:.45rem;
        }

        .av-large-copy {
            font-size:.72rem;
            color:#b36d50;
            margin-bottom:.8rem;
        }

        a.av-video-button {
            display:block;
            width:100%;
            box-sizing:border-box;
            text-align:center;
            text-decoration:none;
            padding:1.15rem 1rem;
            border:1px solid #d65e31;
            border-radius:999px;
            color:#d65e31 !important;
            font-family:"Noto Sans",Arial,sans-serif;
            font-size:.74rem;
            letter-spacing:.18em;
            margin-top:.7rem;
        }

        a.av-video-button:hover {
            background:rgba(214,94,49,.04);
        }

        .av-summary {
            text-align:center;
            font-size:.78rem;
            color:#9d6b58;
            margin:.65rem 0;
        }

        .av-thanks {
            text-align:center;
            margin-top:1rem;
            padding:1rem;
        }

        .av-thanks-title {
            font-family:"GFS Didot","Noto Serif","Times New Roman",serif;
            font-size:1.65rem;
            margin-bottom:.25rem;
        }

        @media (max-width:600px) {

            .block-container {
                padding-left:1rem;
                padding-right:1rem;
                padding-top:1.8rem;
            }

            .av-names {
                font-size:clamp(1.9rem,8.7vw,2.55rem);
                line-height:1.05;
                white-space:nowrap;
            }

            .av-amp {
                display:inline-block;
                padding:0 .08em;
                margin:0;
                font-size:.60em;
            }

            .av-partyline {
                font-size:.98rem;
            }

            .av-date {
                font-size:.65rem;
                padding:.48rem .9rem;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    inject_css()

    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0

    st.markdown(
        """
        <div class="av-date">✦ 18 · 09 · 2026 ✦</div>

        <div class="av-names">
            Αλέξης <span class="av-amp">&amp;</span> Βασιλίνα
        </div>

        <div class="av-partyline">
            ✦ one night, lots of memories ✦
        </div>

        <div class="av-rule"></div>

        <div class="av-copy">
            Ανέβασε τις φωτογραφίες και τα βίντεο που τράβηξες σήμερα.
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploads = st.file_uploader(
        "Φωτογραφίες & βίντεο",
        type=[
            "jpg",
            "jpeg",
            "png",
            "heic",
            "webp",
            "mp4",
            "mov",
            "m4v",
            "avi",
            "webm",
        ],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key=f"wedding_upload_{st.session_state.uploader_key}",
    )

    if uploads:
        total_size = sum(f.size for f in uploads)
        total_mb = total_size / (1024 * 1024)

        st.markdown(
            f"""
            <div class="av-summary">
                <strong>{len(uploads)} αρχεία επιλέχθηκαν</strong>
                · {total_mb:,.1f} MB συνολικά
            </div>
            """,
            unsafe_allow_html=True,
        )

    upload_clicked = st.button(
        "ΠΑΤΑ ΕΔΩ",
        disabled=not uploads,
        use_container_width=True,
    )

    if upload_clicked and uploads:
        progress = st.progress(
            0,
            text="Προετοιμασία αρχείων…",
        )

        successful = 0
        errors = []

        try:
            dbx = get_dropbox()

            # Ελέγχουμε ότι λειτουργεί το Dropbox connection
            dbx.users_get_current_account()

            for i, uploaded_file in enumerate(uploads, start=1):
                try:
                    filename = safe_filename(uploaded_file.name)

                    stamp = datetime.now().strftime(
                        "%Y%m%d_%H%M%S_%f"
                    )

                    destination = (
                        f"{DROPBOX_FOLDER}/"
                        f"{stamp}_{filename}"
                    )

                    size_mb = uploaded_file.size / (1024 * 1024)

                    progress.progress(
                        (i - 1) / len(uploads),
                        text=(
                            f"Ανέβασμα {i} από {len(uploads)}"
                            f" · {filename}"
                            f" · {size_mb:,.1f} MB"
                        ),
                    )

                    upload_to_dropbox(
                        dbx,
                        uploaded_file,
                        destination,
                    )

                    successful += 1

                    progress.progress(
                        i / len(uploads),
                        text=(
                            f"Ολοκληρώθηκε {i}"
                            f" από {len(uploads)}"
                        ),
                    )

                    # Μικρό διάλειμμα ανάμεσα στα uploads
                    time.sleep(0.15)

                except Exception as exc:
                    errors.append(
                        f"{uploaded_file.name}: {exc}"
                    )

            if errors:
                st.warning(
                    f"Ανέβηκαν {successful} από "
                    f"{len(uploads)} αρχεία."
                )

                with st.expander(
                    "Προβολή σφαλμάτων"
                ):
                    for error in errors:
                        st.write(error)

            else:
                st.markdown(
                    """
                    <div class="av-thanks">
                        <div class="av-thanks-title">
                            Τέλειο! 🧡
                        </div>
                        <div>
                            Τα αρχεία ανέβηκαν.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.success(
                    "Όλα ανέβηκαν με επιτυχία."
                )

                st.session_state.uploader_key += 1

        except Exception as exc:
            st.error(
                "Δεν μπορέσαμε να συνδεθούμε "
                "με το Dropbox αυτή τη στιγμή."
            )

            with st.expander(
                "Τεχνικές λεπτομέρειες"
            ):
                st.code(str(exc))

        st.markdown(
        f"""
<div class="av-large">
    <div class="av-large-title">
        Έχεις πολύ μεγάλο βίντεο;
    </div>
    <div class="av-large-copy">
        Για βίντεο πάνω από 1 GB.
    </div>
    <a class="av-video-button"
       href="{LARGE_VIDEO_URL}"
       target="_blank"
       rel="noopener noreferrer">ΑΝΕΒΑΣΕ ΤΟ ΒΙΝΤΕΟ</a>
</div>
""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
