import React, { useState } from 'react';

export default function FAQ() {
  // Theme context removed as it was unused
  const [openQuestion, setOpenQuestion] = useState(null);

  const toggleQuestion = (index) => {
    if (openQuestion === index) {
      setOpenQuestion(null);
    } else {
      setOpenQuestion(index);
    }
  };

  const faqItems = [
    {
      question: "O que é o JuSimples e como ele pode me ajudar?",
      answer: "O JuSimples é uma plataforma online que utiliza inteligência artificial para simplificar demandas jurídicas de menor complexidade. Nossa IA foi treinada com a legislação brasileira e casos reais para fornecer orientações jurídicas precisas, gerar documentos e ajudar a resolver questões legais cotidianas de forma rápida e acessível, sem precisar usar linguagem jurídica complexa."
    },
    {
      question: "Eu posso usar o JuSimples sem um advogado?",
      answer: "Sim! O JuSimples foi desenvolvido justamente para ajudar em questões legais mais simples sem a necessidade de consultar um advogado. No entanto, para casos complexos ou que exijam representação legal, sempre recomendamos buscar orientação de um profissional habilitado. Inclusive, oferecemos uma rede de advogados parceiros que podem dar continuidade ao seu caso quando necessário."
    },
    {
      question: "Como funciona a criação de documentos?",
      answer: "Nossa plataforma gera documentos jurídicos personalizados com base nas informações que você fornece. Após responder algumas perguntas específicas sobre sua situação, o sistema utiliza modelos validados por especialistas para criar documentos prontos para uso, como notificações extrajudiciais, recursos administrativos, petições simples, contratos e muito mais. Tudo em português claro e compatível com as exigências legais brasileiras."
    },
    {
      question: "Preciso pagar pra usar o JuSimples?",
      answer: "O JuSimples possui um plano gratuito que permite consultas básicas e acesso limitado aos recursos da plataforma. Para funcionalidades avançadas, como geração de documentos ilimitada, armazenamento de casos e acesso à rede de advogados, oferecemos planos pagos acessíveis. Nosso objetivo é democratizar o acesso à justiça com opções que cabem no orçamento de todos."
    },
    {
      question: "Meus dados estão seguros no JuSimples?",
      answer: "Absolutamente! A segurança e privacidade dos seus dados são nossas prioridades máximas. Utilizamos criptografia avançada e seguimos rigorosamente a LGPD (Lei Geral de Proteção de Dados). Suas informações são utilizadas apenas para fornecer os serviços solicitados e nunca são compartilhadas com terceiros sem seu consentimento explícito. Todo nosso tratamento de dados está detalhado em nossa Política de Privacidade."
    },
    {
      question: "A orientação do JuSimples tem validade legal?",
      answer: "O JuSimples fornece orientações baseadas na legislação brasileira vigente e jurisprudência relevante. Embora nossas recomendações sejam fundamentadas e os documentos gerados sigam os requisitos legais, é importante entender que a plataforma oferece auxílio informativo. Os documentos produzidos têm validade legal quando utilizados no contexto apropriado, mas a interpretação final sempre depende das autoridades judiciais competentes."
    },
    {
      question: "Quais áreas do direito o JuSimples abrange?",
      answer: "Atualmente, o JuSimples abrange diversas áreas do direito mais comuns para o cidadão comum, incluindo: Direito do Consumidor, Direito Civil básico, Direito Trabalhista, questões de condomínio, problemas com contratos simples, cobranças indevidas, e reclamações administrativas. Estamos constantemente expandindo nossa cobertura para incluir mais áreas jurídicas."
    },
    {
      question: "Como posso acompanhar meus casos no JuSimples?",
      answer: "Após criar sua conta, todas as suas consultas e documentos ficam salvos no Dashboard pessoal. Lá você pode visualizar o histórico completo, retomar conversas anteriores, baixar documentos gerados e receber atualizações sobre prazos importantes. O sistema também envia notificações por e-mail para manter você informado sobre o andamento dos seus casos."
    }
  ];

  return (
    <div className="main-content">
      <div className="faq-container">
        <h1 className="faq-title">Dúvidas Frequentes</h1>
        <p className="faq-subtitle">
          Encontre respostas para as perguntas mais comuns sobre o JuSimples e como podemos ajudar você com questões jurídicas.
        </p>

        <div className="faq-list">
          {faqItems.map((item, index) => (
            <div 
              key={index} 
              className={`faq-item ${openQuestion === index ? 'open' : ''}`}
            >
              <button 
                className="faq-question"
                onClick={() => toggleQuestion(index)}
              >
                {item.question}
                <span className="faq-icon">{openQuestion === index ? '−' : '+'}</span>
              </button>
              {openQuestion === index && (
                <div className="faq-answer">
                  <p>{item.answer}</p>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="faq-cta">
          <h2>Ainda tem dúvidas?</h2>
          <p>Entre em contato conosco diretamente e teremos prazer em ajudar.</p>
          <div className="faq-cta-buttons">
            <a href="mailto:contato@jusimples.com" className="btn btn-primary">
              Enviar Email
            </a>
            <a href="/" className="btn btn-outline">
              Voltar para a Página Inicial
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
