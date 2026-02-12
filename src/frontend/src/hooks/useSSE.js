import { useState, useCallback, useRef } from 'react';

export const useSSE = (url) => {
    const [data, setData] = useState('');
    const [status, setStatus] = useState('');
    const [error, setError] = useState(null);
    const [isStreaming, setIsStreaming] = useState(false);
    const eventSourceRef = useRef(null);

    const startStreaming = useCallback((query) => {
        if (eventSourceRef.current) {
            eventSourceRef.current.close();
        }

        setData('');
        setError(null);
        setStatus('Initializing...');
        setIsStreaming(true);

        const fullUrl = `${url}?question=${encodeURIComponent(query)}`;
        const evtSource = new EventSource(fullUrl);
        eventSourceRef.current = evtSource;

        evtSource.addEventListener('search', () => setStatus('Searching...'));
        evtSource.addEventListener('read', () => setStatus('Reading...'));
        evtSource.addEventListener('think', () => setStatus('Preparing answer...'));

        evtSource.addEventListener('token', (e) => {
            const msg = JSON.parse(e.data);
            setData((prev) => prev + msg.text);
            setStatus('');
        });

        evtSource.addEventListener('done', () => {
            setIsStreaming(false);
            setStatus('');
            evtSource.close();
        });

        evtSource.onerror = (err) => {
            console.error('SSE Error:', err);
            setIsStreaming(false);
            setStatus('');
            setError('Connection error occurred. Please ensure the backend is running.');
            evtSource.close();
        };
    }, [url]);

    const stopStreaming = useCallback(() => {
        if (eventSourceRef.current) {
            eventSourceRef.current.close();
            setIsStreaming(false);
        }
    }, []);

    return { data, status, error, isStreaming, startStreaming, stopStreaming };
};
