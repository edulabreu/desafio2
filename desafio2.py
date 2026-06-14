from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


options = Options()

options.add_argument("--disable-notifications")
options.add_argument("--disable-save-password-bubble")

options.add_experimental_option(
    "prefs",
    {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
)


navegador = webdriver.Chrome(options=options)
wait = WebDriverWait(navegador, 10)


navegador.get("https://www.saucedemo.com/")
navegador.maximize_window()


# LOGIN

wait.until(
    EC.visibility_of_element_located(
        (By.ID, "user-name")
    )
).send_keys("standard_user")


navegador.find_element(
    By.ID,
    "password"
).send_keys("secret_sauce")


navegador.find_element(
    By.ID,
    "login-button"
).click()


# valida login

wait.until(
    EC.url_contains("inventory")
)

assert "inventory" in navegador.current_url

print("Login realizado")


# FILTRO PRICE LOW TO HIGH


select = Select(
    wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "product_sort_container")
        )
    )
)


select.select_by_visible_text(
    "Price (low to high)"
)


# valida ordenação

precos = navegador.find_elements(
    By.CLASS_NAME,
    "inventory_item_price"
)

lista_precos = [
    float(p.text.replace("$", ""))
    for p in precos
]

assert lista_precos == sorted(lista_precos)

print("Filtro aplicado")


# ADICIONAR 3 PRODUTOS


botoes = wait.until(
    EC.presence_of_all_elements_located(
        (
            By.XPATH,
            '//button[contains(@id,"add-to-cart")]'
        )
    )
)


for botao in botoes[:3]:
    botao.click()


# valida badge

badge = wait.until(
    EC.visibility_of_element_located(
        (By.CLASS_NAME, "shopping_cart_badge")
    )
)


assert badge.text == "3"

print("3 produtos adicionados ao carrinho")


# CHECKOUT


wait.until(
    EC.element_to_be_clickable(
        (By.CLASS_NAME, "shopping_cart_link")
    )
).click()


wait.until(
    EC.url_contains("cart")
)


wait.until(
    EC.element_to_be_clickable(
        (By.ID, "checkout")
    )
).click()


# dados checkout

wait.until(
    EC.visibility_of_element_located(
        (By.ID, "first-name")
    )
).send_keys("Eduardo")


navegador.find_element(
    By.ID,
    "last-name"
).send_keys("Gonzaga")


navegador.find_element(
    By.ID,
    "postal-code"
).send_keys("30100000")


navegador.find_element(
    By.ID,
    "continue"
).click()


# finaliza compra

wait.until(
    EC.element_to_be_clickable(
        (By.ID, "finish")
    )
).click()


wait.until(
    EC.url_contains("complete")
)


assert "complete" in navegador.current_url

print("Checkout concluído")


# LOGOUT


# abre menu lateral

wait.until(
    EC.element_to_be_clickable(
        (By.ID, "react-burger-menu-btn")
    )
).click()


# espera o menu aparecer

wait.until(
    EC.visibility_of_element_located(
        (By.CLASS_NAME, "bm-menu")
    )
)


# clica logout

logout = wait.until(
    EC.element_to_be_clickable(
        (By.ID, "logout_sidebar_link")
    )
)

navegador.execute_script(
    "arguments[0].click();",
    logout
)


# valida retorno para login

wait.until(
    EC.url_contains("saucedemo.com")
)


# valida tela login

login_btn = wait.until(
    EC.visibility_of_element_located(
        (By.ID, "login-button")
    )
)

assert login_btn.is_displayed()

print("Logout validado com sucesso")

navegador.quit()