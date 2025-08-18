import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import HeroImage from '../components/HeroImage';

export default function Consumidores() {
  // Use theme for conditional styling if needed
  const { theme } = useTheme();
  // Apply theme-specific class
  const pageThemeClass = `consumers-page-${theme}`;

  // State for FAQ accordion
  const [activeFaq, setActiveFaq] = useState(null);

  // Toggle FAQ item
  const toggleFaq = (index) => {
    setActiveFaq(activeFaq === index ? null : index);
  };
  
  return (
    <div className={`page-container consumers-page ${pageThemeClass}`}>
      <div className="hero-section">
        <HeroImage type="consumidores" className="hero-background" />
        <h1 className="page-title">JuSimples para Consumidores</h1>
        <div className="divider"></div>
        <p className="hero-description">
          Proteja seus direitos como consumidor de forma rápida e eficiente
        </p>
        <div className="cta-buttons">
          <Link to="/register" className="btn btn-primary btn-lg">
            Comece Gratuitamente
          </Link>
          <a href="#como-funciona" className="btn btn-secondary btn-lg">
            Saiba Como Funciona
          </a>
        </div>
      </div>

      <section className="features-section">
        <h2 className="section-title">Como a JuSimples pode te ajudar</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">
              <span className="icon-lg">🛡️</span>
            </div>
            <h3>Defesa do Consumidor</h3>
            <p>
              Respostas rápidas para problemas com produtos e serviços. Saiba seus direitos e como
              fazer valer o código de defesa do consumidor de forma prática.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <span className="icon-lg">📜</span>
            </div>
            <h3>Documentos Automáticos</h3>
            <p>
              Gere cartas de reclamação, notificações extrajudiciais e outros documentos em questão de
              minutos, com base na legislação atual.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <span className="icon-lg">⚖️</span>
            </div>
            <h3>Orientação Jurídica</h3>
            <p>
              Tire suas dúvidas sobre situações de consumo e receba orientações precisas sobre os
              melhores caminhos para resolver seu problema.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <span className="icon-lg">💬</span>
            </div>
            <h3>Mediação de Conflitos</h3>
            <p>
              Facilitamos a comunicação com empresas para resolver problemas sem a necessidade de
              processos judiciais demorados.
            </p>
          </div>
        </div>
      </section>

      <section id="como-funciona" className="how-it-works-section">
        <h2 className="section-title">Como Funciona</h2>
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <div className="step-content">
              <h3>Cadastre-se</h3>
              <p>
                Crie sua conta gratuita na plataforma JuSimples em menos de 2 minutos.
              </p>
            </div>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <div className="step-content">
              <h3>Descreva seu problema</h3>
              <p>
                Conte-nos o que aconteceu. Nossa IA analisará seu caso e identificará as
                leis aplicáveis à sua situação.
              </p>
            </div>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <div className="step-content">
              <h3>Receba orientação</h3>
              <p>
                Obtenha orientações personalizadas sobre seus direitos e as opções
                disponíveis para resolver seu problema.
              </p>
            </div>
          </div>
          <div className="step">
            <div className="step-number">4</div>
            <div className="step-content">
              <h3>Tome providências</h3>
              <p>
                Utilize nossos modelos de documentos ou, se necessário, conecte-se com um
                advogado parceiro especializado em direito do consumidor.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="cases-section">
        <h2 className="section-title">Como ajudamos consumidores</h2>
        <div className="cases-grid">
          <div className="case-card">
            <h3>Problemas com compras online</h3>
            <p>
              "Comprei um produto que nunca foi entregue. A JuSimples me ajudou a elaborar uma
              notificação formal que resolveu meu problema em 48 horas."
            </p>
            <p className="case-author">— Maria S., São Paulo</p>
          </div>
          <div className="case-card">
            <h3>Cancelamento de serviços</h3>
            <p>
              "Tentei cancelar meu plano de TV por assinatura por meses sem sucesso. Com a
              orientação da JuSimples, consegui finalizar o cancelamento e receber reembolso
              das cobranças indevidas."
            </p>
            <p className="case-author">— João P., Rio de Janeiro</p>
          </div>
          <div className="case-card">
            <h3>Produto com defeito</h3>
            <p>
              "Meu notebook apresentou defeito dentro da garantia, mas a loja se recusava a
              trocar. A JuSimples me orientou sobre meus direitos e me ajudou a redigir um
              documento formal que resultou na substituição do produto."
            </p>
            <p className="case-author">— Carlos M., Belo Horizonte</p>
          </div>
          <div className="case-card">
            <h3>Cobrança indevida</h3>
            <p>
              "Recebi cobranças de um serviço que nunca contratei. Com a ajuda da JuSimples,
              consegui provar que nunca autorizei o serviço e obtive o cancelamento da cobrança
              com devolução em dobro dos valores."
            </p>
            <p className="case-author">— Ana L., Salvador</p>
          </div>
        </div>
      </section>

      <section className="common-issues-section">
        <h2 className="section-title">Problemas comuns que resolvemos</h2>
        <div className="issues-list">
          <ul>
            <li>Produtos com defeito ou não entregues</li>
            <li>Cobranças indevidas ou abusivas</li>
            <li>Cancelamento de serviços</li>
            <li>Problemas com garantia</li>
            <li>Publicidade enganosa</li>
            <li>Serviços não prestados conforme contratado</li>
            <li>Cláusulas abusivas em contratos</li>
            <li>Problemas com transporte aéreo (cancelamentos, atrasos)</li>
            <li>Dificuldades com seguro e planos de saúde</li>
            <li>Questões bancárias e financeiras</li>
          </ul>
        </div>
      </section>

      <section className="pricing-section">
        <h2 className="section-title">Planos e Preços</h2>
        <div className="pricing-cards">
          <div className="pricing-card">
            <div className="pricing-header">
              <h3>Básico</h3>
              <div className="price">Grátis</div>
            </div>
            <div className="pricing-features">
              <ul>
                <li>Consulta a informações legais</li>
                <li>1 documento automático por mês</li>
                <li>Acesso à base de conhecimento</li>
                <li>Avaliação inicial do caso</li>
              </ul>
            </div>
            <Link to="/register" className="btn btn-outline-primary btn-block">
              Começar Grátis
            </Link>
          </div>
          <div className="pricing-card popular">
            <div className="popular-tag">Mais popular</div>
            <div className="pricing-header">
              <h3>Premium</h3>
              <div className="price">R$29,90<span>/mês</span></div>
            </div>
            <div className="pricing-features">
              <ul>
                <li>Tudo do plano Básico</li>
                <li>Documentos automáticos ilimitados</li>
                <li>Análise detalhada do caso</li>
                <li>Modelos avançados de petições</li>
                <li>Suporte por chat</li>
              </ul>
            </div>
            <Link to="/register?plan=premium" className="btn btn-primary btn-block">
              Assinar Premium
            </Link>
          </div>
          <div className="pricing-card">
            <div className="pricing-header">
              <h3>Completo</h3>
              <div className="price">R$79,90<span>/mês</span></div>
            </div>
            <div className="pricing-features">
              <ul>
                <li>Tudo do plano Premium</li>
                <li>Consulta com advogado (1x por mês)</li>
                <li>Revisão de documentos por especialistas</li>
                <li>Mediação de conflitos</li>
                <li>Suporte prioritário 24/7</li>
              </ul>
            </div>
            <Link to="/register?plan=completo" className="btn btn-outline-primary btn-block">
              Assinar Completo
            </Link>
          </div>
        </div>
      </section>

      <section className="faq-section">
        <h2 className="section-title">Perguntas Frequentes</h2>
        <div className="faq-content">
          <div 
            className={`faq-item ${activeFaq === 0 ? 'active' : ''}`}
            onClick={() => toggleFaq(0)}
          >
            <h3>A JuSimples substitui um advogado?</h3>
            {activeFaq === 0 && (
              <p>
                Não. A JuSimples é uma ferramenta tecnológica que facilita o acesso à informação
                jurídica e automatiza a geração de documentos. Para casos complexos, recomendamos
                consultar um advogado especializado, e podemos ajudar a conectar você a um dos
                nossos parceiros.
              </p>
            )}
          </div>
          <div 
            className={`faq-item ${activeFaq === 1 ? 'active' : ''}`}
            onClick={() => toggleFaq(1)}
          >
            <h3>Quanto tempo leva para resolver meu problema?</h3>
            {activeFaq === 1 && (
              <p>
                O tempo varia de acordo com a complexidade do caso. Problemas simples podem ser
                resolvidos em dias, enquanto situações mais complexas podem levar semanas. Nossa
                plataforma visa acelerar esse processo ao fornecer as ferramentas e informações
                necessárias imediatamente.
              </p>
            )}
          </div>
          <div 
            className={`faq-item ${activeFaq === 2 ? 'active' : ''}`}
            onClick={() => toggleFaq(2)}
          >
            <h3>Os documentos gerados pela JuSimples têm validade jurídica?</h3>
            {activeFaq === 2 && (
              <p>
                Sim. Todos os nossos modelos são desenvolvidos por especialistas em direito do
                consumidor e seguem a legislação brasileira atual. Os documentos gerados podem ser
                utilizados em procedimentos administrativos e judiciais.
              </p>
            )}
          </div>
          <div 
            className={`faq-item ${activeFaq === 3 ? 'active' : ''}`}
            onClick={() => toggleFaq(3)}
          >
            <h3>Preciso pagar para utilizar a plataforma?</h3>
            {activeFaq === 3 && (
              <p>
                Oferecemos um plano básico gratuito com recursos limitados. Para acesso completo,
                temos planos pagos com valores acessíveis. Consulte nossa seção de preços para
                mais detalhes.
              </p>
            )}
          </div>
        </div>
        <div className="faq-more">
          <Link to="/faq" className="btn btn-outline-secondary">
            Ver Todas as Perguntas Frequentes
          </Link>
        </div>
      </section>

      <section className="cta-section">
        <div className="cta-content">
          <h2>Pronto para defender seus direitos como consumidor?</h2>
          <p>
            Junte-se a milhares de brasileiros que já resolveram seus problemas de consumo
            com a ajuda da JuSimples.
          </p>
          <div className="cta-buttons">
            <Link to="/register" className="btn btn-primary btn-lg">
              Criar Conta Gratuitamente
            </Link>
            <Link to="/contato" className="btn btn-outline-secondary btn-lg">
              Fale Conosco
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
