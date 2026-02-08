import React, { useEffect, useRef } from 'react';
import { Streamdown } from 'streamdown';
import { code } from "@streamdown/code";
import { mermaid } from "@streamdown/mermaid";
import { math } from "@streamdown/math";
import { cjk } from "@streamdown/cjk";
import { Loader2, Sparkles, AlertCircle } from 'lucide-react';
import "katex/dist/katex.min.css";

const ResponseArea = ({ data, status, error, isStreaming }) => {
    const bottomRef = useRef(null);

    useEffect(() => {
        if (isStreaming) {
            bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
        }
    }, [data, isStreaming]);

    if (!data && !status && !isStreaming && !error) return null;

    if (error) {
        return (
            <div className="mt-12 p-6 bg-red-50 dark:bg-red-900/10 border border-red-100 dark:border-red-900/20 rounded-2xl animate-in fade-in slide-in-from-bottom-2 duration-500">
                <div className="flex items-center gap-3 text-red-600 dark:text-red-400 mb-2">
                    <div className="p-1 bg-red-100 dark:bg-red-900/20 rounded-md">
                        <AlertCircle className="w-4 h-4" />
                    </div>
                    <span className="text-sm font-semibold tracking-wide uppercase">Error</span>
                </div>
                <p className="text-red-700 dark:text-red-300 text-sm leading-relaxed">
                    {error}
                </p>
            </div>
        );
    }

    return (
        <div className="mt-12 space-y-6">
            <div className="flex items-center gap-3 text-neutral-600 dark:text-neutral-400">
                <div className="p-1 bg-neutral-100 dark:bg-neutral-800 rounded-md">
                    <Sparkles className="w-4 h-4" />
                </div>
                <span className="text-sm font-medium tracking-wide">Answer</span>
            </div>

            <div className="max-w-none overflow-x-hidden">
                {data ? (
                    <div className="prose prose-neutral dark:prose-invert max-w-none">
                        <Streamdown
                            mode="streaming"
                            plugins={{ code, mermaid, math, cjk }}
                            isAnimating={isStreaming}
                            shikiTheme={['github-light', 'github-dark']}
                        >
                            {data}
                        </Streamdown>
                    </div>
                ) : (
                    <div className="h-20" />
                )}
            </div>

            {status && (
                <div className="flex items-center gap-3 py-2.5 px-5 bg-neutral-50 dark:bg-dark-surface rounded-2xl border border-neutral-100 dark:border-dark-border w-fit animate-pulse shadow-sm">
                    <Loader2 className="w-4 h-4 animate-spin text-neutral-500" />
                    <span className="text-sm text-neutral-600 dark:text-neutral-400 font-medium">
                        {status}
                    </span>
                </div>
            )}
            <div ref={bottomRef} className="h-px" />
        </div>
    );
};

export default ResponseArea;
