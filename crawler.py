import time
import random

from googletrans import Translator
from number2words import Number2Words


class SSocialCrawler:
    url = "https://w6.seg-social.es/ProsaInternetAnonimo/OnlineAccess?ARQ.SPM.ACTION=LOGIN&ARQ.SPM.APPTYPE=SERVICE&" \
          "ARQ.IDAPP=XV106001"

    def __init__(self, driver, user_data):
        self.driver = driver
        self.user_data = user_data

    def run_until_success(self):
        while True:
            self.run_process()
            # if self.is_step_three() and self.has_desired_dates():
            if self.is_step_three():
                print('SUCCESS')
                return
            else:
                print('NO SUCCESS')
                time.sleep(5)

    def run_process(self):
        self.access_form()
        self.fill_fields()
        self.solve_captcha()
        self.choose_option()

    def access_form(self):
        self.driver.get(self.url)
        seg_social_square = self.driver.find_element_by_css_selector("div div div input")
        seg_social_square.click()

    def fill_fields(self):
        self.driver.find_element_by_name("nombreApellidos").send_keys(self.user_data.get("name"))

        # TODO NIF/NIE/PASAPORTE
        self.driver.find_element_by_name("tipo").send_keys("N")
        self.driver.find_element_by_name("numeroDocumento").send_keys(self.user_data.get("NIF"))

        self.driver.find_element_by_name("telefono").send_keys(self.user_data.get("telf"))
        self.driver.find_element_by_name("eMail").send_keys(self.user_data.get("mail"))

        # TODO CODIGO POSTAL/PROVINCIA
        cp = self.user_data.get("codigo_postal")
        if cp and len(cp) == 5:
            self.driver.find_element_by_name("codigoPostal").send_keys(cp)
        else:
            self.driver.find_element_by_id("radioProvincia").click()
            self.driver.find_element_by_name("provincia").send_keys("m")

    def solve_captcha(self):
        while not self.is_paso_2():
            # print("probando...")
            self.try_solution()

    def choose_option(self, option=None):
        # TODO more options
        self.driver.find_element_by_id("335").click()
        self.driver.find_element_by_name("SPM.ACC.CONTINUAR_TRAS_SELECCIONAR_SERVICIO").click()

    def is_step_three(self):
        campos = self.driver.find_elements_by_css_selector(
            "#ARQcapaPrincipal div.margenSup4.rellenoSup4.rellenoInf4.bordeAzulOscuro.fondoOscuro.alineacionCentrada "
            "span strong"
        )

        if campos and campos[0].text == "Paso 3 de 4. Selección de Cita.":
            return True
        else:
            return False

    def has_desired_dates(self):
        min_date = self.user_data.get("min_date")
        max_date = self.user_data.get("max_date")

        if min_date or max_date:
            # html tags which could be dates
            elements = self.driver.find_elements_by_css_selector(
                "#ARQcapaPrincipal fieldset div:nth-child(3) table tbody tr:nth-child(1) td:nth-child(3) "
                "div:nth-child(1) span:nth-child(2)"
            )

            # html tags with actual dates + date extraction
            dates = [elem.text for elem in elements if elem.text.count("/") == 2]
            print(dates)
            # is there any desired date?
            for d in dates:
                # TODO datetime comparison
                if min_date <= d <= max_date:
                    return True
            else:
                return False

        else:
            # all dates are OK
            return True

    def try_solution(self):
        word = self.driver.find_element_by_class_name("p2").text[112:]
        print(word)
        words = self.driver.find_element_by_css_selector("p.p0").text.split(": ")[:-1]
        time.sleep(1)
        print(words)

        number = is_number_expression(word)

        if number:
            solution = get_spanish_number_written(number)
        else:
            solution = random.choice(words)

        print(solution)
        self.driver.find_element_by_name("ARQ.CAPTCHA").send_keys(solution)
        self.driver.find_element_by_name("SPM.ACC.SIGUIENTE").click()

    def is_paso_2(self):
        try:
            self.driver.find_element_by_class_name("p2")
            return False
        except:
            return True


def get_spanish_number_written(number):
    # Turns 11 to "Once"
    # print(number)
    number_word = Number2Words(number).convert()[:-5]
    # print(number_word)
    translator = Translator()
    number_text = translator.translate(number_word, src='en', dest='es').text

    if len(number_text.split()) == 2:
        # print("dos palabras...")
        number_text = number_text.split()[1]

    # print(number_text)

    return number_text


def is_number_expression(word):
    word = word.replace("x", "*")
    try:
        number = eval(word)
    except:
        return False
    else:
        return number
