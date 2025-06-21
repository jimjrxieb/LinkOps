import React, { useEffect, useState } from "react";
import "./WhisTab.css";

const WhisTab = () => {
  const [queueStatus, setQueueStatus] = useState({});
  const [approvals, setApprovals] = useState([]);
  const [digest, setDigest] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchQueueStatus();
    fetchApprovals();
    fetchDigest();
  }, []);

  const fetchQueueStatus = async () => {
    try {
      const res = await fetch("/api/whis/queue");
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      const data = await res.json();
      setQueueStatus(data);
    } catch (error) {
      console.error("Error fetching queue status:", error);
      setError("Failed to fetch queue status");
    }
  };

  const fetchApprovals = async () => {
    try {
      const res = await fetch("/api/whis/approvals");
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      const data = await res.json();
      setApprovals(data);
    } catch (error) {
      console.error("Error fetching approvals:", error);
      setError("Failed to fetch approvals");
    }
  };

  const fetchDigest = async () => {
    try {
      const res = await fetch("/api/whis/digest");
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      const data = await res.json();
      setDigest(data);
    } catch (error) {
      console.error("Error fetching digest:", error);
      setError("Failed to fetch digest");
    }
  };

  const approveRune = async (rune_id) => {
    try {
      setLoading(true);
      const res = await fetch("/api/whis/approve-rune", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rune_id }),
      });
      
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      
      // Refresh approvals after successful approval
      await fetchApprovals();
      await fetchDigest(); // Also refresh digest as it might change
      
      setError(null);
    } catch (error) {
      console.error("Error approving rune:", error);
      setError("Failed to approve rune");
    } finally {
      setLoading(false);
    }
  };

  const triggerNightTraining = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const res = await fetch("/api/whis/train-nightly", { method: "POST" });
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      
      const result = await res.json();
      console.log("Night training result:", result);
      
      // Refresh all data after training
      await Promise.all([
        fetchDigest(),
        fetchQueueStatus(),
        fetchApprovals()
      ]);
      
    } catch (error) {
      console.error("Error triggering night training:", error);
      setError("Failed to trigger night training");
    } finally {
      setLoading(false);
    }
  };

  const refreshAll = async () => {
    setLoading(true);
    setError(null);
    await Promise.all([
      fetchQueueStatus(),
      fetchApprovals(),
      fetchDigest()
    ]);
    setLoading(false);
  };

  return (
    <div className="whis-tab">
      <div className="whis-header">
        <h2>🧠 Whis: AI Training & Learning</h2>
        <button 
          onClick={refreshAll} 
          disabled={loading}
          className="refresh-all-btn"
        >
          🔄 Refresh All
        </button>
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      <div className="whis-grid">
        <section className="whis-section">
          <h3>🎓 How Whis Learns</h3>
          <ul>
            <li>📚 Learns from sanitized task inputs via James</li>
            <li>🔄 Updates Orbs when tasks are repeated or patterns found</li>
            <li>🌙 Nightly training processes all entries from the day</li>
            <li>✅ Human approval required for new knowledge</li>
          </ul>
        </section>

        <section className="whis-section">
          <h3>📊 Training Queue Status</h3>
          <div className="status-grid">
            <div className="status-item">
              <span className="status-label">🕒 Pending:</span>
              <span className="status-value">{queueStatus.pending || 0}</span>
            </div>
            <div className="status-item">
              <span className="status-label">✅ Trained:</span>
              <span className="status-value">{queueStatus.trained || 0}</span>
            </div>
            <div className="status-item">
              <span className="status-label">📎 Match Usages:</span>
              <span className="status-value">{queueStatus.matches || 0}</span>
            </div>
            <div className="status-item">
              <span className="status-label">🧩 Fallbacks:</span>
              <span className="status-value">{queueStatus.fallbacks || 0}</span>
            </div>
          </div>
          <button 
            onClick={fetchQueueStatus} 
            disabled={loading}
            className="action-btn"
          >
            🔄 Refresh Status
          </button>
        </section>

        <section className="whis-section">
          <h3>🧾 Orb & Runes Approval Queue</h3>
          {approvals.length === 0 ? (
            <div className="no-approvals">
              <p>✅ No pending approvals</p>
              <small>All runes have been reviewed and approved</small>
            </div>
          ) : (
            <div className="approvals-list">
              {approvals.map((rune) => (
                <div key={rune.rune_id} className="approval-item">
                  <div className="approval-header">
                    <h4>{rune.orb}</h4>
                    <span className="task-id">{rune.task_id}</span>
                  </div>
                  <div className="approval-content">
                    <pre className="script-content">{rune.script}</pre>
                    <div className="approval-actions">
                      <button 
                        onClick={() => approveRune(rune.rune_id)}
                        disabled={loading}
                        className="approve-btn"
                      >
                        ✅ Approve
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="whis-section">
          <h3>📅 Daily Summary</h3>
          <div className="summary-grid">
            <div className="summary-item">
              <span className="summary-label">🌀 Orbs Updated:</span>
              <span className="summary-value">{digest.orbs_updated?.length || 0}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">📜 Runes Created:</span>
              <span className="summary-value">{digest.runes_created || 0}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">📚 Logs Processed:</span>
              <span className="summary-value">{digest.logs_processed || 0}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">🕒 Last Updated:</span>
              <span className="summary-value">
                {digest.timestamp ? new Date(digest.timestamp).toLocaleString() : 'N/A'}
              </span>
            </div>
          </div>
          <button 
            onClick={fetchDigest} 
            disabled={loading}
            className="action-btn"
          >
            🔄 Refresh Summary
          </button>
        </section>

        <section className="whis-section">
          <h3>🌙 Night Training</h3>
          <p>Process all today's logs and create new runes for approval</p>
          <button 
            onClick={triggerNightTraining} 
            disabled={loading}
            className="night-training-btn"
          >
            {loading ? "🔄 Training..." : "🚀 Trigger Night Training"}
          </button>
          {loading && (
            <div className="loading-indicator">
              <p>Processing logs and creating runes...</p>
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default WhisTab; 