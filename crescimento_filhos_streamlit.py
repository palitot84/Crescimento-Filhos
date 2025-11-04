import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Dados dos quartis de crescimento (altura em cm)

QUARTIS_MENINO = {
    0: {'p3': 46.0, 'p15': 47.8, 'p50': 49.7, 'p85': 51.6, 'p97': 53.5},
    6: {'p3': 63.0, 'p15': 65.2, 'p50': 67.4, 'p85': 69.6, 'p97': 71.7},
    12: {'p3': 70.8, 'p15': 73.2, 'p50': 75.5, 'p85': 77.9, 'p97': 80.3},
    18: {'p3': 76.7, 'p15': 79.4, 'p50': 82.1, 'p85': 84.8, 'p97': 87.5},
    24: {'p3': 81.5, 'p15': 84.6, 'p50': 87.6, 'p85': 90.7, 'p97': 93.7},
    30: {'p3': 85.5, 'p15': 89.0, 'p50': 92.5, 'p85': 95.9, 'p97': 99.4},
    36: {'p3': 88.8, 'p15': 92.7, 'p50': 96.5, 'p85': 100.4, 'p97': 104.3},
    42: {'p3': 91.7, 'p15': 95.9, 'p50': 100.2, 'p85': 104.4, 'p97': 108.7},
    48: {'p3': 94.2, 'p15': 98.9, 'p50': 103.6, 'p85': 108.3, 'p97': 113.0},
    54: {'p3': 96.5, 'p15': 101.6, 'p50': 106.7, 'p85': 111.8, 'p97': 116.9},
    60: {'p3': 98.5, 'p15': 104.1, 'p50': 109.7, 'p85': 115.2, 'p97': 120.8},
    66: {'p3': 100.5, 'p15': 106.4, 'p50': 112.3, 'p85': 118.2, 'p97': 124.2},
    72: {'p3': 102.3, 'p15': 108.5, 'p50': 114.8, 'p85': 121.1, 'p97': 127.4},
    78: {'p3': 104.0, 'p15': 110.5, 'p50': 117.1, 'p85': 123.7, 'p97': 130.3},
    84: {'p3': 105.6, 'p15': 112.3, 'p50': 119.2, 'p85': 126.2, 'p97': 133.1},
    90: {'p3': 107.2, 'p15': 114.0, 'p50': 121.2, 'p85': 128.5, 'p97': 135.7},
    96: {'p3': 108.7, 'p15': 115.6, 'p50': 123.0, 'p85': 130.6, 'p97': 138.2},
    102: {'p3': 110.1, 'p15': 117.1, 'p50': 124.7, 'p85': 132.6, 'p97': 140.5},
    108: {'p3': 111.4, 'p15': 118.5, 'p50': 126.2, 'p85': 134.4, 'p97': 142.7},
    114: {'p3': 112.6, 'p15': 119.8, 'p50': 127.6, 'p85': 136.1, 'p97': 144.7},
    120: {'p3': 113.7, 'p15': 121.0, 'p50': 128.9, 'p85': 137.6, 'p97': 146.6}
}


QUARTIS_MENINA =  {
    0: {'p3': 45.3, 'p15': 47.2, 'p50': 49.0, 'p85': 50.8, 'p97': 52.6},
    6: {'p3': 61.7, 'p15': 63.9, 'p50': 66.1, 'p85': 68.2, 'p97': 70.4},
    12: {'p3': 68.8, 'p15': 71.3, 'p50': 73.9, 'p85': 76.5, 'p97': 79.1},
    18: {'p3': 74.1, 'p15': 77.0, 'p50': 79.9, 'p85': 82.8, 'p97': 85.6},
    24: {'p3': 78.3, 'p15': 81.6, 'p50': 84.8, 'p85': 88.1, 'p97': 91.3},
    30: {'p3': 81.8, 'p15': 85.6, 'p50': 89.3, 'p85': 93.0, 'p97': 96.8},
    36: {'p3': 84.8, 'p15': 88.9, 'p50': 93.0, 'p85': 97.1, 'p97': 101.2},
    42: {'p3': 87.3, 'p15': 91.8, 'p50': 96.3, 'p85': 100.8, 'p97': 105.3},
    48: {'p3': 89.5, 'p15': 94.3, 'p50': 99.2, 'p85': 104.1, 'p97': 108.9},
    54: {'p3': 91.5, 'p15': 96.6, 'p50': 101.8, 'p85': 106.9, 'p97': 112.1},
    60: {'p3': 93.3, 'p15': 98.7, 'p50': 104.2, 'p85': 109.6, 'p97': 115.1},
    66: {'p3': 95.0, 'p15': 100.6, 'p50': 106.3, 'p85': 112.0, 'p97': 117.7},
    72: {'p3': 96.6, 'p15': 102.4, 'p50': 108.3, 'p85': 114.3, 'p97': 120.2},
    78: {'p3': 98.1, 'p15': 104.1, 'p50': 110.1, 'p85': 116.3, 'p97': 122.5},
    84: {'p3': 99.5, 'p15': 105.7, 'p50': 111.8, 'p85': 118.2, 'p97': 124.7},
    90: {'p3': 100.9, 'p15': 107.2, 'p50': 113.4, 'p85': 120.0, 'p97': 126.7},
    96: {'p3': 102.2, 'p15': 108.6, 'p50': 114.9, 'p85': 121.6, 'p97': 128.5},
    102: {'p3': 103.5, 'p15': 109.9, 'p50': 116.3, 'p85': 123.1, 'p97': 130.2},
    108: {'p3': 104.7, 'p15': 111.2, 'p50': 117.5, 'p85': 124.5, 'p97': 131.8},
    114: {'p3': 105.9, 'p15': 112.4, 'p50': 118.7, 'p85': 125.8, 'p97': 133.3},
    120: {'p3': 107.0, 'p15': 113.5, 'p50': 119.7, 'p85': 127.0, 'p97': 134.7}
}


def inicializar_dados():
    if 'criancas' not in st.session_state:
        st.session_state.criancas = []

def salvar_dados():
    with open('dados_crescimento.json', 'w') as f:
        json.dump(st.session_state.criancas, f)

def carregar_dados():
    try:
        with open('dados_crescimento.json', 'r') as f:
            st.session_state.criancas = json.load(f)
    except FileNotFoundError:
        st.session_state.criancas = []

def obter_quartis(sexo):
    return QUARTIS_MENINO if sexo == 'Masculino' else QUARTIS_MENINA

def plotar_grafico(crianca_nome):
    crianca = next((c for c in st.session_state.criancas if c['nome'] == crianca_nome), None)
    if not crianca or not crianca['medidas']:
        st.warning("Nenhuma medida encontrada para esta criança.")
        return
    
    quartis = obter_quartis(crianca['sexo'])
    
    # Criar DataFrame com os quartis
    idades_quartis = list(quartis.keys())
    df_quartis = pd.DataFrame({
        'idade_meses': idades_quartis,
        'P3': [quartis[idade]['p3'] for idade in idades_quartis],
        'P15': [quartis[idade]['p15'] for idade in idades_quartis],
        'P50': [quartis[idade]['p50'] for idade in idades_quartis],
        'P85': [quartis[idade]['p85'] for idade in idades_quartis],
        'P97': [quartis[idade]['p97'] for idade in idades_quartis]
    })
    
    # Criar DataFrame com as medidas da criança
    df_crianca = pd.DataFrame(crianca['medidas'])
    
    # Criar gráfico
    fig = go.Figure()
    
    # Adicionar linhas dos quartis
    fig.add_trace(go.Scatter(x=df_quartis['idade_meses'], y=df_quartis['P3'], 
                            mode='lines', name='P3', line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=df_quartis['idade_meses'], y=df_quartis['P15'], 
                            mode='lines', name='P15', line=dict(color='orange', dash='dash')))
    fig.add_trace(go.Scatter(x=df_quartis['idade_meses'], y=df_quartis['P50'], 
                            mode='lines', name='P50 (Mediana)', line=dict(color='blue', width=3)))
    fig.add_trace(go.Scatter(x=df_quartis['idade_meses'], y=df_quartis['P85'], 
                            mode='lines', name='P85', line=dict(color='orange', dash='dash')))
    fig.add_trace(go.Scatter(x=df_quartis['idade_meses'], y=df_quartis['P97'], 
                            mode='lines', name='P97', line=dict(color='red', dash='dash')))
    
    # Adicionar pontos da criança
    fig.add_trace(go.Scatter(x=df_crianca['idade_meses'], y=df_crianca['altura'], 
                            mode='markers+lines', name=f'{crianca_nome}', 
                            marker=dict(size=10, color='green'),
                            line=dict(color='green', width=3)))
    
    fig.update_layout(
        title=f'Crescimento de {crianca_nome} ({crianca["sexo"]})',
        xaxis_title='Idade (meses)',
        yaxis_title='Altura (cm)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("📏 Controle de Crescimento Infantil")
    st.write("Acompanhe o crescimento dos seus filhos com base nos quartis de crescimento da OMS")
    
    inicializar_dados()
    carregar_dados()
    
    # Sidebar para navegação
    st.sidebar.title("Menu")
    opcao = st.sidebar.selectbox("Escolha uma opção:", 
                                ["Cadastrar Criança", "Registrar Medida", "Editar Medidas", "Visualizar Gráfico"])
    
    if opcao == "Cadastrar Criança":
        st.header("👶 Cadastrar Nova Criança")
        
        with st.form("cadastro_crianca"):
            nome = st.text_input("Nome da criança:")
            sexo = st.selectbox("Sexo:", ["Masculino", "Feminino"])
            
            if st.form_submit_button("Cadastrar"):
                if nome:
                    # Verificar se já existe
                    if any(c['nome'] == nome for c in st.session_state.criancas):
                        st.error("Criança já cadastrada!")
                    else:
                        nova_crianca = {
                            'nome': nome,
                            'sexo': sexo,
                            'medidas': []
                        }
                        st.session_state.criancas.append(nova_crianca)
                        salvar_dados()
                        st.success(f"Criança {nome} cadastrada com sucesso!")
                else:
                    st.error("Por favor, informe o nome da criança.")
    
    elif opcao == "Registrar Medida":
        st.header("📐 Registrar Nova Medida")
        
        if not st.session_state.criancas:
            st.warning("Nenhuma criança cadastrada. Cadastre uma criança primeiro.")
            return
        
        nomes = [c['nome'] for c in st.session_state.criancas]
        
        with st.form("registrar_medida"):
            nome_selecionado = st.selectbox("Selecione a criança:", nomes)
            idade_anos = st.number_input("Idade (anos):", min_value=0, max_value=10, value=0)
            idade_meses_extra = st.number_input("Meses adicionais:", min_value=0, max_value=11, value=0)
            altura = st.number_input("Altura (cm):", min_value=30.0, max_value=200.0, value=50.0, step=0.1)
            
            if st.form_submit_button("Registrar"):
                idade_total_meses = (idade_anos * 12) + idade_meses_extra
                
                if idade_total_meses > 120:
                    st.error("Idade máxima é 10 anos (120 meses).")
                    return
                
                # Encontrar a criança e adicionar medida
                for crianca in st.session_state.criancas:
                    if crianca['nome'] == nome_selecionado:
                        nova_medida = {
                            'idade_meses': idade_total_meses,
                            'altura': altura,
                            'data': datetime.now().strftime('%Y-%m-%d')
                        }
                        crianca['medidas'].append(nova_medida)
                        # Ordenar por idade
                        crianca['medidas'].sort(key=lambda x: x['idade_meses'])
                        break
                
                salvar_dados()
                st.success("Medida registrada com sucesso!")
    
    elif opcao == "Editar Medidas":
        st.header("✏️ Editar Medidas")
        
        if not st.session_state.criancas:
            st.warning("Nenhuma criança cadastrada.")
            return
        
        nomes = [c['nome'] for c in st.session_state.criancas]
        nome_selecionado = st.selectbox("Selecione a criança:", nomes, key="editar_crianca")
        
        if nome_selecionado:
            crianca = next((c for c in st.session_state.criancas if c['nome'] == nome_selecionado), None)
            
            if not crianca['medidas']:
                st.warning("Esta criança não possui medidas registradas.")
                return
            
            st.subheader("Medidas Registradas")
            
            # Mostrar medidas com opções de edição e exclusão
            for i, medida in enumerate(crianca['medidas']):
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.write(f"**Data:** {medida['data']}")
                    st.write(f"**Idade:** {medida['idade_meses']} meses ({medida['idade_meses']/12:.1f} anos)")
                
                with col2:
                    st.write(f"**Altura:** {medida['altura']} cm")
                
                with col3:
                    if st.button("✏️ Editar", key=f"edit_{i}"):
                        st.session_state[f'editando_{i}'] = True
                
                with col4:
                    if st.button("🗑️ Excluir", key=f"delete_{i}"):
                        crianca['medidas'].pop(i)
                        salvar_dados()
                        st.success("Medida excluída com sucesso!")
                        st.rerun()
                
                # Formulário de edição
                if st.session_state.get(f'editando_{i}', False):
                    st.write("---")
                    st.write("**Editando medida:**")
                    
                    with st.form(f"edit_form_{i}"):
                        col_edit1, col_edit2 = st.columns(2)
                        
                        with col_edit1:
                            nova_idade_anos = st.number_input("Nova idade (anos):", 
                                                            min_value=0, max_value=10, 
                                                            value=int(medida['idade_meses'] // 12),
                                                            key=f"nova_idade_anos_{i}")
                            nova_idade_meses_extra = st.number_input("Meses adicionais:", 
                                                                   min_value=0, max_value=11, 
                                                                   value=int(medida['idade_meses'] % 12),
                                                                   key=f"nova_idade_meses_{i}")
                        
                        with col_edit2:
                            nova_altura = st.number_input("Nova altura (cm):", 
                                                        min_value=30.0, max_value=200.0, 
                                                        value=float(medida['altura']),
                                                        step=0.1,
                                                        key=f"nova_altura_{i}")
                        
                        col_btn1, col_btn2 = st.columns(2)
                        
                        with col_btn1:
                            if st.form_submit_button("💾 Salvar"):
                                nova_idade_total = (nova_idade_anos * 12) + nova_idade_meses_extra
                                
                                if nova_idade_total > 120:
                                    st.error("Idade máxima é 10 anos (120 meses).")
                                else:
                                    medida['idade_meses'] = nova_idade_total
                                    medida['altura'] = nova_altura
                                    # Reordenar por idade
                                    crianca['medidas'].sort(key=lambda x: x['idade_meses'])
                                    salvar_dados()
                                    st.session_state[f'editando_{i}'] = False
                                    st.success("Medida atualizada com sucesso!")
                                    st.rerun()
                        
                        with col_btn2:
                            if st.form_submit_button("❌ Cancelar"):
                                st.session_state[f'editando_{i}'] = False
                                st.rerun()
                
                st.write("---")
    
    elif opcao == "Visualizar Gráfico":
        st.header("📊 Gráfico de Crescimento")
        
        if not st.session_state.criancas:
            st.warning("Nenhuma criança cadastrada.")
            return
        
        nomes = [c['nome'] for c in st.session_state.criancas]
        nome_selecionado = st.selectbox("Selecione a criança para visualizar:", nomes)
        
        if nome_selecionado:
            plotar_grafico(nome_selecionado)
            
            # Mostrar tabela de medidas
            crianca = next((c for c in st.session_state.criancas if c['nome'] == nome_selecionado), None)
            if crianca and crianca['medidas']:
                st.subheader("Histórico de Medidas")
                
                # Criar DataFrame para exibição
                df_medidas = pd.DataFrame(crianca['medidas'])
                df_medidas['idade_anos'] = df_medidas['idade_meses'] / 12
                df_display = df_medidas[['data', 'idade_anos', 'altura']].round(2)
                df_display.columns = ['Data', 'Idade (anos)', 'Altura (cm)']
                
                # Adicionar índices para identificação
                df_display.index = range(len(df_display))
                
                st.dataframe(df_display, use_container_width=True)
                
                # Opção rápida para excluir medida
                st.write("**Ações Rápidas:**")
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if len(crianca['medidas']) > 0:
                        indices_medidas = list(range(len(crianca['medidas'])))
                        labels_medidas = [f"Medida {i+1}: {medida['data']} - {medida['altura']}cm" 
                                        for i, medida in enumerate(crianca['medidas'])]
                        
                        medida_para_excluir = st.selectbox(
                            "Selecione uma medida para excluir:",
                            options=[-1] + indices_medidas,
                            format_func=lambda x: "Selecione uma medida..." if x == -1 else labels_medidas[x],
                            key="excluir_rapido"
                        )
                
                with col2:
                    if st.button("🗑️ Excluir Selecionada", key="btn_excluir_rapido"):
                        if medida_para_excluir != -1:
                            crianca['medidas'].pop(medida_para_excluir)
                            salvar_dados()
                            st.success("Medida excluída com sucesso!")
                            st.rerun()
                        else:
                            st.warning("Selecione uma medida para excluir.")
                
                st.info("💡 **Dica:** Para editar medidas ou fazer alterações mais detalhadas, use a opção 'Editar Medidas' no menu lateral.")

if __name__ == "__main__":
    main()

