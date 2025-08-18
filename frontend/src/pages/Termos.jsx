import React from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import HeroImage from '../components/HeroImage';

export default function Termos() {
  // Use theme for conditional styling if needed
  const { theme } = useTheme();
  // Apply theme-specific class
  const pageThemeClass = `terms-page-${theme}`;

  return (
    <div className={`page-container terms-page ${pageThemeClass}`}>
      <div className="hero-section">
        <HeroImage type="termos" className="hero-background" />
        <h1 className="page-title">Termos de Uso</h1>
        <div className="divider"></div>
        <p className="hero-description">
          Condições gerais para utilização da plataforma JuSimples
        </p>
      </div>

      <div className="terms-content">
        <div className="terms-effective-date">
          <strong>Última atualização:</strong> 15 de Julho de 2024
        </div>

        <section className="terms-section">
          <h2>1. Aceitação dos Termos</h2>
          <p>
            Ao acessar ou utilizar a plataforma JuSimples, incluindo nosso site, aplicativo móvel e todos os 
            serviços relacionados (coletivamente, a "Plataforma"), você concorda em ficar vinculado a estes 
            Termos de Uso ("Termos"). Se você não concordar com estes Termos, não deverá acessar ou utilizar 
            a Plataforma.
          </p>
          <p>
            Estes Termos constituem um acordo legal entre você e JuSimples Tecnologia Ltda. ("JuSimples", "nós", 
            "nos" ou "nosso"). A Plataforma é de propriedade e operada pela JuSimples.
          </p>
        </section>

        <section className="terms-section">
          <h2>2. Alterações aos Termos</h2>
          <p>
            Reservamo-nos o direito de modificar estes Termos a qualquer momento, a nosso critério exclusivo. 
            Se fizermos alterações, notificaremos você publicando os Termos atualizados na Plataforma e 
            atualizando a data da "Última atualização" no topo deste documento. Seu uso continuado da Plataforma 
            após tais alterações constitui sua aceitação dos Termos modificados.
          </p>
          <p>
            É sua responsabilidade revisar periodicamente estes Termos para se manter informado sobre quaisquer 
            atualizações.
          </p>
        </section>

        <section className="terms-section">
          <h2>3. Elegibilidade</h2>
          <p>
            Para utilizar a Plataforma, você deve ter pelo menos 18 anos de idade ou a idade legal de maioridade 
            em sua jurisdição, o que for maior. Ao utilizar a Plataforma, você representa e garante que atende 
            a todos os requisitos de elegibilidade.
          </p>
        </section>

        <section className="terms-section">
          <h2>4. Cadastro e Conta</h2>
          <p>
            Para acessar determinados recursos da Plataforma, você precisará criar uma conta. Ao se cadastrar, 
            você concorda em fornecer informações precisas, atuais e completas, e em manter essas informações 
            atualizadas.
          </p>
          <p>
            Você é responsável por manter a confidencialidade de sua senha e por todas as atividades que ocorrem 
            em sua conta. Você concorda em notificar imediatamente a JuSimples sobre qualquer uso não autorizado 
            de sua conta ou qualquer outra violação de segurança.
          </p>
          <p>
            Reservamo-nos o direito de suspender ou encerrar sua conta a qualquer momento, por qualquer motivo, 
            sem aviso prévio ou responsabilidade.
          </p>
        </section>

        <section className="terms-section">
          <h2>5. Serviços da Plataforma</h2>
          <p>
            A JuSimples oferece uma plataforma baseada em tecnologia que fornece:
          </p>
          <ul>
            <li>
              <strong>Informações jurídicas:</strong> Conteúdo educacional sobre questões jurídicas comuns.
            </li>
            <li>
              <strong>Automação de documentos:</strong> Ferramentas para criar documentos jurídicos com base em 
              modelos pré-aprovados.
            </li>
            <li>
              <strong>Assistência baseada em IA:</strong> Respostas a perguntas jurídicas usando inteligência artificial.
            </li>
            <li>
              <strong>Conexão com advogados:</strong> Para casos que requerem assistência jurídica profissional.
            </li>
          </ul>
          <p>
            <strong>Importante:</strong> A JuSimples não presta serviços jurídicos e não substitui o aconselhamento 
            de um advogado qualificado. Nossa Plataforma é uma ferramenta de tecnologia projetada para facilitar 
            o acesso a informações jurídicas e automatizar certos processos, mas não constitui representação legal.
          </p>
        </section>

        <section className="terms-section">
          <h2>6. Limitações dos Serviços de IA</h2>
          <p>
            Nossa Plataforma utiliza tecnologias de inteligência artificial para fornecer informações e 
            orientações. Você reconhece e concorda que:
          </p>
          <ul>
            <li>As respostas geradas por IA são baseadas em padrões identificados em dados de treinamento e na 
              legislação vigente até a data de atualização de nossos sistemas;</li>
            <li>A tecnologia de IA tem limitações e pode não considerar todas as nuances de sua situação específica;</li>
            <li>As informações fornecidas pela IA são de natureza geral e informativa, não constituindo aconselhamento 
              jurídico personalizado;</li>
            <li>Em situações complexas ou de alto risco, você deve sempre consultar um profissional jurídico qualificado.</li>
          </ul>
        </section>

        <section className="terms-section">
          <h2>7. Responsabilidades do Usuário</h2>
          <p>
            Ao utilizar a Plataforma, você concorda em:
          </p>
          <ul>
            <li>Fornecer informações precisas e completas;</li>
            <li>Utilizar a Plataforma apenas para fins legais e de acordo com estes Termos;</li>
            <li>Não utilizar a Plataforma de maneira que possa prejudicar, desativar, sobrecarregar ou comprometer 
              os sistemas da JuSimples;</li>
            <li>Não tentar acessar áreas restritas da Plataforma;</li>
            <li>Não utilizar a Plataforma para enviar material ilegal, prejudicial, ameaçador, abusivo, difamatório, 
              vulgar ou de qualquer forma censurável;</li>
            <li>Não utilizar a Plataforma para distribuir vírus ou outros códigos maliciosos;</li>
            <li>Não utilizar a Plataforma para violar direitos de propriedade intelectual de terceiros;</li>
            <li>Utilizar seu próprio discernimento ao avaliar as informações fornecidas pela Plataforma.</li>
          </ul>
        </section>

        <section className="terms-section">
          <h2>8. Propriedade Intelectual</h2>
          <p>
            Todo o conteúdo, recursos e funcionalidades da Plataforma, incluindo, mas não se limitando a texto, 
            gráficos, logotipos, ícones, imagens, clipes de áudio, downloads digitais, compilações de dados e 
            software, são propriedade da JuSimples, de seus licenciadores ou de outros provedores de conteúdo, 
            e são protegidos por leis de direitos autorais, marcas registradas e outras leis de propriedade 
            intelectual do Brasil e de outros países.
          </p>
          <p>
            Você não pode reproduzir, distribuir, modificar, criar trabalhos derivados, exibir publicamente, 
            executar publicamente, republicar, baixar, armazenar ou transmitir qualquer material da Plataforma, 
            exceto conforme expressamente permitido por estes Termos ou com nosso consentimento prévio por escrito.
          </p>
        </section>

        <section className="terms-section">
          <h2>9. Conteúdo do Usuário</h2>
          <p>
            A Plataforma pode permitir que você envie, poste, armazene ou compartilhe conteúdo, incluindo 
            informações pessoais, documentos, perguntas e outros materiais (coletivamente, "Conteúdo do Usuário").
          </p>
          <p>
            Ao fornecer Conteúdo do Usuário para a Plataforma, você mantém seus direitos de propriedade, mas 
            concede à JuSimples uma licença mundial, não exclusiva, isenta de royalties, sublicenciável e 
            transferível para usar, reproduzir, modificar, adaptar, publicar, traduzir, criar trabalhos derivados, 
            distribuir e exibir esse Conteúdo do Usuário em conexão com a operação e fornecimento da Plataforma.
          </p>
          <p>
            Você representa e garante que:
          </p>
          <ul>
            <li>Você possui ou tem os direitos necessários para fornecer qualquer Conteúdo do Usuário que você 
              envia à Plataforma;</li>
            <li>Seu Conteúdo do Usuário não viola os direitos de privacidade, direitos de publicidade, direitos 
              autorais, direitos contratuais ou quaisquer outros direitos de qualquer pessoa.</li>
          </ul>
        </section>

        <section className="terms-section">
          <h2>10. Isenções de Responsabilidade</h2>
          <p>
            A PLATAFORMA E TODO O SEU CONTEÚDO SÃO FORNECIDOS "COMO ESTÃO", SEM GARANTIAS DE QUALQUER TIPO, 
            EXPRESSAS OU IMPLÍCITAS. A JUSIMPLES RENUNCIA EXPRESSAMENTE A TODAS AS GARANTIAS DE QUALQUER TIPO, 
            SEJAM EXPRESSAS OU IMPLÍCITAS, INCLUINDO, MAS NÃO SE LIMITANDO A, GARANTIAS IMPLÍCITAS DE 
            COMERCIALIZAÇÃO, ADEQUAÇÃO A UM DETERMINADO FIM E NÃO VIOLAÇÃO.
          </p>
          <p>
            A JUSIMPLES NÃO GARANTE QUE A PLATAFORMA ATENDA AOS SEUS REQUISITOS, OU QUE A OPERAÇÃO DA 
            PLATAFORMA SERÁ ININTERRUPTA, SEGURA OU LIVRE DE ERROS. VOCÊ ASSUME TODO O RISCO PELO USO DA 
            PLATAFORMA.
          </p>
          <p>
            VOCÊ RECONHECE E CONCORDA EXPRESSAMENTE QUE:
          </p>
          <ol>
            <li>A JUSIMPLES NÃO É UM ESCRITÓRIO DE ADVOCACIA E NÃO PRESTA SERVIÇOS JURÍDICOS;</li>
            <li>A PLATAFORMA NÃO SUBSTITUI O ACONSELHAMENTO JURÍDICO PROFISSIONAL;</li>
            <li>AS INFORMAÇÕES FORNECIDAS ATRAVÉS DA PLATAFORMA SÃO DE NATUREZA GERAL E PODEM NÃO 
              SER APLICÁVEIS À SUA SITUAÇÃO ESPECÍFICA;</li>
            <li>A JUSIMPLES NÃO É RESPONSÁVEL POR QUAISQUER DECISÕES QUE VOCÊ TOME COM BASE NAS 
              INFORMAÇÕES OBTIDAS ATRAVÉS DA PLATAFORMA.</li>
          </ol>
        </section>

        <section className="terms-section">
          <h2>11. Limitação de Responsabilidade</h2>
          <p>
            EM NENHUMA CIRCUNSTÂNCIA A JUSIMPLES, SEUS DIRETORES, FUNCIONÁRIOS, AGENTES, PARCEIROS 
            OU FORNECEDORES SERÃO RESPONSÁVEIS POR QUAISQUER DANOS DIRETOS, INDIRETOS, INCIDENTAIS, 
            ESPECIAIS, EXEMPLARES, PUNITIVOS, CONSEQUENCIAIS OU OUTROS (INCLUINDO, MAS NÃO SE LIMITANDO 
            A, DANOS POR PERDA DE LUCROS, PERDA DE DADOS OU OUTRAS PERDAS INTANGÍVEIS) DECORRENTES DE 
            OU RELACIONADOS AO SEU USO DA PLATAFORMA, MESMO SE A JUSIMPLES TIVER SIDO AVISADA DA 
            POSSIBILIDADE DE TAIS DANOS.
          </p>
        </section>

        <section className="terms-section">
          <h2>12. Indenização</h2>
          <p>
            Você concorda em indenizar, defender e isentar a JuSimples, suas afiliadas, licenciadores 
            e prestadores de serviços, bem como seus respectivos diretores, funcionários, contratados, 
            agentes, licenciadores, fornecedores, sucessores e cessionários de e contra quaisquer 
            reclamações, responsabilidades, danos, julgamentos, prêmios, perdas, custos, despesas ou 
            honorários (incluindo honorários advocatícios razoáveis) decorrentes de ou relacionados 
            à sua violação destes Termos ou ao seu uso da Plataforma.
          </p>
        </section>

        <section className="terms-section">
          <h2>13. Lei Aplicável e Resolução de Disputas</h2>
          <p>
            Estes Termos serão regidos e interpretados de acordo com as leis do Brasil, sem consideração 
            aos princípios de conflitos de leis.
          </p>
          <p>
            Qualquer ação legal ou procedimento relacionado a estes Termos ou à Plataforma será resolvido 
            exclusivamente nos tribunais estaduais e federais localizados em São Paulo, SP, e você consente 
            com a jurisdição e foro desses tribunais.
          </p>
        </section>

        <section className="terms-section">
          <h2>14. Disposições Gerais</h2>
          <p>
            Estes Termos constituem o acordo integral entre você e a JuSimples a respeito do uso da Plataforma.
          </p>
          <p>
            Se qualquer disposição destes Termos for considerada inválida, ilegal ou inexequível, tal 
            disposição será limitada ou eliminada na medida mínima necessária para que as demais disposições 
            destes Termos permaneçam em pleno vigor e efeito.
          </p>
          <p>
            Nossa falha em exercer ou fazer cumprir qualquer direito ou disposição destes Termos não 
            constituirá uma renúncia a tal direito ou disposição.
          </p>
        </section>

        <section className="terms-section">
          <h2>15. Contato</h2>
          <p>
            Se você tiver alguma dúvida sobre estes Termos, entre em contato conosco em:
          </p>
          <div className="contact-info">
            <p><strong>E-mail:</strong> <a href="mailto:termos@jusimples.com">termos@jusimples.com</a></p>
            <p><strong>Endereço:</strong> Av. Paulista, 1000, São Paulo - SP, CEP 01310-100</p>
            <p><strong>Telefone:</strong> (11) 3000-0000</p>
          </div>
        </section>

        <div className="terms-footer">
          <p>
            Ao utilizar nossa Plataforma, você concorda com estes Termos de Uso.
          </p>
          <div className="related-links">
            <Link to="/privacidade">Política de Privacidade</Link>
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
