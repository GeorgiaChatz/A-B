import streamlit as st
import dropbox

st.set_page_config(page_title="Dropbox Refresh Token Helper", page_icon="🔑")

st.title("Dropbox Refresh Token Helper")
st.write("Use this one-time page to create a Dropbox refresh token for your wedding upload app.")

app_key = st.text_input("Dropbox App Key")
app_secret = st.text_input("Dropbox App Secret", type="password")

if app_key and app_secret:
    auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(
        app_key,
        app_secret,
        token_access_type="offline",
    )

    auth_url = auth_flow.start()

    st.markdown("### Step 1")
    st.write("Open this Dropbox authorization page:")
    st.link_button("AUTHORIZE WITH DROPBOX", auth_url)

    st.markdown("### Step 2")
    st.write("After approving access, Dropbox will show you an authorization code.")
    auth_code = st.text_input("Paste the authorization code here")

    if st.button("CREATE REFRESH TOKEN"):
        try:
            result = auth_flow.finish(auth_code.strip())
            refresh_token = result.refresh_token

            if not refresh_token:
                st.error("Dropbox did not return a refresh token. Make sure offline access is being requested.")
            else:
                st.success("Refresh token created.")
                st.warning("Keep this private. Do not put it in GitHub or send it to anyone.")
                st.code(
                    f'DROPBOX_APP_KEY = "{app_key}"\n'
                    f'DROPBOX_APP_SECRET = "{app_secret}"\n'
                    f'DROPBOX_REFRESH_TOKEN = "{refresh_token}"',
                    language="toml",
                )
        except Exception as exc:
            st.error("Could not create the refresh token.")
            st.code(str(exc))
