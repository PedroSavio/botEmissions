import csv
import json
import time
import zipfile

import pandas as pd

from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from BDFacade import DBFacade


def baixarDataSet():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(
        "https://www.kaggle.com/datasets/thedevastator/global-fossil-co2-emissions-by-country-2002-2022?resource=download")

    time.sleep(10)

    btnDownload = driver.find_element(By.XPATH, "//a[@data-disable-rapidash='true']")
    btnDownload.click()
    wait = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Sign in with Email']")))
    time.sleep(5)

    btnLoginEmail = (driver.find_element(By.XPATH, "//*[text()='Sign in with Email']"))
    btnLoginEmail.click()

    wait = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter your "
                                                                                 "email address or username']")))
    time.sleep(3)

    inputEmail = driver.find_element(By.XPATH, "//input[@placeholder='Enter your email address or username']")
    inputEmail.send_keys("saviokbca@gmail.com")

    inputSenha = driver.find_element(By.XPATH, "//input[@placeholder='Enter password']")
    inputSenha.send_keys("flamengo2012")

    btnLogin = driver.find_element(By.XPATH, "//button[@type='submit']")
    btnLogin.click()

    time.sleep(5)

    btnDownload = driver.find_element(By.XPATH, "//*[contains(@href, "
                                                "'/datasets/thedevastator/global-fossil-co2-emissions-by-country-2002"
                                                "-2022/download')]")
    btnDownload.click()

    time.sleep(10)
    extractZip()


def extractZip():
    # Se atentar ao caminho do arquivo mudar caso o arquivo seja baixado em outro local
    with zipfile.ZipFile('C:/Users/savio/Downloads/archive.zip', 'r') as zip_ref:
        zip_ref.extract('GCB2022v27_MtCO2_flat.csv')

    print("Arquivo extraído com sucesso!")
    leituraArquivo()


def leituraArquivo():
    # Se atentar ao caminho do arquivo mudar caso o arquivo seja baixado em outro local
    arquivoCsv = pd.read_csv('GCB2022v27_MtCO2_flat.csv', sep=',')
    json_object = json.dumps(arquivoCsv.to_dict('records'), indent=4)
    print("Qtd de registros: ", len(arquivoCsv))

    db = DBFacade()
    qtdRegistrosBD = db.quantidadeRegistro()

    if len(arquivoCsv) > qtdRegistrosBD:
        db.atualizarNumeros(json_object)

    with open("sample.json", "w") as outfile:
        outfile.write(json_object)


def main():
    print("Iniciando o processo de extração de dados...")
    baixarDataSet()


main()
