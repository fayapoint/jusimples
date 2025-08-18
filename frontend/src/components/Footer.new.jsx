import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";
import {
  HomeIcon,
  DashboardIcon,
  AdminIcon,
  AboutIcon,
  ContactIcon,
  GithubIcon,
  EmailIcon,
  LinkedInIcon,
  TwitterIcon,
  LightThemeIcon,
  DarkThemeIcon,
  NormalThemeIcon
} from "./icons/NavigationIcons";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";
const LOCAL_FALLBACK = "http://localhost:5000";

function Footer() {
  const { user } = useAuth();
  const { theme, changeTheme } = useTheme();
  const [news, setNews] = useState([]);
  const [ads, setAds] = useState([]);
  const [loadingNews, setLoadingNews] = useState(true);
  const [loadingAds, setLoadingAds] = useState(true);
  const [errorNews, setErrorNews] = useState(null);
  const [errorAds, setErrorAds] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchWithFallback(path) {
      const urls = ["", API_URL, LOCAL_FALLBACK];
      let lastErr = null;
      for (const base of urls) {
        try {
          const controller = new AbortController();
          const t = setTimeout(() => controller.abort(), 7000);
          const url = base ? `${base}${path}` : path;
          const res = await fetch(url, { signal: controller.signal });
          clearTimeout(t);
          if (!res.ok) {
            lastErr = new Error(`HTTP ${res.status}`);
            continue;
          }
          return await res.json();
        } catch (e) {
          lastErr = e;
          continue;
        }
      }
      throw lastErr || new Error("Falha ao buscar dados");
    }
    
    const fetchData = async () => {
      try {
        setLoadingNews(true);
        const n = await fetchWithFallback("/api/news");
        if (!cancelled) setNews(Array.isArray(n.news) ? n.news : []);
      } catch (e) {
        if (!cancelled) setErrorNews("Não foi possível carregar as notícias.");
      } finally {
        if (!cancelled) setLoadingNews(false);
      }

      try {
        setLoadingAds(true);
        const a = await fetchWithFallback("/api/ads");
        if (!cancelled) setAds(Array.isArray(a.ads) ? a.ads : []);
      } catch (e) {
        if (!cancelled) setErrorAds("Não foi possível carregar os patrocinados.");
      } finally {
        if (!cancelled) setLoadingAds(false);
      }
    };
    
    fetchData();

    return () => {
      cancelled = true;
    };
  }, []);

  const SkeletonLoader = ({ className, style }) => (
    <div
      className={`animate-pulse bg-gradient-to-r from-slate-200 via-slate-300 to-slate-200 bg-[length:200%_100%] ${className || ""}`}
      style={{
        animation: "shimmer 2s infinite linear",
        backgroundImage: "linear-gradient(90deg, #e5e7eb 0%, #cbd5e1 50%, #e5e7eb 100%)",
        backgroundSize: "200% 100%",
        ...(style || {}),
      }}
    />
  );

  const socialLinks = [
    { name: "GitHub", href: "https://github.com/juximplex", icon: <GithubIcon /> },
    { name: "Email", href: "mailto:contato@jusimples.com", icon: <EmailIcon /> },
    { name: "LinkedIn", href: "#", icon: <LinkedInIcon /> },
    { name: "Twitter", href: "#", icon: <TwitterIcon /> },
  ];

  const navigationLinks = [
    { name: "Início", href: "/", icon: <HomeIcon /> },
    { name: "Dashboard", href: "/dashboard", icon: <DashboardIcon /> },
    { name: "Admin", href: "/admin", icon: <AdminIcon /> },
    { name: "Sobre", href: "/about", icon: <AboutIcon /> },
    { name: "Contato", href: "/contact", icon: <ContactIcon /> },
  ];

  return (
    <>
      <style>{`
        @keyframes shimmer {
          0% { background-position: -200% 0; }
          100% { background-position: 200% 0; }
        }
        
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .fade-in-up {
          animation: fadeInUp 0.6s ease-out forwards;
        }
        
        .hover-lift {
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .hover-lift:hover {
          transform: translateY(-2px);
          box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }

        .line-clamp-2 {
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }

        .group:hover .group-hover\\:scale-110 {
          transform: scale(1.1);
        }
      `}</style>

      <footer
        className={`relative overflow-hidden ${
          theme === 'dark'
            ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white'
            : theme === 'light'
            ? 'bg-gradient-to-br from-blue-50 via-white to-blue-50 text-gray-800'
            : 'bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 text-white'
        }`}
        style={{ fontSize: "12px", lineHeight: 1.25, position: "relative", overflow: "hidden" }}
      >
        <div className="relative max-w-7xl mx-auto px-4 py-8">
          {/* Main Navigation - Horizontal Layout at Top */}
          <div className="flex flex-wrap justify-center border-b border-white/10 pb-4 mb-6">
            {navigationLinks.map((link) => (
              <a
                key={link.name}
                href={link.href}
                className="flex items-center space-x-2 text-slate-300 hover:text-white hover:bg-white/10 px-3 py-2 rounded-lg transition-all duration-300 group hover-lift text-sm m-1"
              >
                <span className="group-hover:scale-110 transition-transform duration-300">
                  {link.icon}
                </span>
                <span className="font-medium">{link.name}</span>
              </a>
            ))}
          </div>
          
          {/* Content Grid - Two Columns */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {/* Legal News Section */}
            <div className="fade-in-up space-y-2 p-4 bg-white/5 rounded-xl">
              <div className="flex items-center space-x-2 mb-3">
                <div className="w-6 h-6 bg-gradient-to-r from-blue-400 to-cyan-400 rounded-lg flex items-center justify-center">
                  <span className="text-sm font-bold">📰</span>
                </div>
                <h4 className="text-sm font-semibold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                  Notícias Jurídicas
                </h4>
              </div>

              <div className="space-y-2">
                {loadingNews && (
                  <>
                    {[...Array(3)].map((_, i) => (
                      <div key={i} className="flex space-x-2 animate-pulse">
                        <SkeletonLoader className="w-10 h-10 rounded-lg" />
                        <div className="flex-1 space-y-2">
                          <SkeletonLoader className="h-3 rounded" />
                          <SkeletonLoader className="h-3 rounded w-3/4" />
                        </div>
                      </div>
                    ))}
                  </>
                )}

                {!loadingNews &&
                  news.slice(0, 3).map((item, index) => (
                    <a
                      key={item.id}
                      href={item.url}
                      target="_blank"
                      rel="noreferrer"
                      className="flex space-x-2 p-2 rounded-lg hover-lift bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-400/50 group transition-all duration-300"
                    >
                      <img
                        className="w-10 h-10 rounded-lg object-cover group-hover:scale-105 transition-transform duration-300"
                        src={item.thumbnail || "/placeholder.svg"}
                        alt={item.title || "Notícia jurídica"}
                        onError={(e) => {
                          e.currentTarget.style.display = "none";
                        }}
                      />
                      <div className="flex-1 min-w-0">
                        <div className="text-xs font-medium text-white group-hover:text-blue-300 transition-colors line-clamp-2">
                          {item.title}
                        </div>
                        <div className="text-xs text-slate-400 mt-1 line-clamp-2">{item.summary}</div>
                      </div>
                    </a>
                  ))}

                {!loadingNews && !news.length && !errorNews && (
                  <div className="text-slate-400 text-sm italic">Sem notícias no momento.</div>
                )}
                {errorNews && <div className="text-red-400 text-sm">{errorNews}</div>}
              </div>
            </div>

            {/* Sponsored Section */}
            <div className="fade-in-up space-y-2 p-4 bg-white/5 rounded-xl">
              <div className="flex items-center space-x-2 mb-3">
                <div className="w-6 h-6 bg-gradient-to-r from-emerald-400 to-teal-400 rounded-lg flex items-center justify-center">
                  <span className="text-sm font-bold">💼</span>
                </div>
                <h4 className="text-sm font-semibold bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
                  Patrocinado
                </h4>
              </div>

              <div className="space-y-2">
                {loadingAds && (
                  <>
                    {[...Array(2)].map((_, i) => (
                      <div key={i} className="space-y-1">
                        <SkeletonLoader className="h-14 rounded-lg" />
                        <SkeletonLoader className="h-3 rounded w-2/3" />
                      </div>
                    ))}
                  </>
                )}

                {!loadingAds &&
                  ads.slice(0, 2).map((ad, index) => (
                    <a
                      key={ad.id}
                      href={ad.url}
                      target="_blank"
                      rel="noreferrer"
                      className="block hover-lift group"
                    >
                      <img
                        className="w-full h-14 object-cover rounded-lg group-hover:scale-105 transition-transform duration-300"
                        src={ad.image || "/placeholder.svg"}
                        alt={ad.title || "Patrocinado"}
                        onError={(e) => {
                          e.currentTarget.style.visibility = "hidden";
                        }}
                      />
                      <div className="text-xs font-medium text-slate-300 mt-1 group-hover:text-blue-300 transition-colors">
                        {ad.title}
                      </div>
                    </a>
                  ))}

                {!loadingAds && !ads.length && !errorAds && (
                  <div className="text-slate-400 text-sm italic">Nenhum patrocinado no momento.</div>
                )}
                {errorAds && <div className="text-red-400 text-sm">{errorAds}</div>}
              </div>
            </div>
          </div>
          
          {/* Theme Selection - Centered at Bottom */}
          <div className="mt-6 border-t border-white/10 pt-4">
            <div className="flex justify-center items-center">
              <div className="flex space-x-4">
                {/* Normal Theme Button */}
                <button
                  onClick={() => changeTheme('normal')}
                  className={`px-4 py-2 rounded-lg transition-all duration-300 flex items-center justify-center ${
                    theme === 'normal' ? 'bg-blue-500 text-white' : 'bg-white/10 text-slate-300 hover:bg-white/20'
                  }`}
                >
                  <NormalThemeIcon className={`mr-2 ${theme === 'normal' ? 'text-white' : 'text-slate-300'}`} />
                  <span className="font-medium">Normal</span>
                </button>
                
                {/* Light Theme Button */}
                <button
                  onClick={() => changeTheme('light')}
                  className={`px-4 py-2 rounded-lg transition-all duration-300 flex items-center justify-center ${
                    theme === 'light' ? 'bg-blue-500 text-white' : 'bg-white/10 text-slate-300 hover:bg-white/20'
                  }`}
                >
                  <LightThemeIcon className={`mr-2 ${theme === 'light' ? 'text-white' : 'text-slate-300'}`} />
                  <span className="font-medium">Claro</span>
                </button>
                
                {/* Dark Theme Button */}
                <button
                  onClick={() => changeTheme('dark')}
                  className={`px-4 py-2 rounded-lg transition-all duration-300 flex items-center justify-center ${
                    theme === 'dark' ? 'bg-blue-500 text-white' : 'bg-white/10 text-slate-300 hover:bg-white/20'
                  }`}
                >
                  <DarkThemeIcon className={`mr-2 ${theme === 'dark' ? 'text-white' : 'text-slate-300'}`} />
                  <span className="font-medium">Escuro</span>
                </button>
              </div>
            </div>
          </div>

          {/* Footer Bottom */}
          <div className="mt-6 pt-4 border-t border-white/10">
            <div className="flex flex-col lg:flex-row justify-between items-center space-y-2 lg:space-y-0">
              {/* Copyright */}
              <div>
                <p className="text-xs text-slate-400">
                  © {new Date().getFullYear()} JuSimples. Todos os direitos reservados.
                </p>
              </div>

              {/* Social Links */}
              <div className="flex items-center space-x-2">
                <span className="text-xs text-slate-400 font-medium">Siga-nos:</span>
                <div className="flex space-x-2">
                  {socialLinks.map((social) => (
                    <a
                      key={social.name}
                      href={social.href}
                      target="_blank"
                      rel="noreferrer"
                      className="w-8 h-8 bg-white/10 hover:bg-gradient-to-r hover:from-blue-500 hover:to-purple-500 rounded-full flex items-center justify-center transition-all duration-300 hover-lift group"
                      title={social.name}
                    >
                      <span className="text-xs group-hover:scale-110 transition-transform duration-300">
                        {social.icon}
                      </span>
                    </a>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </>
  );
}

export default Footer;
