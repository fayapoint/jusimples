import React from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import HeroImage from '../components/HeroImage';

export default function Privacidade() {
  // Use theme for conditional styling if needed
  const { theme } = useTheme();
  // Apply theme-specific class
  const pageThemeClass = `privacy-page-${theme}`;

  return (
    <div className={`page-container privacy-page ${pageThemeClass}`}>
      <div className="hero-section">
        <HeroImage type="privacy" className="hero-background" />
        <h1 className="page-title">Política de Privacidade</h1>
        <div className="divider"></div>
        <p className="hero-description">
          Entenda como coletamos, utilizamos e protegemos suas informações pessoais
        </p>
      </div>

      <div className="privacy-content">
        <div className="privacy-effective-date">
          <strong>Última atualização:</strong> 15 de Julho de 2024
        </div>

        <section className="privacy-section">
          <h2>Introdução</h2>
          <p>
            A JuSimples ("nós", "nossos" ou "JuSimples") está comprometida em proteger sua privacidade. 
            Esta Política de Privacidade descreve como coletamos, usamos e compartilhamos informações sobre você 
            quando você utiliza nosso site, aplicativos e outros produtos e serviços online (coletivamente, os "Serviços"), 
            ou quando interage conosco de outra forma.
          </p>
          <p>
            Ao utilizar nossos Serviços, você concorda com a coleta e uso de informações de acordo com esta política. 
            Recomendamos que você leia este documento cuidadosamente para entender nossas práticas.
          </p>
        </section>

        <section className="privacy-section">
          <h2>Informações que Coletamos</h2>
          
          <h3>Informações fornecidas por você</h3>
          <p>
            Coletamos informações que você nos fornece diretamente quando utiliza nossos Serviços, incluindo:
          </p>
          <ul>
            <li>
              <strong>Informações de registro:</strong> Quando você cria uma conta, podemos coletar seu nome, 
              endereço de e-mail, número de telefone, CPF ou CNPJ, e outras informações necessárias para a 
              criação de sua conta.
            </li>
            <li>
              <strong>Informações de perfil:</strong> Podemos coletar informações adicionais que você optar 
              por adicionar ao seu perfil, como seu endereço, profissão e histórico profissional.
            </li>
            <li>
              <strong>Comunicações:</strong> Quando você se comunica conosco, coletamos o conteúdo de suas 
              mensagens, bem como qualquer informação adicional que você optar por fornecer.
            </li>
            <li>
              <strong>Informações de pagamento:</strong> Se você fizer uma compra, coletaremos informações 
              de pagamento, como detalhes do cartão de crédito ou informações da conta bancária. Note que as 
              informações completas de pagamento são processadas por nossos processadores de pagamento 
              terceirizados.
            </li>
          </ul>

          <h3>Informações coletadas automaticamente</h3>
          <p>
            Quando você acessa ou utiliza nossos Serviços, podemos coletar automaticamente:
          </p>
          <ul>
            <li>
              <strong>Informações de uso:</strong> Coletamos informações sobre como você utiliza nossos 
              Serviços, como as páginas que você visita, quanto tempo você passa em cada página, links 
              em que clica, e suas interações com recursos e funcionalidades.
            </li>
            <li>
              <strong>Informações do dispositivo:</strong> Coletamos informações sobre o dispositivo que 
              você utiliza para acessar nossos Serviços, incluindo modelo de hardware, sistema operacional, 
              navegador web, endereço IP, identificadores únicos de dispositivo e informações sobre rede móvel.
            </li>
            <li>
              <strong>Cookies e tecnologias similares:</strong> Utilizamos cookies e tecnologias similares 
              para coletar informações sobre sua atividade, navegador e dispositivo. Para mais informações 
              sobre como utilizamos cookies, consulte nossa Política de Cookies.
            </li>
          </ul>

          <h3>Informações de documentos e casos</h3>
          <p>
            Quando você utiliza nossos serviços para criar documentos jurídicos ou buscar orientação legal, 
            podemos coletar informações relacionadas à sua situação legal específica, documentos fornecidos 
            e detalhes dos casos.
          </p>
        </section>

        <section className="privacy-section">
          <h2>Como Utilizamos suas Informações</h2>
          <p>Utilizamos as informações que coletamos para:</p>
          <ul>
            <li>Fornecer, manter e melhorar nossos Serviços;</li>
            <li>Processar suas transações e gerenciar sua conta;</li>
            <li>Enviar informações técnicas, atualizações, alertas de segurança e mensagens de suporte;</li>
            <li>Responder a seus comentários, perguntas e solicitações;</li>
            <li>Comunicar-se com você sobre produtos, serviços, ofertas e eventos;</li>
            <li>Monitorar e analisar tendências, uso e atividades relacionadas aos nossos Serviços;</li>
            <li>Detectar, prevenir e abordar questões técnicas, fraudes ou atividades ilegais;</li>
            <li>Personalizar e melhorar sua experiência com nossos Serviços;</li>
            <li>Fornecer recomendações legais personalizadas através de nossa tecnologia de IA;</li>
            <li>Cumprir com obrigações legais e regulatórias.</li>
          </ul>
        </section>

        <section className="privacy-section">
          <h2>Compartilhamento de Informações</h2>
          <p>
            Podemos compartilhar informações sobre você nas seguintes circunstâncias:
          </p>
          <ul>
            <li>
              <strong>Com prestadores de serviços:</strong> Compartilhamos informações com prestadores 
              de serviços terceirizados que realizam serviços em nosso nome, como processamento de 
              pagamentos, análise de dados, entrega de e-mail, hospedagem e serviços de atendimento ao cliente.
            </li>
            <li>
              <strong>Com advogados parceiros:</strong> Se você optar por ser conectado a um advogado 
              através de nossa plataforma, compartilharemos as informações necessárias para facilitar 
              essa conexão e a prestação de serviços jurídicos.
            </li>
            <li>
              <strong>Para conformidade legal:</strong> Podemos divulgar suas informações quando 
              acreditarmos de boa fé que a divulgação é necessária para cumprir com uma obrigação legal, 
              ordem judicial, ou para proteger os direitos, propriedades ou segurança nossa, de nossos 
              usuários ou do público.
            </li>
            <li>
              <strong>Em caso de transferência de negócios:</strong> Se estivermos envolvidos em uma 
              fusão, aquisição, ou venda de todos ou uma parte de nossos ativos, suas informações 
              podem ser transferidas como parte dessa transação.
            </li>
          </ul>
          <p>
            Não vendemos suas informações pessoais a terceiros para fins de marketing direto sem 
            seu consentimento explícito.
          </p>
        </section>

        <section className="privacy-section">
          <h2>Segurança dos Dados</h2>
          <p>
            A segurança de suas informações pessoais é importante para nós. Implementamos medidas 
            técnicas, administrativas e físicas projetadas para proteger suas informações contra 
            acesso não autorizado, uso indevido ou divulgação.
          </p>
          <p>
            No entanto, nenhum método de transmissão pela Internet ou método de armazenamento 
            eletrônico é 100% seguro. Embora nos esforcemos para proteger suas informações pessoais, 
            não podemos garantir sua segurança absoluta.
          </p>
        </section>

        <section className="privacy-section">
          <h2>Seus Direitos e Escolhas</h2>
          <p>
            De acordo com a Lei Geral de Proteção de Dados (LGPD) e outras leis aplicáveis, 
            você tem certos direitos em relação às suas informações pessoais, incluindo:
          </p>
          <ul>
            <li>
              <strong>Acesso:</strong> Você tem o direito de acessar as informações pessoais que 
              mantemos sobre você.
            </li>
            <li>
              <strong>Correção:</strong> Você tem o direito de solicitar a correção de informações 
              imprecisas ou incompletas que mantemos sobre você.
            </li>
            <li>
              <strong>Exclusão:</strong> Em determinadas circunstâncias, você tem o direito de 
              solicitar a exclusão de suas informações pessoais.
            </li>
            <li>
              <strong>Restrição de processamento:</strong> Em determinadas circunstâncias, você 
              tem o direito de solicitar que restrinjamos o processamento de suas informações pessoais.
            </li>
            <li>
              <strong>Portabilidade de dados:</strong> Você tem o direito de receber suas informações 
              pessoais em um formato estruturado, comumente usado e legível por máquina.
            </li>
            <li>
              <strong>Objeção:</strong> Você tem o direito de se opor ao processamento de suas 
              informações pessoais em determinadas circunstâncias.
            </li>
          </ul>
          <p>
            Para exercer qualquer um destes direitos, entre em contato conosco através do e-mail 
            <a href="mailto:privacidade@jusimples.com"> privacidade@jusimples.com</a> ou através dos 
            canais de contato fornecidos abaixo.
          </p>
        </section>

        <section className="privacy-section">
          <h2>Alterações a esta Política</h2>
          <p>
            Podemos atualizar esta Política de Privacidade periodicamente para refletir mudanças 
            em nossas práticas ou por outros motivos operacionais, legais ou regulatórios. 
            Notificaremos você sobre quaisquer alterações materiais publicando a nova Política de 
            Privacidade em nosso site e, quando apropriado, enviando um aviso diretamente a você.
          </p>
          <p>
            Recomendamos que você revise esta Política periodicamente para se manter informado 
            sobre como estamos protegendo suas informações.
          </p>
        </section>

        <section className="privacy-section">
          <h2>Contato</h2>
          <p>
            Se você tiver dúvidas sobre esta Política de Privacidade ou nossas práticas de privacidade, 
            entre em contato conosco em:
          </p>
          <div className="contact-info">
            <p><strong>E-mail:</strong> <a href="mailto:privacidade@jusimples.com">privacidade@jusimples.com</a></p>
            <p><strong>Endereço:</strong> Av. Paulista, 1000, São Paulo - SP, CEP 01310-100</p>
            <p><strong>Telefone:</strong> (11) 3000-0000</p>
          </div>
        </section>

        <div className="privacy-footer">
          <p>
            Ao utilizar nossos Serviços, você concorda com esta Política de Privacidade. 
            Se você não concordar com esta política, por favor, não utilize nossos Serviços.
          </p>
          <div className="related-links">
            <Link to="/termos">Termos de Uso</Link>
            <span className="separator">•</span>
            <Link to="/faq">Perguntas Frequentes</Link>
            <span className="separator">•</span>
            <Link to="/contato">Contato</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
