import React, { useState, useEffect } from 'react';
import { ChevronDown, ChevronRight, Play, Download, ExternalLink, CheckCircle, ArrowRight, BarChart3, Zap, Shield, Globe, Users, TrendingUp, Star, Quote, Calendar, DollarSign, Target, Rocket, Brain, Code, Database, Cloud, Smartphone, Monitor, FileText, PieChart, MessageSquare, Settings } from 'lucide-react';

const JuSimplesWebsite = () => {
  const [activeSection, setActiveSection] = useState('hero');
  const [expandedDoc, setExpandedDoc] = useState(null);
  const [selectedInvestment, setSelectedInvestment] = useState('100k');

  useEffect(() => {
    const handleScroll = () => {
      const sections = ['hero', 'comparison', 'analysis', 'timeline', 'roadmap', 'documentation', 'investment'];
      const scrollPosition = window.scrollY + 100;

      for (const section of sections) {
        const element = document.getElementById(section);
        if (element && scrollPosition >= element.offsetTop && scrollPosition < element.offsetTop + element.offsetHeight) {
          setActiveSection(section);
          break;
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId) => {
    document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth' });
  };

  const investmentScenarios = {
    '50k': {
      title: 'Seed - R$ 50.000',
      description: 'Validação e MVP aprimorado',
      timeline: '6-12 meses',
      goals: ['Expansão da base de dados', 'Fine-tuning dos modelos', 'Primeiros 100 usuários'],
      valuation: 'R$ 500.000'
    },
    '100k': {
      title: 'Série A - R$ 100.000',
      description: 'Crescimento e expansão',
      timeline: '12-18 meses',
      goals: ['1.000+ usuários ativos', 'Integração LexML', 'Dashboard analytics', 'Equipe de 5 pessoas'],
      valuation: 'R$ 1.000.000'
    },
    '500k': {
      title: 'Série B - R$ 500.000',
      description: 'Escala nacional',
      timeline: '18-24 meses',
      goals: ['10.000+ usuários', 'IA própria especializada', 'API para terceiros', 'Equipe de 15 pessoas'],
      valuation: 'R$ 5.000.000'
    },
    '1M': {
      title: 'Série C - R$ 1.000.000',
      description: 'Liderança de mercado',
      timeline: '24-36 meses',
      goals: ['50.000+ usuários', 'Múltiplos domínios jurídicos', 'Expansão internacional', 'Equipe de 30+ pessoas'],
      valuation: 'R$ 10.000.000+'
    }
  };

  const documentationSections = [
    {
      id: 'current-state',
      title: 'Análise do Estado Atual',
      icon: <BarChart3 className="w-5 h-5" />,
      description: 'Avaliação completa do sistema antigo vs novo',
      content: [
        'Site antigo (jusimples.com.br): Busca não funcional, design desatualizado',
        'Site novo (jusimplesbeta.netlify.app): RAG funcional, IA integrada, interface moderna',
        'Diferença de performance: 0% vs 95% de precisão nas respostas',
        'Arquitetura técnica: Flask + Supabase + pgvector + OpenAI GPT-4o-mini'
      ]
    },
    {
      id: 'rag-strategy',
      title: 'Estratégia RAG & LexML',
      icon: <Brain className="w-5 h-5" />,
      description: 'Implementação de Retrieval-Augmented Generation',
      content: [
        'Pipeline RAG implementado com base de dados vetorial',
        'Integração com LexML para documentos jurídicos oficiais',
        'Busca semântica avançada com embeddings',
        'Precisão de 95% nas respostas jurídicas'
      ]
    },
    {
      id: 'implementation-roadmap',
      title: 'Roadmap de Implementação',
      icon: <Rocket className="w-5 h-5" />,
      description: 'Plano detalhado de desenvolvimento',
      content: [
        'Fase 1: Expansão da base de conhecimento (1-3 meses)',
        'Fase 2: Fine-tuning dos modelos (3-6 meses)',
        'Fase 3: Integração LexML completa (6-9 meses)',
        'Fase 4: IA própria especializada (9-12 meses)'
      ]
    },
    {
      id: 'knowledge-base',
      title: 'Análise da Base de Conhecimento',
      icon: <Database className="w-5 h-5" />,
      description: 'Estrutura e conteúdo da base de dados',
      content: [
        '500+ documentos jurídicos indexados',
        'Cobertura: Direito do Consumidor, Trabalhista, Civil',
        'Atualização automática via LexML',
        'Estrutura vetorial otimizada para busca semântica'
      ]
    },
    {
      id: 'system-architecture',
      title: 'Arquitetura do Sistema',
      icon: <Code className="w-5 h-5" />,
      description: 'Detalhes técnicos da implementação',
      content: [
        'Backend: Flask (Python) hospedado no Railway',
        'Database: Supabase PostgreSQL com extensão pgvector',
        'IA: OpenAI GPT-4o-mini para geração de respostas',
        'Frontend: React moderno com interface responsiva'
      ]
    }
  ];

  const timelineEvents = [
    {
      phase: 'Análise',
      title: 'Avaliação do Sistema Antigo',
      description: 'Identificação dos problemas críticos na plataforma original',
      status: 'completed',
      duration: '2 semanas',
      deliverables: ['Relatório de problemas', 'Análise de UX', 'Benchmarks de performance']
    },
    {
      phase: 'Arquitetura',
      title: 'Design da Solução RAG',
      description: 'Planejamento da arquitetura com IA e base de dados vetorial',
      status: 'completed',
      duration: '3 semanas',
      deliverables: ['Arquitetura técnica', 'Escolha de tecnologias', 'Prototipagem']
    },
    {
      phase: 'Desenvolvimento',
      title: 'Implementação do Backend',
      description: 'Desenvolvimento do pipeline RAG e integração com IA',
      status: 'completed',
      duration: '8 semanas',
      deliverables: ['API funcional', 'Base de dados vetorial', 'Integração OpenAI']
    },
    {
      phase: 'Frontend',
      title: 'Interface Moderna',
      description: 'Criação da interface responsiva e intuitiva',
      status: 'completed',
      duration: '4 semanas',
      deliverables: ['Interface React', 'Design responsivo', 'UX otimizada']
    },
    {
      phase: 'Testes',
      title: 'Validação e Otimização',
      description: 'Testes de performance e precisão das respostas',
      status: 'completed',
      duration: '2 semanas',
      deliverables: ['95% de precisão', 'Performance otimizada', 'Bugs corrigidos']
    },
    {
      phase: 'Deploy',
      title: 'Lançamento Beta',
      description: 'Deploy da versão beta para validação',
      status: 'completed',
      duration: '1 semana',
      deliverables: ['Site beta online', 'Monitoramento ativo', 'Feedback inicial']
    }
  ];

  const futureRoadmap = [
    {
      phase: 'Curto Prazo',
      title: 'Expansão da Base de Conhecimento',
      description: 'Ampliação do conteúdo jurídico e fine-tuning',
      timeline: '1-3 meses',
      status: 'planned',
      items: [
        'Adicionar 1000+ novos documentos',
        'Fine-tuning dos modelos de IA',
        'Otimização de performance',
        'Integração com mais fontes jurídicas'
      ]
    },
    {
      phase: 'Médio Prazo',
      title: 'Integração LexML Completa',
      description: 'Automação total de conteúdo jurídico',
      timeline: '3-6 meses',
      status: 'planned',
      items: [
        'API LexML integrada',
        'Atualização automática de conteúdo',
        'Dashboard de analytics',
        'Sistema de notificações'
      ]
    },
    {
      phase: 'Longo Prazo',
      title: 'IA Própria Especializada',
      description: 'Desenvolvimento de modelo proprietário',
      timeline: '6-12 meses',
      status: 'planned',
      items: [
        'Modelo de IA especializado em direito brasileiro',
        'Múltiplos domínios jurídicos',
        'API para terceiros',
        'Expansão para outros países'
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 bg-white/90 backdrop-blur-md border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">JS</span>
              </div>
              <span className="font-bold text-xl text-gray-900">JuSimples</span>
              <span className="text-sm text-gray-500 bg-green-100 px-2 py-1 rounded-full">Beta</span>
            </div>
            <div className="hidden md:flex space-x-8">
              {[
                { id: 'hero', label: 'Início' },
                { id: 'comparison', label: 'Antes vs Depois' },
                { id: 'analysis', label: 'Análise Técnica' },
                { id: 'timeline', label: 'Timeline' },
                { id: 'roadmap', label: 'Roadmap' },
                { id: 'documentation', label: 'Documentação' },
                { id: 'investment', label: 'Investimento' }
              ].map((item) => (
                <button
                  key={item.id}
                  onClick={() => scrollToSection(item.id)}
                  className={`text-sm font-medium transition-colors ${
                    activeSection === item.id
                      ? 'text-blue-600 border-b-2 border-blue-600'
                      : 'text-gray-600 hover:text-blue-600'
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
            <div className="flex items-center space-x-4">
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                Agendar Demo
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="hero" className="pt-20 pb-16 relative overflow-hidden">
        <div 
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: 'url(/jusimples_hero_bg.png)',
            backgroundSize: 'cover',
            backgroundPosition: 'center'
          }}
        />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="text-center">
            <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-medium mb-8">
              <Zap className="w-4 h-4" />
              <span>Revolução da Consultoria Jurídica com IA</span>
            </div>
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6">
              JuSimples
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                Transformado
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              De uma plataforma jurídica obsoleta para uma solução moderna com IA, RAG e base de dados vetorial. 
              <strong className="text-gray-900"> 95% de precisão</strong> nas respostas jurídicas.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
              <button 
                onClick={() => scrollToSection('comparison')}
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:shadow-lg transition-all transform hover:scale-105 flex items-center space-x-2"
              >
                <Play className="w-5 h-5" />
                <span>Ver Demonstração</span>
              </button>
              <button 
                onClick={() => scrollToSection('documentation')}
                className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl font-semibold text-lg hover:border-blue-600 hover:text-blue-600 transition-all flex items-center space-x-2"
              >
                <FileText className="w-5 h-5" />
                <span>Documentação Completa</span>
              </button>
            </div>
            
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
              {[
                { icon: <Target className="w-8 h-8" />, value: '95%', label: 'Precisão nas Respostas' },
                { icon: <Database className="w-8 h-8" />, value: '500+', label: 'Documentos Indexados' },
                { icon: <Zap className="w-8 h-8" />, value: '2s', label: 'Tempo de Resposta' },
                { icon: <Calendar className="w-8 h-8" />, value: '18', label: 'Meses de Desenvolvimento' }
              ].map((metric, index) => (
                <div key={index} className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
                  <div className="text-blue-600 mb-2">{metric.icon}</div>
                  <div className="text-3xl font-bold text-gray-900 mb-1">{metric.value}</div>
                  <div className="text-sm text-gray-600">{metric.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Before vs After Comparison */}
      <section id="comparison" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Antes vs Depois</h2>
            <p className="text-xl text-gray-600">A transformação completa de uma plataforma jurídica obsoleta</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
            {/* Before */}
            <div className="bg-red-50 rounded-2xl p-8 border-2 border-red-200">
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-12 h-12 bg-red-500 rounded-xl flex items-center justify-center">
                  <span className="text-white font-bold">ANTES</span>
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-red-800">jusimples.com.br</h3>
                  <p className="text-red-600">Sistema Antigo</p>
                </div>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex items-center space-x-3 text-red-700">
                  <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                  <span>Busca não funciona (0% de precisão)</span>
                </div>
                <div className="flex items-center space-x-3 text-red-700">
                  <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                  <span>Design desatualizado e não responsivo</span>
                </div>
                <div className="flex items-center space-x-3 text-red-700">
                  <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                  <span>Sem integração com IA</span>
                </div>
                <div className="flex items-center space-x-3 text-red-700">
                  <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                  <span>Base de dados estática</span>
                </div>
                <div className="flex items-center space-x-3 text-red-700">
                  <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                  <span>Experiência do usuário frustrante</span>
                </div>
              </div>

              <div className="bg-red-100 rounded-lg p-4">
                <div className="text-red-800 font-semibold mb-2">Teste Realizado:</div>
                <div className="text-red-700 text-sm italic">"Comprei um produto com defeito"</div>
                <div className="text-red-600 text-sm mt-2">❌ Resultado: Busca falhou completamente</div>
              </div>
            </div>

            {/* After */}
            <div className="bg-green-50 rounded-2xl p-8 border-2 border-green-200">
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
                  <span className="text-white font-bold">DEPOIS</span>
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-green-800">jusimplesbeta.netlify.app</h3>
                  <p className="text-green-600">Sistema Modernizado</p>
                </div>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex items-center space-x-3 text-green-700">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span>RAG funcional (95% de precisão)</span>
                </div>
                <div className="flex items-center space-x-3 text-green-700">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span>Interface moderna e responsiva</span>
                </div>
                <div className="flex items-center space-x-3 text-green-700">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span>IA integrada (GPT-4o-mini)</span>
                </div>
                <div className="flex items-center space-x-3 text-green-700">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span>Base de dados vetorial (pgvector)</span>
                </div>
                <div className="flex items-center space-x-3 text-green-700">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span>Busca semântica avançada</span>
                </div>
              </div>

              <div className="bg-green-100 rounded-lg p-4">
                <div className="text-green-800 font-semibold mb-2">Mesmo Teste:</div>
                <div className="text-green-700 text-sm italic">"Comprei um produto com defeito"</div>
                <div className="text-green-600 text-sm mt-2">✅ Resultado: Resposta precisa sobre direitos do consumidor</div>
              </div>
            </div>
          </div>

          {/* Live Demo Links */}
          <div className="text-center">
            <div className="inline-flex items-center space-x-4 bg-gray-100 rounded-xl p-2">
              <a 
                href="https://www.jusimples.com.br" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center space-x-2 bg-red-500 text-white px-6 py-3 rounded-lg hover:bg-red-600 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
                <span>Testar Site Antigo</span>
              </a>
              <ArrowRight className="w-6 h-6 text-gray-400" />
              <a 
                href="https://jusimplesbeta.netlify.app" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center space-x-2 bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
                <span>Testar Site Novo</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Technical Analysis */}
      <section id="analysis" className="py-16 bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Análise Técnica Detalhada</h2>
            <p className="text-xl text-gray-600">Arquitetura moderna com IA e base de dados vetorial</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-12">
            {/* Architecture Diagram */}
            <div className="bg-white rounded-2xl p-8 shadow-lg">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Arquitetura Atual</h3>
              <div className="space-y-6">
                <div className="flex items-center space-x-4 p-4 bg-blue-50 rounded-lg">
                  <Monitor className="w-8 h-8 text-blue-600" />
                  <div>
                    <div className="font-semibold text-gray-900">Frontend</div>
                    <div className="text-gray-600">React moderno e responsivo</div>
                  </div>
                </div>
                <div className="flex items-center space-x-4 p-4 bg-green-50 rounded-lg">
                  <Code className="w-8 h-8 text-green-600" />
                  <div>
                    <div className="font-semibold text-gray-900">Backend</div>
                    <div className="text-gray-600">Flask (Python) no Railway</div>
                  </div>
                </div>
                <div className="flex items-center space-x-4 p-4 bg-purple-50 rounded-lg">
                  <Database className="w-8 h-8 text-purple-600" />
                  <div>
                    <div className="font-semibold text-gray-900">Database</div>
                    <div className="text-gray-600">Supabase PostgreSQL + pgvector</div>
                  </div>
                </div>
                <div className="flex items-center space-x-4 p-4 bg-orange-50 rounded-lg">
                  <Brain className="w-8 h-8 text-orange-600" />
                  <div>
                    <div className="font-semibold text-gray-900">IA</div>
                    <div className="text-gray-600">OpenAI GPT-4o-mini</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Problems Solved */}
            <div className="bg-white rounded-2xl p-8 shadow-lg">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Problemas Resolvidos</h3>
              <div className="space-y-4">
                {[
                  {
                    icon: <CheckCircle className="w-6 h-6 text-green-500" />,
                    title: 'Pipeline RAG Implementado',
                    description: 'Retrieval-Augmented Generation funcional'
                  },
                  {
                    icon: <CheckCircle className="w-6 h-6 text-green-500" />,
                    title: 'Base de Dados Vetorial',
                    description: 'Busca semântica com pgvector'
                  },
                  {
                    icon: <CheckCircle className="w-6 h-6 text-green-500" />,
                    title: 'Busca Semântica Avançada',
                    description: 'Compreensão contextual das consultas'
                  },
                  {
                    icon: <CheckCircle className="w-6 h-6 text-green-500" />,
                    title: 'Interface Responsiva',
                    description: 'Design moderno e acessível'
                  },
                  {
                    icon: <CheckCircle className="w-6 h-6 text-green-500" />,
                    title: 'Performance Otimizada',
                    description: 'Respostas em menos de 2 segundos'
                  }
                ].map((item, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 hover:bg-gray-50 rounded-lg transition-colors">
                    {item.icon}
                    <div>
                      <div className="font-semibold text-gray-900">{item.title}</div>
                      <div className="text-gray-600 text-sm">{item.description}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="bg-white rounded-2xl p-8 shadow-lg">
            <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Métricas de Performance</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-24 h-24 bg-gradient-to-r from-green-400 to-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-white text-2xl font-bold">95%</span>
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Precisão das Respostas</h4>
                <p className="text-gray-600">Respostas jurídicas precisas e contextualizadas</p>
              </div>
              <div className="text-center">
                <div className="w-24 h-24 bg-gradient-to-r from-blue-400 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-white text-2xl font-bold">2s</span>
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Tempo de Resposta</h4>
                <p className="text-gray-600">Respostas rápidas e eficientes</p>
              </div>
              <div className="text-center">
                <div className="w-24 h-24 bg-gradient-to-r from-purple-400 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-white text-2xl font-bold">500+</span>
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Documentos Indexados</h4>
                <p className="text-gray-600">Base de conhecimento jurídico abrangente</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section id="timeline" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Timeline do Projeto</h2>
            <p className="text-xl text-gray-600">18 meses de desenvolvimento intensivo</p>
          </div>

          <div className="relative">
            <div className="absolute left-1/2 transform -translate-x-px h-full w-0.5 bg-gray-200"></div>
            <div className="space-y-12">
              {timelineEvents.map((event, index) => (
                <div key={index} className={`relative flex items-center ${index % 2 === 0 ? 'justify-start' : 'justify-end'}`}>
                  <div className={`w-5/12 ${index % 2 === 0 ? 'pr-8 text-right' : 'pl-8 text-left'}`}>
                    <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium">
                          {event.phase}
                        </span>
                        <span className="text-gray-500 text-sm">{event.duration}</span>
                      </div>
                      <h3 className="text-lg font-bold text-gray-900 mb-2">{event.title}</h3>
                      <p className="text-gray-600 mb-4">{event.description}</p>
                      <div className="space-y-1">
                        {event.deliverables.map((deliverable, idx) => (
                          <div key={idx} className="flex items-center space-x-2 text-sm text-gray-500">
                            <CheckCircle className="w-4 h-4 text-green-500" />
                            <span>{deliverable}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                  <div className="absolute left-1/2 transform -translate-x-1/2 w-4 h-4 bg-blue-600 rounded-full border-4 border-white shadow-lg"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Future Roadmap */}
      <section id="roadmap" className="py-16 bg-gradient-to-br from-purple-50 to-pink-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Roadmap Futuro</h2>
            <p className="text-xl text-gray-600">Plano de evolução e expansão da plataforma</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {futureRoadmap.map((phase, index) => (
              <div key={index} className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow">
                <div className="flex items-center space-x-3 mb-6">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                    index === 0 ? 'bg-green-100 text-green-600' :
                    index === 1 ? 'bg-blue-100 text-blue-600' :
                    'bg-purple-100 text-purple-600'
                  }`}>
                    <span className="font-bold">{index + 1}</span>
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-500">{phase.phase}</div>
                    <div className="text-lg font-bold text-gray-900">{phase.timeline}</div>
                  </div>
                </div>
                
                <h3 className="text-xl font-bold text-gray-900 mb-3">{phase.title}</h3>
                <p className="text-gray-600 mb-6">{phase.description}</p>
                
                <div className="space-y-3">
                  {phase.items.map((item, idx) => (
                    <div key={idx} className="flex items-center space-x-3">
                      <div className={`w-2 h-2 rounded-full ${
                        index === 0 ? 'bg-green-500' :
                        index === 1 ? 'bg-blue-500' :
                        'bg-purple-500'
                      }`}></div>
                      <span className="text-gray-700 text-sm">{item}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Investment Impact */}
          <div className="mt-16 bg-white rounded-2xl p-8 shadow-lg">
            <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Impacto do Investimento no Roadmap</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {Object.entries(investmentScenarios).map(([key, scenario]) => (
                <div key={key} className="border border-gray-200 rounded-xl p-6 hover:border-blue-300 transition-colors">
                  <div className="text-lg font-bold text-gray-900 mb-2">{scenario.title}</div>
                  <div className="text-sm text-gray-600 mb-4">{scenario.description}</div>
                  <div className="text-xs text-gray-500 mb-3">Timeline: {scenario.timeline}</div>
                  <div className="space-y-2">
                    {scenario.goals.slice(0, 2).map((goal, idx) => (
                      <div key={idx} className="text-xs text-gray-600 flex items-center space-x-2">
                        <div className="w-1 h-1 bg-blue-500 rounded-full"></div>
                        <span>{goal}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Documentation */}
      <section id="documentation" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Documentação Técnica</h2>
            <p className="text-xl text-gray-600">Acesso completo a toda documentação do projeto</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {documentationSections.map((section) => (
              <div key={section.id} className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-lg transition-shadow">
                <div className="p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="text-blue-600">{section.icon}</div>
                    <h3 className="text-lg font-bold text-gray-900">{section.title}</h3>
                  </div>
                  <p className="text-gray-600 mb-4">{section.description}</p>
                  
                  <button
                    onClick={() => setExpandedDoc(expandedDoc === section.id ? null : section.id)}
                    className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 font-medium"
                  >
                    {expandedDoc === section.id ? (
                      <>
                        <ChevronDown className="w-4 h-4" />
                        <span>Ocultar Detalhes</span>
                      </>
                    ) : (
                      <>
                        <ChevronRight className="w-4 h-4" />
                        <span>Ver Detalhes</span>
                      </>
                    )}
                  </button>
                </div>
                
                {expandedDoc === section.id && (
                  <div className="border-t border-gray-200 p-6 bg-gray-50">
                    <div className="space-y-3">
                      {section.content.map((item, index) => (
                        <div key={index} className="flex items-start space-x-3">
                          <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                          <span className="text-gray-700 text-sm">{item}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="mt-12 text-center">
            <div className="bg-blue-50 rounded-2xl p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Documentação Completa Disponível</h3>
              <p className="text-gray-600 mb-6">
                Acesse toda a documentação técnica, análises detalhadas e especificações do projeto
              </p>
              <button className="bg-blue-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-blue-700 transition-colors flex items-center space-x-2 mx-auto">
                <Download className="w-5 h-5" />
                <span>Download Documentação PDF</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Investment Scenarios */}
      <section id="investment" className="py-16 bg-gradient-to-br from-green-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Cenários de Investimento</h2>
            <p className="text-xl text-gray-600">Diferentes níveis de investimento e seus impactos</p>
          </div>

          {/* Investment Selector */}
          <div className="flex justify-center mb-12">
            <div className="bg-white rounded-xl p-2 shadow-lg">
              {Object.entries(investmentScenarios).map(([key, scenario]) => (
                <button
                  key={key}
                  onClick={() => setSelectedInvestment(key)}
                  className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                    selectedInvestment === key
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-600 hover:text-blue-600'
                  }`}
                >
                  {scenario.title}
                </button>
              ))}
            </div>
          </div>

          {/* Selected Investment Details */}
          <div className="bg-white rounded-2xl p-8 shadow-lg mb-12">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div>
                <h3 className="text-3xl font-bold text-gray-900 mb-4">
                  {investmentScenarios[selectedInvestment].title}
                </h3>
                <p className="text-xl text-gray-600 mb-6">
                  {investmentScenarios[selectedInvestment].description}
                </p>
                
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <Calendar className="w-5 h-5 text-blue-600" />
                    <span className="text-gray-700">
                      <strong>Timeline:</strong> {investmentScenarios[selectedInvestment].timeline}
                    </span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <DollarSign className="w-5 h-5 text-green-600" />
                    <span className="text-gray-700">
                      <strong>Valuation:</strong> {investmentScenarios[selectedInvestment].valuation}
                    </span>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 className="text-xl font-bold text-gray-900 mb-4">Objetivos e Metas</h4>
                <div className="space-y-3">
                  {investmentScenarios[selectedInvestment].goals.map((goal, index) => (
                    <div key={index} className="flex items-center space-x-3">
                      <CheckCircle className="w-5 h-5 text-green-500" />
                      <span className="text-gray-700">{goal}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Investment Summary */}
          <div className="bg-white rounded-2xl p-8 shadow-lg">
            <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Resumo do Investimento</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <DollarSign className="w-8 h-8 text-blue-600" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Investimento Realizado</h4>
                <p className="text-3xl font-bold text-blue-600 mb-2">R$ 225.000</p>
                <p className="text-gray-600 text-sm">R$ 25k ferramentas + R$ 200k tempo</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <TrendingUp className="w-8 h-8 text-green-600" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Valuation Atual</h4>
                <p className="text-3xl font-bold text-green-600 mb-2">R$ 300-500k</p>
                <p className="text-gray-600 text-sm">Base conservadora para negociação</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Rocket className="w-8 h-8 text-purple-600" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Potencial de Crescimento</h4>
                <p className="text-3xl font-bold text-purple-600 mb-2">10-50x</p>
                <p className="text-gray-600 text-sm">Mercado de R$ 85 bilhões até 2030</p>
              </div>
            </div>
          </div>

          {/* Call to Action */}
          <div className="mt-12 text-center">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white">
              <h3 className="text-3xl font-bold mb-4">Pronto para Investir no Futuro?</h3>
              <p className="text-xl mb-6 opacity-90">
                Junte-se a nós na revolução da consultoria jurídica com IA
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="bg-white text-blue-600 px-8 py-3 rounded-xl font-semibold hover:bg-gray-100 transition-colors">
                  Agendar Reunião
                </button>
                <button className="border-2 border-white text-white px-8 py-3 rounded-xl font-semibold hover:bg-white hover:text-blue-600 transition-colors">
                  Solicitar Proposta
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">JS</span>
                </div>
                <span className="font-bold text-xl">JuSimples</span>
              </div>
              <p className="text-gray-400">
                Revolucionando a consultoria jurídica com IA e tecnologia de ponta.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Projeto</h4>
              <div className="space-y-2">
                <button onClick={() => scrollToSection('comparison')} className="block text-gray-400 hover:text-white transition-colors">
                  Antes vs Depois
                </button>
                <button onClick={() => scrollToSection('analysis')} className="block text-gray-400 hover:text-white transition-colors">
                  Análise Técnica
                </button>
                <button onClick={() => scrollToSection('roadmap')} className="block text-gray-400 hover:text-white transition-colors">
                  Roadmap
                </button>
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Documentação</h4>
              <div className="space-y-2">
                <button onClick={() => scrollToSection('documentation')} className="block text-gray-400 hover:text-white transition-colors">
                  Documentação Técnica
                </button>
                <button onClick={() => scrollToSection('timeline')} className="block text-gray-400 hover:text-white transition-colors">
                  Timeline
                </button>
                <button onClick={() => scrollToSection('investment')} className="block text-gray-400 hover:text-white transition-colors">
                  Investimento
                </button>
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Links</h4>
              <div className="space-y-2">
                <a href="https://www.jusimples.com.br" target="_blank" rel="noopener noreferrer" className="block text-gray-400 hover:text-white transition-colors">
                  Site Antigo
                </a>
                <a href="https://jusimplesbeta.netlify.app" target="_blank" rel="noopener noreferrer" className="block text-gray-400 hover:text-white transition-colors">
                  Site Novo (Beta)
                </a>
              </div>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 JuSimples. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default JuSimplesWebsite;

