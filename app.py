import streamlit as st

st.set_page_config(
    page_title="Αλέξης & Βασιλίνα",
    page_icon="🧡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Dropbox File Request
UPLOAD_URL = "https://www.dropbox.com/request/ws9oyzx9oaf25ror8ub9"


st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=GFS+Didot&family=Noto+Sans:wght@400;500;600&family=Noto+Serif:ital,wght@0,400;1,400&display=swap');

.stApp {
    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(218,91,43,.045),
            transparent 34rem
        ),
        #fffaf4;
    color: #29231f;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu,
footer {
    visibility: hidden;
}

.block-container {
    max-width: 780px;
    padding-top: 2.6rem;
    padding-bottom: 4rem;
}

html,
body,
[class*="css"] {
    font-family: "Noto Sans", Arial, sans-serif;
}


/* ΗΜΕΡΟΜΗΝΙΑ */

.av-date {
    width: max-content;
    margin: 0 auto 1.25rem auto;
    padding: .55rem 1.25rem;

    border: 1px solid rgba(211,91,43,.30);
    border-radius: 999px;

    font-size: .72rem;
    letter-spacing: .35em;

    color: #c65c35;
}


/* ΟΝΟΜΑΤΑ */

.av-names {
    text-align: center;

    font-family:
        "GFS Didot",
        "Noto Serif",
        "Times New Roman",
        serif;

    font-size: clamp(2.15rem, 5.8vw, 3.35rem);
    line-height: 1;
    letter-spacing: -.015em;

    color: #29231f;

    white-space: nowrap;
}

.av-amp {
    display: inline-block;

    font-size: .68em;

    padding: 0 .14em;

    color: #d65e31;
}


/* PARTY LINE */

.av-partyline {
    text-align: center;

    margin-top: .7rem;

    font-family:
        "Noto Serif",
        "Times New Roman",
        serif;

    font-style: italic;
    font-size: 1.05rem;

    color: #d45e31;
}


/* ΓΡΑΜΜΗ */

.av-rule {
    width: 74%;
    height: 1px;

    background: rgba(211,91,43,.20);

    margin: 2rem auto 1.8rem auto;
}


/* ΚΕΙΜΕΝΟ */

.av-copy {
    text-align: center;

    font-size: .86rem;

    color: #a5654e;

    margin-bottom: 1.3rem;
}


/* ΚΥΡΙΟ ΚΟΥΜΠΙ UPLOAD */

a.av-upload-button {
    display: block;

    width: 100%;
    box-sizing: border-box;

    text-align: center;
    text-decoration: none;

    padding: 1.2rem 1rem;

    border: 1px solid #d65e31;
    border-radius: 999px;

    color: #d65e31 !important;

    background: rgba(255,255,255,.38);

    font-family:
        "Noto Sans",
        Arial,
        sans-serif;

    font-size: .76rem;
    font-weight: 500;

    letter-spacing: .14em;

    box-shadow:
        0 10px 30px rgba(95,55,35,.05);

    transition: all .2s ease;
}

a.av-upload-button:hover {
    background: rgba(214,94,49,.05);

    box-shadow:
        0 12px 32px rgba(95,55,35,.08);
}


/* ΚΕΙΜΕΝΟ ΚΑΤΩ ΑΠΟ ΚΟΥΜΠΙ */

.av-upload-note {
    text-align: center;

    margin-top: .9rem;

    font-size: .73rem;
    line-height: 1.6;

    color: #a97864;
}


/* ΜΕΓΑΛΟ ΒΙΝΤΕΟ */

.av-large {
    margin-top: 3rem;

    text-align: center;
}

.av-large-title {
    font-family:
        "GFS Didot",
        "Noto Serif",
        "Times New Roman",
        serif;

    font-style: italic;

    font-size: 1.55rem;

    color: #29231f;

    margin-bottom: .45rem;
}

.av-large-copy {
    font-size: .72rem;

    color: #b36d50;

    margin-bottom: .9rem;
}

a.av-video-button {
    display: block;

    width: 100%;
    box-sizing: border-box;

    text-align: center;
    text-decoration: none;

    padding: 1.15rem 1rem;

    border: 1px solid rgba(211,91,43,.40);
    border-radius: 999px;

    color: #d65e31 !important;

    font-family:
        "Noto Sans",
        Arial,
        sans-serif;

    font-size: .74rem;

    letter-spacing: .18em;
}

a.av-video-button:hover {
    background: rgba(214,94,49,.04);
}


/* FOOTER */

.av-footer {
    margin-top: 3.4rem;

    text-align: center;

    font-family:
        "Noto Serif",
        "Times New Roman",
        serif;

    font-style: italic;

    font-size: .82rem;

    color: #b4816c;
}


/* ΚΙΝΗΤΟ */

@media (max-width: 600px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1.8rem;
    }

    .av-date {
        font-size: .65rem;

        padding: .48rem .9rem;
    }

    .av-names {
        font-size: clamp(
            1.9rem,
            8.7vw,
            2.55rem
        );

        line-height: 1.05;

        white-space: nowrap;
    }

    .av-amp {
        padding: 0 .08em;

        font-size: .60em;
    }

    .av-partyline {
        font-size: .98rem;
    }

    .av-copy {
        padding-left: .3rem;
        padding-right: .3rem;

        line-height: 1.55;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


st.markdown(
    """
<div class="av-date">
    ✦ 18 · 09 · 2026 ✦
</div>

<div class="av-names">
    Αλέξης <span class="av-amp">&amp;</span> Βασιλίνα
</div>

<div class="av-partyline">
    ✦ one night, lots of memories ✦
</div>

<div class="av-rule"></div>

<div class="av-copy">
    Ανέβασε τις φωτογραφίες και τα βίντεο
    που τράβηξες σήμερα.
</div>
""",
    unsafe_allow_html=True,
)


st.markdown(
    f"""
<a
    class="av-upload-button"
    href="{UPLOAD_URL}"
    target="_blank"
    rel="noopener noreferrer"
>
    ΑΝΕΒΑΣΕ ΦΩΤΟΓΡΑΦΙΕΣ &amp; ΒΙΝΤΕΟ
</a>

<div class="av-upload-note">
    Μπορείς να επιλέξεις πολλές φωτογραφίες
    και βίντεο μαζί.
</div>
""",
    unsafe_allow_html=True,
)


st.markdown(
    f"""
<div class="av-large">

    <div class="av-large-title">
        Έχεις πολύ μεγάλο βίντεο;
    </div>

    <div class="av-large-copy">
        Μπορείς να το ανεβάσεις απευθείας
        στο Dropbox.
    </div>

    <a
        class="av-video-button"
        href="{UPLOAD_URL}"
        target="_blank"
        rel="noopener noreferrer"
    >
        ΑΝΕΒΑΣΕ ΤΟ ΒΙΝΤΕΟ
    </a>

</div>

<div class="av-footer">
    οι στιγμές της βραδιάς, μέσα από τα μάτια σας ♡
</div>
""",
    unsafe_allow_html=True,
)
