import React, { useState } from 'react';
import WhisTab from './components/WhisTab';
import './App.css';

const App = () => {
  const [activeTab, setActiveTab] = useState('whis');

  const tabs = [
    { id: 'whis', label: '🧠 Whis AI', component: WhisTab },
    // Add more tabs here as needed
  ];

  const ActiveComponent = tabs.find(tab => tab.id === activeTab)?.component || WhisTab;

  return (
    <div className="app">
      <header className="app-header">
        <h1>🔗 LinkOps Core</h1>
        <p>AI-Powered Operations Management System</p>
      </header>

      <nav className="app-nav">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <main className="app-main">
        <ActiveComponent />
      </main>

      <footer className="app-footer">
        <p>LinkOps Core v1.0 - AI Training & Learning System</p>
      </footer>
    </div>
  );
};

export default App; 