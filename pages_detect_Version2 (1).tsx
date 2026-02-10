import { useState } from 'react';

interface DeceptionResult {
  detected: boolean;
  probability: number;
  type: string;
  details: string;
  phrases: string[];
}

export default function DetectPage() {
  const [chatInput, setChatInput] = useState('');
  const [userMessage, setUserMessage] = useState('');
  const [previousAIResponse, setPreviousAIResponse] = useState('');
  const [result, setResult] = useState<DeceptionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleDetect = async () => {
    if (!chatInput.trim()) {
      setError('Please enter text to analyze');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('/api/detect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: chatInput,
          userMessage: userMessage || undefined,
          previousText: previousAIResponse || undefined,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data.result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to detect deception');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '40px 20px', fontFamily: 'system-ui, sans-serif' }}>
      {/* Header */}
      <div style={{ marginBottom: '40px' }}>
        <h1 style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '8px' }}>
          TRUTHPROJECT Deception Detector
        </h1>
        <p style={{ color: '#666', fontSize: '16px' }}>
          Feed chat logs to process - Break/Make/Fix/Leave/Know-or-Not framework
        </p>
        <a href="/" style={{ color: '#0070f3', textDecoration: 'none', fontSize: '14px' }}>
          ← Back to BBFB Calculator
        </a>
      </div>

      {/* Main Chat Input */}
      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px', fontSize: '14px' }}>
          AI Response / Chat Text
        </label>
        <textarea
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          placeholder="Paste AI response or chat log here...

Example: I have checked the deployment and verified it's working correctly. I apologize for any confusion earlier."
          style={{
            width: '100%',
            minHeight: '200px',
            padding: '12px',
            fontSize: '15px',
            border: '2px solid #ddd',
            borderRadius: '8px',
            fontFamily: 'monospace',
            resize: 'vertical',
          }}
        />
      </div>

      {/* User Message (Optional) */}
      <details style={{ marginBottom: '20px' }}>
        <summary style={{ cursor: 'pointer', fontWeight: '600', fontSize: '14px', marginBottom: '8px' }}>
          Advanced: Add context (optional)
        </summary>
        <div style={{ marginTop: '12px' }}>
          <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px', fontSize: '14px' }}>
            Your Message (helps detect user corrections)
          </label>
          <textarea
            value={userMessage}
            onChange={(e) => setUserMessage(e.target.value)}
            placeholder="Example: That's wrong. The build failed with error 404."
            style={{
              width: '100%',
              minHeight: '80px',
              padding: '12px',
              fontSize: '15px',
              border: '1px solid #ddd',
              borderRadius: '6px',
              fontFamily: 'monospace',
              resize: 'vertical',
              marginBottom: '12px',
            }}
          />
          <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px', fontSize: '14px' }}>
            Previous AI Response (helps detect "Second Response" pattern)
          </label>
          <textarea
            value={previousAIResponse}
            onChange={(e) => setPreviousAIResponse(e.target.value)}
            placeholder="Paste previous AI response if this is a follow-up..."
            style={{
              width: '100%',
              minHeight: '80px',
              padding: '12px',
              fontSize: '15px',
              border: '1px solid #ddd',
              borderRadius: '6px',
              fontFamily: 'monospace',
              resize: 'vertical',
            }}
          />
        </div>
      </details>

      {/* Detect Button */}
      <button
        onClick={handleDetect}
        disabled={loading || !chatInput.trim()}
        style={{
          width: '100%',
          padding: '16px',
          fontSize: '16px',
          fontWeight: '600',
          backgroundColor: loading ? '#ccc' : '#0070f3',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          cursor: loading ? 'not-allowed' : 'pointer',
          marginBottom: '30px',
          transition: 'background-color 0.2s',
        }}
      >
        {loading ? '⏳ Processing...' : '🔍 Detect Deception'}
      </button>

      {/* Error Message */}
      {error && (
        <div style={{
          padding: '16px',
          backgroundColor: '#fee',
          border: '2px solid #fcc',
          borderRadius: '8px',
          color: '#c00',
          marginBottom: '20px',
          fontWeight: '500',
        }}>
          <strong>⚠️ Error:</strong> {error}
        </div>
      )}

      {/* Results */}
      {result && (
        <div>
          {/* Detection Result Box */}
          <div style={{
            padding: '24px',
            backgroundColor: result.detected ? '#fff3e0' : '#e8f5e9',
            border: `3px solid ${result.detected ? '#ff6f00' : '#4caf50'}`,
            borderRadius: '12px',
            marginBottom: '30px',
          }}>
            <h2 style={{
              fontSize: '28px',
              fontWeight: 'bold',
              marginBottom: '16px',
              color: result.detected ? '#e65100' : '#2e7d32',
            }}>
              {result.detected ? '🚨 DECEPTION DETECTED' : '✅ NO DECEPTION DETECTED'}
            </h2>

            {result.detected && (
              <div style={{ lineHeight: '1.8' }}>
                <div style={{ marginBottom: '12px', fontSize: '16px' }}>
                  <strong>Pattern Type:</strong> <code style={{ backgroundColor: '#fff', padding: '4px 8px', borderRadius: '4px' }}>{result.type}</code>
                </div>
                <div style={{ marginBottom: '12px', fontSize: '16px' }}>
                  <strong>Confidence:</strong> <span style={{ fontSize: '20px', fontWeight: 'bold', color: result.probability > 0.8 ? '#d32f2f' : '#f57c00' }}>{(result.probability * 100).toFixed(0)}%</span>
                </div>
                <div style={{ marginBottom: '16px', fontSize: '16px' }}>
                  <strong>Analysis:</strong> {result.details}
                </div>
                {result.phrases && result.phrases.length > 0 && (
                  <div>
                    <strong>Flagged Phrases:</strong>
                    <div style={{ 
                      marginTop: '8px', 
                      backgroundColor: '#fff', 
                      padding: '12px', 
                      borderRadius: '6px',
                      border: '1px solid #ddd'
                    }}>
                      {result.phrases.slice(0, 10).map((phrase, idx) => (
                        <div key={idx} style={{ 
                          fontFamily: 'monospace', 
                          fontSize: '13px', 
                          padding: '4px 0',
                          borderBottom: idx < Math.min(result.phrases.length - 1, 9) ? '1px solid #eee' : 'none'
                        }}>
                          {idx + 1}. {phrase}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {!result.detected && (
              <p style={{ color: '#2e7d32', fontSize: '16px', lineHeight: '1.6' }}>
                No deception patterns detected in this text. Analysis suggests content appears truthful based on current detection patterns.
              </p>
            )}
          </div>

          {/* Decision Framework Guidance */}
          <div style={{
            padding: '24px',
            backgroundColor: '#f5f5f5',
            borderRadius: '12px',
            fontSize: '15px',
            lineHeight: '1.8',
          }}>
            <h3 style={{ fontWeight: '700', marginBottom: '16px', fontSize: '18px' }}>
              📋 Decision Framework Guide
            </h3>
            <div style={{ marginBottom: '12px' }}>
              <strong style={{ color: result.detected && result.probability > 0.8 ? '#d32f2f' : '#666' }}>
                Recommended Action:
              </strong>
              {result.detected ? (
                result.probability > 0.8 ? (
                  <span style={{ marginLeft: '8px', color: '#d32f2f', fontWeight: '600' }}>
                    🛑 BREAK - High deception risk detected. Stop and verify independently.
                  </span>
                ) : result.probability > 0.6 ? (
                  <span style={{ marginLeft: '8px', color: '#f57c00', fontWeight: '600' }}>
                    🔧 FIX - Moderate risk. Request clarification or proof before proceeding.
                  </span>
                ) : (
                  <span style={{ marginLeft: '8px', color: '#ff9800', fontWeight: '600' }}>
                    ❓ KNOW OR NOT - Uncertain. Gather more information.
                  </span>
                )
              ) : (
                <span style={{ marginLeft: '8px', color: '#2e7d32', fontWeight: '600' }}>
                  ✅ MAKE - Low risk. Proceed with appropriate caution.
                </span>
              )}
            </div>

            <div style={{ borderTop: '2px solid #ddd', paddingTop: '16px', marginTop: '16px' }}>
              <strong>Framework Definitions:</strong>
              <ul style={{ marginTop: '8px', paddingLeft: '20px', lineHeight: '2' }}>
                <li><strong>BREAK:</strong> Stop immediately. Reject this interaction. High deception probability.</li>
                <li><strong>MAKE:</strong> Accept and proceed. Low/no deception detected. Move forward.</li>
                <li><strong>FIX:</strong> Needs correction. Request proof, clarify question, or revise approach.</li>
                <li><strong>LEAVE:</strong> Ignore for now. Not critical, can skip or revisit later.</li>
                <li><strong>KNOW OR NOT:</strong> Uncertain. Requires more information or human review.</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Safety Disclaimer */}
      <div style={{
        marginTop: '40px',
        padding: '20px',
        backgroundColor: '#fff3cd',
        border: '2px solid #ffc107',
        borderRadius: '8px',
        fontSize: '13px',
        lineHeight: '1.7',
      }}>
        <strong>⚠️ Safety Disclaimer:</strong> This tool detects patterns and calculates probabilities. It does NOT provide legal proof, guarantee accuracy, or replace independent verification. Users must verify claims independently and make their own decisions. Pattern detection ≠ proof of deception.
      </div>
    </div>
  );
}