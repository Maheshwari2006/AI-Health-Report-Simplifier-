# ==========================================
# AI Health Report Simplifier PRO
# PDF + Image OCR + Translation + Risk Score
# ==========================================

import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
import re
from googletrans import Translator

# SET TESSERACT PATH (CHANGE IF NEEDED)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

translator = Translator()

st.set_page_config(page_title="AI Health Simplifier PRO")

st.title("🏥 AI Health Report Simplifier PRO")

# ------------------------------------------
# Medical dictionary
# ------------------------------------------

medical_dictionary = {
    "hypertension": "high blood pressure",
    "hyperglycemia": "high blood sugar",
    "hypoglycemia": "low blood sugar",
    "myocardial infarction": "heart attack",
    "anemia": "low red blood cells",
    "tachycardia": "fast heart rate",
    "pregnant": "currently carrying a baby",
    "infection": "body infection"
}

# ------------------------------------------
# Risk prediction score
# ------------------------------------------

risk_data = {
    "high blood pressure": 80,
    "high blood sugar": 75,
    "heart attack": 95,
    "low red blood cells": 60,
    "infection": 50,
    "currently carrying a baby": 40
}

# ------------------------------------------
# simplify
# ------------------------------------------

def simplify(text):

    text = text.lower()

    for term, meaning in medical_dictionary.items():
        text = re.sub(term, meaning, text)

    return text


# ------------------------------------------
# risk score
# ------------------------------------------

def calculate_risk(text):

    results = []

    for disease, score in risk_data.items():

        if disease in text:

            results.append((disease, score))

    return results


# ------------------------------------------
# translate
# ------------------------------------------

def translate_text(text, lang):

    if lang == "English":
        return text

    if lang == "Hindi":
        return translator.translate(text, dest="hi").text

    if lang == "Marathi":
        return translator.translate(text, dest="mr").text


# ------------------------------------------
# PDF reader
# ------------------------------------------

def read_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            text += page.extract_text()

    return text


# ------------------------------------------
# image OCR
# ------------------------------------------

def read_image(file):

    image = Image.open(file)

    text = pytesseract.image_to_string(image)

    return text


# ------------------------------------------
# UI
# ------------------------------------------

option = st.radio(
    "Select Input Method",
    ["Manual Text", "Upload PDF", "Upload Image"]
)

report = ""

if option == "Manual Text":

    report = st.text_area("Enter report")


elif option == "Upload PDF":

    file = st.file_uploader("Upload PDF", type="pdf")

    if file:
        report = read_pdf(file)
        st.success("PDF loaded")


elif option == "Upload Image":

    file = st.file_uploader("Upload image", type=["png","jpg","jpeg"])

    if file:
        report = read_image(file)
        st.success("Image processed")


# language
language = st.selectbox(
    "Select Language",
    ["English", "Hindi", "Marathi"]
)


# process
if st.button("Analyze Report"):

    if report == "":
        st.error("No report found")
    else:

        simplified = simplify(report)

        translated = translate_text(simplified, language)

        risks = calculate_risk(simplified)

        st.subheader("📄 Simplified Report")

        st.write(translated)

        st.subheader("⚠ Disease Risk Score")

        if risks:

            for disease, score in risks:

                st.write(f"{disease} : {score}% risk")

                st.progress(score)

        else:
            st.success("No major disease detected")


        st.subheader("🩺 Prevention")

        st.write("""
• Exercise daily  
• Eat healthy food  
• Avoid junk food  
• Regular doctor checkups  
""")

        st.warning("This is AI support tool only")

# ------------------------------------------
# Smart Medical Advice
# ------------------------------------------

advice_data = {

    "high blood pressure": [
        "Reduce salt intake",
        "Exercise at least 30 minutes daily",
        "Avoid stress and get enough sleep",
        "Monitor blood pressure regularly"
    ],

    "high blood sugar": [
        "Reduce sugar and refined carbs",
        "Exercise regularly",
        "Maintain healthy body weight",
        "Check blood glucose levels"
    ],

    "heart attack": [
        "Avoid smoking and alcohol",
        "Eat heart healthy foods",
        "Control cholesterol levels",
        "Consult a cardiologist"
    ],

    "low red blood cells": [
        "Eat iron rich foods (spinach, dates, beetroot)",
        "Increase vitamin B12 intake",
        "Consult doctor for iron supplements"
    ],

    "infection": [
        "Maintain good hygiene",
        "Drink enough water",
        "Get proper rest",
        "Consult doctor if symptoms worsen"
    ],

    "currently carrying a baby": [
        "Take regular prenatal checkups",
        "Eat nutritious food",
        "Take folic acid supplements",
        "Avoid heavy physical work"
    ]
}


def smart_medical_advice(risks):

    advice = []

    for disease, score in risks:

        if disease in advice_data:

            advice.extend(advice_data[disease])

    return list(set(advice))

# ------------------------------------------
# Patient Profile
# ------------------------------------------
st.sidebar.header("👤 Patient Profile")

patient_name = st.sidebar.text_input("Patient Name")

age = st.sidebar.number_input(
    "Age",
    min_value=0,
    max_value=120,
    value=25
)

gender = st.sidebar.selectbox(
    "Gender",
    ["Male", "Female", "Other"]
)

weight = st.sidebar.number_input(
    "Weight (kg)",
    min_value=1.0,
    max_value=200.0,
    value=60.0
)

height = st.sidebar.number_input(
    "Height (cm)",
    min_value=50.0,
    max_value=250.0,
    value=170.0
)

blood_group = st.sidebar.selectbox(
    "Blood Group",
    ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
)
st.subheader("👤 Patient Information")

st.write("Name:", patient_name)
st.write("Age:", age)
st.write("Gender:", gender)
st.write("Blood Group:", blood_group)

