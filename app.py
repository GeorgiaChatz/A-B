import re
import uuid
from datetime import datetime, timezone
from pathlib import PurePosixPath

import dropbox
import streamlit as st
from dropbox.files import CommitInfo, UploadSessionCursor, WriteMode

DROPBOX_FOLDER = "/Alexis & Vasilina Wedding"
LARGE_VIDEO_URL = "https://www.dropbox.com/scl/fo/wcq3e9t1y0a6a7iv2z2qi/ADwYz9KlavpR7d1NrporAyo?rlkey=2f123fnlcnhgfi2h2pjurw7o2&st=eeg4o9yt&dl=0"

SIMPLE_UPLOAD_LIMIT = 150 * 1024 * 1024
CHUNK_SIZE = 8 * 1024 * 1024
LARGE_FILE_WARNING_MB = 700

st.set_page_config(
    page_title="Αλέξης & Βασιλίνα — Wedding Memories",
    page_icon="🧡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Montserrat:wght@400;500;600&display=swap');

        :root{
            --paper:#fbf6ef;
            --paper2:#fffdf9;
            --ink:#2b2622;
            --muted:#8f7563;
            --accent:#b9653a;
            --accent-soft:#ead5c6;
            --line:rgba(43,38,34,.15);
        }

        html, body, [class*="css"]{
            font-family:"Montserrat", Arial, sans-serif;
        }

        .stApp{
            background:
              radial-gradient(circle at 12% 8%, rgba(255,255,255,.95), transparent 28rem),
              radial-gradient(circle at 88% 92%, rgba(185,101,58,.10), transparent 30rem),
              linear-gradient(180deg,var(--paper2),var(--paper));
            color:var(--ink);
        }

        header[data-testid="stHeader"]{background:transparent;}
        #MainMenu, footer{visibility:hidden;}

        .block-container{
            max-width:780px;
            padding-top:1.5rem;
            padding-bottom:4rem;
        }

        .av-hero{
            text-align:center;
            padding:1.2rem .8rem .6rem;
        }

        .av-eyebrow{
            font-size:.68rem;
            letter-spacing:.34em;
            text-transform:uppercase;
            color:var(--accent);
            margin-bottom:1.5rem;
        }

        .av-names{
            font-family:"Cormorant Garamond","Baskerville","Times New Roman",serif !important;
            font-size:clamp(3.2rem,9.5vw,5.5rem) !important;
            line-height:.93 !important;
            font-weight:500 !important;
            letter-spacing:-.035em !important;
            text-align:center !important;
            color:var(--ink) !important;
            margin:0 auto !important;
        }

        .av-amp{
            display:inline-block;
            font-style:italic;
            color:var(--accent);
            font-size:.58em;
            padding:0 .10em;
            transform:translateY(-.04em);
        }

        .av-subtitle{
            font-family:"Cormorant Garamond","Baskerville","Times New Roman",serif !important;
            font-size:clamp(1.45rem,4.3vw,1.95rem) !important;
            line-height:1.15 !important;
            font-style:italic !important;
            color:var(--muted) !important;
            margin-top:1.15rem !important;
        }

        .av-date{
            text-align:center;
            font-size:.74rem;
            letter-spacing:.16em;
            text-transform:uppercase;
            color:var(--muted);
            margin-top:.7rem;
        }

        .av-rule{
            width:72%;
            height:1px;
            background:linear-gradient(90deg,transparent,var(--accent-soft),transparent);
            margin:1.6rem auto 2rem;
        }

        .av-copy{
            text-align:center;
            color:var(--muted);
            font-size:.94rem;
            line-height:1.65;
            margin-bottom:1.15rem;
        }

        [data-testid="stFileUploader"]{
            background:rgba(255,255,255,.58);
            border:1px solid var(--line);
            border-radius:24px;
            padding:.4rem;
        }

        [data-testid="stFileUploaderDropzone"]{
            background:rgba(255,255,255,.28);
            border:1px dashed rgba(185,101,58,.30);
            border-radius:20px;
            min-height:145px;
        }

        div.stButton > button{
            width:100%;
            min-height:3.55rem;
            border-radius:999px;
            border:1px solid var(--accent);
            background:var(--accent);
            color:#fff;
            font-size:.82rem;
            font-weight:600;
            letter-spacing:.12em;
            text-transform:uppercase;
        }

        div.stButton > button:hover{
            background:transparent;
            color:var(--accent);
            border-color:var(--accent);
        }

        div[data-testid="stLinkButton"] > a {
            width:100%;
            min-height:3.35rem;
            border-radius:999px !important;
            border:1px solid var(--accent) !important;
            background:transparent !important;
            color:var(--accent) !important;
            font-size:.78rem !important;
            font-weight:600 !important;
            letter-spacing:.1em !important;
            text-transform:uppercase !important;
            display:flex !important;
            align-items:center !important;
            justify-content:center !important;
            text-decoration:none !important;
        }

        .av-large-title{
            text-align:center;
            font-family:"Cormorant Garamond","Baskerville","Times New Roman",serif !important;
            font-size:1.5rem !important;
            font-style:italic;
            color:var(--ink);
            margin-top:1.65rem;
            margin-bottom:.2rem;
        }

        .av-large-copy{
            text-align:center;
            color:var(--muted);
            font-size:.8rem;
            line-height:1.55;
            margin-bottom:.7rem;
        }

        .av-summary{
            background:rgba(255,255,255,.48);
            border:1px solid var(--line);
            border-radius:18px;
            padding:.9rem 1rem;
            margin:.8rem 0 1rem;
        }

        .av-thanks{
            text-align:center;
            padding:2rem 1.3rem;
            border:1px solid var(--line);
            border-radius:24px;
            background:rgba(255,255,255,.52);
            margin-top:1rem;
        }

        .av-thanks-title{
            font-family:"Cormorant Garamond","Baskerville","Times New Roman",serif !important;
            font-size:2.4rem !important;
            font-weight:500 !important;
            color:var(--accent);
            margin-bottom:.25rem;
        }

        .av-privacy{
            text-align:center;
            font-size:.76rem;
            color:var(--muted);
            line-height:1.55;
            margin-top:1.2rem;
        }

        @media(max-width:640px){
            .block-container{padding:1rem .9rem 3rem;}
            .av-names{
                font-size:clamp(2.65rem,12.7vw,4.35rem) !important;
                line-height:.95 !important;
            }
            .av-amp{
                display:block;
                padding:0;
                margin:.03em 0;
                font-size:.50em !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def get_dropbox_client():
    if all(k in st.secrets for k in ("DROPBOX_APP_KEY", "DROPBOX_APP_SECRET", "DROPBOX_REFRESH_TOKEN")):
        return dropbox.Dropbox(
            app_key=st.secrets["DROPBOX_APP_KEY"],
            app_secret=st.secrets["DROPBOX_APP_SECRET"],
            oauth2_refresh_token=st.secrets["DROPBOX_REFRESH_TOKEN"],
            timeout=900,
        )

    if "DROPBOX_ACCESS_TOKEN" in st.secrets:
        return dropbox.Dropbox(
            oauth2_access_token=st.secrets["DROPBOX_ACCESS_TOKEN"],
            timeout=900,
        )

    raise RuntimeError("Dropbox credentials are missing.")

def safe_filename(name):
    name = PurePosixPath(name).name
    name = re.sub(r"[\x00-\x1f\x7f]+", "", name)
    name = re.sub(r'[<>:"/\\\\|?*]+', "_", name)
    return name.strip(" .") or "upload"

def destination_path(original_name):
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    short_id = uuid.uuid4().hex[:6]
    return f"{DROPBOX_FOLDER.rstrip('/')}/{stamp}_{short_id}_{safe_filename(original_name)}"

def upload_to_dropbox(dbx, uploaded_file, path):
    uploaded_file.seek(0, 2)
    size = uploaded_file.tell()
    uploaded_file.seek(0)

    if size <= SIMPLE_UPLOAD_LIMIT:
        dbx.files_upload(
            uploaded_file.read(),
            path,
            mode=WriteMode.add,
            autorename=True,
            mute=True,
        )
        return

    first_chunk = uploaded_file.read(CHUNK_SIZE)
    start_result = dbx.files_upload_session_start(first_chunk)

    cursor = UploadSessionCursor(
        session_id=start_result.session_id,
        offset=len(first_chunk),
    )

    commit = CommitInfo(
        path=path,
        mode=WriteMode.add,
        autorename=True,
        mute=True,
    )

    while cursor.offset < size:
        remaining = size - cursor.offset
        chunk = uploaded_file.read(min(CHUNK_SIZE, remaining))

        if not chunk:
            raise IOError("Upload ended unexpectedly before Dropbox received the full file.")

        next_offset = cursor.offset + len(chunk)
        is_last_chunk = next_offset == size

        if is_last_chunk:
            dbx.files_upload_session_finish(chunk, cursor, commit)
            cursor.offset = next_offset
        else:
            dbx.files_upload_session_append_v2(chunk, cursor)
            cursor.offset = next_offset

def main():
    inject_css()

    st.markdown(
        """
        <div class="av-hero">
            <div class="av-eyebrow">18 · 09 · 2026</div>
            <div class="av-names">Αλέξης <span class="av-amp">&amp;</span> Βασιλίνα</div>
            <div class="av-subtitle">Μοιράσου τις στιγμές μαζί μας</div>
            <div class="av-date">Παρασκευή · Πάτρα</div>
        </div>
        <div class="av-rule"></div>
        <div class="av-copy">
            Ανέβασε τις φωτογραφίες και τα βίντεο που τράβηξες σήμερα.<br>
            Μπορείς να επιλέξεις πολλά αρχεία μαζί.
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploads = st.file_uploader(
        "Photos & videos",
        type=["jpg","jpeg","png","heic","webp","mp4","mov","m4v","avi","webm"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploads:
        total_mb = sum(getattr(f, "size", 0) for f in uploads) / (1024 * 1024)
        st.markdown(
            f'<div class="av-summary"><strong>{len(uploads)} αρχείο(α) επιλέχθηκαν</strong><br>Συνολικό μέγεθος: {total_mb:,.1f} MB</div>',
            unsafe_allow_html=True,
        )

        large = [f for f in uploads if getattr(f, "size", 0)/(1024*1024) >= LARGE_FILE_WARNING_MB]
        if large:
            st.info("Έχεις επιλέξει μεγάλο βίντεο — κράτησε τη σελίδα ανοιχτή μέχρι να ολοκληρωθεί το upload.")

    if st.button("Μοίρασε τις στιγμές", disabled=not uploads, use_container_width=True):
        try:
            dbx = get_dropbox_client()
            progress = st.progress(0, text="Ετοιμάζουμε τα αρχεία…")
            errors = []

            for i, f in enumerate(uploads, start=1):
                size_mb = getattr(f, "size", 0)/(1024*1024)

                progress.progress(
                    (i-1)/len(uploads),
                    text=f"Ανέβασμα {i} από {len(uploads)} · {f.name} · {size_mb:,.1f} MB"
                )

                try:
                    upload_to_dropbox(dbx, f, destination_path(f.name))
                except Exception as exc:
                    errors.append((f.name, str(exc)))

                progress.progress(i/len(uploads), text=f"Ολοκληρώθηκε {i} από {len(uploads)}")

            successful = len(uploads) - len(errors)

            if errors:
                st.warning(f"{successful} αρχείο(α) ανέβηκαν, αλλά {len(errors)} απέτυχαν.")
                with st.expander("Προβολή σφαλμάτων"):
                    for filename, error in errors:
                        st.write(f"**{filename}**")
                        st.code(error)
            else:
                st.balloons()
                st.markdown(
                    """
                    <div class="av-thanks">
                        <div class="av-thanks-title">Ευχαριστούμε 🧡</div>
                        <div>Οι στιγμές σου μόλις έγιναν μέρος της δικής μας βραδιάς.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.success("Όλα τα αρχεία ανέβηκαν με επιτυχία.")

        except Exception as exc:
            st.error("Δεν μπορέσαμε να συνδεθούμε με το album αυτή τη στιγμή. Δοκίμασε ξανά.")
            with st.expander("Τεχνικές λεπτομέρειες"):
                st.code(str(exc))

    st.markdown(
        """
        <div class="av-large-title">Έχεις πολύ μεγάλο βίντεο;</div>
        <div class="av-large-copy">
            Για βίντεο πάνω από 1 GB, χρησιμοποίησε την επιλογή παρακάτω.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.link_button(
        "Ανέβασε μεγάλο βίντεο",
        LARGE_VIDEO_URL,
        use_container_width=True,
    )

    st.markdown(
        """
        <div class="av-privacy">
            Τα αρχεία ανεβαίνουν στον ιδιωτικό φάκελο του γάμου.<br>
            Οι υπόλοιποι καλεσμένοι δεν μπορούν να δουν τι ανεβάζεις.
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
