import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './styles.css';
import './modern-styles.css';
import {
  ChevronRight,
  Play,
  ExternalLink,
  CheckCircle,
  BarChart3,
  Zap,
  Calendar,
  Target,
  Rocket,
  Brain,
  Code,
  Code2,
  Database,
  FileText,
  FileSearch,
  Timer,
  TrendingUp,
  Globe,
  Download,
  X,
  ArrowRight,
  Users,
  Sparkles,
  Infinity as InfinityIcon,
  TestTube,
  Layers,
  Building2,
  Search,
  Smartphone,
  LineChart,
  BarChartBig as ChartLineUp,
} from 'lucide-react';

// Component starts here

// Comparison features data
const comparisonFeatures = [
  {
    name: 'Consulta Jurídica com IA',
    jusimples2: true,
    jusimplesDetail: 'GPT-4o-mini',
    jusimples1: true,
    jusimples1Detail: 'GPT-3.5',
    competitors: false
  },
  {
    name: 'Base de Conhecimento Jurídico',
    jusimples2: true,
    jusimplesDetail: '+100.000 documentos',
    jusimples1: true,
    jusimples1Detail: '5.000 documentos',
    competitors: true,
    competitorsDetail: 'Limitado'
  },
  {
    name: 'RAG Jurídico Especializado',
    jusimples2: true,
    jusimplesDetail: 'Modelo avançado',
    jusimples1: false,
    competitors: false
  },
  {
    name: 'Análise Processual Automatizada',
    jusimples2: true,
    jusimples1: false,
    competitors: false
  },
  {
    name: 'Atualização Automática de Legislação',
    jusimples2: true,
    jusimples1: false,
    competitors: true,
    competitorsDetail: 'Manual'
  },
  {
    name: 'Integração com Tribunais',
    jusimples2: true,
    jusimplesDetail: 'Completa',
    jusimples1: true,
    jusimples1Detail: 'Parcial',
    competitors: true,
    competitorsDetail: 'Limitada'
  }
];

// Documentation sections are defined inside the component

const ProjectSales = () => {
  const [activeSection, setActiveSection] = useState('hero');
  const [expandedDoc, setExpandedDoc] = useState(null);
  const [selectedInvestment, setSelectedInvestment] = useState('100k');

  useEffect(() => {
    const handleScroll = () => {
      const sections = ['hero', 'transformation', 'comparison', 'comparison-alternatives', 'analysis', 'timeline', 'roadmap', 'documentation', 'investment'];
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
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId) => {
    document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth' });
  };

  // Investment scenarios data
  const investmentScenarios = {
    '50k': {
      title: 'Seed - R$ 50.000',
      description: 'Validação e MVP aprimorado',
      timeline: '6-12 meses',
      goals: ['Expansão da base de dados', 'Fine-tuning dos modelos', 'Primeiros 100 usuários'],
      valuation: 'R$ 500.000',
      roi: '10x',
      color: 'from-green-400 to-green-600',
    },
    '100k': {
      title: 'Série A - R$ 100.000',
      description: 'Crescimento e expansão',
      timeline: '12-18 meses',
      goals: ['1.000+ usuários ativos', 'Integração LexML', 'Dashboard analytics', 'Equipe de 5 pessoas'],
      valuation: 'R$ 1.000.000',
      roi: '10x',
      color: 'from-blue-400 to-blue-600',
    },
    '500k': {
      title: 'Série B - R$ 500.000',
      description: 'Escala nacional',
      timeline: '18-24 meses',
      goals: ['10.000+ usuários', 'IA própria especializada', 'API para terceiros', 'Equipe de 15 pessoas'],
      valuation: 'R$ 5.000.000',
      roi: '10x',
      color: 'from-purple-400 to-purple-600',
    },
    '1M': {
      title: 'Série C - R$ 1.000.000',
      description: 'Liderança de mercado',
      timeline: '24-36 meses',
      goals: ['50.000+ usuários', 'Múltiplos domínios jurídicos', 'Expansão internacional', 'Equipe de 30+ pessoas'],
      valuation: 'R$ 10.000.000+',
      roi: '10x+',
      color: 'from-orange-400 to-orange-600',
    },
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
        'Arquitetura técnica: Flask + Supabase + pgvector + OpenAI GPT-4o-mini',
      ],
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
        'Precisão de 95% nas respostas jurídicas',
      ],
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
        'Fase 4: IA própria especializada (9-12 meses)',
      ],
    },
  ];

  return (
    <div className="page-container">
      {/* Fixed Navigation */}
      <motion.nav 
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-md border-b border-gray-200 z-50 shadow-md modern-header"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <motion.div 
              className="flex items-center space-x-3"
              whileHover={{ scale: 1.02 }}
              transition={{ type: 'spring', stiffness: 300 }}
            >
              <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-green-600 rounded-xl flex items-center justify-center shadow-lg">
                <span className="text-white font-bold text-xl">JS</span>
              </div>
              <div>
                <span className="font-bold text-2xl text-gray-900">JuSimples</span>
                <span className="ml-2 bg-gradient-to-r from-green-400 to-green-600 text-white px-3 py-1 rounded-full text-sm font-medium shadow-sm">
                  Transformado
                </span>
              </div>
            </motion.div>

            <div className="hidden md:flex space-x-6">
              {[
                { id: 'hero', label: 'Início' },
                { id: 'transformation', label: 'Transformação' },
                { id: 'comparison', label: 'Antes vs Depois' },
                { id: 'comparison-alternatives', label: 'JuSimples vs Alternativas' },
                { id: 'analysis', label: 'Análise Técnica' },
                { id: 'timeline', label: 'Timeline' },
                { id: 'roadmap', label: 'Roadmap' },
                { id: 'investment', label: 'Investimento' },
              ].map((item) => (
                <motion.button
                  key={item.id}
                  onClick={() => scrollToSection(item.id)}
                  className={`text-sm font-medium transition-all duration-300 relative ${
                    activeSection === item.id
                      ? 'text-blue-600 font-semibold'
                      : 'text-gray-600 hover:text-blue-600'
                  }`}
                  whileHover={{ scale: 1.05 }}
                  transition={{ type: 'spring', stiffness: 400 }}
                >
                  {item.label}
                  {activeSection === item.id && (
                    <motion.div 
                      className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600 rounded-full"
                      layoutId="navIndicator"
                    />
                  )}
                </motion.button>
              ))}
            </div>

            <motion.div 
              className="flex items-center space-x-4"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <motion.button
                onClick={() => scrollToSection('investment')}
                className="bg-gradient-to-r from-blue-600 to-green-600 hover:from-blue-700 hover:to-green-700 text-white px-5 py-2.5 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl"
                whileHover={{ 
                  boxShadow: '0 0 15px rgba(59, 130, 246, 0.5)',
                }}
              >
                <span className="flex items-center">
                  <Calendar className="w-4 h-4 mr-2" />
                  Agendar Demo
                </span>
              </motion.button>
            </motion.div>
          </div>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <motion.section 
        id="hero" 
        className="hero-modern relative overflow-hidden mt-16 pt-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        {/* Modern background elements */}
        <div className="bg-blob blob-1"></div>
        <div className="bg-blob blob-2"></div>
        <div className="bg-blob blob-3"></div>
        
        <div className="content-container">
          <motion.div 
            className="inline-flex items-center space-x-2 bg-gradient-to-r from-green-50 to-blue-50 text-green-800 px-6 py-3 rounded-full text-sm font-medium mb-8"
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.5 }}
            whileHover={{ scale: 1.03 }}
          >
            <Sparkles className="w-5 h-5 text-blue-600" />
            <span>Revolução da Consultoria Jurídica com IA</span>
          </motion.div>

          <motion.h1 
            className="hero-title"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.5 }}
          >
            JuSimples Transformado
          </motion.h1>

          <motion.div 
            className="divider mx-auto"
            initial={{ width: 0 }}
            animate={{ width: '80px' }}
            transition={{ delay: 0.7, duration: 0.6 }}
          ></motion.div>

          <motion.p 
            className="hero-subtitle max-w-3xl mx-auto"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.8, duration: 0.5 }}
          >
            De uma plataforma jurídica obsoleta para uma solução moderna com IA, RAG e base de dados vetorial.
          </motion.p>

          <motion.p 
            className="hero-description"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.8, duration: 0.5 }}
          >
            <strong className="text-blue-600"> 95% de precisão</strong> nas respostas jurídicas.
          </motion.p>

          <motion.div 
            className="cta-buttons"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 1, duration: 0.5 }}
          >
            <motion.button
              onClick={() => scrollToSection('transformation')}
              className="btn-primary bg-gradient-to-r from-blue-600 to-blue-800 hover:from-blue-700 hover:to-blue-900 text-white px-6 py-3 rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all flex items-center justify-center space-x-2"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
            >
              <Play className="w-5 h-5" />
              <span>Ver Demonstração</span>
            </motion.button>
            
            <motion.button
              onClick={() => scrollToSection('documentation')}
              className="btn-outline-secondary border-2 border-gray-300 hover:border-blue-500 text-gray-700 hover:text-blue-600 px-6 py-3 rounded-lg font-semibold transition-all flex items-center justify-center space-x-2"
              whileHover={{ scale: 1.05, borderColor: '#3b82f6' }}
              whileTap={{ scale: 0.98 }}
            >
              <FileText className="w-5 h-5" />
              <span>Documentação Completa</span>
            </motion.button>
          </motion.div>

          {/* Key Metrics Grid */}
          <motion.div 
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-16"
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 1.2, duration: 0.6 }}
          >
            {[
              {
                icon: <Target className="w-10 h-10" />,
                value: '95%',
                label: 'Precisão nas Respostas',
                color: 'from-blue-400 to-blue-600'
              },
              {
                icon: <Database className="w-10 h-10" />,
                value: '500+',
                label: 'Documentos Indexados',
                color: 'from-green-400 to-green-600'
              },
              { 
                icon: <Timer className="w-10 h-10" />, 
                value: '2s', 
                label: 'Tempo de Resposta',
                color: 'from-purple-400 to-purple-600'
              },
              {
                icon: <Calendar className="w-10 h-10" />,
                value: '18',
                label: 'Meses de Desenvolvimento',
                color: 'from-orange-400 to-orange-600'
              },
            ].map((metric, index) => (
              <motion.div 
                key={index} 
                className="modern-card"
                whileHover={{ y: -5 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.2 + (index * 0.1), duration: 0.5, type: 'spring', stiffness: 300 }}
              >
                <div className="text-center">
                  <div className={`w-16 h-16 bg-gradient-to-r ${metric.color} rounded-full flex items-center justify-center mx-auto mb-4 text-white shadow-lg`}>
                    {metric.icon}
                  </div>
                  <div className="mt-4">
                    <div className="text-3xl font-bold text-gray-900">{metric.value}</div>
                    <div className="text-gray-500 text-sm">{metric.label}</div>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </motion.section>

      {/* Transformation Section */}
      <motion.section
        id="transformation"
        className="py-20 px-4 relative overflow-hidden section-padding"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
      >
        <div className="max-w-7xl mx-auto">
          <motion.h2 
            className="text-4xl md:text-5xl font-bold text-center mb-12 bg-gradient-to-r from-blue-600 to-green-600 bg-clip-text text-transparent"
            initial={{ y: 20, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            Transformação Tecnológica
          </motion.h2>

          <motion.div 
            className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16"
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.6 }}
          >
            {[
              {
                title: 'Problemas Resolvidos',
                icon: <CheckCircle className="w-10 h-10" />,
                color: 'from-green-400 to-green-600',
                items: [
                  'Eliminação da dependência de fontes externas',
                  'Solução para consultas jurídicas incorretas',
                  'Redução do tempo de resposta de 10s para 2s',
                  'Fim das limitações de contexto',
                ],
              },
              {
                title: 'Tecnologias Implementadas',
                icon: <Zap className="w-10 h-10" />,
                color: 'from-blue-400 to-blue-600',
                items: [
                  'RAG (Retrieval Augmented Generation)',
                  'Base de dados vetorial para consultas semânticas',
                  'Fine-tuning personalizado para contexto jurídico',
                  'Indexação completa de legislação brasileira',
                ],
              },
              {
                title: 'Resultados Alcançados',
                icon: <BarChart3 className="w-10 h-10" />,
                color: 'from-purple-400 to-purple-600',
                items: [
                  'Precisão de 95% em consultas jurídicas',
                  'Redução de 70% no tempo de pesquisa jurídica',
                  'Aumento de 85% na satisfação dos usuários',
                  'Escalabilidade para 1000+ usuários simultâneos',
                ],
              },
            ].map((advantage, index) => (
            <motion.div 
              key={index} 
              className="modern-card feature-card"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.7 + (index * 0.2), duration: 0.5 }}
              whileHover={{ y: -10 }}
            >
              <div className={`w-20 h-20 bg-gradient-to-r ${advantage.color} rounded-2xl flex items-center justify-center mb-6 text-white shadow-lg transform -rotate-3`}>
                {advantage.icon}
              </div>
              <h3 className="text-2xl font-bold mb-4 text-gray-800">{advantage.title}</h3>
              <ul className="space-y-4">
                {advantage.items.map((item, idx) => (
                  <motion.li 
                    key={idx} 
                    className="flex items-start"
                    initial={{ opacity: 0, x: -10 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.9 + (idx * 0.1) + (index * 0.2), duration: 0.3 }}
                  >
                    <span className="inline-flex items-center justify-center bg-blue-100 text-blue-600 rounded-full w-6 h-6 mr-3 flex-shrink-0">
                      <ChevronRight className="w-4 h-4" />
                    </span>
                    <span className="text-gray-600">{item}</span>
                  </motion.li>
                ))}
              </ul>
            </motion.div>
          ))}
          </motion.div>
        </div>
      </motion.section>

      {/* Before vs After Comparison */}
      <motion.section 
        id="comparison"
        className="py-20 px-4 relative overflow-hidden section-padding"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
      >
        {/* Decorative elements */}
        <div className="absolute top-40 left-0 w-64 h-64 bg-red-200 rounded-full blur-3xl opacity-20 -z-10"></div>
        <div className="absolute bottom-20 right-0 w-80 h-80 bg-green-200 rounded-full blur-3xl opacity-20 -z-10"></div>
        
        <motion.h2 
          className="text-4xl md:text-5xl font-bold text-center mb-4 bg-gradient-to-r from-red-600 to-green-600 bg-clip-text text-transparent"
          initial={{ y: -20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
        >
          Antes vs Depois
        </motion.h2>
        
        <motion.div 
          className="w-24 h-1 bg-gradient-to-r from-red-500 to-green-500 mx-auto mb-6"
          initial={{ width: 0 }}
          whileInView={{ width: 96 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4, duration: 0.8 }}
        ></motion.div>
        
        <motion.p 
          className="text-xl text-gray-600 text-center mb-12 max-w-3xl mx-auto"
          initial={{ y: 20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5 }}
        >
          A transformação completa de uma plataforma jurídica obsoleta para uma solução moderna e eficiente
        </motion.p>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-7xl mx-auto">
          {/* Before */}
          <motion.div 
            className="modern-card bg-white rounded-2xl shadow-xl overflow-hidden border border-red-100"
            initial={{ x: -50, opacity: 0 }}
            whileInView={{ x: 0, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.6, duration: 0.5 }}
            whileHover={{ y: -5, boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)' }}
          >
            <div className="bg-gradient-to-r from-red-500 to-red-700 p-6">
              <div className="flex items-center space-x-4">
                <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center shadow-inner">
                  <X className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h3 className="text-3xl font-bold text-white">jusimples.com.br</h3>
                  <p className="text-red-100 text-lg">Sistema Antigo</p>
                </div>
              </div>
            </div>
            
            <div className="p-8">
              <div className="space-y-5 mb-8">
                {[
                  "Busca não funciona (0% de precisão)",
                  "Design desatualizado e não responsivo",
                  "Sem integração com IA",
                  "Base de dados estática",
                  "Experiência do usuário frustrante",
                ].map((item, index) => (
                  <motion.div 
                    key={index} 
                    className="flex items-center space-x-3 text-gray-700"
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.8 + (index * 0.1) }}
                  >
                    <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
                      <X className="w-4 h-4 text-red-600" />
                    </div>
                    <span className="font-medium">{item}</span>
                  </motion.div>
                ))}
              </div>

              <motion.div 
                className="bg-red-50 border border-red-100 rounded-xl p-6"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 1.4 }}
              >
                <div className="text-red-800 font-semibold mb-3 text-lg flex items-center">
                  <span className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center mr-2">
                    <Target className="w-4 h-4 text-red-600" />
                  </span>
                  Teste Realizado:
                </div>
                <div className="text-gray-700 italic mb-3 pl-10">"Comprei um produto com defeito"</div>
                <div className="text-red-600 font-medium flex items-center pl-10">
                  <X className="w-5 h-5 mr-2" /> Resultado: Busca falhou completamente
                </div>
              </motion.div>
            </div>
          </motion.div>

          {/* After */}
          <motion.div 
            className="modern-card bg-white rounded-2xl shadow-xl overflow-hidden border border-green-100"
            initial={{ x: 50, opacity: 0 }}
            whileInView={{ x: 0, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.8, duration: 0.5 }}
            whileHover={{ y: -5, boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)' }}
          >
            <div className="bg-gradient-to-r from-green-500 to-green-700 p-6">
              <div className="flex items-center space-x-4">
                <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center shadow-inner">
                  <CheckCircle className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h3 className="text-3xl font-bold text-white">JuSimples Transformado</h3>
                  <p className="text-green-100 text-lg">Nova Plataforma</p>
                </div>
              </div>
            </div>
            
            <div className="p-8">
              <div className="space-y-5 mb-8">
                {[
                  "95% de precisão nas respostas",
                  "Design moderno e totalmente responsivo",
                  "IA integrada com RAG",
                  "Base de dados vetorial com embedding",
                  "Experiência do usuário otimizada",
                ].map((item, index) => (
                  <motion.div 
                    key={index} 
                    className="flex items-center space-x-3 text-gray-700"
                    initial={{ opacity: 0, x: 20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 1.0 + (index * 0.1) }}
                  >
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                      <CheckCircle className="w-4 h-4 text-green-600" />
                    </div>
                    <span className="font-medium">{item}</span>
                  </motion.div>
                ))}
              </div>

              <motion.div 
                className="bg-green-50 border border-green-100 rounded-xl p-6"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 1.6 }}
              >
                <div className="text-green-800 font-semibold mb-3 text-lg flex items-center">
                  <span className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-2">
                    <Target className="w-4 h-4 text-green-600" />
                  </span>
                  Mesmo Teste:
                </div>
                <div className="text-gray-700 italic mb-3 pl-10">"Comprei um produto com defeito"</div>
                <div className="text-green-600 font-medium flex items-center pl-10">
                  <CheckCircle className="w-5 h-5 mr-2" /> Resultado: Resposta precisa com referências ao CDC
                </div>
              </motion.div>
            </div>
          </motion.div>
        </div>
        
        <motion.div 
          className="text-center mt-12"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 1.8 }}
        >
          {/* Demo links */}
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            <motion.a
              href="https://www.jusimples.com.br"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center bg-red-100 hover:bg-red-200 text-red-700 px-6 py-3 rounded-lg font-medium transition-all"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
            >
              <ExternalLink className="w-5 h-5 mr-2" />
              Testar Site Antigo
            </motion.a>
            <motion.a
              href="https://jusimplesbeta.netlify.app"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center bg-gradient-to-r from-blue-600 to-green-600 hover:from-blue-700 hover:to-green-700 text-white px-6 py-3 rounded-lg font-medium transition-all shadow-lg"
              whileHover={{ scale: 1.05, boxShadow: '0 0 15px rgba(59, 130, 246, 0.5)' }}
              whileTap={{ scale: 0.98 }}
            >
              <ExternalLink className="w-5 h-5 mr-2" />
              Testar Site Novo
            </motion.a>
          </div>
          
          <motion.button
            onClick={() => scrollToSection('analysis')}
            className="inline-flex items-center bg-blue-50 hover:bg-blue-100 text-blue-700 px-6 py-3 rounded-lg font-medium transition-all"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
          >
            <span>Ver Análise Técnica Detalhada</span>
            <ArrowRight className="w-5 h-5 ml-2" />
          </motion.button>
        </motion.div>
      </motion.section>

      {/* Technical Analysis */}
      <motion.section 
        id="analysis"
        className="py-20 px-4 relative overflow-hidden section-padding"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
      >
        {/* Decorative elements */}
        <div className="absolute top-20 right-10 w-96 h-96 bg-blue-100 rounded-full blur-3xl opacity-20 -z-10"></div>
        <div className="absolute bottom-40 left-0 w-64 h-64 bg-purple-100 rounded-full blur-3xl opacity-20 -z-10"></div>
        
        <motion.h2 
          className="text-4xl md:text-5xl font-bold text-center mb-4 bg-gradient-to-r from-blue-700 to-purple-700 bg-clip-text text-transparent"
          initial={{ y: -20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
        >
          Análise Técnica Detalhada
        </motion.h2>
        
        <motion.div 
          className="w-24 h-1 bg-gradient-to-r from-blue-500 to-purple-500 mx-auto mb-6"
          initial={{ width: 0 }}
          whileInView={{ width: 96 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4, duration: 0.8 }}
        ></motion.div>
        
        <motion.p 
          className="text-xl text-gray-600 text-center mb-12 max-w-3xl mx-auto"
          initial={{ y: 20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5 }}
        >
          Arquitetura moderna com IA e base de dados vetorial para resultados superiores
        </motion.p>

        {/* Architecture and Problem Solving Cards */}
        <motion.div 
          className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-7xl mx-auto mb-16"
          initial={{ y: 40, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.6 }}
        >
          {/* Architecture Diagram */}
          <motion.div 
            className="modern-card p-8"
            whileHover={{ y: -5, boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)' }}
          >
            <motion.div 
              className="flex items-center space-x-3 mb-6"
              initial={{ x: -20, opacity: 0 }}
              whileInView={{ x: 0, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.8 }}
            >
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-700 rounded-xl flex items-center justify-center shadow-lg">
                <Code className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">Arquitetura Atual</h3>
            </motion.div>
            
            <div className="space-y-3">
              {[
                { component: "Frontend", tech: "React + Tailwind", color: "bg-gradient-to-r from-blue-400 to-blue-600 text-white" },
                { component: "Backend", tech: "FastAPI + Python", color: "bg-gradient-to-r from-green-400 to-green-600 text-white" },
                { component: "Database", tech: "PostgreSQL + pgvector", color: "bg-gradient-to-r from-purple-400 to-purple-600 text-white" },
                { component: "AI/ML", tech: "OpenAI GPT-4o-mini", color: "bg-gradient-to-r from-orange-400 to-orange-600 text-white" },
                { component: "RAG", tech: "LangChain + Embeddings", color: "bg-gradient-to-r from-pink-400 to-pink-600 text-white" },
              ].map((item, index) => (
                <motion.div 
                  key={index} 
                  className="flex items-center justify-between p-4 rounded-lg border border-gray-100 hover:border-blue-200 transition-all shadow-sm hover:shadow"
                  initial={{ x: -20, opacity: 0 }}
                  whileInView={{ x: 0, opacity: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.9 + (index * 0.1) }}
                  whileHover={{ scale: 1.02 }}
                >
                  <span className="font-semibold text-gray-800">{item.component}</span>
                  <span className={`${item.color} px-4 py-2 rounded-lg text-sm font-medium shadow-sm`}>
                    {item.tech}
                  </span>
                </motion.div>
              ))}
            </div>

            <motion.div 
              className="mt-6 pt-5 border-t border-gray-200 flex justify-center"
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 1.4 }}
            >
              <div className="bg-blue-50 border border-blue-100 rounded-full px-5 py-2 inline-flex items-center">
                <Database className="w-5 h-5 text-blue-600 mr-2" />
                <span className="text-gray-700 font-medium">Pipeline RAG Completo: </span>
                <span className="text-blue-600 font-bold ml-1">95% de Precisão</span>
              </div>
            </motion.div>
          </motion.div>

          {/* Problems Solved */}
          <motion.div 
            className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100 p-8"
            whileHover={{ y: -5, boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)' }}
          >
            <motion.div 
              className="flex items-center space-x-3 mb-6"
              initial={{ x: 20, opacity: 0 }}
              whileInView={{ x: 0, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.8 }}
            >
              <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-green-700 rounded-xl flex items-center justify-center shadow-lg">
                <CheckCircle className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">Problemas Resolvidos</h3>
            </motion.div>
            
            <div className="space-y-3">
              {[
                { title: "Pipeline RAG Implementado", desc: "Retrieval-Augmented Generation funcional", icon: <Brain className="w-5 h-5" /> },
                { title: "Base de Dados Vetorial", desc: "Busca semântica com pgvector", icon: <Database className="w-5 h-5" /> },
                { title: "Busca Semântica Avançada", desc: "Compreensão contextual das consultas", icon: <Search className="w-5 h-5" /> },
                { title: "Interface Responsiva", desc: "Design moderno e acessível", icon: <Smartphone className="w-5 h-5" /> },
                { title: "Performance Otimizada", desc: "Respostas em menos de 2 segundos", icon: <Zap className="w-5 h-5" /> },
              ].map((item, index) => (
                <motion.div 
                  key={index} 
                  className="flex items-start space-x-3 p-4 border border-gray-100 hover:border-green-200 rounded-lg transition-all shadow-sm hover:shadow"
                  initial={{ x: 20, opacity: 0 }}
                  whileInView={{ x: 0, opacity: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.9 + (index * 0.1) }}
                  whileHover={{ scale: 1.02 }}
                >
                  <div className="w-10 h-10 bg-green-100 text-green-600 rounded-full flex items-center justify-center flex-shrink-0">
                    {item.icon}
                  </div>
                  <div>
                    <div className="font-semibold text-gray-800">{item.title}</div>
                    <div className="text-gray-600 text-sm">{item.desc}</div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </motion.div>

        {/* Performance Metrics */}
        <motion.div
          className="max-w-7xl mx-auto"
          initial={{ y: 40, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 1.2 }}
        >
          <motion.h3 
            className="text-3xl font-bold text-center mb-8"
            initial={{ y: 20, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 1.3 }}
          >
            Métricas de Performance
          </motion.h3>
          
          <motion.div 
            className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-16 timeline-grid"
            initial={{ y: 40, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.5 }}
          >
            {[
              {
                value: "95%",
                label: "Precisão das Respostas",
                desc: "Respostas jurídicas precisas e contextualizadas",
                color: "from-green-400 to-green-600",
                icon: <Target className="w-8 h-8" />
              },
              {
                value: "2s",
                label: "Tempo Médio de Resposta",
                desc: "Otimização do fluxo do RAG e embedding",
                color: "from-blue-400 to-blue-600",
                icon: <Timer className="w-8 h-8" />
              },
              {
                value: "1000+",
                label: "Usuários Simultâneos",
                desc: "Escalabilidade com performance sustentada",
                color: "from-purple-400 to-purple-600",
                icon: <Users className="w-8 h-8" />
              },
            ].map((metric, index) => (
              <motion.div 
                key={index} 
                className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100 text-center hover:shadow-xl transition-all"
                initial={{ y: 30, opacity: 0 }}
                whileInView={{ y: 0, opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: 1.5 + (index * 0.1) }}
                whileHover={{ y: -5 }}
              >
                <div className="flex justify-center mb-4">
                  <div className={`w-20 h-20 bg-gradient-to-r ${metric.color} rounded-2xl flex items-center justify-center text-white shadow-lg transform rotate-3`}>
                    {metric.icon}
                  </div>
                </div>
                <div className="text-5xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent mb-3">
                  {metric.value}
                </div>
                <div className="text-xl font-semibold text-gray-800 mb-2">{metric.label}</div>
                <p className="text-gray-600">{metric.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>
        
        <motion.div 
          className="text-center mt-12"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 1.8 }}
        >
          <motion.button
            onClick={() => scrollToSection('timeline')}
            className="inline-flex items-center bg-blue-50 hover:bg-blue-100 text-blue-700 px-6 py-3 rounded-lg font-medium transition-all"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
          >
            <span>Ver Timeline do Projeto</span>
            <ArrowRight className="w-5 h-5 ml-2" />
          </motion.button>
        </motion.div>
      </motion.section>

      {/* Timeline */}
      <motion.section 
        id="timeline"
        className="py-20 px-4 relative overflow-hidden section-padding timeline-section"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
      >
        {/* Decorative elements */}
        <div className="absolute top-20 left-20 w-80 h-80 bg-blue-100 rounded-full blur-3xl opacity-20 -z-10"></div>
        <div className="absolute bottom-40 right-0 w-72 h-72 bg-purple-100 rounded-full blur-3xl opacity-20 -z-10"></div>
        
        <motion.h2 
          className="text-4xl md:text-5xl font-bold text-center mb-4 bg-gradient-to-r from-purple-700 to-blue-700 bg-clip-text text-transparent"
          initial={{ y: -20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
        >
          Timeline do Projeto
        </motion.h2>
        
        <motion.div 
          className="w-24 h-1 bg-gradient-to-r from-purple-500 to-blue-500 mx-auto mb-6"
          initial={{ width: 0 }}
          whileInView={{ width: 96 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4, duration: 0.8 }}
        ></motion.div>
        
        <motion.p 
          className="text-xl text-gray-600 text-center mb-12 max-w-3xl mx-auto"
          initial={{ y: 20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5 }}
        >
          18 meses de desenvolvimento intensivo com marcos importantes
        </motion.p>

        <div className="relative max-w-5xl mx-auto">
          <motion.div 
            className="absolute left-1/2 transform -translate-x-px h-full w-2 bg-gradient-to-b from-blue-600 via-purple-600 to-green-600 rounded-full"
            initial={{ height: 0 }}
            whileInView={{ height: "100%" }}
            viewport={{ once: true }}
            transition={{ delay: 0.6, duration: 1.5 }}
          ></motion.div>
          
          <div className="space-y-24">
            {[
                {
                  phase: "Análise",
                  title: "Avaliação do Sistema Antigo",
                  description: "Identificação dos problemas críticos na plataforma original",
                  duration: "2 semanas",
                  deliverables: ["Relatório de problemas", "Análise de UX", "Benchmarks de performance"],
                  color: "from-red-400 to-red-600",
                  icon: <FileSearch className="w-5 h-5" />
                },
                {
                  phase: "Arquitetura",
                  title: "Design da Solução RAG",
                  description: "Planejamento da arquitetura com IA e base de dados vetorial",
                  duration: "3 semanas",
                  deliverables: ["Arquitetura técnica", "Escolha de tecnologias", "Prototipagem"],
                  color: "from-yellow-400 to-amber-600",
                  icon: <Building2 className="w-5 h-5" />
                },
                {
                  phase: "Desenvolvimento",
                  title: "Implementação do Backend",
                  description: "Desenvolvimento do pipeline RAG e integração com IA",
                  duration: "8 semanas",
                  deliverables: ["API funcional", "Base de dados vetorial", "Integração OpenAI"],
                  color: "from-blue-400 to-blue-600",
                  icon: <Code2 className="w-5 h-5" />
                },
                {
                  phase: "Frontend",
                  title: "Interface Moderna",
                  description: "Criação da interface responsiva e intuitiva",
                  duration: "4 semanas",
                  deliverables: ["Interface React", "Design responsivo", "UX otimizada"],
                  color: "from-green-400 to-green-600",
                  icon: <Layers className="w-5 h-5" />
                },
                {
                  phase: "Testes",
                  title: "Validação e Otimização",
                  description: "Testes de performance e precisão das respostas",
                  duration: "2 semanas",
                  deliverables: ["95% de precisão", "Performance otimizada", "Bugs corrigidos"],
                  color: "from-purple-400 to-purple-600",
                  icon: <TestTube className="w-5 h-5" />
                },
                {
                  phase: "Deploy",
                  title: "Lançamento Beta",
                  description: "Deploy da versão beta para validação",
                  duration: "1 semana",
                  deliverables: ["Site beta online", "Monitoramento ativo", "Feedback inicial"],
                  color: "from-indigo-400 to-indigo-600",
                  icon: <Rocket className="w-5 h-5" />
                },
            ].map((event, index) => (
              <motion.div 
                key={index} 
                className={`relative flex items-center ${index % 2 === 0 ? "justify-start" : "justify-end"}`}
                initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.5 + (index * 0.2), duration: 0.5 }}
              >
                <motion.div 
                  className={`w-5/12 ${index % 2 === 0 ? "mr-8" : "ml-8"} modern-card timeline-card p-6`}
                  whileHover={{ y: -5, boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.15)' }}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className={`w-10 h-10 rounded-xl bg-gradient-to-r ${event.color} flex items-center justify-center text-white shadow-md`}>
                        {event.icon}
                      </div>
                      <span className="font-semibold text-gray-800">
                        {event.phase}
                      </span>
                    </div>
                    <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm font-medium border border-gray-200">
                      {event.duration}
                    </span>
                  </div>
                  
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">{event.title}</h3>
                  <p className="text-gray-600 mb-6">{event.description}</p>
                  
                  <div className="space-y-2 border-t border-gray-100 pt-4">
                    {event.deliverables.map((deliverable, idx) => (
                      <motion.div 
                        key={idx} 
                        className="flex items-center space-x-2 text-sm"
                        initial={{ opacity: 0, x: -10 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.8 + (index * 0.2) + (idx * 0.1) }}
                      >
                        <div className="w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                          <CheckCircle className="w-3 h-3" />
                        </div>
                        <span className="text-gray-700">{deliverable}</span>
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
                
                <motion.div 
                  className={`absolute left-1/2 transform -translate-x-1/2 z-10`}
                  initial={{ scale: 0 }}
                  whileInView={{ scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.7 + (index * 0.2), type: "spring" }}
                >
                  <div className={`w-8 h-8 bg-gradient-to-r ${event.color} rounded-full flex items-center justify-center border-4 border-white shadow-lg text-white`}>
                    {event.icon}
                  </div>
                </motion.div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Roadmap Section */}
      <motion.section 
        id="roadmap"
        className="py-20 px-4 relative overflow-hidden"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
      >
        {/* Decorative elements */}
        <div className="absolute top-40 right-10 w-72 h-72 bg-green-100 rounded-full blur-3xl opacity-20 -z-10"></div>
        <div className="absolute bottom-20 left-0 w-64 h-64 bg-orange-100 rounded-full blur-3xl opacity-20 -z-10"></div>
        
        <motion.h2 
          className="text-4xl md:text-5xl font-bold text-center mb-4 bg-gradient-to-r from-green-700 to-blue-700 bg-clip-text text-transparent"
          initial={{ y: -20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
        >
          Roadmap Futuro
        </motion.h2>
        
        <motion.div 
          className="w-24 h-1 bg-gradient-to-r from-green-500 to-blue-500 mx-auto mb-6"
          initial={{ width: 0 }}
          whileInView={{ width: 96 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4, duration: 0.8 }}
        ></motion.div>
        
        <motion.p 
          className="text-xl text-gray-600 text-center mb-12 max-w-3xl mx-auto"
          initial={{ y: 20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5 }}
        >
          Plano de evolução e expansão da plataforma para os próximos meses
        </motion.p>

        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                phase: "Curto Prazo",
                title: "Expansão da Base de Conhecimento",
                description: "Ampliação do conteúdo jurídico e fine-tuning",
                timeline: "1-3 meses",
                items: [
                  "Adicionar 1000+ novos documentos",
                  "Fine-tuning dos modelos de IA",
                  "Otimização de performance",
                  "Integração com mais fontes jurídicas",
                ],
                color: "from-green-400 to-green-600",
                icon: <TrendingUp className="w-8 h-8" />,
              },
              {
                phase: "Médio Prazo",
                title: "Integração LexML Completa",
                description: "Automação total de conteúdo jurídico",
                timeline: "3-6 meses",
                items: [
                  "API LexML integrada",
                  "Atualização automática de conteúdo",
                  "Dashboard de analytics",
                  "Sistema de notificações",
                ],
                color: "from-blue-400 to-blue-600",
                icon: <Globe className="w-8 h-8" />,
              },
              {
                phase: "Longo Prazo",
                title: "IA Própria Especializada",
                description: "Desenvolvimento de modelo proprietário",
                timeline: "6-12 meses",
                items: [
                  "Modelo de IA especializado em direito brasileiro",
                  "Múltiplos domínios jurídicos",
                  "API para terceiros",
                  "Expansão para outros países",
                ],
                color: "from-purple-400 to-purple-600",
                icon: <Rocket className="w-8 h-8" />,
              },
            ].map((phase, index) => (
              <motion.div 
                key={index} 
                className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.2 * index, duration: 0.5 }}
                whileHover={{ y: -5, boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.15)' }}
              >
                <div className={`h-2 bg-gradient-to-r ${phase.color} w-full`}></div>
                <div className="p-6">
                  <div className="flex items-center justify-between mb-6">
                    <div className={`w-14 h-14 bg-gradient-to-r ${phase.color} rounded-2xl flex items-center justify-center text-white shadow-lg`}>
                      {phase.icon}
                    </div>
                    <div className="flex flex-col items-end">
                      <span className="text-sm font-medium text-gray-500 mb-1">Timeline</span>
                      <span className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm font-medium border border-gray-200">
                        {phase.timeline}
                      </span>
                    </div>
                  </div>
                  
                  <div className="mb-2 bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent inline-block">
                    {phase.phase}
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">{phase.title}</h3>
                  <p className="text-gray-600 mb-6">{phase.description}</p>
                  
                  <div className="space-y-3 border-t border-gray-100 pt-4">
                    {phase.items.map((item, idx) => (
                      <motion.div 
                        key={idx} 
                        className="flex items-center space-x-3"
                        initial={{ opacity: 0, x: -10 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.4 + (index * 0.1) + (idx * 0.1) }}
                      >
                        <div className={`flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-r ${phase.color} bg-opacity-20 flex items-center justify-center`}>
                          <CheckCircle className="w-3 h-3 text-white" />
                        </div>
                        <span className="text-gray-700">{item}</span>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Investment Section */}
      <motion.section 
        id="investment"
        className="py-20 px-4 relative overflow-hidden"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
      >
        {/* Decorative elements */}
        <div className="absolute top-40 left-20 w-80 h-80 bg-blue-100 rounded-full blur-3xl opacity-20 -z-10"></div>
        <div className="absolute bottom-20 right-10 w-72 h-72 bg-purple-100 rounded-full blur-3xl opacity-20 -z-10"></div>
        
        <motion.h2 
          className="text-4xl md:text-5xl font-bold text-center mb-4 bg-gradient-to-r from-blue-700 to-purple-700 bg-clip-text text-transparent"
          initial={{ y: -20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
        >
          Oportunidade de Investimento
        </motion.h2>
        
        <motion.div 
          className="w-24 h-1 bg-gradient-to-r from-blue-500 to-purple-500 mx-auto mb-6"
          initial={{ width: 0 }}
          whileInView={{ width: 96 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4, duration: 0.8 }}
        ></motion.div>
        
        <motion.p 
          className="text-xl text-gray-600 text-center mb-12 max-w-3xl mx-auto"
          initial={{ y: 20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5 }}
        >
          Múltiplos cenários de crescimento e valuation
        </motion.p>

        <motion.div 
          className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-7xl mx-auto mb-12"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.6 }}
        >
          {Object.entries(investmentScenarios).map(([key, scenario], index) => (
            <motion.div
              key={key}
              onClick={() => setSelectedInvestment(key)}
              className={`bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100 cursor-pointer transition-all ${selectedInvestment === key ? "ring-4 ring-blue-500 shadow-xl" : ""}`}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 * index + 0.7, duration: 0.5 }}
              whileHover={{ y: -5, boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.15)' }}
            >
              <div className={`h-2 w-full ${selectedInvestment === key ? "bg-gradient-to-r from-blue-600 to-purple-600" : "bg-gray-200"}`}></div>
              <div className="p-6">
                <div className="flex justify-between items-start mb-6">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white shadow-md">
                    <ChartLineUp className="w-6 h-6" />
                  </div>
                  <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium border border-green-200">
                    ROI: {scenario.roi}
                  </span>
                </div>
                <div className="mb-5">
                  <div className="text-xl font-bold text-gray-900 mb-2">{scenario.title}</div>
                  <div className="text-sm text-gray-600">{scenario.description}</div>
                </div>
                <div className="flex justify-between items-center pt-4 border-t border-gray-100">
                  <div>
                    <div className="text-xs text-gray-500">Timeline</div>
                    <div className="font-semibold">{scenario.timeline}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-gray-500">Valuation</div>
                    <div className="font-semibold text-blue-600">{scenario.valuation}</div>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {selectedInvestment && (
          <motion.div 
            className="max-w-5xl mx-auto bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            layout
          >
            <div className="p-8">
              <motion.h3 
                className="text-3xl font-bold text-gray-900 mb-8 flex items-center"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center text-white shadow-md mr-4">
                  <LineChart className="w-5 h-5" />
                </div>
                {investmentScenarios[selectedInvestment].title} - Detalhes
              </motion.h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.4 }}
                >
                  <h4 className="text-xl font-semibold text-gray-900 mb-6 flex items-center space-x-2">
                    <Target className="w-5 h-5 text-blue-600" />
                    <span>Objetivos</span>
                  </h4>
                  <div className="space-y-4">
                    {investmentScenarios[selectedInvestment].goals.map((goal, index) => (
                      <motion.div 
                        key={index} 
                        className="flex items-center space-x-3 p-4 border border-gray-100 hover:border-blue-200 rounded-lg transition-all shadow-sm hover:shadow"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.5 + (index * 0.1) }}
                        whileHover={{ scale: 1.02 }}
                      >
                        <div className="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                          <CheckCircle className="w-4 h-4" />
                        </div>
                        <span className="text-gray-800">{goal}</span>
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.4 }}
                >
                  <h4 className="text-xl font-semibold text-gray-900 mb-6 flex items-center space-x-2">
                    <Calendar className="w-5 h-5 text-blue-600" />
                    <span>Cronograma</span>
                  </h4>
                  <motion.div 
                    className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-gray-200 rounded-xl overflow-hidden shadow-sm"
                    whileHover={{ boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1)' }}
                    transition={{ duration: 0.2 }}
                  >
                    <div className="p-6">
                      <div className="mb-6">
                        <div className="text-sm font-medium text-gray-500 mb-1">Timeline esperado</div>
                        <div className="text-3xl font-bold text-gray-900 mb-1">
                          {investmentScenarios[selectedInvestment].timeline}
                        </div>
                        <div className="text-sm text-gray-600">Para atingir todos os objetivos</div>
                      </div>
                      <div className="grid grid-cols-2 gap-6 pt-4 border-t border-gray-200">
                        <motion.div
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.6 }}
                        >
                          <div className="text-sm font-medium text-gray-500 mb-1">ROI Projetado</div>
                          <div className="text-2xl font-bold text-green-600">
                            {investmentScenarios[selectedInvestment].roi}
                          </div>
                        </motion.div>
                        <motion.div
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.7 }}
                        >
                          <div className="text-sm font-medium text-gray-500 mb-1">Valuation</div>
                          <div className="text-2xl font-bold text-blue-600">
                            {investmentScenarios[selectedInvestment].valuation}
                          </div>
                        </motion.div>
                      </div>
                    </div>
                  </motion.div>
                </motion.div>
              </div>
            </div>
          </motion.div>
        )}

        <motion.div 
          className="text-center mt-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.8 }}
        >
          <motion.button
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-12 py-4 text-xl font-semibold shadow-lg hover:shadow-xl transition-all rounded-lg flex items-center mx-auto"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
          >
            <Calendar className="w-6 h-6 mr-3" />
            Agendar Reunião de Investimento
          </motion.button>
        </motion.div>
      </motion.section>

      {/* Comparison Alternatives */}
      <motion.section 
        id="comparison-alternatives"
        className="py-20 px-4 relative overflow-hidden"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
      >
        {/* Decorative elements */}
        <div className="absolute top-20 left-10 w-64 h-64 bg-indigo-100 rounded-full blur-3xl opacity-20 -z-10"></div>
        <div className="absolute bottom-40 right-20 w-80 h-80 bg-blue-100 rounded-full blur-3xl opacity-20 -z-10"></div>
        
        <motion.h2 
          className="text-4xl md:text-5xl font-bold text-center mb-4 bg-gradient-to-r from-indigo-700 to-blue-700 bg-clip-text text-transparent"
          initial={{ y: -20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
        >
          JuSimples vs Alternativas
        </motion.h2>
        
        <motion.div 
          className="w-24 h-1 bg-gradient-to-r from-indigo-500 to-blue-500 mx-auto mb-6"
          initial={{ width: 0 }}
          whileInView={{ width: 96 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4, duration: 0.8 }}
        ></motion.div>
        
        <motion.p 
          className="text-xl text-gray-600 text-center mb-12 max-w-3xl mx-auto"
          initial={{ y: 20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5 }}
        >
          Comparação direta com soluções existentes
        </motion.p>

        <motion.div 
          className="max-w-7xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-200"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.6 }}
        >
          <motion.div 
            className="grid grid-cols-4 bg-gradient-to-r from-indigo-500 to-blue-600 text-white py-4 px-6"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.7 }}
          >
            <div className="font-bold text-lg">Funcionalidades</div>
            <div className="font-bold text-lg text-center">JuSimples 2.0</div>
            <div className="font-bold text-lg text-center">Versão Atual</div>
            <div className="font-bold text-lg text-center">Concorrentes</div>
          </motion.div>
          
          {comparisonFeatures.map((feature, index) => (
            <motion.div 
              key={index} 
              className="grid grid-cols-4 border-b border-gray-100 hover:bg-gray-50 transition-colors"
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.8 + (index * 0.1) }}
              whileHover={{ backgroundColor: "rgba(239, 246, 255, 0.8)" }}
            >
              <div className="p-6 font-medium text-gray-800">{feature.name}</div>
              
              <div className="p-6 flex items-center justify-center">
                {feature.jusimples2 ? (
                  <motion.div 
                    className="flex items-center justify-center"
                    whileHover={{ scale: 1.05 }}
                  >
                    <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center border border-green-200">
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    </div>
                    {feature.jusimplesDetail && (
                      <span className="text-xs text-green-700 ml-2 max-w-[120px]">{feature.jusimplesDetail}</span>
                    )}
                  </motion.div>
                ) : (
                  <motion.div 
                    className="w-10 h-10 bg-red-50 rounded-full flex items-center justify-center border border-red-100"
                    whileHover={{ scale: 1.05 }}
                  >
                    <X className="w-5 h-5 text-red-400" />
                  </motion.div>
                )}
              </div>
              
              <div className="p-6 flex items-center justify-center">
                {feature.jusimples1 ? (
                  <motion.div 
                    className="flex items-center justify-center"
                    whileHover={{ scale: 1.05 }}
                  >
                    <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center border border-blue-200">
                      <CheckCircle className="w-5 h-5 text-blue-600" />
                    </div>
                    {feature.jusimples1Detail && (
                      <span className="text-xs text-blue-600 ml-2 max-w-[120px]">{feature.jusimples1Detail}</span>
                    )}
                  </motion.div>
                ) : (
                  <motion.div 
                    className="w-10 h-10 bg-red-50 rounded-full flex items-center justify-center border border-red-100"
                    whileHover={{ scale: 1.05 }}
                  >
                    <X className="w-5 h-5 text-red-400" />
                  </motion.div>
                )}
              </div>
              
              <div className="p-6 flex items-center justify-center">
                {feature.competitors ? (
                  <motion.div 
                    className="flex items-center justify-center"
                    whileHover={{ scale: 1.05 }}
                  >
                    <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center border border-gray-200">
                      <CheckCircle className="w-5 h-5 text-gray-500" />
                    </div>
                    {feature.competitorsDetail && (
                      <span className="text-xs text-gray-500 ml-2 max-w-[120px]">{feature.competitorsDetail}</span>
                    )}
                  </motion.div>
                ) : (
                  <motion.div 
                    className="w-10 h-10 bg-red-50 rounded-full flex items-center justify-center border border-red-100"
                    whileHover={{ scale: 1.05 }}
                  >
                    <X className="w-5 h-5 text-red-400" />
                  </motion.div>
                )}
              </div>
            </motion.div>
          ))}
        </motion.div>
        
        <motion.div 
          className="flex justify-center mt-12"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 1.0 }}
        >
          <motion.button
            className="bg-white text-indigo-600 border border-indigo-200 hover:bg-indigo-50 px-8 py-3 rounded-lg font-medium transition-all flex items-center shadow-sm hover:shadow"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
          >
            <FileText className="w-5 h-5 mr-2" />
            Ver Análise Completa
          </motion.button>
        </motion.div>
      </motion.section>

      {/* Documentation Section */}
      <motion.section 
        id="documentation"
        className="py-20 px-4 relative overflow-hidden"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
      >
        {/* Decorative elements */}
        <div className="absolute top-20 right-20 w-72 h-72 bg-green-100 rounded-full blur-3xl opacity-20 -z-10"></div>
        <div className="absolute bottom-40 left-10 w-80 h-80 bg-teal-100 rounded-full blur-3xl opacity-20 -z-10"></div>
        
        <motion.h2 
          className="text-4xl md:text-5xl font-bold text-center mb-4 bg-gradient-to-r from-teal-700 to-green-700 bg-clip-text text-transparent"
          initial={{ y: -20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
        >
          Documentação Completa
        </motion.h2>
        
        <motion.div 
          className="w-24 h-1 bg-gradient-to-r from-teal-500 to-green-500 mx-auto mb-6"
          initial={{ width: 0 }}
          whileInView={{ width: 96 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4, duration: 0.8 }}
        ></motion.div>
        
        <motion.p 
          className="text-xl text-gray-600 text-center mb-12 max-w-3xl mx-auto"
          initial={{ y: 20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5 }}
        >
          Análise detalhada e estratégias de implementação
        </motion.p>

        <motion.div 
          className="max-w-5xl mx-auto space-y-6"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.6 }}
        >
          {documentationSections.map((section, idx) => (
            <motion.div 
              key={section.id} 
              className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.6 + (idx * 0.1) }}
              whileHover={{ y: -5, boxShadow: '0 20px 40px -12px rgba(0, 0, 0, 0.1)' }}
            >
              <motion.div
                className="cursor-pointer transition-colors p-6"
                onClick={() => setExpandedDoc(expandedDoc === section.id ? null : section.id)}
                whileHover={{ backgroundColor: "rgba(249, 250, 251, 0.8)" }}
                transition={{ duration: 0.2 }}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <motion.div 
                      className="w-16 h-16 bg-gradient-to-br from-teal-400 to-green-500 rounded-2xl flex items-center justify-center text-white shadow-lg"
                      whileHover={{ rotate: 5, scale: 1.05 }}
                      transition={{ type: "spring", stiffness: 300 }}
                    >
                      {section.icon}
                    </motion.div>
                    <div>
                      <h3 className="text-2xl font-bold text-gray-900">{section.title}</h3>
                      <p className="text-gray-600">{section.description}</p>
                    </div>
                  </div>
                  <motion.div
                    animate={{ rotate: expandedDoc === section.id ? 90 : 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <ChevronRight className="w-6 h-6 text-gray-400" />
                  </motion.div>
                </div>
              </motion.div>

              <AnimatePresence>
                {expandedDoc === section.id && (
                  <motion.div 
                    className="px-6 pb-6 overflow-hidden"
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className="border-t border-gray-200 pt-6">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {section.content.map((item, index) => (
                          <motion.div 
                            key={index} 
                            className="flex items-start space-x-3 p-4 border border-gray-100 hover:border-green-200 bg-white rounded-lg transition-all shadow-sm hover:shadow"
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 * index }}
                            whileHover={{ scale: 1.02, backgroundColor: "rgba(243, 250, 247, 0.5)" }}
                          >
                            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-green-600 flex-shrink-0">
                              <CheckCircle className="w-4 h-4" />
                            </div>
                            <span className="text-gray-800">{item}</span>
                          </motion.div>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </motion.div>
        
        <motion.div 
          className="flex justify-center mt-12"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 1.0 }}
        >
          <motion.button
            className="bg-gradient-to-r from-teal-500 to-green-500 hover:from-teal-600 hover:to-green-600 text-white px-8 py-3 rounded-lg font-medium transition-all flex items-center shadow-md"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
          >
            <Download className="w-5 h-5 mr-2" />
            Baixar Documentação Completa
          </motion.button>
        </motion.div>
      </motion.section>

      {/* Footer CTA */}
      <motion.section 
        id="cta" 
        className="py-24 px-4 relative overflow-hidden cta-modern section-padding"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
      >
        {/* Decorative elements */}
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-green-400 to-blue-500 opacity-80"></div>
        <div className="absolute top-20 right-20 w-96 h-96 bg-blue-400 rounded-full blur-3xl opacity-20 -z-10"></div>
        <div className="absolute bottom-40 left-10 w-80 h-80 bg-purple-400 rounded-full blur-3xl opacity-20 -z-10"></div>

        <div className="max-w-5xl mx-auto text-center">
          <motion.h2 
            className="text-4xl md:text-5xl font-bold text-white mb-6 relative"
            initial={{ y: -30, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <motion.span 
              className="inline-block bg-clip-text text-transparent bg-gradient-to-r from-green-300 to-blue-300" 
              animate={{ filter: ["brightness(1)", "brightness(1.2)", "brightness(1)"] }}
              transition={{ repeat: Number.POSITIVE_INFINITY, duration: 3, ease: "easeInOut" }}
            >
              Pronto para Revolucionar o Direito?
            </motion.span>
          </motion.h2>

          <motion.p
            className="text-xl text-white/90 mb-12 max-w-3xl mx-auto"
            initial={{ y: 20, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.4, duration: 0.5 }}
          >
            Junte-se a nós nesta jornada de transformação da consultoria jurídica com IA
          </motion.p>
          
          <motion.div 
            className="flex flex-wrap justify-center gap-5 mt-8"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 1, duration: 0.5 }}
          >
            <motion.button
              className="btn-primary"
              whileHover={{ y: -5, boxShadow: '0 10px 25px rgba(59, 130, 246, 0.5)' }}
              whileTap={{ scale: 0.95 }}
            >
              <Play className="w-5 h-5 mr-3" />
              Ver Demo
            </motion.button>
            <motion.button
              className="btn-secondary"
              whileHover={{ y: -5, boxShadow: '0 5px 15px rgba(59, 130, 246, 0.2)' }}
              whileTap={{ scale: 0.95 }}
            >
              <FileText className="w-5 h-5 mr-3" />
              Documentação Completa
            </motion.button>
          </motion.div>
          
          <motion.div 
            className="mt-16 flex justify-center"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.8, duration: 0.5 }}
          >
            <div className="flex items-center space-x-4 text-white/70">
              <Users className="w-5 h-5" />
              <span>+20 empresas já aderiram à transformação</span>
            </div>
          </motion.div>
        </div>
      </motion.section>
    </div>
  );
}

export default ProjectSales;
