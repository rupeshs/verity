import React, { useRef, useEffect } from 'react';
import { ArrowUp, X } from 'lucide-react';

const SearchInput = ({ query, setQuery, onSearch, isLoading }) => {
    const textareaRef = useRef(null);

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            onSearch();
        }
    };

    // Auto-resize textarea
    useEffect(() => {
        const textarea = textareaRef.current;
        if (textarea) {
            textarea.style.height = 'auto';
            textarea.style.height = `${textarea.scrollHeight}px`;
        }
    }, [query]);

    const handleClear = () => {
        setQuery('');
        if (textareaRef.current) {
            textareaRef.current.focus();
        }
    };

    return (
        <div className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-neutral-200 to-neutral-300 dark:from-neutral-800/20 dark:to-neutral-700/20 rounded-2xl blur opacity-25 group-focus-within:opacity-100 transition duration-1000 group-focus-within:duration-200 pointer-events-none z-0"></div>
            <div className="relative z-10 flex items-end gap-3 bg-white dark:bg-dark-surface border border-neutral-200 dark:border-dark-border rounded-2xl px-5 py-4 shadow-sm ring-1 ring-black/5 dark:ring-white/5 cursor-text" onClick={() => textareaRef.current?.focus()}>
                <textarea
                    ref={textareaRef}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask anything..."
                    rows={1}
                    className="flex-1 bg-transparent outline-none text-base resize-none placeholder-neutral-500 dark:placeholder-neutral-400 py-1 min-h-[24px] max-h-[200px] overflow-y-auto select-text"
                />

                <div className="flex items-center gap-2 pb-0.5">
                    {query && !isLoading && (
                        <button
                            onClick={handleClear}
                            className="p-1.5 text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-200 transition-colors rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800"
                            title="Clear input"
                        >
                            <X className="w-4 h-4" />
                        </button>
                    )}
                    <button
                        onClick={onSearch}
                        disabled={isLoading || !query.trim()}
                        className="p-2 bg-neutral-900 dark:bg-neutral-100 text-neutral-100 dark:text-neutral-900 rounded-xl disabled:opacity-30 disabled:cursor-not-allowed transition-all hover:scale-105 active:scale-95 shadow-lg flex items-center justify-center"
                    >
                        <ArrowUp className="w-5 h-5 font-bold" />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default SearchInput;
