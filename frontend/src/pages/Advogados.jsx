import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import HeroImage from '../components/HeroImage';

export default function Advogados() {
  // Use theme for conditional styling if needed
  const { theme } = useTheme();
  // Apply theme-specific class
  const pageThemeClass = `lawyers-page-${theme}`;

  // State for FAQ accordions
  const [activeFaq, setActiveFaq] = useState(null);

  // Toggle FAQ item
  const toggleFaq = (index) => {
    setActiveFaq(activeFaq === index ? null : index);
  };
  
  return (
    <div className={`page-container lawyers-page ${pageThemeClass}`}>
      <div className="hero-section">
        <HeroImage type="advogados" className="hero-background" />
        <h1 className="page-title">JuSimples para Advogados</h1>
        <div className="divider"></div>
        <p className="hero-description">
          Potencialize sua prática jurídica com automação inteligente e amplie seu alcance
        </p>
        <div className="cta-buttons">
          <Link to="/register?type=lawyer" className="btn btn-primary btn-lg">
            Torne-se um Parceiro
          </Link>
          <a href="#vantagens" className="btn btn-secondary btn-lg">
            Conheça as Vantagens
          </a>
        </div>
      </div>

      <section id="vantagens" className="advantages-section">
        <h2 className="section-title">Por que se tornar um advogado parceiro?</h2>
        <div className="advantages-grid">
          <div className="advantage-card">
            <div className="advantage-icon">
              <span className="icon-lg">👥</span>
            </div>
            <h3>Amplie sua base de clientes</h3>
            <p>
              Conecte-se com clientes pré-qualificados que necessitam de seu conhecimento
              especializado para resolver questões jurídicas reais.
            </p>
          </div>
          <div className="advantage-card">
            <div className="advantage-icon">
              <span className="icon-lg">🤖</span>
            </div>
            <h3>Automação de rotinas</h3>
            <p>
              Economize tempo com a automação de tarefas repetitivas como geração de contratos, 
              petições e documentos jurídicos padrão.
            </p>
          </div>
          <div className="advantage-card">
            <div className="advantage-icon">
              <span className="icon-lg">⚖️</span>
            </div>
            <h3>Foco no que importa</h3>
            <p>
              Dedique mais tempo ao raciocínio jurídico estratégico enquanto nossas ferramentas
              cuidam das tarefas operacionais.
            </p>
          </div>
          <div className="advantage-card">
            <div className="advantage-icon">
              <span className="icon-lg">📈</span>
            </div>
            <h3>Crescimento sustentável</h3>
            <p>
              Aumente sua capacidade de atendimento sem proporcionalmente aumentar custos operacionais 
              ou administrativos.
            </p>
          </div>
        </div>
      </section>

      <section className="partnership-section">
        <h2 className="section-title">Como funciona a parceria</h2>
        <div className="partnership-model">
          <div className="model-item">
            <div className="model-number">01</div>
            <div className="model-content">
              <h3>Cadastro e verificação</h3>
              <p>
                Faça seu cadastro como advogado parceiro. Nossa equipe verificará suas credenciais
                e experiência para garantir a qualidade da nossa rede.
              </p>
            </div>
          </div>
          <div className="model-item">
            <div className="model-number">02</div>
            <div className="model-content">
              <h3>Definição de especialidades</h3>
              <p>
                Especifique suas áreas de atuação e expertise para que possamos encaminhar apenas
                casos relevantes para sua prática.
              </p>
            </div>
          </div>
          <div className="model-item">
            <div className="model-number">03</div>
            <div className="model-content">
              <h3>Recebimento de casos</h3>
              <p>
                Receba notificações sobre novos casos compatíveis com seu perfil e decida quais
                deseja assumir, sem compromissos mínimos.
              </p>
            </div>
          </div>
          <div className="model-item">
            <div className="model-number">04</div>
            <div className="model-content">
              <h3>Atendimento e remuneração</h3>
              <p>
                Atenda os clientes através de nossa plataforma segura e receba seus honorários
                diretamente, pagando apenas uma taxa por caso concluído.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="tools-section">
        <h2 className="section-title">Ferramentas para advogados</h2>
        <div className="tools-grid">
          <div className="tool-card">
            <h3>Automação de documentos</h3>
            <p>
              Gere petições, contratos e outros documentos jurídicos com base em modelos 
              customizáveis e atualizados conforme a legislação vigente.
            </p>
            <ul className="tool-features">
              <li>Mais de 100 modelos personalizáveis</li>
              <li>Preenchimento automatizado com dados do cliente</li>
              <li>Controle de versões e histórico de edições</li>
              <li>Possibilidade de upload de modelos próprios</li>
            </ul>
          </div>
          
          <div className="tool-card">
            <h3>Gestão de processos</h3>
            <p>
              Acompanhe todos os seus casos em um único painel, com lembretes de prazos, 
              organização de documentos e histórico completo de cada processo.
            </p>
            <ul className="tool-features">
              <li>Dashboard personalizado</li>
              <li>Alertas de prazos processuais</li>
              <li>Integração com tribunais</li>
              <li>Histórico de interações com clientes</li>
            </ul>
          </div>
          
          <div className="tool-card">
            <h3>Assistente de pesquisa jurídica</h3>
            <p>
              Utilize nossa IA para pesquisar jurisprudência, doutrina e legislação de forma 
              rápida e eficiente, economizando horas de pesquisa manual.
            </p>
            <ul className="tool-features">
              <li>Busca semântica em bases de dados jurídicas</li>
              <li>Sugestões de precedentes relevantes</li>
              <li>Alertas de alterações legislativas</li>
              <li>Exportação de citações formatadas</li>
            </ul>
          </div>
          
          <div className="tool-card">
            <h3>Comunicação com clientes</h3>
            <p>
              Mantenha uma comunicação clara e organizada com seus clientes através de nossa 
              plataforma segura, com registro automático de todas as interações.
            </p>
            <ul className="tool-features">
              <li>Chat criptografado</li>
              <li>Agendamento de reuniões virtuais</li>
              <li>Compartilhamento seguro de arquivos</li>
              <li>Registro de aprovações e decisões</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="specialties-section">
        <h2 className="section-title">Áreas de atuação</h2>
        <p className="section-description">
          Buscamos advogados especializados em diversas áreas para atender a demanda crescente de nossos usuários:
        </p>
        <div className="specialties-grid">
          <div className="specialty-item">
            <h3>Direito do Consumidor</h3>
            <p>
              Casos envolvendo relações de consumo, produtos defeituosos, cobranças indevidas e 
              práticas abusivas de empresas.
            </p>
          </div>
          <div className="specialty-item">
            <h3>Direito Civil</h3>
            <p>
              Ações de indenização, contratos, responsabilidade civil, direitos reais e questões 
              familiares e sucessórias.
            </p>
          </div>
          <div className="specialty-item">
            <h3>Direito Trabalhista</h3>
            <p>
              Reclamações trabalhistas, verbas rescisórias, horas extras, assédio moral e outros 
              direitos do trabalhador.
            </p>
          </div>
          <div className="specialty-item">
            <h3>Direito Empresarial</h3>
            <p>
              Assessoria a pequenos negócios, contratos empresariais, propriedade intelectual e 
              questões societárias.
            </p>
          </div>
          <div className="specialty-item">
            <h3>Direito Digital</h3>
            <p>
              Proteção de dados, crimes cibernéticos, direito ao esquecimento e responsabilidade 
              de plataformas online.
            </p>
          </div>
          <div className="specialty-item">
            <h3>Direito Tributário</h3>
            <p>
              Planejamento tributário, defesa contra cobranças indevidas, recuperação de tributos 
              e regularização fiscal.
            </p>
          </div>
        </div>
      </section>

      <section className="testimonials-section">
        <h2 className="section-title">O que dizem nossos advogados parceiros</h2>
        <div className="testimonials-slider">
          <div className="testimonial-card">
            <div className="testimonial-content">
              <p>
                "Desde que me tornei parceiro do JuSimples, consegui expandir minha prática para 
                além dos limites geográficos do meu escritório. A plataforma me conecta com clientes 
                que realmente precisam da minha especialização."
              </p>
            </div>
            <div className="testimonial-author">
              <h4>Dr. Marcelo Alves</h4>
              <p>Advogado especialista em Direito do Consumidor - OAB/SP 123.456</p>
            </div>
          </div>
          
          <div className="testimonial-card">
            <div className="testimonial-content">
              <p>
                "As ferramentas de automação do JuSimples transformaram minha produtividade. Consigo 
                atender mais clientes com a mesma qualidade, dedicando meu tempo ao que realmente 
                importa: a estratégia jurídica."
              </p>
            </div>
            <div className="testimonial-author">
              <h4>Dra. Fernanda Lima</h4>
              <p>Advogada especialista em Direito Civil - OAB/RJ 78.910</p>
            </div>
          </div>
          
          <div className="testimonial-card">
            <div className="testimonial-content">
              <p>
                "Como advogado solo, o JuSimples me permitiu competir com escritórios maiores. 
                A automação de documentos e a gestão de processos me deram escalabilidade sem 
                perder a qualidade no atendimento."
              </p>
            </div>
            <div className="testimonial-author">
              <h4>Dr. Rafael Costa</h4>
              <p>Advogado especialista em Direito Empresarial - OAB/MG 54.321</p>
            </div>
          </div>
        </div>
      </section>

      <section className="plans-section">
        <h2 className="section-title">Planos para Advogados Parceiros</h2>
        <div className="plans-grid">
          <div className="plan-card">
            <div className="plan-header">
              <h3>Essencial</h3>
              <div className="plan-price">
                <span className="amount">R$149</span>
                <span className="period">/mês</span>
              </div>
            </div>
            <div className="plan-features">
              <ul>
                <li>Receba até 5 indicações de casos por mês</li>
                <li>Acesso básico às ferramentas de automação</li>
                <li>10 documentos automáticos por mês</li>
                <li>Assistente de pesquisa jurídica (limite de consultas)</li>
                <li>1 usuário</li>
              </ul>
            </div>
            <Link to="/register?plan=lawyer-essential" className="btn btn-outline-primary btn-block">
              Selecionar Plano
            </Link>
          </div>
          
          <div className="plan-card featured-plan">
            <div className="plan-badge">Mais Popular</div>
            <div className="plan-header">
              <h3>Premium</h3>
              <div className="plan-price">
                <span className="amount">R$299</span>
                <span className="period">/mês</span>
              </div>
            </div>
            <div className="plan-features">
              <ul>
                <li>Receba até 15 indicações de casos por mês</li>
                <li>Acesso completo às ferramentas de automação</li>
                <li>Documentos automáticos ilimitados</li>
                <li>Assistente de pesquisa jurídica ilimitado</li>
                <li>Integração com tribunais</li>
                <li>Até 3 usuários</li>
                <li>Taxa reduzida por caso concluído</li>
              </ul>
            </div>
            <Link to="/register?plan=lawyer-premium" className="btn btn-primary btn-block">
              Selecionar Plano
            </Link>
          </div>
          
          <div className="plan-card">
            <div className="plan-header">
              <h3>Escritório</h3>
              <div className="plan-price">
                <span className="amount">R$599</span>
                <span className="period">/mês</span>
              </div>
            </div>
            <div className="plan-features">
              <ul>
                <li>Receba indicações de casos ilimitadas</li>
                <li>Acesso completo às ferramentas de automação</li>
                <li>Documentos automáticos ilimitados</li>
                <li>Assistente de pesquisa jurídica avançado</li>
                <li>Integração com tribunais e sistemas de gestão</li>
                <li>Até 10 usuários</li>
                <li>Taxa mínima por caso concluído</li>
                <li>Perfil destacado na plataforma</li>
              </ul>
            </div>
            <Link to="/register?plan=lawyer-office" className="btn btn-outline-primary btn-block">
              Selecionar Plano
            </Link>
          </div>
        </div>
        <div className="plan-note">
          <p>
            * Planos anuais com 20% de desconto disponíveis.
            Para escritórios com mais de 10 advogados, entre em contato para um plano personalizado.
          </p>
        </div>
      </section>

      <section className="faq-section">
        <h2 className="section-title">Perguntas Frequentes</h2>
        <div className="faq-list">
          <div 
            className={`faq-item ${activeFaq === 0 ? 'active' : ''}`}
            onClick={() => toggleFaq(0)}
          >
            <h3>Como são selecionados os advogados parceiros?</h3>
            {activeFaq === 0 && (
              <p>
                Realizamos uma verificação completa de credenciais, incluindo situação junto à OAB, 
                experiência profissional e especialidades declaradas. Também coletamos feedback dos 
                clientes para garantir a qualidade do serviço prestado.
              </p>
            )}
          </div>
          
          <div 
            className={`faq-item ${activeFaq === 1 ? 'active' : ''}`}
            onClick={() => toggleFaq(1)}
          >
            <h3>Qual é o modelo de remuneração?</h3>
            {activeFaq === 1 && (
              <p>
                Os advogados definem seus próprios honorários, que são pagos diretamente pelos clientes. 
                O JuSimples cobra uma taxa por caso concluído, que varia de acordo com o plano escolhido 
                e a complexidade do caso.
              </p>
            )}
          </div>
          
          <div 
            className={`faq-item ${activeFaq === 2 ? 'active' : ''}`}
            onClick={() => toggleFaq(2)}
          >
            <h3>Sou obrigado a aceitar todos os casos?</h3>
            {activeFaq === 2 && (
              <p>
                Não. Você tem total liberdade para escolher quais casos deseja assumir, de acordo com 
                sua disponibilidade, especialização e interesse.
              </p>
            )}
          </div>
          
          <div 
            className={`faq-item ${activeFaq === 3 ? 'active' : ''}`}
            onClick={() => toggleFaq(3)}
          >
            <h3>Como funciona a proteção de dados na plataforma?</h3>
            {activeFaq === 3 && (
              <p>
                O JuSimples segue rigorosamente a LGPD e implementa medidas de segurança avançadas para 
                proteger dados sensíveis. Todas as comunicações são criptografadas e os dados são 
                armazenados de forma segura.
              </p>
            )}
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="cta-container">
          <h2>Pronto para transformar sua prática jurídica?</h2>
          <p>
            Junte-se a centenas de advogados que já estão potencializando seus serviços 
            e expandindo sua base de clientes com o JuSimples.
          </p>
          <div className="cta-buttons">
            <Link to="/register?type=lawyer" className="btn btn-primary btn-lg">
              Tornar-se Parceiro
            </Link>
            <Link to="/contato?subject=parceria" className="btn btn-outline-secondary btn-lg">
              Falar com um Representante
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
