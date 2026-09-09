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
    page_title="Αλέξης & Βασιλίνα",
    page_icon="🧡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=GFS+Didot&family=Noto+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Noto+Serif:ital,wght@0,400;0,500;1,400&display=swap');

        :root{
            --paper:#fff9f2;
            --paper2:#fffdf9;
            --ink:#2b2521;
            --muted:#9a7967;
            --accent:#c86d3f;
            --accent2:#f0c3a8;
            --line:rgba(43,37,33,.14);
        }

        html, body, [class*="css"]{
            font-family:"Noto Sans", Arial, sans-serif;
        }

        .stApp{
            background:
              radial-gradient(circle at 9% 9%, rgba(240,195,168,.20), transparent 17rem),
              radial-gradient(circle at 90% 88%, rgba(200,109,63,.11), transparent 24rem),
              linear-gradient(180deg,var(--paper2),var(--paper));
            color:var(--ink);
        }

        header[data-testid="stHeader"]{background:transparent;}
        #MainMenu, footer{visibility:hidden;}

        .block-container{
            max-width:760px;
            padding-top:1.3rem;
            padding-bottom:3.2rem;
        }

        .av-hero{
            text-align:center;
            padding:1.0rem .8rem .4rem;
        }

        .av-date-wrap{
            display:flex;
            justify-content:center;
            align-items:center;
            margin-bottom:1.15rem;
        }

        .av-date{
            display:inline-flex;
            align-items:center;
            justify-content:center;
            gap:.55rem;
            font-family:"Noto Sans",Arial,sans-serif !important;
            font-size:.70rem !important;
            letter-spacing:.30em !important;
            color:var(--accent) !important;
            border:1px solid rgba(200,109,63,.30);
            border-radius:999px;
            padding:.52rem .95rem .52rem 1.15rem;
            background:rgba(255,255,255,.55);
            white-space:nowrap;
        }

        .av-date::before,
        .av-date::after{
            content:"✦";
            font-size:.62rem;
            letter-spacing:0;
            color:var(--accent);
        }

        .av-names{
            font-family:"GFS Didot","Noto Serif","Times New Roman",serif !important;
            font-size:clamp(2.15rem,5.8vw,3.35rem) !important;
            line-height:.98 !important;
            font-weight:500 !important;
            letter-spacing:-.015em !important;
            text-align:center !important;
            color:var(--ink) !important;
            margin:0 auto !important;
        }

        .av-amp{
            display:inline-block;
            font-style:italic;
            color:var(--accent);
            font-size:.60em;
            padding:0 .08em;
            transform:translateY(-.02em) rotate(-4deg);
        }

        .av-partyline{
            text-align:center;
            margin-top:.72rem;
            color:var(--accent);
            font-family:"Noto Serif","Times New Roman",serif !important;
            font-style:italic;
            font-size:1.15rem;
            letter-spacing:.03em;
        }

        .av-rule{
            width:68%;
            height:1px;
            background:linear-gradient(90deg,transparent,var(--accent2),transparent);
            margin:1.4rem auto 1.6rem;
        }

        .av-copy{
            text-align:center;
            color:var(--muted);
            font-size:.95rem;
            line-height:1.6;
            margin-bottom:1.05rem;
        }

        [data-testid="stFileUploader"]{
            background:rgba(255,255,255,.60);
            border:1px solid var(--line);
            border-radius:24px;
            padding:.4rem;
            box-shadow:0 10px 30px rgba(87,57,40,.03);
        }

        [data-testid="stFileUploaderDropzone"]{
            background:rgba(255,255,255,.32);
            border:1px dashed rgba(200,109,63,.34);
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
            font-family:"Noto Sans",Arial,sans-serif !important;
            font-size:.82rem;
            font-weight:600;
            letter-spacing:.13em;
            text-transform:uppercase;
        }

        div.stButton > button:hover{
            background:#b95e34;
            color:#fff;
            border-color:#b95e34;
        }

        div[data-testid="stLinkButton"] > a {
            width:100%;
            min-height:3.4rem;
            border-radius:999px !important;
            border:1px solid var(--accent) !important;
            background:transparent !important;
            color:var(--accent) !important;
            font-family:"Noto Sans",Arial,sans-serif !important;
            font-size:.80rem !important;
            font-weight:600 !important;
            letter-spacing:.10em !important;
            text-transform:uppercase !important;
            display:flex !important;
            align-items:center !important;
            justify-content:center !important;
            text-decoration:none !important;
        }

        div[data-testid="stLinkButton"] > a:hover {
            background:var(--accent) !important;
            color:#fff !important;
        }

        .av-large-title{
            text-align:center;
            font-family:"GFS Didot","Noto Serif","Times New Roman",serif !important;
            font-size:1.55rem !important;
            font-style:italic;
            color:var(--ink);
            margin-top:1.6rem;
            margin-bottom:.18rem;
        }

        .av-large-copy{
            text-align:center;
            color:var(--muted);
            font-size:.80rem;
            line-height:1.55;
            margin-bottom:.7rem;
        }

        .av-summary{
            background:rgba(255,255,255,.52);
            border:1px solid var(--line);
            border-radius:18px;
            padding:.9rem 1rem;
            margin:.8rem 0 1rem;
        }

        .av-thanks{
            text-align:center;
            padding:1.8rem 1.3rem;
            border:1px solid var(--line);
            border-radius:24px;
            background:rgba(255,255,255,.56);
            margin-top:1rem;
        }

        .av-thanks-title{
            font-family:"GFS Didot","Noto Serif","Times New Roman",serif !important;
            font-size:2.25rem !important;
            font-weight:500 !important;
            color:var(--accent);
            margin-bottom:.2rem;
        }

        @media(max-width:640px){
            .block-container{padding:1rem .9rem 2.5rem;}
            .av-names{
                font-size:clamp(1.9rem,8.7vw,2.55rem) !important;
                line-height:.98 !important;
            }
            .av-amp{
                display:inline-block;
                padding:0 .08em;
                margin:0;
                font-size:.60em !important;
            }
            .av-date{
                font-size:.64rem !important;
                letter-spacing:.23em !important;
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
            <div class="av-date-wrap">
                <div class="av-date">18 · 09 · 2026</div>
            </div>
            <div class="av-names">Αλέξης <span class="av-amp">&amp;</span> Βασιλίνα</div>
            <div class="av-partyline">✦ one night, lots of memories ✦</div>
        </div>
        <div class="av-rule"></div>
        <div class="av-copy">
            Ανέβασε τις φωτογραφίες και τα βίντεο που τράβηξες σήμερα.
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

    if st.button("ΠΑΤΑ ΕΔΩ", disabled=not uploads, use_container_width=True):
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
                        <div class="av-thanks-title">Τέλειο! 🧡</div>
                        <div>Τα αρχεία ανέβηκαν.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.success("Όλα ανέβηκαν με επιτυχία.")

        except Exception as exc:
            st.error("Δεν μπορέσαμε να συνδεθούμε με το album αυτή τη στιγμή. Δοκίμασε ξανά.")
            with st.expander("Τεχνικές λεπτομέρειες"):
                st.code(str(exc))

    st.markdown(
        """
        <div class="av-large-title">Έχεις πολύ μεγάλο βίντεο;</div>
        <div class="av-large-copy">
            Για βίντεο πάνω από 1 GB.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.link_button(
        "ΑΝΕΒΑΣΕ ΤΟ ΒΙΝΤΕΟ",
        LARGE_VIDEO_URL,
        use_container_width=True,
    )

if __name__ == "__main__":
    main()
