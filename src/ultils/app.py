import streamlit as st
from services.blob_service import upload_blob
from services.credit_card_service import analyze_credit_card

def configure_interface():
    st.title("Upload files: DIO Challenge - Azure - Fake Docs")
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        fileName = uploaded_file.name
        # Enviar para o blob storage
        blob_url = upload_blob(uploaded_file, fileName)
        if blob_url:
            st.write(f"Arquivo {fileName} enviado com sucesso para o Azure Blob Storage")
            credit_card_info = analyze_credit_card(blob_url) #Call credit card info detection function
            show_image_and_validation(blob_url, credit_card_info)
        else:
            st.write(f"Erro ao enviar o arquivo {fileName} para o Azure Blob Storage")
            
def show_image_and_validation(blob_url, credit_card_info):
    st.image(blob_url, caption="Image sent", use_column_width=True)
    st.write("Validation result:")
    if credit_card_info and credit_card_info["card_name"]:
        st.markdown(f"<h1 style='color: green;'>Valid Card</h1>", unsafe_allow_html=True)
        st.write(f"Titular name: {credit_card_info['card_name']}")
        st.write(f"Bank: {credit_card_info['bank_name']}")
        st.write(f"Credit Card: {credit_card_info['expiry_date']}")
    else:
        st.markdown(f"<h1 style='color: red;'>Invalid Card</h1>", unsafe_allow_html=True)
        st.write("This is a invalid credit card")


if __name__ == "__main__":
    configure_interface()