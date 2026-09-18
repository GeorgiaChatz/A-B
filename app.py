import streamlit as st

st.set_page_config(
    page_title="Αλέξης & Βασιλίνα",
    page_icon="🧡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

UPLOAD_URL = "https://www.dropbox.com/request/ws9oyzx9oaf25ror8ub9"

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=GFS+Didot&family=Noto+Sans:wght@400;500;600&family=Noto+Serif:ital,wght@0,400;1,400&display=swap');

.stApp {
    background: #fffaf4;
    color: #29231f;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 780px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

html, body, [class*="css"] {
    font-family: "Noto Sans", Arial, sans-serif;
}

.av-date {
    width: max-content;
    margin: 0 auto 1.25rem auto;
    padding: .55rem 1.25rem;
    border: 1px solid rgba(211,91,43,.30);
    border-radius: 999px;
    font-size: .72rem;
    letter-spacing: .30em;
    color: #c65c35;
}

.av-names {
    text-align: center;
    font-family: "GFS Didot", "Noto Serif", serif;
    font-size: clamp(2.15rem,5.8vw,3.35rem);
    line-height: 1;
    color: #29231f;
    white-space: nowrap;
}

.av-amp {
    font-size: .68em;
    color: #d65e31;
    padding: 0 .12em;
}

.av-partyline {
    text-align: center;
    margin-top: .8rem;
    font-family: "Noto Serif", serif;
    font-style: italic;
    font-size: 1.05rem;
    color: #d45e31;
}

.av-rule {
    width: 74%;
    height: 1px;
    background: rgba(211,91,43,.20);
    margin: 2rem auto 1.8rem auto;
}

.av-copy {
    text-align: center;
    font-size: .86rem;
    line-height: 1.6;
    color: #a5654e;
    margin-bottom: 1.2rem;
}

.av-note {
    text-align: center;
    font-size: .74rem;
    line-height: 1.6;
    color: #a97864;
    margin-top: .8rem;
}

.av-large {
    text-align: center;
    margin-top: 3rem;
}

.av-large-title {
    font-family: "GFS Didot", "Noto Serif", serif;
    font-style: italic;
    font-size: 1.55rem;
    color: #29231f;
}

.av-large-copy {
    font-size: .74rem;
    color: #b36d50;
    margin-top: .4rem;
    margin-bottom: 1rem;
}

.av-footer {
    text-align: center;
    margin-top: 3.5rem;
    font-family: "Noto Serif", serif;
    font-style: italic;
    font-size: .82rem;
    color: #b4816c;
}

/* Streamlit link buttons */
div[data-testid="stLinkButton"] a {
    width: 100%;
    min-height: 58px;
    border-radius: 999px;
    border: 1px solid #d65e31;
    background: transparent;
    color: #d65e31;
    font-family: "Noto Sans", Arial, sans-serif;
    font-size: .76rem;
    letter-spacing: .10em;
}

div[data-testid="stLinkButton"] a:hover {
    border-color: #d65e31;
    color: #d65e31;
    background: rgba(214,94,49,.05);
}

@media (max-width:600px) {
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
        font-size: clamp(1.9rem,8.7vw,2.55rem);
        white-space: nowrap;
    }

    .av-amp {
        font-size: .60em;
    }

    .av-partyline {
        font-size: .98rem;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="av-date">✦ 18 · 09 · 2026 ✦</div>
<div class="av-names">Αλέξης <span class="av-amp">&amp;</span> Βασιλίνα</div>
<div class="av-partyline">✦ one night, lots of memories ✦</div>
<div class="av-rule"></div>
<div class="av-copy">Ανέβασε τις φωτογραφίες και τα βίντεο που τράβηξες σήμερα.</div>
""",
    unsafe_allow_html=True,
)

st.link_button(
    "ΑΝΕΒΑΣΕ ΦΩΤΟΓΡΑΦΙΕΣ & ΒΙΝΤΕΟ",
    UPLOAD_URL,
    use_container_width=True,
)

st.markdown(
    """
<div class="av-note">
Μπορείς να επιλέξεις πολλές φωτογραφίες και βίντεο μαζί.
</div>

<div class="av-large">
<div class="av-large-title">Έχεις πολύ μεγάλο βίντεο;</div>
<div class="av-large-copy">Ανέβασέ το απευθείας στο Dropbox.</div>
</div>
""",
    unsafe_allow_html=True,
)

st.link_button(
    "ΑΝΕΒΑΣΕ ΤΟ ΒΙΝΤΕΟ",
    UPLOAD_URL,
    use_container_width=True,
)

st.markdown(
    """
<div class="av-footer">
οι στιγμές της βραδιάς, μέσα από τα μάτια σας ♡
</div>
""",
    unsafe_allow_html=True,
)
