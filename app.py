import streamlit as st
from fpdf import FPDF
import base64
from PIL import Image
import os

# ----------------------------
# PDF Class with Photo Support
# ----------------------------
class CVPDF(FPDF):
    def __init__(self, title, image_path=None):
        super().__init__()
        self.title = title
        self.image_path = image_path

    def header(self):
        # Page border
        self.set_line_width(0.5)
        self.rect(10, 10, 190, 277)

        # Title
        self.set_font("Arial", "B", 18)
        self.cell(0, 15, self.title, ln=True, align="C")
        self.ln(5)

        # Image (top-right)
        if self.image_path:
            self.image(self.image_path, x=160, y=20, w=30, h=35)

    def add_cv_section(self, fields):
        self.set_xy(20, 60)
        self.set_font("Arial", "", 12)
        line_height = 9
        label_width = 65
        value_width = 100

        for label, value in fields.items():
            self.set_x(20)
            self.set_font("Arial", "B", 11)
            self.cell(label_width, line_height, f"{label}:", border=0)
            self.set_font("Arial", "", 11)
            self.multi_cell(value_width, line_height, str(value))
            self.ln(1)

# ----------------------------
# Generate the CV PDF
# ----------------------------
def create_cv_pdf(data, title, image):
    image_path = None
    if image:
        image_path = "temp_photo.jpg"
        img = Image.open(image)
        img.save(image_path)

    pdf = CVPDF(title, image_path)
    pdf.add_page()

    fields = {
        "Full Name": data["name"],
        "Selected Position": data["position"],
        "Height (cm)": data["height"],
        "Weight (kg)": data["weight"],
        "Date of Birth": data["dob"],
        "Email": data["email"],
        "Address": data["address"],
        "Mobile No": data["mobile"],
        "WhatsApp No": data["whatsapp"],
        "Workplace": data["workplace"],
        "Workplace Address": data["work_address"],
        "International Tournaments (last 5 years)": data["tournaments"]
    }

    pdf.add_cv_section(fields)

    file_path = "generated_cv.pdf"
    pdf.output(file_path)

    # Clean temp photo
    if image_path and os.path.exists(image_path):
        os.remove(image_path)

    return file_path

# ----------------------------
# Streamlit App
# ----------------------------
st.title("🏐 Volleyball Player CV Generator")

with st.form("cv_form"):
    heading = st.text_input("PDF Title", value="Volleyball Player Profile")

    name = st.text_input("Name (e.g., H.N. Anupama Perera) *")
    position = st.selectbox("Selected Position *", ["High Attacker", "Quick Attacker", "Setter", "Libero"])
    height = st.text_input("Height (cm) *")
    weight = st.text_input("Weight (kg) *")
    dob = st.date_input("Date of Birth *")
    email = st.text_input("Email *")
    address = st.text_area("Address (Personal)")
    mobile = st.text_input("Mobile No *")
    whatsapp = st.text_input("WhatsApp Mobile No *")
    workplace = st.text_input('Workplace (if not working, type "N/A") *')
    work_address = st.text_area("Workplace Address *")
    tournaments = st.text_area("Participated International Tournaments (last 05 Years) * (If none, type 'N/A')")
    photo = st.file_uploader("Photograph (White Background) *", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Generate CV")

    if submitted:
        data = {
            "name": name,
            "position": position,
            "height": height,
            "weight": weight,
            "dob": str(dob),
            "email": email,
            "address": address,
            "mobile": mobile,
            "whatsapp": whatsapp,
            "workplace": workplace,
            "work_address": work_address,
            "tournaments": tournaments
        }

        file_path = create_cv_pdf(data, heading, photo)
        st.success("✅ CV PDF created successfully!")
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_path}">📄 Download CV PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
