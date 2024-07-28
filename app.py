from faker import Faker 
import streamlit as st
import pandas as pd
from io import BytesIO

fake = Faker("es_AR")


available_fields = {
    "Nombre": fake.name,
    "Dirección": fake.address,
    "Correo Electrónico": fake.email,
    "Teléfono": fake.phone_number,
    "Empresa": fake.company,
    "Fecha": fake.date,
    "Numero Tarjeta Crédito": fake.credit_card_number
}

def generate_fake_data(fields,num_rows):
    data= {field:[func()for _ in range(num_rows)] for field, func in fields.items() }
    return pd.DataFrame(data)

st.title("Generador de datos falsos con Faker")
st.write("Selecciona los campos que quieres generar y la cantidad de datos")

selected_fields= st.multiselect("Selecciona los campos",
                                options=list(available_fields.keys()),
                                default=list(available_fields.keys()))

num_rows= st.number_input("Cantidad de datos a generar",
                          min_value=1,
                          max_value=1000,
                          value=10)


if st.button("Generar datos"):
    selected_funcs= {field: available_fields[field] for field in selected_fields}
    df = generate_fake_data(selected_funcs, num_rows)
    
    
    output= BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        writer.book.use_constant_memory = True
        df.to_excel(writer, index=False)
    
    output.seek(0)
    
    st.success("Datos generados exitosamente")
    st.write(df)
    
    st.download_button(
        label= "Descargar Excel",
        data= output,
        file_name= "datos_falsos.xlsx",
        mime= "application/vnd.openxmlformats-officedocument_spredsheetml.sheet"
    )