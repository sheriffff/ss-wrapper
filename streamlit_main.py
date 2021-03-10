import streamlit as st
from selenium import webdriver
from PIL import Image

from crawler import SSocialCrawler
from streamlit_utils import is_dni_correct, is_telf_correct, is_mail_correct
from config import options_ids_interface_map, options_ids_interface_order, run_selenium



button_pushed = False
# intro
# image_ss_logo = Image.open("./media/ss_logo.jpg")
# image_sheriff = Image.open("./media/sheriff_badge.jpg")
image_ss_sheriff = Image.open("media/ss_sheriff_logo.jpg")

col1, col2 = st.beta_columns([2, 1])
with col1:
    st.write("Hola. Si estás aquí, es por que quieres sacar una cita para la Seguridad Social. "
             "Te ayudará el Sheriff del condado madrileño.")
with col2:
    st.image(image_ss_sheriff, width=200)

form_fields = ["name", "NIF", "telf", "mail", "notify"]
# fill fields
user_data = {k: None for k in form_fields}
error_placeholders = dict()

col1, col2 = st.beta_columns([5, 3])
with col1:
    name = st.text_input("Nombre")
    if name:
        st.write("Hola,", name.split()[0])
        user_data["name"] = name
    else:
        error_placeholders["name"] = st.empty()

with col2:
    dni = st.text_input("DNI")
    if dni:
        if is_dni_correct(dni):
            # poner letra mayúscula
            dni = dni[:-1] + dni[-1].upper()
            user_data["NIF"] = dni
        else:
            st.error("Introduce 8 números y una letra seguidos, sin espacios ni guiones")
    else:
        error_placeholders["NIF"] = st.empty()

col1, col2 = st.beta_columns([2, 5])
with col1:
    telf = st.text_input("Teléfono")
    if telf:
        if is_telf_correct(telf):
            user_data["telf"] = telf
        else:
            st.error("Introduce 9 números, sin espacios")
    else:
        error_placeholders["telf"] = st.empty()

with col2:
    mail = st.text_input("E-mail")
    if mail:
        if is_mail_correct(mail):
            user_data["mail"] = mail
        else:
            st.error("E-mail incorrecto")
    else:
        error_placeholders["mail"] = st.empty()

# appointment type
appointment_type_box_value = st.selectbox("¿Cuál es el motivo de tu cita?", options_ids_interface_order)
appointment_type = options_ids_interface_map[appointment_type_box_value]

# TODO max min date calendar
# TODO deseas recibir un mail o un wasap?
st.write("¿Dónde quieres recibir la confirmación de tu cita?")

user_data["notify"] = ""
if st.checkbox("Whatsapp"):
    user_data["notify"] += "w"
if st.checkbox("E-mail"):
    user_data["notify"] += "m"
error_placeholders["notify"] = st.empty()

# button
if st.button("Consígue mi cita"):
    some_error = False
    for key in form_fields:
        if not user_data.get(key):
            if error_placeholders.get(key):
                error_placeholders[key].error("Campo obligatorio")
            some_error = True

    if not some_error:
        st.balloons()
        mensaje_common = "La información que has proporcionado parece correcta. Una vez confirmada tu cita, "
        mensaje_wasap = f"recibirás un Whatsapp en {telf}"
        mensaje_mail = f"recibirás un e-mail en {mail}"

        mensaje_total = mensaje_common
        if user_data["notify"] == "wm":
            st.success(mensaje_common + mensaje_wasap + " y " + mensaje_mail)
        elif user_data["notify"] == "w":
            st.success(mensaje_common + mensaje_wasap)
        elif user_data["notify"] == "m":
            st.success(mensaje_common + mensaje_mail)

        if run_selenium:
            driver = webdriver.Chrome("./chromedriver")
            ss = SSocialCrawler(driver, user_data)
            ss.run_until_success()
