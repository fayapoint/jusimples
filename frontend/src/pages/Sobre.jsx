import React from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import HeroImage from '../components/HeroImage';

export default function Sobre() {
  // Use theme for conditional styling if needed
  const { theme } = useTheme();
  // Apply theme-specific class
  const pageThemeClass = `about-page-${theme}`;

  return (
    <div className={`page-container about-page ${pageThemeClass}`}>
      <div className="hero-section">
        <HeroImage type="sobre" className="hero-background" />
        <h1 className="page-title">Sobre o JuSimples</h1>
        <div className="divider"></div>
        <p className="hero-description">
          Conheça nossa missão, visão e história por trás da revolução no acesso à justiça brasileira
        </p>
      </div>

      <div className="about-content">
        <section className="about-section">
          <h2>Nossa Missão</h2>
          <p>
            O JuSimples nasceu com uma missão clara: democratizar o acesso à justiça no Brasil, 
            simplificando processos jurídicos e tornando-os acessíveis para todos os cidadãos e 
            pequenas empresas, independentemente de seu conhecimento jurídico prévio ou recursos financeiros.
          </p>
          <p>
            Acreditamos que o acesso à justiça é um direito fundamental e que a tecnologia pode 
            ser uma aliada poderosa na quebra de barreiras que historicamente dificultaram esse acesso.
          </p>
        </section>

        <section className="about-section">
          <h2>Nossa História</h2>
          <p>
            Fundada em 2023 por um grupo de profissionais do direito e tecnologia, a JuSimples 
            surgiu da frustração comum com a complexidade desnecessária e os altos custos dos 
            processos jurídicos no Brasil.
          </p>
          <p>
            Nossos fundadores perceberam que, enquanto a tecnologia avançava rapidamente em 
            outros setores, o campo jurídico permanecia preso a práticas antiquadas e ineficientes. 
            Era hora de uma mudança.
          </p>
          <div className="timeline">
            <div className="timeline-item">
              <div className="timeline-marker"></div>
              <div className="timeline-content">
                <h4>2023</h4>
                <p>Fundação da JuSimples com foco em assistência jurídica para consumidores</p>
              </div>
            </div>
            <div className="timeline-item">
              <div className="timeline-marker"></div>
              <div className="timeline-content">
                <h4>2024</h4>
                <p>Lançamento da plataforma de IA para automação de documentos e consultas jurídicas</p>
              </div>
            </div>
            <div className="timeline-item">
              <div className="timeline-marker"></div>
              <div className="timeline-content">
                <h4>2025</h4>
                <p>Expansão para soluções corporativas e parcerias com escritórios de advocacia</p>
              </div>
            </div>
          </div>
        </section>

        <section className="about-section">
          <h2>Nossa Abordagem</h2>
          <div className="approach-cards">
            <div className="approach-card">
              <div className="approach-icon">🤖</div>
              <h3>Inteligência Artificial</h3>
              <p>
                Utilizamos tecnologia de ponta em IA para analisar documentos, identificar precedentes 
                relevantes e oferecer orientações jurídicas precisas com base na legislação brasileira.
              </p>
            </div>
            <div className="approach-card">
              <div className="approach-icon">📝</div>
              <h3>Automação de Documentos</h3>
              <p>
                Nossa plataforma permite a criação automatizada de documentos jurídicos personalizados, 
                eliminando erros e reduzindo drasticamente o tempo necessário para sua elaboração.
              </p>
            </div>
            <div className="approach-card">
              <div className="approach-icon">🤝</div>
              <h3>Rede de Profissionais</h3>
              <p>
                Para casos que exigem intervenção humana, conectamos os usuários a uma rede de 
                advogados qualificados e pré-selecionados, garantindo atendimento de qualidade.
              </p>
            </div>
          </div>
        </section>

        <section className="about-section">
          <h2>Nossos Valores</h2>
          <div className="values-list">
            <div className="value-item">
              <h3>Acessibilidade</h3>
              <p>
                Comprometemo-nos a tornar o conhecimento e serviços jurídicos acessíveis a todos, 
                independentemente de sua condição socioeconômica.
              </p>
            </div>
            <div className="value-item">
              <h3>Transparência</h3>
              <p>
                Acreditamos em comunicação clara sobre processos, custos e expectativas, sem 
                linguagem obscura ou termos complexos desnecessários.
              </p>
            </div>
            <div className="value-item">
              <h3>Inovação</h3>
              <p>
                Buscamos constantemente novas tecnologias e abordagens para melhorar a 
                experiência jurídica e torná-la mais eficiente.
              </p>
            </div>
            <div className="value-item">
              <h3>Qualidade</h3>
              <p>
                Comprometemo-nos com a excelência em todos os aspectos de nosso serviço, 
                desde a precisão das informações até a experiência do usuário.
              </p>
            </div>
          </div>
        </section>

        <section className="about-section team-section">
          <h2>Nossa Equipe</h2>
          <p>
            A JuSimples é composta por uma equipe multidisciplinar de profissionais apaixonados 
            por direito, tecnologia e impacto social. Reunimos advogados, desenvolvedores, 
            especialistas em IA, designers e profissionais de atendimento ao cliente para 
            oferecer a melhor experiência possível.
          </p>
        </section>

        <section className="about-section cta-section">
          <h2>Faça Parte da Revolução Jurídica</h2>
          <p>
            Estamos apenas no começo de nossa jornada para transformar o acesso à justiça no Brasil. 
            Junte-se a nós nessa missão!
          </p>
          <div className="cta-buttons">
            <Link to="/register" className="btn btn-primary">Crie sua conta</Link>
            <Link to="/contato" className="btn btn-secondary">Entre em contato</Link>
          </div>
        </section>
      </div>
    </div>
  );
}
