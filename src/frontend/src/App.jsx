import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import SearchInput from './components/SearchInput';
import ResponseArea from './components/ResponseArea';
import { useSSE } from './hooks/useSSE';

function App() {
  const [query, setQuery] = useState('');
  const [darkMode, setDarkMode] = useState(
    localStorage.theme === 'dark' ||
    (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)
  );

  const { data, status, error, isStreaming, startStreaming } = useSSE(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/ask`);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.theme = 'dark';
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.theme = 'light';
    }
  }, [darkMode]);

  const handleSearch = () => {
    if (query.trim()) {
      startStreaming(query);
    }
  };

  const toggleDarkMode = () => setDarkMode(!darkMode);

  return (
    <div className="min-h-screen bg-white dark:bg-dark-bg text-neutral-900 dark:text-neutral-200 transition-colors duration-300">
      <Header darkMode={darkMode} toggleDarkMode={toggleDarkMode} />

      <main className="max-w-4xl mx-auto px-4 pt-20 pb-24">
        {!data && !isStreaming && (
          <div className="text-center space-y-4 mb-20 animate-in fade-in slide-in-from-bottom-5 duration-700">
            <h2 className="text-4xl md:text-5xl font-bold tracking-tight">
              Trusted answers. Local compute.
            </h2>
            <p className="text-neutral-500 dark:text-neutral-400 text-lg">
              Ask anything and get a summarized response.
            </p>
          </div>
        )}

        <SearchInput
          query={query}
          setQuery={setQuery}
          onSearch={handleSearch}
          isLoading={isStreaming}
        />

        <ResponseArea
          data={data}
          status={status}
          error={error}
          isStreaming={isStreaming}
        />
      </main>

      <footer className="fixed bottom-0 w-full border-t border-neutral-200 dark:border-dark-border bg-white/50 dark:bg-dark-bg/50 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto px-4 py-3 flex justify-between items-center text-[10px]  tracking-widest font-semibold text-neutral-400 dark:text-neutral-500">
          <span>Copyright © 2026 Rupesh Sreeraman </span>
          <span className="hidden sm:inline">OpenVINO | Ollama</span>
        </div>
      </footer>
    </div>
  );
}

export default App;
