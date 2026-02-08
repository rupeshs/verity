import React from 'react';
import { Sun, Moon, Search } from 'lucide-react';

const Header = ({ darkMode, toggleDarkMode }) => {
    return (
        <header className="sticky top-0 z-50 w-full border-b border-neutral-200 dark:border-dark-border bg-white/80 dark:bg-dark-bg/80 backdrop-blur-md">
            <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <div className="p-1.5 bg-neutral-900 dark:bg-neutral-100 rounded-lg">
                        <Search className="w-5 h-5 text-neutral-100 dark:text-neutral-900" />
                    </div>
                    <h1 className="text-xl font-bold tracking-tight">Verity</h1>
                </div>

                <button
                    onClick={toggleDarkMode}
                    className="p-2 rounded-xl border border-neutral-200 dark:border-dark-border bg-neutral-50 dark:bg-dark-surface hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
                    aria-label="Toggle Theme"
                >
                    {darkMode ? (
                        <Sun className="w-5 h-5 text-neutral-100" />
                    ) : (
                        <Moon className="w-5 h-5 text-neutral-900" />
                    )}
                </button>
            </div>
        </header>
    );
};

export default Header;
