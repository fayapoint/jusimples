import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
// Icons temporarily removed to fix compilation errors

export default function Documentos() {
  // Use theme for conditional styling if needed
  const { theme } = useTheme();
  // Theme is used for potential styling
  const [activeCategory, setActiveCategory] = useState('todos');
  const [searchQuery, setSearchQuery] = useState('');

  const documentCategories = [
    { id: 'todos', name: 'Todos', icon: '📄' },
    { id: 'contratos', name: 'Contratos', icon: '✍️' },
    { id: 'consumidor', name: 'Consumidor', icon: '🤝' },
    { id: 'empresarial', name: 'Empresarial', icon: '🏢' },
    { id: 'trabalhista', name: 'Trabalhista', icon: '👔' },
    { id: 'imobiliario', name: 'Imobiliário', icon: '🏠' }
  ];

  const documentsList = [
    {
      id: 1,
      title: 'Contrato de Prestação de Serviços',
      category: 'contratos',
      description: 'Modelo completo de contrato para prestação de serviços diversos, com cláusulas personalizáveis.',
      popularity: 'Alta',
      complexity: 'Média'
    },
    {
      id: 2,
      title: 'Reclamação de Consumidor',
      category: 'consumidor',
      description: 'Documento formal para registro de reclamações referentes a produtos ou serviços adquiridos.',
      popularity: 'Alta',
      complexity: 'Baixa'
    },
    {
      id: 3,
      title: 'Contrato Social de Empresa Limitada',
      category: 'empresarial',
      description: 'Modelo de contrato social para constituição de sociedade limitada, conforme legislação vigente.',
      popularity: 'Média',
      complexity: 'Alta'
    },
    {
      id: 4,
      title: 'Contrato de Trabalho CLT',
      category: 'trabalhista',
      description: 'Modelo de contrato de trabalho seguindo a Consolidação das Leis do Trabalho (CLT).',
      popularity: 'Alta',
      complexity: 'Média'
    },
    {
      id: 5,
      title: 'Contrato de Aluguel Residencial',
      category: 'imobiliario',
      description: 'Modelo de contrato de locação para imóveis residenciais, com todas as cláusulas obrigatórias.',
      popularity: 'Alta',
      complexity: 'Média'
    },
    {
      id: 6,
      title: 'Termo de Confidencialidade (NDA)',
      category: 'empresarial',
      description: 'Acordo de não divulgação para proteger informações confidenciais compartilhadas entre partes.',
      popularity: 'Média',
      complexity: 'Média'
    },
    {
      id: 7,
      title: 'Notificação Extrajudicial',
      category: 'consumidor',
      description: 'Documento formal para notificar uma pessoa ou empresa sobre uma situação irregular que precisa ser resolvida.',
      popularity: 'Alta',
      complexity: 'Média'
    },
    {
      id: 8,
      title: 'Contrato de Compra e Venda',
      category: 'contratos',
      description: 'Modelo de contrato para formalização de compra e venda de bens móveis ou imóveis.',
      popularity: 'Alta',
      complexity: 'Média'
    },
    {
      id: 9,
      title: 'Termo de Rescisão Contratual',
      category: 'contratos',
      description: 'Documento para formalizar o encerramento de contratos de forma amigável entre as partes.',
      popularity: 'Média',
      complexity: 'Baixa'
    },
    {
      id: 10,
      title: 'Acordo de Parcelamento de Dívida',
      category: 'empresarial',
      description: 'Modelo de acordo para parcelamento de débitos, com reconhecimento formal da dívida.',
      popularity: 'Alta',
      complexity: 'Média'
    },
    {
      id: 11,
      title: 'Contrato de Cessão de Direitos Autorais',
      category: 'contratos',
      description: 'Modelo para transferência de direitos autorais sobre obras intelectuais.',
      popularity: 'Baixa',
      complexity: 'Alta'
    },
    {
      id: 12,
      title: 'Termo de Rescisão Trabalhista',
      category: 'trabalhista',
      description: 'Documento para formalizar o encerramento do contrato de trabalho, com discriminação de verbas rescisórias.',
      popularity: 'Alta',
      complexity: 'Alta'
    },
    {
      id: 13,
      title: 'Carta de Advertência',
      category: 'trabalhista',
      description: 'Modelo de comunicado formal para advertência de colaborador por descumprimento de normas.',
      popularity: 'Média',
      complexity: 'Baixa'
    },
    {
      id: 14,
      title: 'Contrato de Locação Comercial',
      category: 'imobiliario',
      description: 'Modelo de contrato para locação de imóveis para fins comerciais.',
      popularity: 'Média',
      complexity: 'Alta'
    },
    {
      id: 15,
      title: 'Procuração Geral',
      category: 'contratos',
      description: 'Documento que confere poderes para que uma pessoa represente outra em atos jurídicos.',
      popularity: 'Alta',
      complexity: 'Média'
    }
  ];

  const filteredDocuments = documentsList.filter(doc => 
    (activeCategory === 'todos' || doc.category === activeCategory) &&
    (searchQuery === '' || doc.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
     doc.description.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="page-container documents-page">
      <div className="hero-section">
        <h1 className="page-title">Documentos Automáticos</h1>
        <div className="divider"></div>
        <p className="hero-description">
          Crie documentos jurídicos profissionais em minutos com nossa plataforma inteligente
        </p>
        <div className="search-bar-container">
          <div className="search-bar">
            <span className="search-icon">🔍</span>
            <input 
              type="text" 
              placeholder="Buscar documentos..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
          </div>
        </div>
      </div>

      <section className="documents-section">
        <div className="document-categories">
          {documentCategories.map(category => (
            <button 
              key={category.id}
              className={`category-btn ${activeCategory === category.id ? 'active' : ''}`}
              onClick={() => setActiveCategory(category.id)}
            >
              <span className="category-icon">{category.icon}</span>
              <span className="category-name">{category.name}</span>
            </button>
          ))}
        </div>
        
        <div className="documents-list">
          {filteredDocuments.length > 0 ? (
            filteredDocuments.map(doc => (
              <div key={doc.id} className="document-card">
                <div className="document-icon">
                  📄
                </div>
                <div className="document-info">
                  <h3>{doc.title}</h3>
                  <p>{doc.description}</p>
                  <div className="document-meta">
                    <span className="document-popularity">Popularidade: {doc.popularity}</span>
                    <span className="document-complexity">Complexidade: {doc.complexity}</span>
                  </div>
                </div>
                <div className="document-actions">
                  <Link to={`/documentos/${doc.id}`} className="btn btn-sm btn-primary">
                    Criar Documento
                  </Link>
                  <button className="btn btn-sm btn-outline-secondary">
                    Pré-visualizar
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div className="no-documents">
              <p>Nenhum documento encontrado para sua busca.</p>
              <button 
                className="btn btn-outline-primary"
                onClick={() => {
                  setSearchQuery('');
                  setActiveCategory('todos');
                }}
              >
                Limpar filtros
              </button>
            </div>
          )}
        </div>
      </section>

      <section className="process-section">
        <h2 className="section-title">Como criar seu documento</h2>
        <div className="process-steps">
          <div className="process-step">
            <div className="step-number">1</div>
            <div className="step-content">
              <h3>Selecione o modelo</h3>
              <p>
                Escolha entre nossa ampla biblioteca de modelos jurídicos, desenvolvidos
                por especialistas e atualizados conforme a legislação vigente.
              </p>
            </div>
          </div>
          <div className="process-step">
            <div className="step-number">2</div>
            <div className="step-content">
              <h3>Personalize os detalhes</h3>
              <p>
                Responda a perguntas simples sobre sua situação específica para que nosso 
                sistema adapte o documento às suas necessidades.
              </p>
            </div>
          </div>
          <div className="process-step">
            <div className="step-number">3</div>
            <div className="step-content">
              <h3>Revise o conteúdo</h3>
              <p>
                Verifique se todas as informações estão corretas e faça ajustes adicionais
                caso necessário antes de finalizar.
              </p>
            </div>
          </div>
          <div className="process-step">
            <div className="step-number">4</div>
            <div className="step-content">
              <h3>Baixe ou compartilhe</h3>
              <p>
                Baixe seu documento em formato PDF ou Word, ou compartilhe diretamente
                com os envolvidos via e-mail ou link seguro.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="features-section">
        <h2 className="section-title">Vantagens dos Documentos JuSimples</h2>
        <div className="features-grid">
          <div className="feature-card">
            <h3>Legalmente Válidos</h3>
            <p>
              Todos os modelos são desenvolvidos por especialistas e estão em conformidade com
              a legislação brasileira vigente, garantindo validade jurídica.
            </p>
          </div>
          <div className="feature-card">
            <h3>Economia de Tempo</h3>
            <p>
              Crie documentos complexos em minutos, sem necessidade de conhecimento jurídico
              avançado ou horas de pesquisa.
            </p>
          </div>
          <div className="feature-card">
            <h3>Personalização Inteligente</h3>
            <p>
              Nossa tecnologia adapta automaticamente cláusulas e termos com base nas suas
              respostas, garantindo que o documento atenda às suas necessidades específicas.
            </p>
          </div>
          <div className="feature-card">
            <h3>Sempre Atualizados</h3>
            <p>
              Nossos modelos são constantemente atualizados para refletir mudanças na legislação
              e jurisprudência, garantindo que você tenha acesso ao conteúdo mais atual.
            </p>
          </div>
        </div>
      </section>

      <section className="testimonials-section">
        <h2 className="section-title">O que nossos usuários dizem</h2>
        <div className="testimonials-grid">
          <div className="testimonial-card">
            <p>
              "Os documentos automáticos do JuSimples economizaram semanas do meu tempo e milhares
              de reais em honorários advocatícios. Usei o modelo de contrato social para abrir
              minha empresa e foi surpreendentemente fácil."
            </p>
            <div className="testimonial-author">
              <h4>Carlos Eduardo</h4>
              <p>Empreendedor</p>
            </div>
          </div>
          <div className="testimonial-card">
            <p>
              "Como advogada solo, os documentos automáticos multiplicaram minha produtividade.
              Consigo atender mais clientes com a mesma qualidade, personalizando apenas os
              pontos específicos de cada caso."
            </p>
            <div className="testimonial-author">
              <h4>Dra. Mariana Silva</h4>
              <p>Advogada</p>
            </div>
          </div>
          <div className="testimonial-card">
            <p>
              "Utilizei o modelo de notificação extrajudicial e consegui resolver um problema
              com uma empresa que se arrastava há meses. A qualidade e o profissionalismo do
              documento fizeram toda diferença."
            </p>
            <div className="testimonial-author">
              <h4>Roberto Almeida</h4>
              <p>Consumidor</p>
            </div>
          </div>
        </div>
      </section>

      <section className="plans-section">
        <h2 className="section-title">Planos e Preços</h2>
        <div className="plans-grid">
          <div className="plan-card">
            <div className="plan-header">
              <h3>Básico</h3>
              <div className="price">
                <span className="amount">Gratuito</span>
              </div>
            </div>
            <div className="plan-features">
              <ul>
                <li>Acesso a 5 modelos básicos</li>
                <li>Limitado a 2 documentos por mês</li>
                <li>Exportação em formato PDF</li>
                <li>Sem armazenamento de documentos</li>
              </ul>
            </div>
            <Link to="/register?plan=free" className="btn btn-outline-primary btn-block">
              Começar Grátis
            </Link>
          </div>
          
          <div className="plan-card featured-plan">
            <div className="plan-badge">Mais Popular</div>
            <div className="plan-header">
              <h3>Profissional</h3>
              <div className="price">
                <span className="amount">R$49</span>
                <span className="period">/mês</span>
              </div>
            </div>
            <div className="plan-features">
              <ul>
                <li>Acesso a todos os modelos</li>
                <li>Documentos ilimitados</li>
                <li>Exportação em PDF e Word</li>
                <li>Armazenamento por 1 ano</li>
                <li>Personalização avançada</li>
                <li>Assinatura digital básica</li>
              </ul>
            </div>
            <Link to="/register?plan=pro" className="btn btn-primary btn-block">
              Assinar Agora
            </Link>
          </div>
          
          <div className="plan-card">
            <div className="plan-header">
              <h3>Empresarial</h3>
              <div className="price">
                <span className="amount">R$129</span>
                <span className="period">/mês</span>
              </div>
            </div>
            <div className="plan-features">
              <ul>
                <li>Todos os benefícios do Profissional</li>
                <li>Até 5 usuários</li>
                <li>Modelos personalizados para sua empresa</li>
                <li>Armazenamento ilimitado</li>
                <li>Assinatura digital avançada</li>
                <li>Suporte prioritário</li>
              </ul>
            </div>
            <Link to="/register?plan=business" className="btn btn-outline-primary btn-block">
              Contrate Agora
            </Link>
          </div>
        </div>
      </section>

      <section className="faq-section">
        <h2 className="section-title">Perguntas Frequentes</h2>
        <div className="faq-grid">
          <div className="faq-item">
            <h3>Os documentos gerados têm validade jurídica?</h3>
            <p>
              Sim. Todos os documentos são elaborados seguindo a legislação brasileira vigente
              e, quando devidamente preenchidos e assinados, possuem validade jurídica.
            </p>
          </div>
          
          <div className="faq-item">
            <h3>Posso editar os documentos depois de gerados?</h3>
            <p>
              Sim. Nossos documentos são totalmente editáveis. Após a geração automática, você
              pode fazer ajustes adicionais conforme suas necessidades específicas.
            </p>
          </div>
          
          <div className="faq-item">
            <h3>Como funciona a assinatura digital?</h3>
            <p>
              Utilizamos uma plataforma segura de assinatura eletrônica que atende aos requisitos
              da legislação brasileira, garantindo a autenticidade e integridade do documento.
            </p>
          </div>
          
          <div className="faq-item">
            <h3>Preciso de conhecimento jurídico para usar?</h3>
            <p>
              Não. Nossa plataforma foi projetada para ser acessível a qualquer pessoa. O sistema
              guia você com perguntas simples e claras, sem necessidade de conhecimento técnico.
            </p>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="cta-container">
          <h2>Pronto para criar seu documento?</h2>
          <p>
            Junte-se a milhares de brasileiros que já simplificaram sua vida jurídica com o JuSimples.
          </p>
          <div className="cta-buttons">
            <Link to="/register" className="btn btn-primary btn-lg">
              Criar Conta Gratuitamente
            </Link>
            <Link to="/contato" className="btn btn-outline-secondary btn-lg">
              Falar com um Especialista
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
