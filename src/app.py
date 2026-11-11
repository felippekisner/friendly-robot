from __future__ import annotations

import pandas as pd
import streamlit as st

try:
    from src.crud import (
        create_food,
        create_price,
        create_supplier,
        create_worker,
        delete_food,
        delete_price,
        delete_supplier,
        delete_worker,
        list_foods,
        list_prices,
        list_suppliers,
        list_workers,
        update_food,
        update_price,
        update_supplier,
        update_worker,
    )
    from src.database import init_db
    from src.models import Food, FoodPrice, Supplier, Worker
except ModuleNotFoundError:
    from crud import (
        create_food,
        create_price,
        create_supplier,
        create_worker,
        delete_food,
        delete_price,
        delete_supplier,
        delete_worker,
        list_foods,
        list_prices,
        list_suppliers,
        list_workers,
        update_food,
        update_price,
        update_supplier,
        update_worker,
    )
    from database import init_db
    from models import Food, FoodPrice, Supplier, Worker


init_db()


st.set_page_config(page_title="Festa IFC", page_icon="🎉", layout="wide")
st.title("Gestão da Festa do IFC - Campus Blumenau")

with st.sidebar:
    st.header("Configuração do banco")
    st.write("SQLite: usado para testes locais")
    st.write("MySQL: usado em produção")
    st.caption("Defina USE_MYSQL=true e as variáveis MYSQL_* para ativar o MySQL.")


def render_food_section():
    st.subheader("Cadastro de alimentos")
    foods = list_foods()
    food_names = ["Novo alimento"] + [food.name for food in foods]
    selected_name = st.selectbox("Selecionar alimento para editar", food_names, index=0)

    existing_food = next((food for food in foods if food.name == selected_name), None)

    with st.form("food_form"):
        name = st.text_input("Nome do alimento", value=existing_food.name if existing_food else "")
        description = st.text_area("Descrição", value=existing_food.description if existing_food else "")
        category = st.text_input("Categoria", value=existing_food.category if existing_food else "")
        donated = st.checkbox("Doado / sem custo", value=existing_food.donated if existing_food else False)

        supplier_options = list_suppliers()
        supplier_map = {supplier.name: supplier.id for supplier in supplier_options}
        selected_suppliers = st.multiselect(
            "Fornecedores de insumos",
            options=list(supplier_map.keys()),
            default=[supplier.name for supplier in (existing_food.suppliers if existing_food else [])],
        )

        submitted = st.form_submit_button("Salvar alimento")

        if submitted:
            payload = {
                "name": name,
                "description": description,
                "category": category,
                "donated": donated,
            }
            supplier_ids = [supplier_map[supplier_name] for supplier_name in selected_suppliers]
            if existing_food:
                update_food(existing_food.id, payload, supplier_ids)
                st.success(f"Alimento atualizado: {name}")
            else:
                create_food(payload, supplier_ids)
                st.success(f"Alimento cadastrado: {name}")

    if foods:
        st.subheader("Lista de alimentos")
        food_rows = [
            {
                "Nome": food.name,
                "Categoria": food.category,
                "Descrição": food.description or "",
                "Doado": "Sim" if food.donated else "Não",
                "Fornecedores": ", ".join(supplier.name for supplier in food.suppliers) if food.suppliers else "Nenhum fornecedor associado",
            }
            for food in foods
        ]
        st.dataframe(pd.DataFrame(food_rows), use_container_width=True)

        for food in foods:
            if st.button(f"Excluir {food.name}", key=f"delete_food_{food.id}"):
                delete_food(food.id)
                st.rerun()


def render_supplier_section():
    st.subheader("Cadastro de fornecedores")
    suppliers = list_suppliers()
    supplier_names = ["Novo fornecedor"] + [supplier.name for supplier in suppliers]
    selected_name = st.selectbox("Selecionar fornecedor para editar", supplier_names, index=0)

    existing_supplier = next((supplier for supplier in suppliers if supplier.name == selected_name), None)

    with st.form("supplier_form"):
        name = st.text_input("Nome do fornecedor", value=existing_supplier.name if existing_supplier else "")
        contact = st.text_input("Contato", value=existing_supplier.contact if existing_supplier else "")
        supplier_type = st.text_input("Tipo", value=existing_supplier.type if existing_supplier else "")
        notes = st.text_area("Observações", value=existing_supplier.notes if existing_supplier else "")

        submitted = st.form_submit_button("Salvar fornecedor")

        if submitted:
            payload = {
                "name": name,
                "contact": contact,
                "type": supplier_type,
                "notes": notes,
            }
            if existing_supplier:
                update_supplier(existing_supplier.id, payload)
                st.success(f"Fornecedor atualizado: {name}")
            else:
                create_supplier(payload)
                st.success(f"Fornecedor cadastrado: {name}")

    if suppliers:
        st.subheader("Lista de fornecedores")
        supplier_rows = [
            {
                "Nome": supplier.name,
                "Tipo": supplier.type,
                "Contato": supplier.contact or "",
                "Observações": supplier.notes or "",
                "Alimentos": ", ".join(food.name for food in supplier.foods) if supplier.foods else "Sem alimentos vinculados",
            }
            for supplier in suppliers
        ]
        st.dataframe(pd.DataFrame(supplier_rows), use_container_width=True)

        for supplier in suppliers:
            if st.button(f"Excluir {supplier.name}", key=f"delete_supplier_{supplier.id}"):
                delete_supplier(supplier.id)
                st.rerun()


def render_worker_section():
    st.subheader("Cadastro de trabalhadores")
    workers = list_workers()
    worker_names = ["Nova pessoa"] + [worker.name for worker in workers]
    selected_name = st.selectbox("Selecionar pessoa para editar", worker_names, index=0)

    existing_worker = next((worker for worker in workers if worker.name == selected_name), None)

    with st.form("worker_form"):
        name = st.text_input("Nome", value=existing_worker.name if existing_worker else "")
        role = st.text_input("Função", value=existing_worker.role if existing_worker else "")
        category = st.selectbox(
            "Categoria",
            ["Aluno", "Pai/Mãe de aluno", "Servidor"],
            index=["Aluno", "Pai/Mãe de aluno", "Servidor"].index(existing_worker.category) if existing_worker else 0,
        )
        phone = st.text_input("Telefone", value=existing_worker.phone if existing_worker else "")
        notes = st.text_area("Observações", value=existing_worker.notes if existing_worker else "")

        submitted = st.form_submit_button("Salvar pessoa")

        if submitted:
            payload = {
                "name": name,
                "role": role,
                "category": category,
                "phone": phone,
                "notes": notes,
            }
            if existing_worker:
                update_worker(existing_worker.id, payload)
                st.success(f"Pessoa atualizada: {name}")
            else:
                create_worker(payload)
                st.success(f"Pessoa cadastrada: {name}")

    if workers:
        st.subheader("Lista de pessoas")
        worker_rows = [
            {
                "Nome": worker.name,
                "Função": worker.role,
                "Categoria": worker.category,
                "Telefone": worker.phone or "",
                "Observações": worker.notes or "",
            }
            for worker in workers
        ]
        st.dataframe(pd.DataFrame(worker_rows), use_container_width=True)

        for worker in workers:
            if st.button(f"Excluir {worker.name}", key=f"delete_worker_{worker.id}"):
                delete_worker(worker.id)
                st.rerun()


def render_price_section():
    st.subheader("Cadastro de preços de venda")
    prices = list_prices()
    foods = list_foods()

    with st.form("price_form"):
        food_choice = st.selectbox("Alimento", [food.name for food in foods], index=0 if foods else None)
        sale_price = st.number_input("Preço de venda (R$)", min_value=0.0, step=0.50, format="%.2f")
        submitted = st.form_submit_button("Salvar preço")

        if submitted and food_choice:
            food = next((item for item in foods if item.name == food_choice), None)
            if food:
                create_price({"food_id": food.id, "price": sale_price})
                st.success(f"Preço registrado para {food_choice}: R$ {sale_price:.2f}")

    if prices:
        st.subheader("Histórico de preços")
        price_rows = [
            {
                "Alimento": next((food.name for food in foods if food.id == price.food_id), "Alimento removido"),
                "Preço": f"R$ {price.price:.2f}",
            }
            for price in prices
        ]
        st.dataframe(pd.DataFrame(price_rows), use_container_width=True)

        for price in prices:
            if st.button(f"Excluir preço {price.id}", key=f"delete_price_{price.id}"):
                delete_price(price.id)
                st.rerun()


tab_alimentos, tab_fornecedores, tab_trabalhadores, tab_precos = st.tabs([
    "Alimentos",
    "Fornecedores",
    "Trabalhadores",
    "Preços",
])

with tab_alimentos:
    render_food_section()

with tab_fornecedores:
    render_supplier_section()

with tab_trabalhadores:
    render_worker_section()

with tab_precos:
    render_price_section()
