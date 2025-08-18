import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import HeroImage from '../components/HeroImage';

export default function Empresas() {
  // Use theme for conditional styling if needed
  const { theme } = useTheme();
  // Apply theme-specific class
  const pageThemeClass = `business-page-${theme}`;

  // State for FAQ accordion
  const [activeFaq, setActiveFaq] = useState(null);

  // Toggle FAQ item
  const toggleFaq = (index) => {
    setActiveFaq(activeFaq === index ? null : index);
  };
  
  return (
    <div className={`page-container business-page ${pageThemeClass}`}>
      <div className="hero-section">
        <HeroImage type="empresas" className="hero-background" />
        <h1 className="page-title">JuSimples para Pequenas Empresas</h1>
        <div className="divider"></div>
        <p className="hero-description">
          Soluções jurídicas acessíveis para o crescimento do seu negócio
        </p>
        <div className="cta-buttons">
          <Link to="/register?type=business" className="btn btn-primary btn-lg">
            Começar Agora
          </Link>
          <a href="#solucoes" className="btn btn-secondary btn-lg">
            Ver Soluções
          </a>
        </div>
      </div>

      <section className="benefits-section">
        <h2 className="section-title">Por que escolher o JuSimples?</h2>
        <div className="benefits-grid">
          <div className="benefit-card">
            <h3>Economia</h3>
            <p>
              Reduza custos com serviços jurídicos através de nossa plataforma de automação.
              Sem surpresas ou taxas ocultas.
            </p>
          </div>
          <div className="benefit-card">
            <h3>Praticidade</h3>
            <p>
              Acesse documentos e orientações jurídicas 24h por dia, 7 dias por semana,
              sem agendamentos ou deslocamentos.
            </p>
          </div>
          <div className="benefit-card">
            <h3>Segurança</h3>
            <p>
              Documentos elaborados por especialistas e atualizados constantemente conforme
              a legislação brasileira vigente.
            </p>
          </div>
          <div className="benefit-card">
            <h3>Produtividade</h3>
            <p>
              Dedique mais tempo ao seu negócio enquanto automatizamos as questões jurídicas
              do dia a dia da sua empresa.
            </p>
          </div>
        </div>
      </section>

      <section id="solucoes" className="solutions-section">
        <h2 className="section-title">Nossas Soluções</h2>
        <div className="solutions-grid">
          <div className="solution-card">
            <div className="solution-icon">
              <span className="icon-lg">📄</span>
            </div>
            <h3>Contratos Automáticos</h3>
            <p>
              Gere contratos personalizados para diversas necessidades: prestação de serviços,
              fornecimento, confidencialidade, termos de uso e muito mais.
            </p>
            <ul className="solution-features">
              <li>Modelos atualizados conforme legislação</li>
              <li>Personalização de cláusulas</li>
              <li>Assinatura digital integrada</li>
              <li>Armazenamento seguro</li>
            </ul>
            <Link to="/documentos?type=contratos" className="btn btn-outline-primary">
              Ver Contratos
            </Link>
          </div>

          <div className="solution-card">
            <div className="solution-icon">
              <span className="icon-lg">👔</span>
            </div>
            <h3>Gestão Trabalhista</h3>
            <p>
              Simplifique a administração de recursos humanos com documentos e orientações
              para contratação, demissão e gestão de colaboradores.
            </p>
            <ul className="solution-features">
              <li>Contratos de trabalho</li>
              <li>Termos de rescisão</li>
              <li>Políticas internas</li>
              <li>Orientação sobre legislação trabalhista</li>
            </ul>
            <Link to="/documentos?type=trabalhista" className="btn btn-outline-primary">
              Acessar Ferramentas
            </Link>
          </div>

          <div className="solution-card">
            <div className="solution-icon">
              <span className="icon-lg">🤝</span>
            </div>
            <h3>Cobrança e Recuperação</h3>
            <p>
              Ferramentas para gestão de inadimplência, cobrança eficiente e recuperação
              de créditos de forma amigável e legal.
            </p>
            <ul className="solution-features">
              <li>Notificações de cobrança automáticas</li>
              <li>Acordos de parcelamento</li>
              <li>Termos de confissão de dívida</li>
              <li>Estratégias de negociação</li>
            </ul>
            <Link to="/documentos?type=cobranca" className="btn btn-outline-primary">
              Ver Soluções
            </Link>
          </div>

          <div className="solution-card">
            <div className="solution-icon">
              <span className="icon-lg">💡</span>
            </div>
            <h3>Consultoria Empresarial</h3>
            <p>
              Obtenha respostas rápidas para dúvidas jurídicas do dia a dia e orientações
              para decisões estratégicas da sua empresa.
            </p>
            <ul className="solution-features">
              <li>Consultas ilimitadas via IA</li>
              <li>Análise de riscos contratuais</li>
              <li>Orientação sobre aspectos regulatórios</li>
              <li>Acesso a advogados especializados</li>
            </ul>
            <Link to="/register?type=business" className="btn btn-outline-primary">
              Consultar Agora
            </Link>
          </div>
        </div>
      </section>

      <section className="process-section">
        <h2 className="section-title">Como Funciona</h2>
        <div className="process-steps">
          <div className="process-step">
            <div className="step-number">1</div>
            <h3>Cadastre sua empresa</h3>
            <p>
              Crie sua conta empresarial em minutos, fornecendo informações básicas sobre
              seu negócio para personalizar sua experiência.
            </p>
          </div>
          <div className="process-step">
            <div className="step-number">2</div>
            <h3>Escolha suas ferramentas</h3>
            <p>
              Navegue por nossa biblioteca de soluções e selecione as que melhor atendem
              às necessidades do seu negócio.
            </p>
          </div>
          <div className="process-step">
            <div className="step-number">3</div>
            <h3>Personalize os documentos</h3>
            <p>
              Responda a perguntas simples para que nosso sistema gere documentos
              personalizados para sua empresa.
            </p>
          </div>
          <div className="process-step">
            <div className="step-number">4</div>
            <h3>Implemente as soluções</h3>
            <p>
              Utilize os documentos gerados em sua operação ou consulte nossas orientações
              para implementar as melhores práticas jurídicas.
            </p>
          </div>
        </div>
      </section>

      <section className="testimonials-section">
        <h2 className="section-title">O que dizem nossos clientes</h2>
        <div className="testimonials-grid">
          <div className="testimonial-card">
            <div className="testimonial-content">
              <p>
                "O JuSimples transformou a forma como gerenciamos contratos em nossa empresa.
                Economizamos tempo e dinheiro, além de termos mais segurança jurídica em nossas operações."
              </p>
            </div>
            <div className="testimonial-author">
              <h4>Ana Martins</h4>
              <p>Sócia-fundadora | Martins Design</p>
            </div>
          </div>
          
          <div className="testimonial-card">
            <div className="testimonial-content">
              <p>
                "Como startup, não tínhamos orçamento para um departamento jurídico.
                O JuSimples nos permite ter acesso a ferramentas jurídicas de qualidade
                a um custo acessível. Recomendo fortemente."
              </p>
            </div>
            <div className="testimonial-author">
              <h4>Rodrigo Almeida</h4>
              <p>CEO | TechSolutions</p>
            </div>
          </div>
          
          <div className="testimonial-card">
            <div className="testimonial-content">
              <p>
                "Nossos contratos de prestação de serviços eram um pesadelo antes do JuSimples.
                Agora, temos um processo padronizado e seguro que nos poupa horas de trabalho por semana."
              </p>
            </div>
            <div className="testimonial-author">
              <h4>Carolina Santos</h4>
              <p>Administradora | CS Consultoria</p>
            </div>
          </div>
        </div>
      </section>

      <section className="plans-section">
        <h2 className="section-title">Planos para Empresas</h2>
        <div className="plans-grid">
          <div className="plan-card">
            <div className="plan-header">
              <h3>Básico</h3>
              <div className="plan-price">
                <span className="amount">R$99</span>
                <span className="period">/mês</span>
              </div>
            </div>
            <div className="plan-features">
              <ul>
                <li>5 documentos automáticos por mês</li>
                <li>Acesso à biblioteca de modelos básicos</li>
                <li>Consultas ilimitadas via IA</li>
                <li>1 usuário</li>
              </ul>
            </div>
            <Link to="/register?plan=business-basic" className="btn btn-outline-primary btn-block">
              Selecionar Plano
            </Link>
          </div>
          
          <div className="plan-card featured-plan">
            <div className="plan-badge">Mais Popular</div>
            <div className="plan-header">
              <h3>Profissional</h3>
              <div className="plan-price">
                <span className="amount">R$249</span>
                <span className="period">/mês</span>
              </div>
            </div>
            <div className="plan-features">
              <ul>
                <li>Documentos automáticos ilimitados</li>
                <li>Acesso completo à biblioteca de modelos</li>
                <li>Assinatura digital (até 10 por mês)</li>
                <li>Consultas ilimitadas via IA</li>
                <li>1 consulta mensal com advogado</li>
                <li>Até 3 usuários</li>
              </ul>
            </div>
            <Link to="/register?plan=business-pro" className="btn btn-primary btn-block">
              Selecionar Plano
            </Link>
          </div>
          
          <div className="plan-card">
            <div className="plan-header">
              <h3>Empresarial</h3>
              <div className="plan-price">
                <span className="amount">R$499</span>
                <span className="period">/mês</span>
              </div>
            </div>
            <div className="plan-features">
              <ul>
                <li>Tudo do plano Profissional</li>
                <li>Personalização de modelos</li>
                <li>Assinatura digital ilimitada</li>
                <li>4 consultas mensais com advogado</li>
                <li>Até 10 usuários</li>
                <li>Suporte prioritário</li>
              </ul>
            </div>
            <Link to="/register?plan=business-enterprise" className="btn btn-outline-primary btn-block">
              Selecionar Plano
            </Link>
          </div>
        </div>
        <div className="plan-note">
          <p>
            * Planos anuais com 20% de desconto disponíveis.
            Para empresas com mais de 10 usuários, entre em contato para um plano personalizado.
          </p>
        </div>
      </section>

      <section className="faq-section">
        <h2 className="section-title">Perguntas Frequentes</h2>
        <div className="faq-grid">
          <div 
            className={`faq-item ${activeFaq === 0 ? 'active' : ''}`}
            onClick={() => toggleFaq(0)}
          >
            <h3>Os documentos gerados têm validade jurídica?</h3>
            {activeFaq === 0 && (
              <p>
                Sim. Todos os nossos modelos são desenvolvidos por advogados especializados
                e estão em conformidade com a legislação brasileira vigente. Quando assinados
                adequadamente, possuem plena validade jurídica.
              </p>
            )}
          </div>
          
          <div 
            className={`faq-item ${activeFaq === 1 ? 'active' : ''}`}
            onClick={() => toggleFaq(1)}
          >
            <h3>Posso personalizar os modelos para minha empresa?</h3>
            {activeFaq === 1 && (
              <p>
                Sim. Nossos modelos são automaticamente personalizados com base nas informações
                que você fornece. Nos planos Empresarial, também oferecemos personalização
                adicional para incluir cláusulas específicas do seu negócio.
              </p>
            )}
          </div>
          
          <div 
            className={`faq-item ${activeFaq === 2 ? 'active' : ''}`}
            onClick={() => toggleFaq(2)}
          >
            <h3>Como funciona a consulta com advogados?</h3>
            {activeFaq === 2 && (
              <p>
                Dependendo do seu plano, você tem direito a consultas mensais com advogados
                especializados. Basta agendar um horário pela plataforma e realizar a consulta
                por videochamada ou telefone.
              </p>
            )}
          </div>
          
          <div 
            className={`faq-item ${activeFaq === 3 ? 'active' : ''}`}
            onClick={() => toggleFaq(3)}
          >
            <h3>Posso cancelar meu plano a qualquer momento?</h3>
            {activeFaq === 3 && (
              <p>
                Sim. Não trabalhamos com fidelidade. Você pode cancelar seu plano a qualquer
                momento, sem multas. O acesso permanecerá ativo até o final do período já pago.
              </p>
            )}
          </div>
        </div>
        <div className="faq-cta">
          <Link to="/faq?section=empresas" className="btn btn-outline-secondary">
            Ver Mais Perguntas
          </Link>
        </div>
      </section>

      <section className="cta-section">
        <div className="cta-container">
          <h2>Pronto para simplificar o jurídico da sua empresa?</h2>
          <p>
            Junte-se a milhares de pequenas empresas que já utilizam o JuSimples para
            economizar tempo e recursos com questões jurídicas.
          </p>
          <div className="cta-buttons">
            <Link to="/register?type=business" className="btn btn-primary btn-lg">
              Começar Agora
            </Link>
            <Link to="/contato" className="btn btn-outline-secondary btn-lg">
              Falar com um Consultor
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
